# CSR Study Design Core Extraction Schema

Extract only study design information that is explicitly stated or reasonably supportable from the source text.

Do NOT invent or over-specify.

If an element is not stated, unclear, or not applicable, indicate that explicitly.

---

## OUTPUT FORMAT

Return structured JSON only.

{
  "study_identification": {
    "study_phase": "",
    "study_type": "",
    "study_objective_or_design_purpose": "",
    "population_type": "",
    "indication_or_context": ""
  },
  "overall_design": {
    "overall_design_summary": "",
    "randomized": "",
    "randomization_details": "",
    "blinding_status": "",
    "blinding_details": "",
    "control_status": "",
    "comparator_type": "",
    "comparator_description": "",
    "parallel_or_crossover": "",
    "center_structure": "",
    "number_of_centers": ""
  },
  "population": {
    "population_description": "",
    "key_population_qualifiers": [],
    "special_population_notes": ""
  },
  "treatment_structure": {
    "number_of_treatment_groups_or_arms": "",
    "treatment_groups_or_arms_description": [],
    "number_of_cohorts": "",
    "cohort_structure": "",
    "dose_escalation_structure": "",
    "treatment_sequence_structure": "",
    "sentinel_dosing": "",
    "special_design_components": []
  },
  "study_structure": {
    "number_of_parts": "",
    "part_descriptions": [],
    "number_of_periods": "",
    "period_descriptions": [],
    "screening_period": "",
    "treatment_period": "",
    "washout_period": "",
    "follow_up_period": "",
    "extension_period": ""
  },
  "duration_timing": {
    "overall_study_duration": "",
    "participant_duration": "",
    "treatment_duration": "",
    "follow_up_duration": ""
  },
  "special_design_features": {
    "adaptive_features": "",
    "cohort_expansion": "",
    "interim_review_features": "",
    "substudies_or_design_subcomponents": [],
    "other_special_design_features": []
  },
  "objective_framing": {
    "primary_design_objective_framing": "",
    "secondary_design_objective_framing": ""
  },
  "source_quality_flags": {
    "ambiguities": [],
    "missing_or_unclear_design_elements": [],
    "weakly_supported_interpretations": [],
    "elements_requiring_human_review": []
  }
}
