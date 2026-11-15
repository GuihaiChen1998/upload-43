# Issue #1 figure drafts

Based on manuscript and experimental records at `9c276cff67cdc7fbd2e363899268c74ece53b4ff`. The PDFs contain vector text and marks. The SVGs can be edited. To reproduce both formats, run `python render_issue1.py` with Matplotlib installed. `worked_examples.json` gives the source revision, row IDs and unrounded scores. Numbers printed on the RM64 bars are rounded to two decimals.

## Motivation figure — final rendering brief

Draw a 3.50 × 2.24 inch white-background IEEE single-column diagram with flat vector marks. Ask “Which records did the model use?” above a left-to-right Query → four numbered records → “LLM API · text only” → Answer pipeline. Below, put two sibling panels. Use blue for “Saying,” one self-report call and the example “I used [2].” Use orange for “Doing,” three illustrative leave-one-out queries that cross out one original record each, with filled and hollow dots distinguishing changed and unchanged answers. Cost labels are “V1 · 1 call” and “LOO M+1 · RM@k ≤k+1 calls.” Put two compact callouts below: “Redundancy” for an exact copy that remains when one record is deleted, and “Answer variation” for a changed string after deleting a distractor. No access to logits, hidden states or other internals is depicted. The crossed cards refer to the original context positions for illustration.

Suggested caption: Text-only access gives two ways to probe provenance. A self-report asks the model for source IDs. An intervention queries edited contexts and compares their answers to a full-context reference. Costs include that reference; repeated masks can reduce the number of distinct RM queries.

## Worked examples — final rendering brief

Draw a 7.15 × 2.78 inch IEEE double-column figure with three aligned panels. Show the task, reference answer, selected records in original 1-based numbering, and V1, P1, LOI and RM64 for each selected record. Use shared signed score geometry with a zero line. Lengths use the exact values in `worked_examples.json`; zeros are dots and negative values extend left. Place printed values at the right. Use fixed method labels and colors. Stars mark the annotated support set, including the K3 copy.

- (a) HotpotQA K3, Gemini Flash-Lite, `5ab7867c5542992aa3b8c822::K3::C`. Show sources [3], [7], [8]. [3] and [7] have identical text. P1's score is zero at all eleven positions.
- (b) Symmetric FEVER test, Claude Haiku, `symfever_242640000002`. Quote the **synthetic** evidence for source [7] and show the pacemaking-cell distractor [6]. The reference is `no`; deleting either displayed source returned `unknown`. RM64 scores are 1.00 and −0.10. The example shows the observed responses to those edits.
- (c) Qasper test, Gemini Flash-Lite, `qasper_a28c73a6a8c46a43a1eec2b42b542dd7fde1e30e`. Show [7] on Gigaword and [6] on machine translation. Removing [6] yields `English Gigaword` instead of `English Gigaword corpus`.

Suggested caption: Three illustrative instances with selected records in their original numbering. Stars denote annotated support and include the K3 copy. In (b), the evidence text is a synthetic benchmark sentence and the labels refer to the supplied context. Bars show raw estimator scores on a shared signed scale.
