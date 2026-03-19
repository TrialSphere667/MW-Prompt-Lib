# CSR Study Design Workflow Rules

This document defines the shared rules, terminology, and operating conventions for the CSR Study Design modular workflow.

These rules apply across all modules in the workflow, including:
- extractor
- generator
- verifier
- generator scorer
- verifier scorer

The purpose of these shared rules is to ensure that all modules operate under the same assumptions, evidence hierarchy, terminology, and quality logic.

---

## 1. Workflow Objective

The CSR Study Design workflow is intended to support source-grounded, modular generation and evaluation of a CSR Study Design section.

The workflow should:
- preserve factual faithfulness to source text
- reduce hallucination risk
- improve completeness through structured extraction
- support human review
- distinguish between generation quality and verification quality
- provide outputs that are reviewable, testable, and reusable

The workflow is not intended to:
- infer unstated study design details
- replace source-grounded human judgment
- reward polished language when content is unsupported
- use style examples as a substitute for factual evidence

---

## 2. Standard Workflow Sequence

The intended workflow is:

1. SOURCE_TEXT is provided
2. Extractor identifies source-supported study design elements
3. STRUCTURED_ELEMENTS are reviewed if needed
4. Generator produces CSR Study Design text
5. Verifier reviews the generated text
6. Generator scorer evaluates generated output quality
7. Verifier scorer evaluates verifier performance

Conceptually:

SOURCE_TEXT  
→ EXTRACTOR  
→ STRUCTURED_ELEMENTS  
→ GENERATOR  
→ GENERATED_TEXT  
→ VERIFIER  
→ VERIFIER_OUTPUT  
→ SCORERS

---

## 3. Source Hierarchy

All modules must apply the following hierarchy strictly:

1. **SOURCE_TEXT** = primary ground truth
2. **STRUCTURED_ELEMENTS** = secondary source-derived representation
3. **OPTIONAL_STYLE_GUIDANCE** = style only, never factual authority

### Rules
- If SOURCE_TEXT and STRUCTURED_ELEMENTS differ in certainty, specificity, or emphasis, follow SOURCE_TEXT.
- STRUCTURED_ELEMENTS may help improve completeness, organization, and issue detection, but must not override SOURCE_TEXT.
- OPTIONAL_STYLE_GUIDANCE may influence tone, flow, and structure only.
- OPTIONAL_STYLE_GUIDANCE must never contribute study facts, design assumptions, or methodological descriptors unless independently supported by SOURCE_TEXT.

---

## 4. Core Workflow Rule

**Do not introduce unsupported study design content.**

This rule applies across extraction, generation, verification, and scoring.

Where uncertainty exists:
- prefer omission over unsupported inference
- prefer conservative wording over polished overstatement
- prefer explicit uncertainty handling over hidden assumption

---

## 5. Support Categories

These support categories must be used consistently across modules.

### supported
Clearly stated in SOURCE_TEXT, or directly and clearly represented in STRUCTURED_ELEMENTS without meaningful ambiguity.

### weakly_supported
Plausibly derived from SOURCE_TEXT, but not clearly or explicitly stated.

### unsupported
Not supported by SOURCE_TEXT, materially stronger than the source supports, contradictory, fabricated, or inferred beyond what is reasonably justified.

### Usage rules
- Do not convert weakly supported content into definitive statements.
- Generators should generally omit weakly supported content unless explicitly allowed by workflow design.
- Verifiers may flag weakly supported content as cautionary rather than definite error when appropriate.
- Scorers should distinguish weak support from outright unsupported content.

---

## 6. Materiality Categories

These materiality categories must be used consistently across modules.

### major
Changes the reader’s understanding of study design, creates meaningful factual or regulatory risk, or makes output unsafe to rely on.

### moderate
A meaningful weakness or omission that should be revised.

### minor
A low-risk issue with limited impact on understanding or usability.

### Usage rules
- Not all errors should be treated equally.
- Major issues should be prioritized over moderate and minor issues.
- Critical failure logic should be driven mainly by major issues.

---

## 7. Applicability Rule

A study design element should only be included, expected, or penalized if it is:

1. supported by SOURCE_TEXT and/or clearly represented in STRUCTURED_ELEMENTS, and
2. applicable to the study

### Do not force inclusion or penalize omission of elements that are:
- not stated
- not applicable
- only weakly implied
- uncertain or fragmented in source

This rule is especially important for:
- comparator/control
- blinding
- center structure
- duration
- crossover vs parallel terminology
- dose-escalation structure
- special design features

---

## 8. Style Guidance Policy

OPTIONAL_STYLE_GUIDANCE is allowed only for:
- tone
- phrasing style
- sentence flow
- paragraph structure
- level of formality

OPTIONAL_STYLE_GUIDANCE must not be used to:
- add study facts
- imply design features
- borrow unsupported methodological wording
- strengthen weak support into certainty

If OPTIONAL_STYLE_GUIDANCE conflicts with source-grounded content rules, ignore it.

---

## 9. Shared Expectations by Module

## Extractor
Purpose:
- identify source-supported study design facts
- structure them for downstream use
- flag ambiguities and unclear areas
- avoid adding interpretation beyond support

Extractor should not:
- invent missing design detail
- convert ambiguity into certainty

## Generator
Purpose:
- convert supported facts into a coherent CSR Study Design paragraph
- maintain source faithfulness
- adjust content density according to TARGET_DETAIL_LEVEL

Generator should not:
- infer typical study design detail
- overstate certainty
- import factual content from style guidance

## Verifier
Purpose:
- assess GENERATED_TEXT against SOURCE_TEXT and STRUCTURED_ELEMENTS
- identify unsupported claims, omissions, inconsistencies, and meaningful style issues

Verifier should not:
- invent issues
- treat style preference as factual defect
- use style guidance as factual authority

## Generator scorer
Purpose:
- evaluate generated text quality
- assess factual faithfulness, completeness, writing quality, detail fit, and internal consistency

Generator scorer should not:
- reward polished writing when content is unsupported
- collapse all issue types into a single undifferentiated quality judgment

## Verifier scorer
Purpose:
- evaluate whether the verifier identified real issues accurately and usefully
- assess sensitivity, specificity, actionability, and prioritization

Verifier scorer should not:
- reward a verifier for sounding rigorous if it misses major problems or creates unsupported criticism

---

## 10. Shared Input Names

Use the following input names consistently wherever applicable:

- `SOURCE_TEXT`
- `STRUCTURED_ELEMENTS`
- `GENERATED_TEXT`
- `VERIFIER_OUTPUT`
- `TARGET_DETAIL_LEVEL`
- `OPTIONAL_STYLE_GUIDANCE`

Not all modules require all fields, but naming should remain stable across the prompt pack.

---

## 11. Shared Output Design Principles

Outputs should be:
- structured where appropriate
- concise but sufficient
- easy to review
- easy to compare across runs
- easy to use in downstream modules

### General output philosophy
- Separate issue types where possible
- Distinguish unsupported from weakly supported content
- Distinguish omission from contradiction
- Use severity labels when useful
- Prefer concrete revision guidance over vague comments

---

## 12. Shared Critical Failure Policy

A critical failure is present when an output contains, misses, or mishandles an issue that materially changes understanding of study design or creates meaningful factual/regulatory risk.

Examples include:
- incorrect phase
- incorrect randomization
- incorrect blinding
- incorrect comparator/control
- incorrect population characterization
- invented major design feature
- major omission that makes the output misleading
- major contradiction with SOURCE_TEXT
- materially misleading overall design characterization

### Rules
- Critical failure should be flagged clearly.
- Critical failure should override otherwise strong performance in lower-priority dimensions.
- Numeric scoring should not conceal critical safety problems.

---

## 13. Shared Detail-Level Policy

The workflow recognizes three target detail levels:

### Expanded
Include all supported and relevant study design detail that materially helps characterize the study.

### Standard
Include the key design elements needed for a balanced CSR summary.

### Abbreviated
Include only the essential design-defining elements needed for a safe high-level summary.

### Rules
- Do not invent detail to satisfy a higher level.
- Do not compress so aggressively that the output becomes misleading.
- Omission of low-value detail may be acceptable at lower detail levels.
- Omission of major design-defining detail is not acceptable solely because a lower detail level was requested.

---

## 14. Shared Review Philosophy

Across the workflow:
- factual safety takes priority over elegance
- completeness should be judged relative to support and applicability
- style matters, but only after factual reliability
- outputs should support human review rather than obscure uncertainty

Where trade-offs arise:
- prefer grounded conservatism over fluent overreach
- prefer explicit issue typing over vague criticism
- prefer operational usefulness over theoretical completeness

---

## 15. Maintenance Guidance

When updating any module:
- preserve the shared source hierarchy
- preserve support and materiality definitions
- preserve the style guidance policy
- preserve consistent input names where possible
- align verdict logic with the rest of the workflow

If one module changes its core assumptions, the shared rules should be reviewed before the module is adopted.

---

## 16. Summary

This workflow pack is intended to function as a coherent modular system, not as a loose collection of prompts.

All modules should therefore remain aligned on:
- evidence hierarchy
- support definitions
- materiality
- applicability
- critical failure logic
- detail-level expectations
- style-guidance boundaries
