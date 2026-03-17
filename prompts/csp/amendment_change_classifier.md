# Amendment Change Classifier Prompt

## Task

Classify an amendment change description into the most relevant protocol amendment category or categories.

This prompt is intended to normalize amendment language into structured categories that can be used for dependency lookup, impact discovery, protocol retrieval, and revision workflows.

---

# Purpose

Amendment descriptions are often written in inconsistent or highly variable language. Before downstream impact analysis, it is useful to classify the change into one or more standardized categories.

Examples:
- "Updated eligibility requirements for renal function" → Eligibility Criteria
- "Revised timing of PK blood draws" → PK Assessments / Visit Schedule
- "Clarified primary endpoint definition" → Endpoint Definitions

---

# Input

### Amendment Change
[INSERT AMENDMENT CHANGE HERE]

---

# Instructions

Analyze the amendment change and determine the most likely amendment category.

Possible categories include:

- study objectives
- study design
- eligibility criteria
- inclusion criteria
- exclusion criteria
- treatment regimen / dose / administration
- endpoint definitions
- estimands
- sample size / population
- randomization / blinding
- visit schedule / schedule of assessments
- study procedures
- safety monitoring
- efficacy assessments
- laboratory assessments
- PK assessments
- PD / biomarker assessments
- statistical analysis methods
- analysis populations
- concomitant medications / prior treatments
- protocol deviations
- administrative / operational changes
- synopsis

If the amendment clearly affects more than one category, identify:
- one **Primary Change Category**
- optional **Secondary Categories**

If the classification is uncertain, state the most likely category and explain the uncertainty briefly.

---

# Rules

1. Base the classification only on the amendment text provided.
2. Do not infer broader downstream impacts yet; only classify the change itself.
3. Use the most specific category possible where the amendment wording supports it.
4. If the wording is broad, choose the best higher-level category.
5. If multiple categories are plausible, list them in order of relevance.

---

# Output Format

## Classification

- **Primary Change Category:** [category]
- **Secondary Categories:** [list or "None"]
- **Confidence:** High / Moderate / Low

## Rationale

Provide a brief explanation of why the change was classified this way.

---

# Example

### Amendment Change
"Inclusion criteria updated to allow patients with mild renal impairment."

## Classification

- **Primary Change Category:** Inclusion Criteria
- **Secondary Categories:** Eligibility Criteria
- **Confidence:** High

## Rationale

The amendment directly changes who is eligible for enrollment and specifically refers to an inclusion condition related to renal function.
