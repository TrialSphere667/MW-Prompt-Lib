from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

from csr_study_design_evaluation import (
    WorkflowEvaluationInput,
    run_generator_evaluation,
    load_prompt,
    render_prompt,
    extract_json_object,
    parse_generator_result,
)


# ------------------------------------------------------------------------------
# Replace this with your real LLM client
# ------------------------------------------------------------------------------

class DummyLLMClient:
    def generate(self, prompt: str) -> str:
        # This is only a stub.
        # Replace with your actual model call.
        if "version_b_marker" in prompt:
            return (
                "This Phase 1 study was randomized, double-blind, and placebo-controlled "
                "in healthy adult participants receiving investigational product or placebo."
            )
        return (
            "This was a Phase 1 randomized, double-blind, placebo-controlled study in "
            "healthy adult participants."
        )


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------

def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_case(case_dir: Path) -> WorkflowEvaluationInput:
    metadata = read_json(case_dir / "metadata.json")

    source_text = read_text(case_dir / "source_text.txt")
    structured_elements = read_text(case_dir / "structured_elements_gold.json")
    reference_text_path = case_dir / "reference_text.txt"
    reference_text = read_text(reference_text_path) if reference_text_path.exists() else None

    return WorkflowEvaluationInput(
        source_text=source_text,
        structured_elements=structured_elements,
        generated_text="",  # filled later
        target_detail_level=metadata.get("target_detail_level", "Standard"),
        verifier_output=None,
        optional_reference_text=reference_text,
    )


def generate_text(
    llm_client,
    generator_prompt_path: Path,
    workflow_input: WorkflowEvaluationInput,
) -> str:
    template = load_prompt(generator_prompt_path)
    prompt = render_prompt(
        template,
        {
            "SOURCE_TEXT": workflow_input.source_text,
            "STRUCTURED_ELEMENTS": workflow_input.structured_elements,
            "TARGET_DETAIL_LEVEL": workflow_input.target_detail_level,
        },
    )
    return llm_client.generate(prompt).strip()


def score_generated_text(
    llm_client,
    scorer_prompt_path: Path,
    workflow_input: WorkflowEvaluationInput,
    generated_text: str,
):
    scored_input = WorkflowEvaluationInput(
        source_text=workflow_input.source_text,
        structured_elements=workflow_input.structured_elements,
        generated_text=generated_text,
        target_detail_level=workflow_input.target_detail_level,
        verifier_output=None,
        optional_reference_text=workflow_input.optional_reference_text,
    )
    return run_generator_evaluation(
        llm_client=llm_client,
        prompt_path=scorer_prompt_path,
        workflow_input=scored_input,
    )


def choose_winner(result_a, result_b) -> str:
    # Critical failure overrides score
    if result_a.critical_failure.present and not result_b.critical_failure.present:
        return "B"
    if result_b.critical_failure.present and not result_a.critical_failure.present:
        return "A"

    if result_a.overall_score > result_b.overall_score:
        return "A"
    if result_b.overall_score > result_a.overall_score:
        return "B"
    return "Tie"


def summarise_case(
    case_id: str,
    result_a,
    result_b,
    winner: str,
    prompt_a_name: str,
    prompt_b_name: str,
) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "prompt_a": prompt_a_name,
        "prompt_b": prompt_b_name,
        "score_a": result_a.overall_score,
        "score_b": result_b.overall_score,
        "verdict_a": result_a.overall_verdict,
        "verdict_b": result_b.overall_verdict,
        "critical_failure_a": result_a.critical_failure.present,
        "critical_failure_b": result_b.critical_failure.present,
        "source_faithfulness_a": result_a.dimension_scores["source_faithfulness"].score,
        "source_faithfulness_b": result_b.dimension_scores["source_faithfulness"].score,
        "completeness_a": result_a.dimension_scores["completeness"].score,
        "completeness_b": result_b.dimension_scores["completeness"].score,
        "writing_quality_a": result_a.dimension_scores["regulatory_writing_quality"].score,
        "writing_quality_b": result_b.dimension_scores["regulatory_writing_quality"].score,
        "unsupported_claims_a": len(result_a.unsupported_claims),
        "unsupported_claims_b": len(result_b.unsupported_claims),
        "missing_elements_a": len(result_a.missing_elements),
        "missing_elements_b": len(result_b.missing_elements),
        "winner": winner,
    }


def write_csv(rows: List[Dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        return
    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def compute_summary(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    n = len(rows)
    if n == 0:
        return {}

    def avg(key: str) -> float:
        return round(sum(float(r[key]) for r in rows) / n, 2)

    wins_a = sum(1 for r in rows if r["winner"] == "A")
    wins_b = sum(1 for r in rows if r["winner"] == "B")
    ties = sum(1 for r in rows if r["winner"] == "Tie")

    cf_a = sum(1 for r in rows if r["critical_failure_a"])
    cf_b = sum(1 for r in rows if r["critical_failure_b"])

    return {
        "n_cases": n,
        "avg_score_a": avg("score_a"),
        "avg_score_b": avg("score_b"),
        "avg_source_faithfulness_a": avg("source_faithfulness_a"),
        "avg_source_faithfulness_b": avg("source_faithfulness_b"),
        "avg_completeness_a": avg("completeness_a"),
        "avg_completeness_b": avg("completeness_b"),
        "avg_writing_quality_a": avg("writing_quality_a"),
        "avg_writing_quality_b": avg("writing_quality_b"),
        "avg_unsupported_claims_a": avg("unsupported_claims_a"),
        "avg_unsupported_claims_b": avg("unsupported_claims_b"),
        "avg_missing_elements_a": avg("missing_elements_a"),
        "avg_missing_elements_b": avg("missing_elements_b"),
        "critical_failure_rate_a": round(cf_a / n, 2),
        "critical_failure_rate_b": round(cf_b / n, 2),
        "wins_a": wins_a,
        "wins_b": wins_b,
        "ties": ties,
    }


def main() -> None:
    dataset_dir = Path("gold_standard")
    output_dir = Path("ab_test_outputs")

    prompt_a_path = Path("generation/v1/csr_study_design_generator.md")
    prompt_b_path = Path("generation/v2/csr_study_design_generator.md")
    scorer_prompt_path = Path("evaluation/csr_study_design_generator_scorer.md")

    prompt_a_name = "v1"
    prompt_b_name = "v2"

    llm_client = DummyLLMClient()

    rows: List[Dict[str, Any]] = []
    detailed_outputs: Dict[str, Any] = {"cases": []}

    for case_dir in sorted(dataset_dir.iterdir()):
        if not case_dir.is_dir():
            continue

        case_id = case_dir.name
        workflow_input = load_case(case_dir)

        generated_a = generate_text(llm_client, prompt_a_path, workflow_input)
        generated_b = generate_text(llm_client, prompt_b_path, workflow_input)

        result_a = score_generated_text(llm_client, scorer_prompt_path, workflow_input, generated_a)
        result_b = score_generated_text(llm_client, scorer_prompt_path, workflow_input, generated_b)

        winner = choose_winner(result_a, result_b)

        row = summarise_case(
            case_id=case_id,
            result_a=result_a,
            result_b=result_b,
            winner=winner,
            prompt_a_name=prompt_a_name,
            prompt_b_name=prompt_b_name,
        )
        rows.append(row)

        detailed_outputs["cases"].append({
            "case_id": case_id,
            "generated_a": generated_a,
            "generated_b": generated_b,
            "result_a": asdict(result_a),
            "result_b": asdict(result_b),
            "winner": winner,
        })

        print(
            f"{case_id}: winner={winner} | "
            f"{prompt_a_name}={result_a.overall_score:.1f} | "
            f"{prompt_b_name}={result_b.overall_score:.1f}"
        )

    summary = compute_summary(rows)

    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(rows, output_dir / "ab_test_summary.csv")
    (output_dir / "ab_test_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    (output_dir / "ab_test_detailed.json").write_text(
        json.dumps(detailed_outputs, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\nA/B test complete.")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
