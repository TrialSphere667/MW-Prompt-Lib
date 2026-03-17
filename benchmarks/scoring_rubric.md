# AI Output Scoring Rubric for Regulatory MW Benchmarking

This rubric is used to evaluate AI-generated summaries for regulatory medical writing tasks, especially TLF-based summarization.

## Total Score: 10 points

---

## 1. Numeric Fidelity (0–4 points)

Evaluate whether all numerical values are preserved accurately.

Consider:
- exact preservation of numbers
- preservation of percentages
- preservation of denominators (e.g., n/N)
- no introduction of unsupported numbers
- no incorrect rounding changes

### Scoring
- **4** = all numbers preserved exactly
- **3** = minor omission or formatting simplification, but no incorrect numbers
- **2** = one important numeric issue
- **1** = multiple numeric issues
- **0** = major numeric unreliability

---

## 2. Faithfulness / Hallucination Risk (0–2 points)

Evaluate whether the output is fully supported by the source table.

Consider:
- unsupported claims
- invented interpretation
- implied significance not shown in the data
- overstatement of findings

### Scoring
- **2** = fully grounded in source, no unsupported claims
- **1** = minor unsupported wording or slight overinterpretation
- **0** = clear unsupported claims or invented interpretation

---

## 3. Completeness of Key Findings (0–2 points)

Evaluate whether the summary captures the most important findings from the table.

Consider:
- main treatment comparisons
- major endpoint or event findings
- inclusion of central results
- omission of key information

### Scoring
- **2** = key findings captured well
- **1** = partially complete, one notable omission
- **0** = major omissions

---

## 4. Regulatory Tone and Clarity (0–1 point)

Evaluate whether the output uses appropriate regulatory writing style.

Consider:
- neutral and objective tone
- concise presentation
- clarity of wording
- avoidance of promotional or speculative language

### Scoring
- **1** = appropriate regulatory tone and clear wording
- **0** = too interpretive, unclear, casual, or stylistically unsuitable

---

## 5. Domain-Appropriate Summarization (0–1 point)

Evaluate whether the output emphasizes the right kinds of information for the table type.

Examples:
- efficacy: endpoints, treatment comparisons
- safety: incidence, common events, serious events
- PK: parameters such as Cmax, Tmax, AUC, t1/2
- PD/biomarkers: levels, change from baseline, responder status
- demographics: baseline characteristics

### Scoring
- **1** = emphasis is appropriate for the table type
- **0** = emphasis is poorly matched to the table type

---

## Interpretation Guide

- **9–10** = strong output, likely usable with minor edits
- **7–8** = acceptable draft, requires review and revision
- **5–6** = limited utility, substantial revision required
- **0–4** = unreliable output, not suitable for drafting use

---

## Suggested Logging Fields

For each benchmark run, record:
- task name
- table type
- prompt version
- model name
- numeric fidelity score
- hallucination score
- completeness score
- tone/clarity score
- domain-fit score
- total score
- reviewer notes
