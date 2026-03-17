# Amendment Impact Discovery Prompt

## Task

Analyze a protocol amendment change and identify all protocol domains and sections that may be affected, including both direct and indirect impacts.

This prompt uses a protocol dependency map as supporting guidance to improve impact discovery.

It is intended to identify likely review areas before protocol passage retrieval and revision generation.

---

# Purpose

Protocol amendments often affect multiple protocol sections beyond the obvious primary change.

For example:

- eligibility changes may affect study population, screening procedures, and analysis populations
- endpoint changes may affect objectives, estimands, and statistical methods
- visit schedule changes may affect assessments, procedures, and safety monitoring

This prompt helps identify those dependencies systematically so that the medical writer can review the correct areas of the protocol.

---

# Inputs

### Amendment Change
[INSERT AMENDMENT CHANGE HERE]

### Protocol Dependency Guidance
[INSERT PROTOCOL DEPENDENCY GUIDANCE HERE]

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

If the amendment could plausibly belong to more than one category, list the primary category and any secondary candidate categories.

---

## Step 2 — Use the dependency guidance

Use the protocol dependency guidance provided to identify:

1. the most directly affected protocol domains
2. likely secondary protocol domains that may require review because of downstream dependencies

Do not assume every dependency is impacted, but flag them as review candidates where appropriate.

---

## Step 3 — Recommend protocol review areas

Based on the amendment change and the dependency guidance, identify:

- directly affected protocol sections or domains
- secondary sections or domains to review
- areas where impact is uncertain but worth checking

If exact section titles are unknown, provide general section categories.

---

# Rules

1. Do not propose revised protocol text.
2. Focus only on identifying impacted domains and recommended review areas.
3. Use the dependency guidance as a structured aid, not as a rigid rule.
4. If uncertain, flag the area for review rather than assuming it is unaffected.
5. Prioritize completeness over narrow precision for secondary impacts.

---

# Output Format

## Amendment Classification

- **Primary Change Category:** [category]
- **Possible Secondary Categories:** [list or "None"]

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

## Recommended Protocol Areas for Review

1. Section title or category
2. Section title or category
3. Section title or category
4. Section title or category

---

## Rationale

Provide a short explanation of:

- why the primary category was chosen
- why the listed secondary review areas may be relevant
- where the impact remains uncertain

---

# Example

### Amendment Change

"Inclusion criteria updated to allow patients with mild renal impairment."

### Protocol Dependency Guidance

Eligibility criteria may affect:
- inclusion criteria
- exclusion criteria
- study population
- screening procedures
- statistical analysis populations
- safety monitoring

---

## Amendment Classification

- **Primary Change Category:** Eligibility Criteria
- **Possible Secondary Categories:** Study Population

---

## Directly Affected Domains

- Inclusion Criteria
- Exclusion Criteria

---

## Potential Secondary Impact Domains

- Study Population
- Screening Procedures
- Statistical Analysis Populations
- Safety Monitoring

---

## Recommended Protocol Areas for Review

1. Inclusion Criteria
2. Exclusion Criteria
3. Study Population
4. Screening Procedures
5. Safety Monitoring
6. Analysis Populations

---

## Rationale

The amendment directly changes subject eligibility, so inclusion and exclusion sections are the primary review areas. Based on dependency guidance, the enrolled population, related screening procedures, downstream analysis populations, and safety-related monitoring language may also need review.
