"""
csr_study_design_evaluation.py

Evaluation harness for a modular CSR Study Design workflow.

Purpose
-------
Runs 3 evaluator prompts against workflow outputs:
1. extractor scorer
2. generator scorer
3. verifier scorer

Then aggregates the scores into:
- module-level results
- workflow-level weighted score
- critical failure summary
- recommendation summary

Expected prompt files
---------------------
evaluation/
    study_design_extractor_scorer.md
    csr_study_design_generator_scorer.md
    study_design_verifier_scorer.md

Usage pattern
-------------
1. Fill in the WorkflowEvaluationInput object.
2. Implement or adapt an LLMClient.generate() method.
3. Run evaluate_workflow(...).
4. Inspect the returned WorkflowEvaluationResult.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol


# ------------------------------------------------------------------------------
# Types / Interfaces
# ------------------------------------------------------------------------------

class LLMClient(Protocol):
    """
    Minimal interface for plugging in any LLM backend.

    Implement generate(prompt: str) -> str so it returns the raw model output.
    The evaluator prompts are written to return JSON only.
    """

    def generate(self, prompt: str) -> str:
        ...


@dataclass
class WorkflowEvaluationInput:
    """
    Inputs required to evaluate the CSR study design workflow.
    """
    source_text: str
    structured_elements: str
    generated_text: str
    target_detail_level: str
    verifier_output: Optional[str] = None
    optional_reference_text: Optional[str] = None


@dataclass
class ScoreDetail:
    score: float
    rationale: str


@dataclass
class CriticalFailure:
    present: bool
    reason: str


@dataclass
class ExtractorEvaluationResult:
    dimension_scores: Dict[str, ScoreDetail]
    incorrect_fields: List[str]
    missing_fields: List[str]
    ambiguity_errors: List[str]
    critical_failure: CriticalFailure
    overall_score: float
    overall_verdict: str


@dataclass
class GeneratorEvaluationResult:
    dimension_scores: Dict[str, ScoreDetail]
    critical_failure: CriticalFailure
    missing_elements: List[str]
    unsupported_claims: List[str]
    ambiguities: List[str]
    strengths: List[str]
    recommended_revisions: List[str]
    overall_score: float
    overall_verdict: str


@dataclass
class VerifierEvaluationResult:
    dimension_scores: Dict[str, ScoreDetail]
    missed_issues: List[str]
    false_positives: List[str]
    useful_feedback_examples: List[str]
    critical_failure: CriticalFailure
    overall_score: float
    overall_verdict: str


@dataclass
class WorkflowEvaluationResult:
    extractor: Optional[ExtractorEvaluationResult]
    generator: GeneratorEvaluationResult
    verifier: Optional[VerifierEvaluationResult]
    workflow_overall_score: float
    workflow_overall_verdict: str
    critical_failures_present: bool
    critical_failure_reasons: List[str]
    summary: Dict[str, Any] = field(default_factory=dict)


# ------------------------------------------------------------------------------
# Prompt Loading / Rendering
# ------------------------------------------------------------------------------

def load_prompt(prompt_path: str | Path) -> str:
    path = Path(prompt_path)
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def render_prompt(template: str, replacements: Dict[str, str]) -> str:
    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value or "")
    return rendered


# ------------------------------------------------------------------------------
# JSON Extraction / Parsing
# ------------------------------------------------------------------------------

def extract_json_object(text: str) -> Dict[str, Any]:
    """
    Robustly extracts a JSON object from model output.

    Supports:
    - raw JSON
    - fenced code blocks with JSON
    - extra stray text before/after JSON
    """
    text = text.strip()

    # Case 1: fenced code block
    fenced_match = re.search(r"```(?:json)?\s*(\{[\s\S]*\})\s*```", text)
    if fenced_match:
        return json.loads(fenced_match.group(1))

    # Case 2: raw JSON
    if text.startswith("{") and text.endswith("}"):
        return json.loads(text)

    # Case 3: find first JSON-looking object
    first = text.find("{")
    last = text.rfind("}")
    if first != -1 and last != -1 and first < last:
        candidate = text[first:last + 1]
        return json.loads(candidate)

    raise ValueError("No valid JSON object could be extracted from model output.")


def _parse_score_detail_map(raw: Dict[str, Any]) -> Dict[str, ScoreDetail]:
    out: Dict[str, ScoreDetail] = {}
    for key, value in raw.items():
        out[key] = ScoreDetail(
            score=float(value.get("score", 0)),
            rationale=str(value.get("rationale", "")),
        )
    return out


def _parse_critical_failure(raw: Dict[str, Any]) -> CriticalFailure:
    return CriticalFailure(
        present=bool(raw.get("present", False)),
        reason=str(raw.get("reason", "")),
    )


def parse_extractor_result(data: Dict[str, Any]) -> ExtractorEvaluationResult:
    return ExtractorEvaluationResult(
        dimension_scores=_parse_score_detail_map(data.get("dimension_scores", {})),
        incorrect_fields=list(data.get("incorrect_fields", [])),
        missing_fields=list(data.get("missing_fields", [])),
        ambiguity_errors=list(data.get("ambiguity_errors", [])),
        critical_failure=_parse_critical_failure(data.get("critical_failure", {})),
        overall_score=float(data.get("overall_score", 0)),
        overall_verdict=str(data.get("overall_verdict", "")),
    )


def parse_generator_result(data: Dict[str, Any]) -> GeneratorEvaluationResult:
    return GeneratorEvaluationResult(
        dimension_scores=_parse_score_detail_map(data.get("dimension_scores", {})),
        critical_failure=_parse_critical_failure(data.get("critical_failure", {})),
        missing_elements=list(data.get("missing_elements", [])),
        unsupported_claims=list(data.get("unsupported_claims", [])),
        ambiguities=list(data.get("ambiguities", [])),
        strengths=list(data.get("strengths", [])),
        recommended_revisions=list(data.get("recommended_revisions", [])),
        overall_score=float(data.get("overall_score", 0)),
        overall_verdict=str(data.get("overall_verdict", "")),
    )


def parse_verifier_result(data: Dict[str, Any]) -> VerifierEvaluationResult:
    return VerifierEvaluationResult(
        dimension_scores=_parse_score_detail_map(data.get("dimension_scores", {})),
        missed_issues=list(data.get("missed_issues", [])),
        false_positives=list(data.get("false_positives", [])),
        useful_feedback_examples=list(data.get("useful_feedback_examples", [])),
        critical_failure=_parse_critical_failure(data.get("critical_failure", {})),
        overall_score=float(data.get("overall_score", 0)),
        overall_verdict=str(data.get("overall_verdict", "")),
    )


# ------------------------------------------------------------------------------
# Evaluator Calls
# ------------------------------------------------------------------------------

def run_extractor_evaluation(
    llm_client: LLMClient,
    prompt_path: str | Path,
    workflow_input: WorkflowEvaluationInput,
) -> ExtractorEvaluationResult:
    template = load_prompt(prompt_path)
    prompt = render_prompt(
        template,
        {
            "SOURCE_TEXT": workflow_input.source_text,
            "EXTRACTED_ELEMENTS": workflow_input.structured_elements,
        },
    )
    raw = llm_client.generate(prompt)
    parsed = extract_json_object(raw)
    return parse_extractor_result(parsed)


def run_generator_evaluation(
    llm_client: LLMClient,
    prompt_path: str | Path,
    workflow_input: WorkflowEvaluationInput,
) -> GeneratorEvaluationResult:
    template = load_prompt(prompt_path)
    prompt = render_prompt(
        template,
        {
            "SOURCE_TEXT": workflow_input.source_text,
            "STRUCTURED_ELEMENTS": workflow_input.structured_elements,
            "GENERATED_TEXT": workflow_input.generated_text,
            "TARGET_DETAIL_LEVEL": workflow_input.target_detail_level,
            "OPTIONAL_REFERENCE_TEXT": workflow_input.optional_reference_text or "",
        },
    )
    raw = llm_client.generate(prompt)
    parsed = extract_json_object(raw)
    return parse_generator_result(parsed)


def run_verifier_evaluation(
    llm_client: LLMClient,
    prompt_path: str | Path,
    workflow_input: WorkflowEvaluationInput,
) -> VerifierEvaluationResult:
    if not workflow_input.verifier_output:
        raise ValueError("verifier_output is required for verifier evaluation.")

    template = load_prompt(prompt_path)
    prompt = render_prompt(
        template,
        {
            "SOURCE_TEXT": workflow_input.source_text,
            "STRUCTURED_ELEMENTS": workflow_input.structured_elements,
            "GENERATED_TEXT": workflow_input.generated_text,
            "VERIFIER_OUTPUT": workflow_input.verifier_output,
        },
    )
    raw = llm_client.generate(prompt)
    parsed = extract_json_object(raw)
    return parse_verifier_result(parsed)


# ------------------------------------------------------------------------------
# Workflow Aggregation
# ------------------------------------------------------------------------------

def compute_workflow_overall_score(
    extractor: Optional[ExtractorEvaluationResult],
    generator: GeneratorEvaluationResult,
    verifier: Optional[VerifierEvaluationResult],
) -> float:
    """
    Suggested module-level weighting:
    - Extractor: 30%
    - Generator: 50%
    - Verifier: 20%

    If a module is absent, weights are re-normalized.
    """
    weighted_sum = 0.0
    total_weight = 0.0

    if extractor is not None:
        weighted_sum += extractor.overall_score * 0.30
        total_weight += 0.30

    weighted_sum += generator.overall_score * 0.50
    total_weight += 0.50

    if verifier is not None:
        weighted_sum += verifier.overall_score * 0.20
        total_weight += 0.20

    if total_weight == 0:
        return 0.0

    return round(weighted_sum / total_weight, 1)


def collect_critical_failures(
    extractor: Optional[ExtractorEvaluationResult],
    generator: GeneratorEvaluationResult,
    verifier: Optional[VerifierEvaluationResult],
) -> List[str]:
    reasons: List[str] = []

    if extractor and extractor.critical_failure.present:
        reasons.append(f"Extractor: {extractor.critical_failure.reason}")

    if generator.critical_failure.present:
        reasons.append(f"Generator: {generator.critical_failure.reason}")

    if verifier and verifier.critical_failure.present:
        reasons.append(f"Verifier: {verifier.critical_failure.reason}")

    return reasons


def determine_workflow_verdict(
    overall_score: float,
    critical_failures_present: bool,
) -> str:
    """
    Recommended verdict logic:
    - Any critical failure -> Fail
    - Otherwise use score thresholds
    """
    if critical_failures_present:
        return "Fail"
    if overall_score >= 4.5:
        return "Pass"
    if overall_score >= 3.8:
        return "Pass with minor revision"
    if overall_score >= 2.5:
        return "Revise"
    return "Fail"


def build_summary(
    extractor: Optional[ExtractorEvaluationResult],
    generator: GeneratorEvaluationResult,
    verifier: Optional[VerifierEvaluationResult],
) -> Dict[str, Any]:
    summary: Dict[str, Any] = {
        "top_strengths": generator.strengths[:5],
        "top_generator_revisions": generator.recommended_revisions[:5],
        "key_missing_elements": generator.missing_elements[:5],
        "key_unsupported_claims": generator.unsupported_claims[:5],
        "key_ambiguities": generator.ambiguities[:5],
    }

    if extractor:
        summary["extractor_missing_fields"] = extractor.missing_fields[:5]
        summary["extractor_incorrect_fields"] = extractor.incorrect_fields[:5]

    if verifier:
        summary["verifier_missed_issues"] = verifier.missed_issues[:5]
        summary["verifier_false_positives"] = verifier.false_positives[:5]

    return summary


def evaluate_workflow(
    llm_client: LLMClient,
    workflow_input: WorkflowEvaluationInput,
    extractor_prompt_path: Optional[str | Path],
    generator_prompt_path: str | Path,
    verifier_prompt_path: Optional[str | Path] = None,
) -> WorkflowEvaluationResult:
    extractor_result: Optional[ExtractorEvaluationResult] = None
    verifier_result: Optional[VerifierEvaluationResult] = None

    if extractor_prompt_path:
        extractor_result = run_extractor_evaluation(
            llm_client=llm_client,
            prompt_path=extractor_prompt_path,
            workflow_input=workflow_input,
        )

    generator_result = run_generator_evaluation(
        llm_client=llm_client,
        prompt_path=generator_prompt_path,
        workflow_input=workflow_input,
    )

    if verifier_prompt_path and workflow_input.verifier_output:
        verifier_result = run_verifier_evaluation(
            llm_client=llm_client,
            prompt_path=verifier_prompt_path,
            workflow_input=workflow_input,
        )

    critical_failure_reasons = collect_critical_failures(
        extractor=extractor_result,
        generator=generator_result,
        verifier=verifier_result,
    )
    critical_failures_present = len(critical_failure_reasons) > 0

    workflow_overall_score = compute_workflow_overall_score(
        extractor=extractor_result,
        generator=generator_result,
        verifier=verifier_result,
    )

    workflow_overall_verdict = determine_workflow_verdict(
        overall_score=workflow_overall_score,
        critical_failures_present=critical_failures_present,
    )

    summary = build_summary(
        extractor=extractor_result,
        generator=generator_result,
        verifier=verifier_result,
    )

    return WorkflowEvaluationResult(
        extractor=extractor_result,
        generator=generator_result,
        verifier=verifier_result,
        workflow_overall_score=workflow_overall_score,
        workflow_overall_verdict=workflow_overall_verdict,
        critical_failures_present=critical_failures_present,
        critical_failure_reasons=critical_failure_reasons,
        summary=summary,
    )


# ------------------------------------------------------------------------------
# Reporting / Persistence
# ------------------------------------------------------------------------------

def result_to_dict(result: WorkflowEvaluationResult) -> Dict[str, Any]:
    return asdict(result)


def save_result_json(result: WorkflowEvaluationResult, output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result_to_dict(result), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def print_human_summary(result: WorkflowEvaluationResult) -> None:
    print("=" * 80)
    print("CSR STUDY DESIGN WORKFLOW EVALUATION")
    print("=" * 80)
    print(f"Workflow overall score : {result.workflow_overall_score:.1f}/5")
    print(f"Workflow verdict       : {result.workflow_overall_verdict}")
    print(f"Critical failures      : {result.critical_failures_present}")

    if result.critical_failure_reasons:
        print("\nCritical failure reasons:")
        for reason in result.critical_failure_reasons:
            print(f"- {reason}")

    if result.extractor:
        print("\n[Extractor]")
        print(f"Score   : {result.extractor.overall_score:.1f}/5")
        print(f"Verdict : {result.extractor.overall_verdict}")

    print("\n[Generator]")
    print(f"Score   : {result.generator.overall_score:.1f}/5")
    print(f"Verdict : {result.generator.overall_verdict}")

    if result.verifier:
        print("\n[Verifier]")
        print(f"Score   : {result.verifier.overall_score:.1f}/5")
        print(f"Verdict : {result.verifier.overall_verdict}")

    print("\nTop strengths:")
    for item in result.summary.get("top_strengths", []):
        print(f"- {item}")

    print("\nTop recommended revisions:")
    for item in result.summary.get("top_generator_revisions", []):
        print(f"- {item}")

    print("\nKey unsupported claims:")
    for item in result.summary.get("key_unsupported_claims", []):
        print(f"- {item}")

    print("\nKey missing elements:")
    for item in result.summary.get("key_missing_elements", []):
        print(f"- {item}")


# ------------------------------------------------------------------------------
# Example Dummy Client
# ------------------------------------------------------------------------------

class DummyLLMClient:
    """
    Placeholder client for local testing of the harness wiring.

    Replace this with your real model client. For example, your implementation
    could call:
    - an internal tool
    - a model SDK
    - a local inference server
    - a VS Code task wrapper
    """

    def generate(self, prompt: str) -> str:
        # This is only a stub. It returns a minimal valid JSON structure so the
        # harness can be tested without a real model.
        if "critical_field_precision" in prompt:
            return json.dumps({
                "dimension_scores": {
                    "critical_field_precision": {"score": 4, "rationale": "Most fields match source."},
                    "critical_field_recall": {"score": 4, "rationale": "Most core fields were captured."},
                    "uncertainty_handling": {"score": 4, "rationale": "Ambiguity was mostly handled appropriately."},
                    "schema_quality": {"score": 5, "rationale": "Structured output is clean and usable."}
                },
                "incorrect_fields": [],
                "missing_fields": ["study duration not extracted explicitly"],
                "ambiguity_errors": [],
                "critical_failure": {"present": False, "reason": ""},
                "overall_score": 4.3,
                "overall_verdict": "Pass with minor revision"
            })

        if "true_issue_detection" in prompt:
            return json.dumps({
                "dimension_scores": {
                    "true_issue_detection": {"score": 4, "rationale": "Most substantive issues were detected."},
                    "false_positive_control": {"score": 4, "rationale": "Few unsupported criticisms."},
                    "actionability_of_feedback": {"score": 5, "rationale": "Recommendations are concrete."},
                    "prioritization_of_issues": {"score": 4, "rationale": "Major issues were appropriately prioritized."}
                },
                "missed_issues": [],
                "false_positives": [],
                "useful_feedback_examples": ["Requested tighter phrasing for unsupported center claim."],
                "critical_failure": {"present": False, "reason": ""},
                "overall_score": 4.3,
                "overall_verdict": "Pass with minor revision"
            })

        return json.dumps({
            "dimension_scores": {
                "source_faithfulness": {"score": 4, "rationale": "Mostly grounded in source text."},
                "completeness": {"score": 4, "rationale": "Most critical design elements are present."},
                "regulatory_writing_quality": {"score": 4, "rationale": "Tone and clarity are generally appropriate."},
                "detail_level_fit": {"score": 5, "rationale": "Detail level aligns well with target."},
                "internal_consistency": {"score": 4, "rationale": "No major internal contradictions noted."}
            },
            "critical_failure": {"present": False, "reason": ""},
            "missing_elements": ["study duration phrasing could be more explicit"],
            "unsupported_claims": [],
            "ambiguities": ["unclear whether single-center detail is source-supported"],
            "strengths": [
                "Clear high-level design summary",
                "Appropriate regulatory tone",
                "Good alignment with extracted design features"
            ],
            "recommended_revisions": [
                "Clarify study duration if source text supports it",
                "Remove or soften center-structure wording unless explicit in source"
            ],
            "overall_score": 4.1,
            "overall_verdict": "Pass with minor revision"
        })


# ------------------------------------------------------------------------------
# Example Main
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    workflow_input = WorkflowEvaluationInput(
        source_text=(
            "This was a Phase 1, randomized, double-blind, placebo-controlled study "
            "in healthy adult participants. Participants were assigned to receive either "
            "investigational product or placebo."
        ),
        structured_elements=json.dumps({
            "phase": "Phase 1",
            "design": "randomized, double-blind, placebo-controlled",
            "population": "healthy adult participants",
            "groups": ["investigational product", "placebo"]
        }, indent=2),
        generated_text=(
            "This Phase 1 study was randomized, double-blind, and placebo-controlled "
            "in healthy adult participants. Participants received investigational product "
            "or placebo."
        ),
        target_detail_level="Standard",
        verifier_output=(
            "The draft is mostly accurate, but verify whether study duration and center "
            "structure are explicitly stated in the source before adding them."
        ),
        optional_reference_text=""
    )

    client = DummyLLMClient()

    result = evaluate_workflow(
        llm_client=client,
        workflow_input=workflow_input,
        extractor_prompt_path="evaluation/study_design_extractor_scorer.md",
        generator_prompt_path="evaluation/csr_study_design_generator_scorer.md",
        verifier_prompt_path="evaluation/study_design_verifier_scorer.md",
    )

    print_human_summary(result)
    save_result_json(result, "evaluation_outputs/sample_workflow_evaluation.json")
