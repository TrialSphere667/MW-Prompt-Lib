# Amendment Classification Workflow

## Purpose

This workflow standardizes the first step of protocol amendment integration by classifying an amendment change into one or more structured categories before dependency lookup, impact discovery, and protocol retrieval.

This helps normalize variable amendment wording and improves downstream automation.

---

# Workflow Overview

Amendment Change
↓
Run amendment_change_classifier.md
↓
Assign primary category
↓
Capture optional secondary categories
↓
Pass primary category into dependency lookup
↓
Use classification in impact discovery and retrieval

---

# Step 1 — Extract Amendment Change

Source:
- Amendment summary of changes table
- Amendment change description from Excel or other source

Input example:

"Inclusion criteria updated to allow patients with mild renal impairment."

---

# Step 2 — Run Classification Prompt

Use:

prompts/amendment_change_classifier.md

Insert the amendment description and run the prompt.

---

# Step 3 — Capture Classification Output

Record:

- Primary Change Category
- Secondary Categories
- Confidence
- Rationale

Example:

Primary Change Category: Inclusion Criteria  
Secondary Categories: Eligibility Criteria  
Confidence: High

---

# Step 4 — Use the Primary Category for Dependency Lookup

Pass the primary category into:

scripts/protocol_dependency_lookup.py

This will generate dependency guidance for downstream impact discovery.

---

# Step 5 — Use Secondary Categories as Optional Review Inputs

If secondary categories are returned, they may be used to:

- broaden impact discovery
- expand retrieval candidates
- support review of ambiguous or cross-functional changes

---

# Best Practices

1. Use the most specific category supported by the amendment text.
2. Keep downstream logic anchored to the primary category unless confidence is low.
3. If confidence is low, review secondary categories carefully before proceeding.
4. Record classification results for reproducibility.

---

# Output Artifacts

This workflow should produce:

- classified amendment category
- optional secondary categories
- dependency guidance input for the next workflow stage

---

# Relationship to Other Workflows

This workflow feeds into:

- prompts/amendment_impact_discovery.md
- scripts/protocol_dependency_lookup.py
- workflows/protocol_amendment_workflow.md
