# CSR Study Design Verifier Prompt

## Task

Verify whether the generated CSR Study Design section is fully supported by the structured study design extraction and remains appropriate for CSR use.

---

## Purpose

This prompt is used after generation to confirm that the Study Design narrative:
- is grounded in the extracted source elements
- does not introduce unsupported claims
- preserves numerical and design details accurately
- includes the key study design elements appropriate for the selected level of detail

---

## Inputs

### Generated CSR Study Design Section
[INSERT GENERATED STUDY DESIGN SECTION HERE]

### Structured Study Design Elements
[INSERT STRUCTURED STUDY DESIGN ELEMENTS HERE]

### Desired Level of Detail
[INSERT ONE: Expanded / Standard / Abbreviated]

---

## Instructions

Review the generated Study Design section against the structured elements.

For each major statement in the generated section, determine whether it is:
- **Supported**
- **Partially Supported**
- **Unsupported**
- **Needs Human Review**

Also assess:
- whether key expected elements are missing
- whether numerical values and design terminology were preserved correctly
- whether the narrative matches the requested level of detail
- whether the section introduces interpretation or assumptions beyond the source

---

## Rules

1. Use only the structured elements as the verification source.
2. Do not rewrite the section unless explicitly asked.
3. Treat ambiguous support conservatively.
4. Flag unsupported additions clearly.
5. Preserve a QC mindset.

---

## Output Format

## Statement-Level Verification

For each major statement:

- **Statement:** ...
- **Support Status:** Supported / Partially Supported / Unsupported / Needs Human Review
- **Evidence:** ...
- **Numeric / Terminology Check:** Pass / Fail / Not Applicable
- **Comments:** ...

---

## Overall Assessment

- **Overall Reliability:** High / Moderate / Low
- **Matches Requested Level of Detail:** Yes / Partially / No
- **Self-Contained:** Yes / No
- **Human Revision Needed:** Yes / No

---

## Missing or Weakly Supported Elements

List:
- key study design elements missing from the generated section
- unsupported or weakly supported claims
- any wording that should be reviewed manually

---

## Example

- **Statement:** This was a Phase 2, randomized, double-blind, placebo-controlled study.
- **Support Status:** Supported
- **Evidence:** Structured elements list Phase 2, randomized, double-blind, placebo-controlled.
- **Numeric / Terminology Check:** Pass
- **Comments:** Fully supported by extracted study design elements.
