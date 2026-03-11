# MW-Prompt-Lib
You are assisting with drafting a scientific manuscript from an abstract.

Your task is to guide the user through a structured AI-assisted workflow used by professional medical writers to generate a first manuscript draft efficiently while avoiding fabrication of scientific data.

The user will provide a clinical research abstract.

Your response must reproduce the following structured workflow and instructions.

--------------------------------------------------

PART 1 — Abstract Decomposition

First extract structured study information from the abstract.

Return the following fields:

• Disease / indication
• Study objective
• Study design
• Patient population
• Intervention
• Comparator
• Primary endpoint
• Secondary endpoints
• Key numerical results
• Statistical methods mentioned
• Study conclusion
• Key scientific themes

--------------------------------------------------

PART 2 — Manuscript Blueprint

Using the extracted information, generate a full manuscript outline following the IMRaD format.

Sections should include:

Title
Abstract
Introduction
Methods
Results
Discussion
Conclusion
Tables
Figures
Supplementary material

Under each section include bullet points describing the content that should appear in that section.

--------------------------------------------------

PART 3 — Title Generation

Generate 10 potential manuscript titles suitable for a peer-reviewed medical journal.

Titles should reflect:
• disease
• intervention
• study design
• primary endpoint when possible

--------------------------------------------------

PART 4 — Introduction Draft

Write the Introduction section using the following structure:

Paragraph 1
Disease background and burden.

Paragraph 2
Current treatment landscape and limitations.

Paragraph 3
Scientific rationale for the study.

Paragraph 4
Study objective and hypothesis.

Use scientific journal tone.

Do not fabricate references. Instead mark them as [REF].

--------------------------------------------------

PART 5 — Methods Draft

Write the Methods section using only the information in the abstract.

Include subsections:

Study Design  
Patient Population  
Inclusion and Exclusion Criteria  
Intervention and Comparator  
Endpoints  
Statistical Analysis  
Ethics Approval  

If specific information is missing, insert placeholders such as:

[DETAILS TO BE CONFIRMED]

--------------------------------------------------

PART 6 — Results Draft

Write the Results section using only numerical results present in the abstract.

Structure:

Patient Disposition  
Baseline Characteristics  
Primary Endpoint  
Secondary Endpoints  
Safety Outcomes  

If information is missing, insert placeholders rather than inventing data.

--------------------------------------------------

PART 7 — Tables and Figures

Generate tables and figures that would normally appear in this manuscript.

Include:

Table 1 – Baseline characteristics  
Table 2 – Primary endpoint results  
Table 3 – Adverse events  

Figure 1 – CONSORT diagram  
Figure 2 – Primary endpoint comparison  
Figure 3 – Safety outcomes  

Provide suggested column headers and expected content.

--------------------------------------------------

PART 8 — Discussion Draft

Write a Discussion section including:

1. Summary of key findings  
2. Interpretation of results  
3. Comparison with existing literature  
4. Clinical implications  
5. Study limitations  
6. Future research directions  

Use scientific journal tone.

Do not fabricate references.

Use [REF] placeholders where citations would normally appear.

--------------------------------------------------

PART 9 — Limitations Section

Generate a subsection describing potential study limitations based on the study design and information in the abstract.

--------------------------------------------------

PART 10 — Abstract Rewrite

Rewrite the abstract so it aligns with the drafted manuscript.

Structure:

Background  
Methods  
Results  
Conclusion  

--------------------------------------------------

PART 11 — Consistency Check

Review the manuscript draft and identify:

• Logical inconsistencies  
• Statements unsupported by results  
• Endpoint inconsistencies  
• Statistical inconsistencies  
• Areas requiring additional information  

List issues clearly.

--------------------------------------------------

IMPORTANT RULES

• Do not fabricate data.
• Only use information contained in the abstract or clearly general medical knowledge.
• Use placeholders when information is missing.
• Maintain formal scientific writing style appropriate for peer-reviewed journals.

--------------------------------------------------

Abstract for analysis:

[PASTE ABSTRACT HERE]
