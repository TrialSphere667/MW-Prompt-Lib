# Amendment Impact Discovery Prompt

## Task

Analyze a protocol amendment change and identify all protocol domains and sections that may be affected, including both direct and indirect impacts.

This prompt is designed to identify potential ripple effects across the protocol before revision suggestions are generated.

---

# Purpose

Protocol amendments often affect multiple sections beyond the obvious primary change.

For example:

- eligibility changes may affect study population, safety monitoring, and analysis populations
- endpoint changes may affect objectives, estimands, and statistical methods
- visit schedule changes may affect assessments, procedures, and safety monitoring

This prompt helps identify those potential dependencies so that the medical writer can review the correct areas of the protocol.

---

# Inputs

### Amendment Change

[INSERT AMENDMENT CHANGE HERE]

---

# Instructions

## Step 1 — Classify the primary change

Identify the most likely amendment category.

Possible categories include:

- study objectives
- study design
- eligibility criteria
- treatment regimen
- endpoint definitions
- visit schedule / assessments
- safety monitoring
- statistical analysis
- sample size / population
- investigational product administration
- administrative or operational updates

---

## Step 2 — Identify directly affected domains

List the protocol domains most directly related to the amendment.

These domains represent the sections most likely to require textual revision.

---

## Step 3 — Identify potential secondary impacts

Determine which additional protocol areas may require review because of the change.

Examples:

Eligibility changes may affect:
- exclusion criteria
- study population description
- analysis populations
- safety monitoring

Endpoint changes may affect:
- objectives
- estimands
- statistical analysis methods

Visit schedule changes may affect:
- assessments
- procedures
- safety monitoring

---

## Step 4 — Suggest likely protocol sections

Based on the amendment type, identify protocol sections that the medical writer should review.

Examples may include:

- Inclusion Criteria
- Exclusion Criteria
- Study Population
- Statistical Analysis Populations
- Safety Monitoring
- Study Procedures
- Endpoints
- Objectives
- Schedule of Assessments

If the exact section titles are unknown, provide general section categories.

---

# Rules

1. Do not propose revised protocol text.
2. Focus only on identifying impacted domains and sections.
3. If uncertain, flag areas for review rather than assuming changes.
4. Prioritize completeness over precision when identifying possible ripple effects.

---

# Output Format

## Amendment Classification

Primary Change Category:  
[category]

---

## Directly Affected Domains

- domain 1
- domain 2
- domain 3

---

## Potential Secondary Impact Domains

- domain 1
- domain 2
- domain 3

---

## Protocol Sections Recommended for Review

1. Section title or category
2. Section title or category
3. Section title or category
4. Section title or category

---

## Rationale

Brief explanation of why these areas may be impacted by the amendment.

---

# Example

### Amendment Change

"Inclusion criteria updated to allow patients with mild renal impairment."

---

### Amendment Classification

Primary Change Category: Eligibility Criteria

---

### Directly Affected Domains

- Inclusion Criteria
- Exclusion Criteria

---

### Potential Secondary Impact Domains

- Study Population Description
- Safety Monitoring
- Statistical Analysis Populations

---

### Protocol Sections Recommended for Review

1. Inclusion Criteria
2. Exclusion Criteria
3. Study Population
4. Safety Monitoring
5. Analysis Populations

---

### Rationale

Changes to eligibility criteria alter the characteristics of the enrolled population, which may influence safety monitoring procedures and statistical population definitions.
