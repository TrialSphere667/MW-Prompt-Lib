# Study Design Element Extractor Prompt

## Task

Extract the key study design elements from the provided CSP section(s) in a structured format.

---

## Purpose

The purpose of this prompt is to convert protocol study design text into structured elements that can later be used to generate a CSR Study Design narrative.

This is an extraction task, not a writing task.

---

## Inputs

### Study Design Schema
[INSERT STUDY DESIGN SCHEMA HERE]

### CSP Source Text
[INSERT CSP STUDY DESIGN TEXT HERE]

---

## Instructions

Review the CSP text and extract the study design elements explicitly supported by the source.

Use the schema as a guide, but do not force extraction of elements that are not stated.

For each element:
- extract the relevant information exactly and clearly
- preserve scientific meaning
- preserve numerical values exactly
- if an element is not explicitly stated, write: "Not explicitly stated"

If multiple related statements appear in the source, synthesize them into one concise structured entry without changing meaning.

---

## Rules

1. Use only the provided CSP text.
2. Do not generate CSR narrative.
3. Do not infer missing study design details.
4. Preserve numbers, arms, durations, and design terminology exactly where possible.
5. If wording is ambiguous, flag it briefly rather than guessing.

---

## Output Format

## Extracted Study Design Elements

- **Study Phase:** ...
- **Study Design Type:** ...
- **Study Setting / Number of Centers:** ...
- **Treatment Arms / Cohorts:** ...
- **Study Population:** ...
- **Randomization:** ...
- **Blinding / Masking:** ...
- **Control Type:** ...
- **Treatment Duration:** ...
- **Follow-up Duration:** ...
- **Route of Administration:** ...
- **Dose Levels / Regimen:** ...
- **Study Objectives:** ...
- **Primary Endpoint(s):** ...
- **Secondary Endpoint(s):** ...
- **Key Procedures or Design Features:** ...
- **Notable Design Features:** ...

---

## Source Gaps / Ambiguities

List any elements that are unclear, incomplete, or only partially described in the source text.

---

## Example

- **Study Phase:** Phase 2
- **Study Design Type:** Randomized, double-blind, placebo-controlled, multicenter study
- **Treatment Arms / Cohorts:** 3 treatment arms
- **Study Population:** Adult patients with [condition]
- **Randomization:** Subjects randomized 1:1:1
- **Blinding / Masking:** Double-blind
- **Treatment Duration:** 12 weeks
- **Primary Endpoint(s):** [endpoint]
- **Notable Design Features:** Not explicitly stated
