# Phase-2 pilot analysis

## Methods
| dataset | model | method | n | top1 | rec@g | random_top1 | all_zero | unique_max | reaches_tau | calls/inst | full_ctx_change |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | LOI | 12 | 0.758 | 0.499 | 0.200 | 0.250 | 0.583 | 0.750 | 7.833 | None |
| hotpotqa | claude-haiku-5-5 | MEXGEN_LOO | 12 | 0.800 | 0.631 | 0.200 | 0.250 | 0.417 | 0.750 | 0.000 | None |
| hotpotqa | claude-haiku-5-5 | P1 | 12 | 0.772 | 0.624 | 0.200 | 0.250 | 0.333 | 0.750 | 11.667 | 0.028 |
| hotpotqa | claude-haiku-5-5 | P1.r1 | 12 | 0.750 | 0.528 | 0.200 | 0.167 | 0.500 | 0.833 | 14.000 | None |
| hotpotqa | claude-haiku-5-5 | P2 | 12 | 0.906 | 0.679 | 0.200 | 0.083 | 0.667 | 0.917 | 33.000 | 0.056 |
| hotpotqa | claude-haiku-5-5 | P3 | 12 | 0.772 | 0.624 | 0.200 | 0.250 | 0.333 | 0.750 | 14.000 | 0.028 |
| hotpotqa | claude-haiku-5-5 | P4 | 12 | 0.906 | 0.679 | 0.200 | 0.083 | 0.667 | 0.917 | 33.000 | 0.056 |
| hotpotqa | claude-haiku-5-5 | P5 | 12 | 0.892 | 0.776 | 0.200 | 0.083 | 0.750 | 0.917 | 0.000 | 0.056 |
| hotpotqa | claude-haiku-5-5 | RM64 | 12 | 1.000 | 0.750 | 0.200 | 0.000 | 1.000 | 0.917 | 60.333 | None |
| hotpotqa | claude-haiku-5-5 | RM64:banzhaf_exact | 12 | 1.000 | 0.750 | 0.200 | 0.000 | 1.000 | 0.917 | 60.333 | None |
| hotpotqa | claude-haiku-5-5 | RM64:banzhaf_f1 | 12 | 1.000 | 0.750 | 0.200 | 0.000 | 1.000 | 1.000 | 60.333 | None |
| hotpotqa | claude-haiku-5-5 | RM64:linear_exact | 12 | 1.000 | 0.792 | 0.200 | 0.000 | 1.000 | 0.750 | 60.333 | None |
| hotpotqa | claude-haiku-5-5 | RM64:linear_f1 | 12 | 1.000 | 0.833 | 0.200 | 0.000 | 1.000 | 0.750 | 60.333 | None |
| hotpotqa | claude-haiku-5-5 | RM@16 | 12 | 0.833 | 0.625 | 0.200 | 0.000 | 1.000 | 0.917 | 17.000 | None |
| hotpotqa | claude-haiku-5-5 | RM@32 | 12 | 1.000 | 0.729 | 0.200 | 0.000 | 1.000 | 0.750 | 33.000 | None |
| hotpotqa | claude-haiku-5-5 | RM@8 | 12 | 0.667 | 0.438 | 0.200 | 0.000 | 0.833 | 1.000 | 9.000 | None |
| hotpotqa | claude-haiku-5-5 | V1 | 12 | 0.972 | 0.935 | 0.200 | 0.000 | 0.083 | 1.000 | 0.833 | None |
| hotpotqa | claude-haiku-5-5 | V1.r1 | 12 | 0.933 | 0.896 | 0.200 | 0.083 | 0.083 | 0.917 | 1.000 | None |
| hotpotqa | claude-haiku-5-5 | V2 | 12 | 1.000 | 0.963 | 0.200 | 0.000 | 0.083 | 1.000 | 5.000 | None |
| hotpotqa | claude-haiku-5-5 | V3 | 12 | 0.733 | 0.733 | 0.200 | 0.333 | 0.000 | 0.667 | 1.000 | None |
| hotpotqa | claude-haiku-5-5 | V4 | 12 | 1.000 | 0.963 | 0.200 | 0.000 | 0.083 | 1.000 | 4.167 | None |
| hotpotqa | claude-haiku-5-5 | V5 | 12 | 1.000 | 0.963 | 0.200 | 0.000 | 0.083 | 1.000 | 0.000 | None |
| hotpotqa | claude-haiku-5-5 | V6 | 12 | 0.972 | 0.972 | 0.200 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| hotpotqa | claude-haiku-5-5 | V7 | 12 | 0.972 | 0.972 | 0.200 | 0.000 | 0.083 | 1.000 | 5.000 | None |
| hotpotqa | gemini-2.5-flash-lite | LOI | 12 | 0.753 | 0.568 | 0.200 | 0.083 | 0.417 | 0.917 | 9.417 | None |
| hotpotqa | gemini-2.5-flash-lite | MEXGEN_LOO | 12 | 0.744 | 0.501 | 0.200 | 0.250 | 0.583 | 0.750 | 0.000 | None |
| hotpotqa | gemini-2.5-flash-lite | P1 | 12 | 0.680 | 0.457 | 0.200 | 0.250 | 0.500 | 0.750 | 10.417 | 0.167 |
| hotpotqa | gemini-2.5-flash-lite | P1.r1 | 12 | 0.629 | 0.444 | 0.200 | 0.250 | 0.417 | 0.750 | 14.000 | None |
| hotpotqa | gemini-2.5-flash-lite | P2 | 12 | 0.678 | 0.451 | 0.200 | 0.250 | 0.500 | 0.750 | 33.000 | 0.194 |
| hotpotqa | gemini-2.5-flash-lite | P3 | 12 | 0.680 | 0.457 | 0.200 | 0.250 | 0.500 | 0.750 | 14.000 | 0.167 |
| hotpotqa | gemini-2.5-flash-lite | P4 | 12 | 0.678 | 0.451 | 0.200 | 0.250 | 0.500 | 0.750 | 33.000 | 0.194 |
| hotpotqa | gemini-2.5-flash-lite | P5 | 12 | 0.738 | 0.464 | 0.200 | 0.250 | 0.583 | 0.750 | 0.000 | 0.194 |
| hotpotqa | gemini-2.5-flash-lite | RM64 | 12 | 0.850 | 0.642 | 0.200 | 0.083 | 0.917 | 0.667 | 61.250 | None |
| hotpotqa | gemini-2.5-flash-lite | RM64:banzhaf_exact | 12 | 0.850 | 0.642 | 0.200 | 0.083 | 0.917 | 0.667 | 61.250 | None |
| hotpotqa | gemini-2.5-flash-lite | RM64:banzhaf_f1 | 12 | 0.917 | 0.667 | 0.200 | 0.000 | 1.000 | 0.750 | 61.250 | None |
| hotpotqa | gemini-2.5-flash-lite | RM64:linear_exact | 12 | 0.933 | 0.683 | 0.200 | 0.083 | 0.917 | 0.667 | 61.250 | None |
| hotpotqa | gemini-2.5-flash-lite | RM64:linear_f1 | 12 | 1.000 | 0.750 | 0.200 | 0.000 | 1.000 | 0.750 | 61.250 | None |
| hotpotqa | gemini-2.5-flash-lite | RM@16 | 12 | 0.725 | 0.558 | 0.200 | 0.083 | 0.833 | 0.833 | 17.000 | None |
| hotpotqa | gemini-2.5-flash-lite | RM@32 | 12 | 0.933 | 0.517 | 0.200 | 0.083 | 0.917 | 0.583 | 33.000 | None |
| hotpotqa | gemini-2.5-flash-lite | RM@8 | 12 | 0.683 | 0.558 | 0.200 | 0.083 | 0.750 | 0.750 | 9.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V1 | 12 | 0.931 | 0.819 | 0.200 | 0.000 | 0.250 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V1.r1 | 12 | 0.972 | 0.824 | 0.200 | 0.000 | 0.333 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V2 | 12 | 0.972 | 0.819 | 0.200 | 0.000 | 0.333 | 1.000 | 5.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V3 | 12 | 0.931 | 0.819 | 0.200 | 0.000 | 0.250 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V4 | 12 | 0.906 | 0.790 | 0.200 | 0.083 | 0.250 | 0.917 | 5.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V5 | 12 | 0.906 | 0.790 | 0.200 | 0.083 | 0.250 | 0.917 | 0.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V6 | 12 | 0.972 | 0.861 | 0.200 | 0.000 | 0.250 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V7 | 12 | 0.972 | 0.894 | 0.200 | 0.000 | 0.333 | 1.000 | 5.000 | None |
| hotpotqa | gemini-2.5-flash | LOI | 6 | 0.750 | 0.602 | 0.200 | 0.000 | 0.333 | 1.000 | 9.000 | None |
| hotpotqa | gemini-2.5-flash | MEXGEN_LOO | 6 | 0.600 | 0.378 | 0.200 | 0.500 | 0.500 | 0.500 | 0.000 | None |
| hotpotqa | gemini-2.5-flash | P1 | 6 | 0.600 | 0.378 | 0.200 | 0.500 | 0.500 | 0.500 | 13.000 | 0.000 |
| hotpotqa | gemini-2.5-flash | P1.r1 | 6 | 0.467 | 0.319 | 0.200 | 0.667 | 0.333 | 0.333 | 14.000 | None |
| hotpotqa | gemini-2.5-flash | P2 | 6 | 0.600 | 0.378 | 0.200 | 0.500 | 0.500 | 0.500 | 33.000 | 0.000 |
| hotpotqa | gemini-2.5-flash | P3 | 6 | 0.600 | 0.378 | 0.200 | 0.500 | 0.500 | 0.500 | 14.000 | 0.000 |
| hotpotqa | gemini-2.5-flash | P4 | 6 | 0.600 | 0.378 | 0.200 | 0.500 | 0.500 | 0.500 | 29.500 | 0.000 |
| hotpotqa | gemini-2.5-flash | P5 | 6 | 0.600 | 0.378 | 0.200 | 0.500 | 0.500 | 0.500 | 0.000 | 0.000 |
| hotpotqa | gemini-2.5-flash | RM64 | 6 | 0.500 | 0.583 | 0.200 | 0.000 | 1.000 | 0.500 | 62.167 | None |
| hotpotqa | gemini-2.5-flash | RM64:banzhaf_exact | 6 | 0.500 | 0.583 | 0.200 | 0.000 | 1.000 | 0.500 | 62.167 | None |
| hotpotqa | gemini-2.5-flash | RM64:banzhaf_f1 | 6 | 0.667 | 0.583 | 0.200 | 0.000 | 1.000 | 0.500 | 62.167 | None |
| hotpotqa | gemini-2.5-flash | RM64:linear_exact | 6 | 0.500 | 0.583 | 0.200 | 0.000 | 1.000 | 0.500 | 62.167 | None |
| hotpotqa | gemini-2.5-flash | RM64:linear_f1 | 6 | 0.667 | 0.583 | 0.200 | 0.000 | 1.000 | 0.333 | 62.167 | None |
| hotpotqa | gemini-2.5-flash | RM@16 | 6 | 0.833 | 0.583 | 0.200 | 0.000 | 1.000 | 1.000 | 17.000 | None |
| hotpotqa | gemini-2.5-flash | RM@32 | 6 | 0.667 | 0.542 | 0.200 | 0.000 | 1.000 | 0.833 | 33.000 | None |
| hotpotqa | gemini-2.5-flash | RM@8 | 6 | 0.667 | 0.521 | 0.200 | 0.000 | 1.000 | 0.833 | 9.000 | None |
| hotpotqa | gemini-2.5-flash | V1 | 6 | 0.778 | 0.778 | 0.200 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash | V1.r1 | 6 | 0.778 | 0.778 | 0.200 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash | V2 | 6 | 0.778 | 0.778 | 0.200 | 0.000 | 0.333 | 1.000 | 5.000 | None |
| hotpotqa | gemini-2.5-flash | V3 | 6 | 0.778 | 0.778 | 0.200 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash | V4 | 6 | 0.778 | 0.778 | 0.200 | 0.000 | 0.333 | 1.000 | 5.000 | None |
| hotpotqa | gemini-2.5-flash | V5 | 6 | 0.778 | 0.778 | 0.200 | 0.000 | 0.333 | 1.000 | 0.000 | None |
| hotpotqa | gemini-2.5-flash | V6 | 6 | 0.806 | 0.657 | 0.200 | 0.000 | 0.333 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash | V7 | 6 | 0.806 | 0.806 | 0.200 | 0.000 | 0.333 | 1.000 | 5.000 | None |
| hotpotqa | gpt-6-luna | LOI | 12 | 0.732 | 0.510 | 0.200 | 0.083 | 0.500 | 0.917 | 9.500 | None |
| hotpotqa | gpt-6-luna | MEXGEN_LOO | 12 | 0.742 | 0.450 | 0.200 | 0.167 | 0.750 | 0.750 | 0.000 | None |
| hotpotqa | gpt-6-luna | P1 | 12 | 0.686 | 0.436 | 0.200 | 0.167 | 0.667 | 0.833 | 14.000 | 0.028 |
| hotpotqa | gpt-6-luna | P1.r1 | 12 | 0.654 | 0.432 | 0.200 | 0.250 | 0.500 | 0.750 | 14.000 | None |
| hotpotqa | gpt-6-luna | P2 | 12 | 0.867 | 0.510 | 0.200 | 0.167 | 0.833 | 0.833 | 33.000 | 0.056 |
| hotpotqa | gpt-6-luna | P3 | 12 | 0.686 | 0.436 | 0.200 | 0.167 | 0.667 | 0.833 | 14.000 | 0.028 |
| hotpotqa | gpt-6-luna | P4 | 12 | 0.867 | 0.510 | 0.200 | 0.167 | 0.833 | 0.833 | 33.000 | 0.056 |
| hotpotqa | gpt-6-luna | P5 | 12 | 0.933 | 0.535 | 0.200 | 0.083 | 0.917 | 0.833 | 0.000 | 0.056 |
| hotpotqa | gpt-6-luna | RM64 | 12 | 1.000 | 0.625 | 0.200 | 0.000 | 1.000 | 0.917 | 62.000 | None |
| hotpotqa | gpt-6-luna | RM64:banzhaf_exact | 12 | 1.000 | 0.625 | 0.200 | 0.000 | 1.000 | 0.917 | 62.000 | None |
| hotpotqa | gpt-6-luna | RM64:banzhaf_f1 | 12 | 1.000 | 0.667 | 0.200 | 0.000 | 1.000 | 0.917 | 62.000 | None |
| hotpotqa | gpt-6-luna | RM64:linear_exact | 12 | 1.000 | 0.583 | 0.200 | 0.000 | 1.000 | 0.917 | 62.000 | None |
| hotpotqa | gpt-6-luna | RM64:linear_f1 | 12 | 1.000 | 0.667 | 0.200 | 0.000 | 1.000 | 0.750 | 62.000 | None |
| hotpotqa | gpt-6-luna | RM@16 | 12 | 1.000 | 0.667 | 0.200 | 0.000 | 1.000 | 0.917 | 17.000 | None |
| hotpotqa | gpt-6-luna | RM@32 | 12 | 1.000 | 0.604 | 0.200 | 0.000 | 1.000 | 0.917 | 33.000 | None |
| hotpotqa | gpt-6-luna | RM@8 | 12 | 0.892 | 0.600 | 0.200 | 0.083 | 0.833 | 0.917 | 9.000 | None |
| hotpotqa | gpt-6-luna | V1 | 12 | 0.972 | 0.935 | 0.200 | 0.000 | 0.083 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6-luna | V1.r1 | 12 | 0.972 | 0.861 | 0.200 | 0.000 | 0.250 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6-luna | V2 | 12 | 1.000 | 0.963 | 0.200 | 0.000 | 0.250 | 1.000 | 4.583 | None |
| hotpotqa | gpt-6-luna | V3 | 12 | 0.972 | 0.935 | 0.200 | 0.000 | 0.083 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6-luna | V4 | 12 | 1.000 | 0.963 | 0.200 | 0.000 | 0.250 | 1.000 | 5.000 | None |
| hotpotqa | gpt-6-luna | V5 | 12 | 1.000 | 0.963 | 0.200 | 0.000 | 0.250 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6-luna | V6 | 12 | 0.972 | 0.898 | 0.200 | 0.000 | 0.167 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6-luna | V7 | 12 | 1.000 | 1.000 | 0.200 | 0.000 | 0.333 | 1.000 | 5.000 | None |
| hotpotqa | gpt-6.1-terra | LOI | 6 | 0.833 | 0.537 | 0.200 | 0.000 | 0.667 | 1.000 | 9.333 | None |
| hotpotqa | gpt-6.1-terra | MEXGEN_LOO | 6 | 1.000 | 0.556 | 0.200 | 0.000 | 1.000 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6.1-terra | P1 | 6 | 1.000 | 0.556 | 0.200 | 0.000 | 1.000 | 1.000 | 13.000 | 0.000 |
| hotpotqa | gpt-6.1-terra | P1.r1 | 6 | 0.733 | 0.437 | 0.200 | 0.333 | 0.667 | 0.667 | 14.000 | None |
| hotpotqa | gpt-6.1-terra | P2 | 6 | 1.000 | 0.556 | 0.200 | 0.000 | 1.000 | 0.833 | 33.000 | 0.000 |
| hotpotqa | gpt-6.1-terra | P3 | 6 | 1.000 | 0.556 | 0.200 | 0.000 | 1.000 | 1.000 | 14.000 | 0.000 |
| hotpotqa | gpt-6.1-terra | P4 | 6 | 1.000 | 0.556 | 0.200 | 0.000 | 1.000 | 0.833 | 33.000 | 0.000 |
| hotpotqa | gpt-6.1-terra | P5 | 6 | 1.000 | 0.704 | 0.200 | 0.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| hotpotqa | gpt-6.1-terra | RM64 | 6 | 1.000 | 0.542 | 0.200 | 0.000 | 1.000 | 1.000 | 61.667 | None |
| hotpotqa | gpt-6.1-terra | RM64:banzhaf_exact | 6 | 1.000 | 0.542 | 0.200 | 0.000 | 1.000 | 1.000 | 61.667 | None |
| hotpotqa | gpt-6.1-terra | RM64:banzhaf_f1 | 6 | 1.000 | 0.542 | 0.200 | 0.000 | 1.000 | 1.000 | 61.667 | None |
| hotpotqa | gpt-6.1-terra | RM64:linear_exact | 6 | 1.000 | 0.667 | 0.200 | 0.000 | 1.000 | 1.000 | 61.667 | None |
| hotpotqa | gpt-6.1-terra | RM64:linear_f1 | 6 | 1.000 | 0.667 | 0.200 | 0.000 | 1.000 | 1.000 | 61.667 | None |
| hotpotqa | gpt-6.1-terra | RM@16 | 6 | 1.000 | 0.583 | 0.200 | 0.000 | 1.000 | 1.000 | 17.000 | None |
| hotpotqa | gpt-6.1-terra | RM@32 | 6 | 1.000 | 0.667 | 0.200 | 0.000 | 1.000 | 1.000 | 33.000 | None |
| hotpotqa | gpt-6.1-terra | RM@8 | 6 | 0.783 | 0.533 | 0.200 | 0.167 | 0.667 | 0.833 | 9.000 | None |
| hotpotqa | gpt-6.1-terra | V1 | 6 | 1.000 | 0.926 | 0.200 | 0.000 | 0.167 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6.1-terra | V1.r1 | 6 | 1.000 | 0.926 | 0.200 | 0.000 | 0.167 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6.1-terra | V2 | 6 | 1.000 | 0.926 | 0.200 | 0.000 | 0.167 | 1.000 | 4.333 | None |
| hotpotqa | gpt-6.1-terra | V3 | 6 | 1.000 | 0.926 | 0.200 | 0.000 | 0.167 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6.1-terra | V4 | 6 | 1.000 | 0.926 | 0.200 | 0.000 | 0.167 | 1.000 | 5.000 | None |
| hotpotqa | gpt-6.1-terra | V5 | 6 | 1.000 | 0.926 | 0.200 | 0.000 | 0.167 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6.1-terra | V6 | 6 | 1.000 | 1.000 | 0.200 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6.1-terra | V7 | 6 | 1.000 | 1.000 | 0.200 | 0.000 | 0.167 | 1.000 | 5.000 | None |
| musique | claude-haiku-5-5 | LOI | 12 | 0.367 | 0.228 | 0.150 | 0.750 | 0.250 | 0.250 | 20.000 | None |
| musique | claude-haiku-5-5 | MEXGEN_LOO | 12 | 0.778 | 0.644 | 0.150 | 0.000 | 0.083 | 0.917 | 0.000 | None |
| musique | claude-haiku-5-5 | P1 | 12 | 0.724 | 0.586 | 0.150 | 0.000 | 0.083 | 1.000 | 23.833 | 0.111 |
| musique | claude-haiku-5-5 | P1.r1 | 12 | 0.694 | 0.447 | 0.150 | 0.000 | 0.333 | 1.000 | 24.000 | None |
| musique | claude-haiku-5-5 | P2 | 12 | 0.903 | 0.710 | 0.150 | 0.000 | 0.417 | 1.000 | 63.000 | 0.056 |
| musique | claude-haiku-5-5 | P3 | 12 | 0.724 | 0.586 | 0.150 | 0.000 | 0.083 | 1.000 | 24.000 | 0.111 |
| musique | claude-haiku-5-5 | P4 | 12 | 0.903 | 0.710 | 0.150 | 0.000 | 0.417 | 1.000 | 63.000 | 0.056 |
| musique | claude-haiku-5-5 | P5 | 12 | 0.903 | 0.699 | 0.150 | 0.000 | 0.583 | 1.000 | 0.000 | 0.056 |
| musique | claude-haiku-5-5 | RM64 | 12 | 1.000 | 0.708 | 0.150 | 0.000 | 0.917 | 0.500 | 64.000 | None |
| musique | claude-haiku-5-5 | RM64:banzhaf_exact | 12 | 1.000 | 0.708 | 0.150 | 0.000 | 0.917 | 0.500 | 64.000 | None |
| musique | claude-haiku-5-5 | RM64:banzhaf_f1 | 12 | 1.000 | 0.667 | 0.150 | 0.000 | 0.917 | 0.500 | 64.000 | None |
| musique | claude-haiku-5-5 | RM64:linear_exact | 12 | 1.000 | 0.729 | 0.150 | 0.000 | 1.000 | 0.083 | 64.000 | None |
| musique | claude-haiku-5-5 | RM64:linear_f1 | 12 | 1.000 | 0.757 | 0.150 | 0.000 | 1.000 | 0.167 | 64.000 | None |
| musique | claude-haiku-5-5 | RM@16 | 12 | 0.628 | 0.419 | 0.150 | 0.083 | 0.667 | 0.667 | 17.000 | None |
| musique | claude-haiku-5-5 | RM@32 | 12 | 1.000 | 0.677 | 0.150 | 0.000 | 1.000 | 0.500 | 33.000 | None |
| musique | claude-haiku-5-5 | RM@8 | 12 | 0.272 | 0.300 | 0.150 | 0.333 | 0.333 | 0.667 | 9.000 | None |
| musique | claude-haiku-5-5 | V1 | 12 | 0.958 | 0.830 | 0.150 | 0.000 | 0.167 | 1.000 | 1.000 | None |
| musique | claude-haiku-5-5 | V1.r1 | 12 | 0.979 | 0.894 | 0.150 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| musique | claude-haiku-5-5 | V2 | 12 | 1.000 | 0.915 | 0.150 | 0.000 | 0.167 | 1.000 | 4.667 | None |
| musique | claude-haiku-5-5 | V3 | 12 | 0.625 | 0.605 | 0.150 | 0.417 | 0.000 | 0.583 | 1.000 | None |
| musique | claude-haiku-5-5 | V4 | 12 | 1.000 | 0.891 | 0.150 | 0.000 | 0.083 | 1.000 | 5.000 | None |
| musique | claude-haiku-5-5 | V5 | 12 | 1.000 | 0.891 | 0.150 | 0.000 | 0.083 | 1.000 | 0.000 | None |
| musique | claude-haiku-5-5 | V6 | 12 | 0.931 | 0.801 | 0.150 | 0.000 | 0.167 | 1.000 | 1.000 | None |
| musique | claude-haiku-5-5 | V7 | 12 | 1.000 | 0.940 | 0.150 | 0.000 | 0.167 | 1.000 | 5.000 | None |
| musique | gemini-2.5-flash-lite | LOI | 12 | 1.000 | 0.433 | 0.150 | 0.000 | 1.000 | 1.000 | 20.000 | None |
| musique | gemini-2.5-flash-lite | MEXGEN_LOO | 12 | 0.787 | 0.415 | 0.150 | 0.000 | 0.750 | 0.917 | 0.000 | None |
| musique | gemini-2.5-flash-lite | P1 | 12 | 0.731 | 0.404 | 0.150 | 0.000 | 0.667 | 1.000 | 23.000 | 0.083 |
| musique | gemini-2.5-flash-lite | P1.r1 | 12 | 0.605 | 0.376 | 0.150 | 0.167 | 0.417 | 0.833 | 24.000 | None |
| musique | gemini-2.5-flash-lite | P2 | 12 | 0.789 | 0.439 | 0.150 | 0.000 | 0.583 | 0.917 | 63.000 | 0.056 |
| musique | gemini-2.5-flash-lite | P3 | 12 | 0.731 | 0.404 | 0.150 | 0.000 | 0.667 | 1.000 | 24.000 | 0.083 |
| musique | gemini-2.5-flash-lite | P4 | 12 | 0.789 | 0.439 | 0.150 | 0.000 | 0.583 | 0.917 | 63.000 | 0.056 |
| musique | gemini-2.5-flash-lite | P5 | 12 | 0.917 | 0.564 | 0.150 | 0.000 | 0.833 | 1.000 | 0.000 | 0.056 |
| musique | gemini-2.5-flash-lite | RM64 | 12 | 1.000 | 0.583 | 0.150 | 0.000 | 1.000 | 1.000 | 64.000 | None |
| musique | gemini-2.5-flash-lite | RM64:banzhaf_exact | 12 | 1.000 | 0.583 | 0.150 | 0.000 | 1.000 | 1.000 | 64.000 | None |
| musique | gemini-2.5-flash-lite | RM64:banzhaf_f1 | 12 | 1.000 | 0.611 | 0.150 | 0.000 | 1.000 | 0.833 | 64.000 | None |
| musique | gemini-2.5-flash-lite | RM64:linear_exact | 12 | 1.000 | 0.611 | 0.150 | 0.000 | 1.000 | 0.833 | 64.000 | None |
| musique | gemini-2.5-flash-lite | RM64:linear_f1 | 12 | 1.000 | 0.611 | 0.150 | 0.000 | 1.000 | 0.667 | 64.000 | None |
| musique | gemini-2.5-flash-lite | RM@16 | 12 | 0.833 | 0.543 | 0.150 | 0.000 | 0.917 | 0.917 | 17.000 | None |
| musique | gemini-2.5-flash-lite | RM@32 | 12 | 1.000 | 0.545 | 0.150 | 0.000 | 0.917 | 0.917 | 33.000 | None |
| musique | gemini-2.5-flash-lite | RM@8 | 12 | 0.679 | 0.304 | 0.150 | 0.083 | 0.750 | 0.917 | 9.000 | None |
| musique | gemini-2.5-flash-lite | V1 | 12 | 1.000 | 0.810 | 0.150 | 0.000 | 0.167 | 1.000 | 1.000 | None |
| musique | gemini-2.5-flash-lite | V1.r1 | 12 | 1.000 | 0.810 | 0.150 | 0.000 | 0.167 | 1.000 | 1.000 | None |
| musique | gemini-2.5-flash-lite | V2 | 12 | 1.000 | 0.835 | 0.150 | 0.000 | 0.167 | 1.000 | 5.000 | None |
| musique | gemini-2.5-flash-lite | V3 | 12 | 0.792 | 0.647 | 0.150 | 0.250 | 0.167 | 0.750 | 1.000 | None |
| musique | gemini-2.5-flash-lite | V4 | 12 | 0.858 | 0.693 | 0.150 | 0.167 | 0.167 | 0.833 | 5.000 | None |
| musique | gemini-2.5-flash-lite | V5 | 12 | 0.858 | 0.693 | 0.150 | 0.167 | 0.167 | 0.833 | 0.000 | None |
| musique | gemini-2.5-flash-lite | V6 | 12 | 0.958 | 0.847 | 0.150 | 0.000 | 0.083 | 1.000 | 1.000 | None |
| musique | gemini-2.5-flash-lite | V7 | 12 | 0.958 | 0.870 | 0.150 | 0.000 | 0.167 | 1.000 | 4.667 | None |
| musique | gemini-2.5-flash | LOI | 6 | 0.850 | 0.362 | 0.150 | 0.167 | 0.833 | 0.833 | 20.000 | None |
| musique | gemini-2.5-flash | MEXGEN_LOO | 6 | 1.000 | 0.433 | 0.150 | 0.000 | 1.000 | 1.000 | 0.000 | None |
| musique | gemini-2.5-flash | P1 | 6 | 1.000 | 0.433 | 0.150 | 0.000 | 1.000 | 1.000 | 23.000 | 0.000 |
| musique | gemini-2.5-flash | P1.r1 | 6 | 0.867 | 0.405 | 0.150 | 0.167 | 0.833 | 0.833 | 24.000 | None |
| musique | gemini-2.5-flash | P2 | 6 | 0.867 | 0.405 | 0.150 | 0.167 | 0.833 | 0.833 | 51.667 | 0.000 |
| musique | gemini-2.5-flash | P3 | 6 | 1.000 | 0.433 | 0.150 | 0.000 | 1.000 | 1.000 | 24.000 | 0.000 |
| musique | gemini-2.5-flash | P4 | 6 | 0.867 | 0.405 | 0.150 | 0.167 | 0.833 | 0.833 | 63.000 | 0.000 |
| musique | gemini-2.5-flash | P5 | 6 | 0.867 | 0.537 | 0.150 | 0.167 | 0.833 | 0.833 | 0.000 | 0.000 |
| musique | gemini-2.5-flash | RM64 | 6 | 1.000 | 0.458 | 0.150 | 0.000 | 1.000 | 1.000 | 64.000 | None |
| musique | gemini-2.5-flash | RM64:banzhaf_exact | 6 | 1.000 | 0.458 | 0.150 | 0.000 | 1.000 | 1.000 | 64.000 | None |
| musique | gemini-2.5-flash | RM64:banzhaf_f1 | 6 | 1.000 | 0.458 | 0.150 | 0.000 | 1.000 | 1.000 | 64.000 | None |
| musique | gemini-2.5-flash | RM64:linear_exact | 6 | 1.000 | 0.403 | 0.150 | 0.000 | 1.000 | 1.000 | 64.000 | None |
| musique | gemini-2.5-flash | RM64:linear_f1 | 6 | 1.000 | 0.403 | 0.150 | 0.000 | 1.000 | 1.000 | 64.000 | None |
| musique | gemini-2.5-flash | RM@16 | 6 | 1.000 | 0.403 | 0.150 | 0.000 | 1.000 | 1.000 | 17.000 | None |
| musique | gemini-2.5-flash | RM@32 | 6 | 1.000 | 0.417 | 0.150 | 0.000 | 1.000 | 1.000 | 33.000 | None |
| musique | gemini-2.5-flash | RM@8 | 6 | 1.000 | 0.361 | 0.150 | 0.000 | 1.000 | 1.000 | 9.000 | None |
| musique | gemini-2.5-flash | V1 | 6 | 0.958 | 0.780 | 0.150 | 0.000 | 0.333 | 1.000 | 1.000 | None |
| musique | gemini-2.5-flash | V1.r1 | 6 | 0.958 | 0.780 | 0.150 | 0.000 | 0.333 | 1.000 | 1.000 | None |
| musique | gemini-2.5-flash | V2 | 6 | 1.000 | 0.780 | 0.150 | 0.000 | 0.333 | 1.000 | 5.000 | None |
| musique | gemini-2.5-flash | V3 | 6 | 0.958 | 0.780 | 0.150 | 0.000 | 0.333 | 1.000 | 1.000 | None |
| musique | gemini-2.5-flash | V4 | 6 | 1.000 | 0.780 | 0.150 | 0.000 | 0.333 | 1.000 | 5.000 | None |
| musique | gemini-2.5-flash | V5 | 6 | 1.000 | 0.780 | 0.150 | 0.000 | 0.333 | 1.000 | 0.000 | None |
| musique | gemini-2.5-flash | V6 | 6 | 1.000 | 0.861 | 0.150 | 0.000 | 0.167 | 1.000 | 1.000 | None |
| musique | gemini-2.5-flash | V7 | 6 | 1.000 | 0.782 | 0.150 | 0.000 | 0.500 | 1.000 | 5.000 | None |
| musique | gpt-6-luna | LOI | 12 | 0.929 | 0.485 | 0.150 | 0.083 | 0.750 | 0.917 | 20.000 | None |
| musique | gpt-6-luna | MEXGEN_LOO | 12 | 0.808 | 0.391 | 0.150 | 0.167 | 0.750 | 0.750 | 0.000 | None |
| musique | gpt-6-luna | P1 | 12 | 0.671 | 0.345 | 0.150 | 0.167 | 0.583 | 0.833 | 24.000 | 0.083 |
| musique | gpt-6-luna | P1.r1 | 12 | 0.769 | 0.383 | 0.150 | 0.083 | 0.667 | 0.917 | 24.000 | None |
| musique | gpt-6-luna | P2 | 12 | 0.888 | 0.418 | 0.150 | 0.000 | 0.750 | 1.000 | 63.000 | 0.111 |
| musique | gpt-6-luna | P3 | 12 | 0.671 | 0.345 | 0.150 | 0.167 | 0.583 | 0.833 | 24.000 | 0.083 |
| musique | gpt-6-luna | P4 | 12 | 0.888 | 0.418 | 0.150 | 0.000 | 0.750 | 1.000 | 63.000 | 0.111 |
| musique | gpt-6-luna | P5 | 12 | 0.917 | 0.558 | 0.150 | 0.000 | 0.833 | 1.000 | 0.000 | 0.111 |
| musique | gpt-6-luna | RM64 | 12 | 0.929 | 0.478 | 0.150 | 0.083 | 0.917 | 0.833 | 64.000 | None |
| musique | gpt-6-luna | RM64:banzhaf_exact | 12 | 0.929 | 0.478 | 0.150 | 0.083 | 0.917 | 0.833 | 64.000 | None |
| musique | gpt-6-luna | RM64:banzhaf_f1 | 12 | 1.000 | 0.535 | 0.150 | 0.000 | 1.000 | 0.833 | 64.000 | None |
| musique | gpt-6-luna | RM64:linear_exact | 12 | 0.929 | 0.471 | 0.150 | 0.083 | 0.917 | 0.833 | 64.000 | None |
| musique | gpt-6-luna | RM64:linear_f1 | 12 | 1.000 | 0.528 | 0.150 | 0.000 | 1.000 | 0.833 | 64.000 | None |
| musique | gpt-6-luna | RM@16 | 12 | 0.929 | 0.360 | 0.150 | 0.083 | 0.917 | 0.917 | 17.000 | None |
| musique | gpt-6-luna | RM@32 | 12 | 0.929 | 0.443 | 0.150 | 0.083 | 0.917 | 0.833 | 33.000 | None |
| musique | gpt-6-luna | RM@8 | 12 | 0.608 | 0.296 | 0.150 | 0.167 | 0.583 | 0.833 | 9.000 | None |
| musique | gpt-6-luna | V1 | 12 | 0.972 | 0.907 | 0.150 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| musique | gpt-6-luna | V1.r1 | 12 | 0.944 | 0.887 | 0.150 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| musique | gpt-6-luna | V2 | 12 | 0.917 | 0.926 | 0.150 | 0.000 | 0.167 | 1.000 | 4.500 | None |
| musique | gpt-6-luna | V3 | 12 | 0.972 | 0.907 | 0.150 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| musique | gpt-6-luna | V4 | 12 | 0.917 | 0.926 | 0.150 | 0.000 | 0.167 | 1.000 | 5.000 | None |
| musique | gpt-6-luna | V5 | 12 | 0.917 | 0.926 | 0.150 | 0.000 | 0.167 | 1.000 | 0.000 | None |
| musique | gpt-6-luna | V6 | 12 | 0.972 | 0.889 | 0.150 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| musique | gpt-6-luna | V7 | 12 | 0.972 | 0.926 | 0.150 | 0.000 | 0.000 | 1.000 | 5.000 | None |
| musique | gpt-6.1-terra | LOI | 6 | 0.700 | 0.392 | 0.150 | 0.167 | 0.667 | 0.833 | 20.000 | None |
| musique | gpt-6.1-terra | MEXGEN_LOO | 6 | 0.672 | 0.389 | 0.150 | 0.167 | 0.500 | 0.833 | 0.000 | None |
| musique | gpt-6.1-terra | P1 | 6 | 0.522 | 0.322 | 0.150 | 0.167 | 0.333 | 0.833 | 23.000 | 0.111 |
| musique | gpt-6.1-terra | P1.r1 | 6 | 0.511 | 0.332 | 0.150 | 0.167 | 0.333 | 0.833 | 24.000 | None |
| musique | gpt-6.1-terra | P2 | 6 | 0.774 | 0.351 | 0.150 | 0.000 | 0.667 | 1.000 | 63.000 | 0.333 |
| musique | gpt-6.1-terra | P3 | 6 | 0.522 | 0.322 | 0.150 | 0.167 | 0.333 | 0.833 | 24.000 | 0.111 |
| musique | gpt-6.1-terra | P4 | 6 | 0.774 | 0.351 | 0.150 | 0.000 | 0.667 | 1.000 | 63.000 | 0.333 |
| musique | gpt-6.1-terra | P5 | 6 | 0.690 | 0.425 | 0.150 | 0.000 | 0.833 | 1.000 | 0.000 | 0.333 |
| musique | gpt-6.1-terra | RM64 | 6 | 1.000 | 0.403 | 0.150 | 0.000 | 1.000 | 0.500 | 64.000 | None |
| musique | gpt-6.1-terra | RM64:banzhaf_exact | 6 | 1.000 | 0.403 | 0.150 | 0.000 | 1.000 | 0.500 | 64.000 | None |
| musique | gpt-6.1-terra | RM64:banzhaf_f1 | 6 | 1.000 | 0.403 | 0.150 | 0.000 | 1.000 | 0.500 | 64.000 | None |
| musique | gpt-6.1-terra | RM64:linear_exact | 6 | 0.833 | 0.403 | 0.150 | 0.000 | 1.000 | 0.500 | 64.000 | None |
| musique | gpt-6.1-terra | RM64:linear_f1 | 6 | 1.000 | 0.403 | 0.150 | 0.000 | 1.000 | 0.500 | 64.000 | None |
| musique | gpt-6.1-terra | RM@16 | 6 | 0.917 | 0.458 | 0.150 | 0.000 | 0.833 | 0.833 | 17.000 | None |
| musique | gpt-6.1-terra | RM@32 | 6 | 0.667 | 0.361 | 0.150 | 0.000 | 1.000 | 0.500 | 33.000 | None |
| musique | gpt-6.1-terra | RM@8 | 6 | 0.722 | 0.403 | 0.150 | 0.000 | 0.833 | 1.000 | 9.000 | None |
| musique | gpt-6.1-terra | V1 | 6 | 1.000 | 0.887 | 0.150 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| musique | gpt-6.1-terra | V1.r1 | 6 | 1.000 | 0.961 | 0.150 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| musique | gpt-6.1-terra | V2 | 6 | 1.000 | 0.961 | 0.150 | 0.000 | 0.000 | 1.000 | 4.167 | None |
| musique | gpt-6.1-terra | V3 | 6 | 0.575 | 0.536 | 0.150 | 0.500 | 0.000 | 0.500 | 1.000 | None |
| musique | gpt-6.1-terra | V4 | 6 | 1.000 | 0.961 | 0.150 | 0.000 | 0.000 | 1.000 | 5.000 | None |
| musique | gpt-6.1-terra | V5 | 6 | 1.000 | 0.961 | 0.150 | 0.000 | 0.000 | 1.000 | 0.000 | None |
| musique | gpt-6.1-terra | V6 | 6 | 1.000 | 0.887 | 0.150 | 0.000 | 0.000 | 1.000 | 1.000 | None |
| musique | gpt-6.1-terra | V7 | 6 | 1.000 | 0.922 | 0.150 | 0.000 | 0.000 | 1.000 | 5.000 | None |

## Stability (repeat 1 vs 0)
| dataset | model | method | n | identical_phi | per_source_agree | n_same_a0 | per_source_agree_same_a0 | top_group_jaccard | spearman_tie_preserving | n_rho_defined |
|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | V1 | 12 | 0.917 | 0.975 | 0 | nan | 0.942 | 1.000 | 11 |
| hotpotqa | claude-haiku-5-5 | P1 | 12 | 0.500 | 0.867 | 11 | 0.927 | 0.603 | 0.858 | 7 |
| hotpotqa | gemini-2.5-flash-lite | V1 | 12 | 0.917 | 0.992 | 0 | nan | 0.958 | 0.972 | 12 |
| hotpotqa | gemini-2.5-flash-lite | P1 | 12 | 0.750 | 0.967 | 11 | 0.973 | 0.929 | 0.910 | 8 |
| hotpotqa | gemini-2.5-flash | V1 | 6 | 1.000 | 1.000 | 0 | nan | 1.000 | 1.000 | 6 |
| hotpotqa | gemini-2.5-flash | P1 | 6 | 0.833 | 0.983 | 6 | 0.983 | 0.850 | 1.000 | 2 |
| hotpotqa | gpt-6-luna | V1 | 12 | 0.833 | 0.983 | 0 | nan | 0.917 | 0.944 | 12 |
| hotpotqa | gpt-6-luna | P1 | 12 | 0.583 | 0.925 | 12 | 0.925 | 0.703 | 0.719 | 9 |
| hotpotqa | gpt-6.1-terra | V1 | 6 | 0.667 | 0.967 | 0 | nan | 0.833 | 0.889 | 6 |
| hotpotqa | gpt-6.1-terra | P1 | 6 | 0.667 | 0.967 | 5 | 0.960 | 0.700 | 1.000 | 4 |
| musique | claude-haiku-5-5 | V1 | 12 | 0.583 | 0.971 | 0 | nan | 0.819 | 0.882 | 12 |
| musique | claude-haiku-5-5 | P1 | 12 | 0.167 | 0.854 | 11 | 0.882 | 0.449 | 0.483 | 12 |
| musique | gemini-2.5-flash-lite | V1 | 12 | 1.000 | 1.000 | 0 | nan | 1.000 | 1.000 | 12 |
| musique | gemini-2.5-flash-lite | P1 | 12 | 0.500 | 0.904 | 11 | 0.968 | 0.687 | 0.767 | 10 |
| musique | gemini-2.5-flash | V1 | 6 | 1.000 | 1.000 | 0 | nan | 1.000 | 1.000 | 6 |
| musique | gemini-2.5-flash | P1 | 6 | 0.833 | 0.992 | 6 | 0.992 | 0.842 | 1.000 | 5 |
| musique | gpt-6-luna | V1 | 12 | 0.833 | 0.983 | 0 | nan | 0.929 | 0.944 | 12 |
| musique | gpt-6-luna | P1 | 12 | 0.667 | 0.867 | 11 | 0.936 | 0.701 | 0.787 | 9 |
| musique | gpt-6.1-terra | V1 | 6 | 0.833 | 0.983 | 0 | nan | 0.917 | 0.944 | 6 |
| musique | gpt-6.1-terra | P1 | 6 | 0.500 | 0.775 | 4 | 0.938 | 0.637 | 0.512 | 5 |

## RM K-sensitivity (banzhaf, exact). k = prefix vs K_max (overlapping); halves = disjoint first vs second K/2 masks. 'argmax_agree' = tie-aware top-group Jaccard
| dataset | model | k | spearman_vs_Kmax | argmax_agree | unique_masks_min | unique_masks_mean |
|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | halves | 0.335 | 0.833 | 61 | 62.167 |
| hotpotqa | claude-haiku-5-5 | 8 | 0.548 | 0.667 | None | None |
| hotpotqa | claude-haiku-5-5 | 16 | 0.652 | 0.833 | None | None |
| hotpotqa | claude-haiku-5-5 | 32 | 0.805 | 1.000 | None | None |
| hotpotqa | gemini-2.5-flash-lite | halves | 0.503 | 0.792 | 58 | 61.500 |
| hotpotqa | gemini-2.5-flash-lite | 8 | 0.449 | 0.667 | None | None |
| hotpotqa | gemini-2.5-flash-lite | 16 | 0.648 | 0.750 | None | None |
| hotpotqa | gemini-2.5-flash-lite | 32 | 0.843 | 0.917 | None | None |
| hotpotqa | gemini-2.5-flash | halves | 0.387 | 0.583 | 61 | 62.500 |
| hotpotqa | gemini-2.5-flash | 8 | 0.626 | 0.833 | None | None |
| hotpotqa | gemini-2.5-flash | 16 | 0.751 | 0.667 | None | None |
| hotpotqa | gemini-2.5-flash | 32 | 0.786 | 0.833 | None | None |
| hotpotqa | gpt-6-luna | halves | 0.377 | 1.000 | 61 | 62.500 |
| hotpotqa | gpt-6-luna | 8 | 0.482 | 0.883 | None | None |
| hotpotqa | gpt-6-luna | 16 | 0.706 | 1.000 | None | None |
| hotpotqa | gpt-6-luna | 32 | 0.718 | 1.000 | None | None |
| hotpotqa | gpt-6.1-terra | halves | 0.325 | 1.000 | 60 | 62.000 |
| hotpotqa | gpt-6.1-terra | 8 | 0.450 | 0.767 | None | None |
| hotpotqa | gpt-6.1-terra | 16 | 0.621 | 1.000 | None | None |
| hotpotqa | gpt-6.1-terra | 32 | 0.724 | 1.000 | None | None |
| musique | claude-haiku-5-5 | halves | 0.185 | 0.708 | 64 | 64.000 |
| musique | claude-haiku-5-5 | 8 | 0.463 | 0.215 | None | None |
| musique | claude-haiku-5-5 | 16 | 0.570 | 0.453 | None | None |
| musique | claude-haiku-5-5 | 32 | 0.703 | 0.792 | None | None |
| musique | gemini-2.5-flash-lite | halves | 0.259 | 0.958 | 64 | 64.000 |
| musique | gemini-2.5-flash-lite | 8 | 0.347 | 0.671 | None | None |
| musique | gemini-2.5-flash-lite | 16 | 0.505 | 0.708 | None | None |
| musique | gemini-2.5-flash-lite | 32 | 0.772 | 0.958 | None | None |
| musique | gemini-2.5-flash | halves | 0.139 | 1.000 | 64 | 64.000 |
| musique | gemini-2.5-flash | 8 | 0.391 | 0.833 | None | None |
| musique | gemini-2.5-flash | 16 | 0.507 | 1.000 | None | None |
| musique | gemini-2.5-flash | 32 | 0.684 | 1.000 | None | None |
| musique | gpt-6-luna | halves | 0.142 | 1.000 | 64 | 64.000 |
| musique | gpt-6-luna | 8 | 0.381 | 0.671 | None | None |
| musique | gpt-6-luna | 16 | 0.503 | 1.000 | None | None |
| musique | gpt-6-luna | 32 | 0.629 | 1.000 | None | None |
| musique | gpt-6.1-terra | halves | 0.078 | 0.667 | 64 | 64.000 |
| musique | gpt-6.1-terra | 8 | 0.438 | 0.722 | None | None |
| musique | gpt-6.1-terra | 16 | 0.565 | 0.750 | None | None |
| musique | gpt-6.1-terra | 32 | 0.732 | 0.667 | None | None |

## Projected cost of the main run (per-call cost from the pilot x formula calls x evaluable set)
| dataset | model | method | cny_per_call | calls_per_inst | cny_per_inst | n_eval | cny_total |
|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | P2 | 0.000 | 34 | 0.003 | 522 | 1.625 |
| hotpotqa | claude-haiku-5-5 | LOI | 0.000 | 11 | 0.000 | 522 | 0.240 |
| hotpotqa | claude-haiku-5-5 | V1.r1 | 0.000 | 1 | 0.000 | 522 | 0.049 |
| hotpotqa | claude-haiku-5-5 | V6 | 0.000 | 1 | 0.000 | 522 | 0.068 |
| hotpotqa | claude-haiku-5-5 | P3 | 0.000 | 28 | 0.003 | 522 | 1.482 |
| hotpotqa | claude-haiku-5-5 | V1 | 0.000 | 1 | 0.000 | 522 | 0.042 |
| hotpotqa | claude-haiku-5-5 | P1 | 0.000 | 14 | 0.001 | 522 | 0.580 |
| hotpotqa | claude-haiku-5-5 | V7 | 0.000 | 5 | 0.001 | 522 | 0.334 |
| hotpotqa | claude-haiku-5-5 | V4 | 0.000 | 10 | 0.001 | 522 | 0.633 |
| hotpotqa | claude-haiku-5-5 | V3 | 0.000 | 2 | 0.000 | 522 | 0.120 |
| hotpotqa | claude-haiku-5-5 | P4 | 0.000 | 68 | 0.007 | 522 | 3.582 |
| hotpotqa | claude-haiku-5-5 | P1.r1 | 0.000 | 14 | 0.001 | 522 | 0.664 |
| hotpotqa | claude-haiku-5-5 | V2 | 0.000 | 5 | 0.000 | 522 | 0.246 |
| hotpotqa | claude-haiku-5-5 | RM32 | 0.000 | 33 | 0.003 | 522 | 1.325 |
| hotpotqa | gemini-2.5-flash-lite | P2 | 0.000 | 34 | 0.002 | 303 | 0.605 |
| hotpotqa | gemini-2.5-flash-lite | LOI | 0.000 | 11 | 0.000 | 303 | 0.046 |
| hotpotqa | gemini-2.5-flash-lite | V1.r1 | 0.000 | 1 | 0.000 | 303 | 0.020 |
| hotpotqa | gemini-2.5-flash-lite | V6 | 0.000 | 1 | 0.000 | 303 | 0.029 |
| hotpotqa | gemini-2.5-flash-lite | P3 | 0.000 | 28 | 0.002 | 303 | 0.518 |
| hotpotqa | gemini-2.5-flash-lite | V1 | 0.000 | 1 | 0.000 | 303 | 0.020 |
| hotpotqa | gemini-2.5-flash-lite | P1 | 0.000 | 14 | 0.001 | 303 | 0.268 |
| hotpotqa | gemini-2.5-flash-lite | V7 | 0.000 | 5 | 0.000 | 303 | 0.144 |
| hotpotqa | gemini-2.5-flash-lite | V4 | 0.000 | 10 | 0.001 | 303 | 0.196 |
| hotpotqa | gemini-2.5-flash-lite | V3 | 0.000 | 2 | 0.000 | 303 | 0.041 |
| hotpotqa | gemini-2.5-flash-lite | P4 | 0.000 | 68 | 0.004 | 303 | 1.225 |
| hotpotqa | gemini-2.5-flash-lite | P1.r1 | 0.000 | 14 | 0.001 | 303 | 0.249 |
| hotpotqa | gemini-2.5-flash-lite | V2 | 0.000 | 5 | 0.000 | 303 | 0.100 |
| hotpotqa | gemini-2.5-flash-lite | RM32 | 0.000 | 33 | 0.001 | 303 | 0.349 |
| hotpotqa | gemini-2.5-flash | P2 | 0.000 | 34 | 0.006 | 87 | 0.531 |
| hotpotqa | gemini-2.5-flash | LOI | 0.000 | 11 | 0.001 | 87 | 0.049 |
| hotpotqa | gemini-2.5-flash | V1.r1 | 0.000 | 1 | 0.000 | 87 | 0.018 |
| hotpotqa | gemini-2.5-flash | V6 | 0.000 | 1 | 0.000 | 87 | 0.036 |
| hotpotqa | gemini-2.5-flash | P3 | 0.000 | 28 | 0.005 | 87 | 0.448 |
| hotpotqa | gemini-2.5-flash | V1 | 0.000 | 1 | 0.000 | 87 | 0.019 |
| hotpotqa | gemini-2.5-flash | P1 | 0.000 | 14 | 0.003 | 87 | 0.222 |
| hotpotqa | gemini-2.5-flash | V7 | 0.000 | 5 | 0.002 | 87 | 0.181 |
| hotpotqa | gemini-2.5-flash | V4 | 0.000 | 10 | 0.002 | 87 | 0.170 |
| hotpotqa | gemini-2.5-flash | V3 | 0.000 | 2 | 0.000 | 87 | 0.034 |
| hotpotqa | gemini-2.5-flash | P4 | 0.000 | 68 | 0.012 | 87 | 1.067 |
| hotpotqa | gemini-2.5-flash | P1.r1 | 0.000 | 14 | 0.003 | 87 | 0.220 |
| hotpotqa | gemini-2.5-flash | V2 | 0.000 | 5 | 0.001 | 87 | 0.088 |
| hotpotqa | gemini-2.5-flash | RM32 | 0.000 | 33 | 0.004 | 87 | 0.324 |
| hotpotqa | gpt-6-luna | P2 | 0.000 | 34 | 0.001 | 178 | 0.196 |
| hotpotqa | gpt-6-luna | LOI | 0.000 | 11 | 0.000 | 178 | 0.062 |
| hotpotqa | gpt-6-luna | V1.r1 | 0.000 | 1 | 0.000 | 178 | 0.007 |
| hotpotqa | gpt-6-luna | V6 | 0.000 | 1 | 0.000 | 178 | 0.007 |
| hotpotqa | gpt-6-luna | P3 | 0.000 | 28 | 0.001 | 178 | 0.156 |
| hotpotqa | gpt-6-luna | V1 | 0.000 | 1 | 0.000 | 178 | 0.006 |
| hotpotqa | gpt-6-luna | P1 | 0.000 | 14 | 0.000 | 178 | 0.081 |
| hotpotqa | gpt-6-luna | V7 | 0.000 | 5 | 0.000 | 178 | 0.033 |
| hotpotqa | gpt-6-luna | V4 | 0.000 | 10 | 0.000 | 178 | 0.059 |
| hotpotqa | gpt-6-luna | V3 | 0.000 | 2 | 0.000 | 178 | 0.012 |
| hotpotqa | gpt-6-luna | P4 | 0.000 | 68 | 0.002 | 178 | 0.374 |
| hotpotqa | gpt-6-luna | P1.r1 | 0.000 | 14 | 0.000 | 178 | 0.080 |
| hotpotqa | gpt-6-luna | V2 | 0.000 | 5 | 0.000 | 178 | 0.032 |
| hotpotqa | gpt-6-luna | RM32 | 0.000 | 33 | 0.001 | 178 | 0.185 |
| hotpotqa | gpt-6.1-terra | P2 | 0.001 | 34 | 0.049 | 70 | 3.456 |
| hotpotqa | gpt-6.1-terra | LOI | 0.001 | 11 | 0.013 | 70 | 0.918 |
| hotpotqa | gpt-6.1-terra | V1.r1 | 0.001 | 1 | 0.001 | 70 | 0.102 |
| hotpotqa | gpt-6.1-terra | V6 | 0.002 | 1 | 0.002 | 70 | 0.109 |
| hotpotqa | gpt-6.1-terra | P3 | 0.001 | 28 | 0.040 | 70 | 2.802 |
| hotpotqa | gpt-6.1-terra | V1 | 0.001 | 1 | 0.001 | 70 | 0.104 |
| hotpotqa | gpt-6.1-terra | P1 | 0.001 | 14 | 0.020 | 70 | 1.421 |
| hotpotqa | gpt-6.1-terra | V7 | 0.002 | 5 | 0.008 | 70 | 0.535 |
| hotpotqa | gpt-6.1-terra | V4 | 0.001 | 10 | 0.015 | 70 | 1.021 |
| hotpotqa | gpt-6.1-terra | V3 | 0.001 | 2 | 0.003 | 70 | 0.204 |
| hotpotqa | gpt-6.1-terra | P4 | 0.001 | 68 | 0.097 | 70 | 6.799 |
| hotpotqa | gpt-6.1-terra | P1.r1 | 0.001 | 14 | 0.020 | 70 | 1.397 |
| hotpotqa | gpt-6.1-terra | V2 | 0.002 | 5 | 0.008 | 70 | 0.530 |
| hotpotqa | gpt-6.1-terra | RM32 | 0.001 | 33 | 0.043 | 70 | 3.041 |
| musique | claude-haiku-5-5 | P2 | 0.000 | 64 | 0.011 | 762 | 8.212 |
| musique | claude-haiku-5-5 | LOI | 0.000 | 21 | 0.001 | 762 | 0.815 |
| musique | claude-haiku-5-5 | V1.r1 | 0.000 | 1 | 0.000 | 762 | 0.141 |
| musique | claude-haiku-5-5 | V6 | 0.000 | 1 | 0.000 | 762 | 0.150 |
| musique | claude-haiku-5-5 | P3 | 0.000 | 48 | 0.008 | 762 | 6.260 |
| musique | claude-haiku-5-5 | V1 | 0.000 | 1 | 0.000 | 762 | 0.144 |
| musique | claude-haiku-5-5 | P1 | 0.000 | 24 | 0.004 | 762 | 3.043 |
| musique | claude-haiku-5-5 | V7 | 0.000 | 5 | 0.001 | 762 | 0.719 |
| musique | claude-haiku-5-5 | V4 | 0.000 | 10 | 0.002 | 762 | 1.361 |
| musique | claude-haiku-5-5 | V3 | 0.000 | 2 | 0.000 | 762 | 0.268 |
| musique | claude-haiku-5-5 | P4 | 0.000 | 128 | 0.022 | 762 | 16.691 |
| musique | claude-haiku-5-5 | P1.r1 | 0.000 | 24 | 0.004 | 762 | 3.064 |
| musique | claude-haiku-5-5 | V2 | 0.000 | 5 | 0.001 | 762 | 0.724 |
| musique | claude-haiku-5-5 | RM32 | 0.000 | 33 | 0.004 | 762 | 3.062 |
| musique | gemini-2.5-flash-lite | P2 | 0.000 | 64 | 0.007 | 786 | 5.178 |
| musique | gemini-2.5-flash-lite | LOI | 0.000 | 21 | 0.000 | 786 | 0.233 |
| musique | gemini-2.5-flash-lite | V1.r1 | 0.000 | 1 | 0.000 | 786 | 0.086 |
| musique | gemini-2.5-flash-lite | V6 | 0.000 | 1 | 0.000 | 786 | 0.115 |
| musique | gemini-2.5-flash-lite | P3 | 0.000 | 48 | 0.005 | 786 | 3.934 |
| musique | gemini-2.5-flash-lite | V1 | 0.000 | 1 | 0.000 | 786 | 0.088 |
| musique | gemini-2.5-flash-lite | P1 | 0.000 | 24 | 0.002 | 786 | 1.953 |
| musique | gemini-2.5-flash-lite | V7 | 0.000 | 5 | 0.001 | 786 | 0.589 |
| musique | gemini-2.5-flash-lite | V4 | 0.000 | 10 | 0.001 | 786 | 0.867 |
| musique | gemini-2.5-flash-lite | V3 | 0.000 | 2 | 0.000 | 786 | 0.177 |
| musique | gemini-2.5-flash-lite | P4 | 0.000 | 128 | 0.013 | 786 | 10.517 |
| musique | gemini-2.5-flash-lite | P1.r1 | 0.000 | 24 | 0.002 | 786 | 1.944 |
| musique | gemini-2.5-flash-lite | V2 | 0.000 | 5 | 0.001 | 786 | 0.439 |
| musique | gemini-2.5-flash-lite | RM32 | 0.000 | 33 | 0.002 | 786 | 1.513 |
| musique | gemini-2.5-flash | P2 | 0.000 | 64 | 0.019 | 68 | 1.293 |
| musique | gemini-2.5-flash | LOI | 0.000 | 21 | 0.001 | 68 | 0.076 |
| musique | gemini-2.5-flash | V1.r1 | 0.000 | 1 | 0.000 | 68 | 0.023 |
| musique | gemini-2.5-flash | V6 | 0.001 | 1 | 0.001 | 68 | 0.041 |
| musique | gemini-2.5-flash | P3 | 0.000 | 48 | 0.015 | 68 | 1.018 |
| musique | gemini-2.5-flash | V1 | 0.000 | 1 | 0.000 | 68 | 0.023 |
| musique | gemini-2.5-flash | P1 | 0.000 | 24 | 0.007 | 68 | 0.499 |
| musique | gemini-2.5-flash | V7 | 0.001 | 5 | 0.003 | 68 | 0.218 |
| musique | gemini-2.5-flash | V4 | 0.000 | 10 | 0.003 | 68 | 0.222 |
| musique | gemini-2.5-flash | V3 | 0.000 | 2 | 0.001 | 68 | 0.043 |
| musique | gemini-2.5-flash | P4 | 0.000 | 128 | 0.039 | 68 | 2.655 |
| musique | gemini-2.5-flash | P1.r1 | 0.000 | 24 | 0.007 | 68 | 0.506 |
| musique | gemini-2.5-flash | V2 | 0.000 | 5 | 0.002 | 68 | 0.114 |
| musique | gemini-2.5-flash | RM32 | 0.000 | 33 | 0.006 | 68 | 0.406 |
| musique | gpt-6-luna | P2 | 0.000 | 64 | 0.004 | 614 | 2.688 |
| musique | gpt-6-luna | LOI | 0.000 | 21 | 0.001 | 614 | 0.850 |
| musique | gpt-6-luna | V1.r1 | 0.000 | 1 | 0.000 | 614 | 0.048 |
| musique | gpt-6-luna | V6 | 0.000 | 1 | 0.000 | 614 | 0.053 |
| musique | gpt-6-luna | P3 | 0.000 | 48 | 0.003 | 614 | 1.927 |
| musique | gpt-6-luna | V1 | 0.000 | 1 | 0.000 | 614 | 0.046 |
| musique | gpt-6-luna | P1 | 0.000 | 24 | 0.002 | 614 | 1.012 |
| musique | gpt-6-luna | V7 | 0.000 | 5 | 0.000 | 614 | 0.243 |
| musique | gpt-6-luna | V4 | 0.000 | 10 | 0.001 | 614 | 0.405 |
| musique | gpt-6-luna | V3 | 0.000 | 2 | 0.000 | 614 | 0.081 |
| musique | gpt-6-luna | P4 | 0.000 | 128 | 0.008 | 614 | 5.084 |
| musique | gpt-6-luna | P1.r1 | 0.000 | 24 | 0.002 | 614 | 1.014 |
| musique | gpt-6-luna | V2 | 0.000 | 5 | 0.000 | 614 | 0.246 |
| musique | gpt-6-luna | RM32 | 0.000 | 33 | 0.002 | 614 | 1.384 |
| musique | gpt-6.1-terra | P2 | 0.002 | 64 | 0.118 | 60 | 7.067 |
| musique | gpt-6.1-terra | LOI | 0.001 | 21 | 0.028 | 60 | 1.652 |
| musique | gpt-6.1-terra | V1.r1 | 0.002 | 1 | 0.002 | 60 | 0.120 |
| musique | gpt-6.1-terra | V6 | 0.002 | 1 | 0.002 | 60 | 0.142 |
| musique | gpt-6.1-terra | P3 | 0.002 | 48 | 0.087 | 60 | 5.201 |
| musique | gpt-6.1-terra | V1 | 0.002 | 1 | 0.002 | 60 | 0.122 |
| musique | gpt-6.1-terra | P1 | 0.002 | 24 | 0.045 | 60 | 2.712 |
| musique | gpt-6.1-terra | V7 | 0.002 | 5 | 0.011 | 60 | 0.634 |
| musique | gpt-6.1-terra | V4 | 0.002 | 10 | 0.019 | 60 | 1.128 |
| musique | gpt-6.1-terra | V3 | 0.002 | 2 | 0.004 | 60 | 0.232 |
| musique | gpt-6.1-terra | P4 | 0.002 | 128 | 0.231 | 60 | 13.851 |
| musique | gpt-6.1-terra | P1.r1 | 0.002 | 24 | 0.044 | 60 | 2.624 |
| musique | gpt-6.1-terra | V2 | 0.002 | 5 | 0.010 | 60 | 0.614 |
| musique | gpt-6.1-terra | RM32 | 0.002 | 33 | 0.052 | 60 | 3.133 |

## Cost
| dataset | model | method | n | cost_cny | cny_per_inst | calls_issued | truncated |
|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | P2 | 12 | 0.036 | 0.003 | 396 | 0 |
| hotpotqa | claude-haiku-5-5 | LOI | 12 | 0.004 | 0.000 | 94 | 0 |
| hotpotqa | claude-haiku-5-5 | V1.r1 | 12 | 0.001 | 0.000 | 12 | 0 |
| hotpotqa | claude-haiku-5-5 | V6 | 12 | 0.002 | 0.000 | 12 | 0 |
| hotpotqa | claude-haiku-5-5 | P3 | 12 | 0.017 | 0.001 | 168 | 0 |
| hotpotqa | claude-haiku-5-5 | V1 | 12 | 0.001 | 0.000 | 10 | 0 |
| hotpotqa | claude-haiku-5-5 | P5 | 12 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | claude-haiku-5-5 | P1 | 12 | 0.011 | 0.001 | 140 | 0 |
| hotpotqa | claude-haiku-5-5 | V7 | 12 | 0.008 | 0.001 | 60 | 0 |
| hotpotqa | claude-haiku-5-5 | V4 | 12 | 0.006 | 0.001 | 50 | 0 |
| hotpotqa | claude-haiku-5-5 | V3 | 12 | 0.001 | 0.000 | 12 | 0 |
| hotpotqa | claude-haiku-5-5 | P4 | 12 | 0.040 | 0.003 | 396 | 0 |
| hotpotqa | claude-haiku-5-5 | P1.r1 | 12 | 0.015 | 0.001 | 168 | 0 |
| hotpotqa | claude-haiku-5-5 | V2 | 12 | 0.006 | 0.000 | 60 | 0 |
| hotpotqa | claude-haiku-5-5 | RM64 | 12 | 0.056 | 0.005 | 724 | 0 |
| hotpotqa | claude-haiku-5-5 | V5 | 12 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P2 | 12 | 0.023 | 0.002 | 396 | 0 |
| hotpotqa | gemini-2.5-flash-lite | LOI | 12 | 0.002 | 0.000 | 113 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V1.r1 | 12 | 0.001 | 0.000 | 12 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V6 | 12 | 0.001 | 0.000 | 12 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P3 | 12 | 0.010 | 0.001 | 168 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V1 | 12 | 0.001 | 0.000 | 12 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P5 | 12 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P1 | 6 | 0.003 | 0.000 | 47 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V7 | 12 | 0.006 | 0.000 | 60 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V4 | 12 | 0.004 | 0.000 | 60 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V3 | 12 | 0.001 | 0.000 | 12 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P4 | 12 | 0.024 | 0.002 | 396 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P1.r1 | 12 | 0.010 | 0.001 | 168 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V2 | 12 | 0.004 | 0.000 | 60 | 0 |
| hotpotqa | gemini-2.5-flash-lite | RM64 | 12 | 0.026 | 0.002 | 735 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V5 | 12 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | P2 | 6 | 0.036 | 0.006 | 198 | 0 |
| hotpotqa | gemini-2.5-flash | LOI | 6 | 0.003 | 0.000 | 54 | 0 |
| hotpotqa | gemini-2.5-flash | V1.r1 | 6 | 0.001 | 0.000 | 6 | 0 |
| hotpotqa | gemini-2.5-flash | V6 | 6 | 0.002 | 0.000 | 6 | 0 |
| hotpotqa | gemini-2.5-flash | P3 | 6 | 0.015 | 0.003 | 84 | 0 |
| hotpotqa | gemini-2.5-flash | V1 | 6 | 0.001 | 0.000 | 6 | 0 |
| hotpotqa | gemini-2.5-flash | P5 | 6 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | P1 | 6 | 0.014 | 0.002 | 78 | 0 |
| hotpotqa | gemini-2.5-flash | V7 | 6 | 0.012 | 0.002 | 30 | 0 |
| hotpotqa | gemini-2.5-flash | V4 | 6 | 0.006 | 0.001 | 30 | 0 |
| hotpotqa | gemini-2.5-flash | V3 | 6 | 0.001 | 0.000 | 6 | 0 |
| hotpotqa | gemini-2.5-flash | P4 | 6 | 0.032 | 0.005 | 177 | 0 |
| hotpotqa | gemini-2.5-flash | P1.r1 | 6 | 0.015 | 0.003 | 84 | 0 |
| hotpotqa | gemini-2.5-flash | V2 | 6 | 0.006 | 0.001 | 30 | 0 |
| hotpotqa | gemini-2.5-flash | RM64 | 6 | 0.042 | 0.007 | 373 | 0 |
| hotpotqa | gemini-2.5-flash | V5 | 6 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6-luna | P2 | 12 | 0.013 | 0.001 | 396 | 0 |
| hotpotqa | gpt-6-luna | LOI | 12 | 0.004 | 0.000 | 114 | 0 |
| hotpotqa | gpt-6-luna | V1.r1 | 12 | 0.000 | 0.000 | 12 | 0 |
| hotpotqa | gpt-6-luna | V6 | 12 | 0.000 | 0.000 | 12 | 0 |
| hotpotqa | gpt-6-luna | P3 | 12 | 0.005 | 0.000 | 168 | 0 |
| hotpotqa | gpt-6-luna | V1 | 12 | 0.000 | 0.000 | 12 | 0 |
| hotpotqa | gpt-6-luna | P5 | 12 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6-luna | P1 | 12 | 0.005 | 0.000 | 168 | 0 |
| hotpotqa | gpt-6-luna | V7 | 12 | 0.002 | 0.000 | 60 | 0 |
| hotpotqa | gpt-6-luna | V4 | 12 | 0.002 | 0.000 | 60 | 0 |
| hotpotqa | gpt-6-luna | V3 | 12 | 0.000 | 0.000 | 12 | 0 |
| hotpotqa | gpt-6-luna | P4 | 12 | 0.012 | 0.001 | 396 | 0 |
| hotpotqa | gpt-6-luna | P1.r1 | 12 | 0.005 | 0.000 | 168 | 0 |
| hotpotqa | gpt-6-luna | V2 | 9 | 0.001 | 0.000 | 40 | 0 |
| hotpotqa | gpt-6-luna | RM64 | 12 | 0.023 | 0.002 | 744 | 0 |
| hotpotqa | gpt-6-luna | V5 | 12 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6.1-terra | P2 | 6 | 0.287 | 0.048 | 198 | 0 |
| hotpotqa | gpt-6.1-terra | LOI | 6 | 0.067 | 0.011 | 56 | 0 |
| hotpotqa | gpt-6.1-terra | V1.r1 | 6 | 0.009 | 0.001 | 6 | 0 |
| hotpotqa | gpt-6.1-terra | V6 | 6 | 0.009 | 0.002 | 6 | 0 |
| hotpotqa | gpt-6.1-terra | P3 | 6 | 0.120 | 0.020 | 84 | 0 |
| hotpotqa | gpt-6.1-terra | V1 | 6 | 0.009 | 0.001 | 6 | 0 |
| hotpotqa | gpt-6.1-terra | P5 | 6 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6.1-terra | P1 | 6 | 0.113 | 0.019 | 78 | 0 |
| hotpotqa | gpt-6.1-terra | V7 | 6 | 0.046 | 0.008 | 30 | 0 |
| hotpotqa | gpt-6.1-terra | V4 | 6 | 0.044 | 0.007 | 30 | 0 |
| hotpotqa | gpt-6.1-terra | V3 | 6 | 0.009 | 0.001 | 6 | 0 |
| hotpotqa | gpt-6.1-terra | P4 | 6 | 0.283 | 0.047 | 198 | 0 |
| hotpotqa | gpt-6.1-terra | P1.r1 | 6 | 0.120 | 0.020 | 84 | 0 |
| hotpotqa | gpt-6.1-terra | V2 | 3 | 0.017 | 0.006 | 11 | 0 |
| hotpotqa | gpt-6.1-terra | RM64 | 6 | 0.487 | 0.081 | 370 | 0 |
| hotpotqa | gpt-6.1-terra | V5 | 6 | 0.000 | 0.000 | 0 | 0 |
| musique | claude-haiku-5-5 | P2 | 12 | 0.127 | 0.011 | 756 | 0 |
| musique | claude-haiku-5-5 | LOI | 12 | 0.012 | 0.001 | 240 | 0 |
| musique | claude-haiku-5-5 | V1.r1 | 12 | 0.002 | 0.000 | 12 | 0 |
| musique | claude-haiku-5-5 | V6 | 12 | 0.002 | 0.000 | 12 | 0 |
| musique | claude-haiku-5-5 | P3 | 12 | 0.049 | 0.004 | 288 | 0 |
| musique | claude-haiku-5-5 | V1 | 12 | 0.002 | 0.000 | 12 | 0 |
| musique | claude-haiku-5-5 | P5 | 12 | 0.000 | 0.000 | 0 | 0 |
| musique | claude-haiku-5-5 | P1 | 12 | 0.048 | 0.004 | 286 | 0 |
| musique | claude-haiku-5-5 | V7 | 12 | 0.011 | 0.001 | 60 | 0 |
| musique | claude-haiku-5-5 | V4 | 12 | 0.011 | 0.001 | 60 | 0 |
| musique | claude-haiku-5-5 | V3 | 12 | 0.002 | 0.000 | 12 | 0 |
| musique | claude-haiku-5-5 | P4 | 12 | 0.129 | 0.011 | 756 | 0 |
| musique | claude-haiku-5-5 | P1.r1 | 12 | 0.048 | 0.004 | 288 | 0 |
| musique | claude-haiku-5-5 | V2 | 1 | 0.000 | 0.000 | 1 | 0 |
| musique | claude-haiku-5-5 | RM64 | 12 | 0.094 | 0.008 | 768 | 0 |
| musique | claude-haiku-5-5 | V5 | 12 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash-lite | P2 | 12 | 0.078 | 0.006 | 756 | 0 |
| musique | gemini-2.5-flash-lite | LOI | 12 | 0.003 | 0.000 | 240 | 0 |
| musique | gemini-2.5-flash-lite | V1.r1 | 12 | 0.001 | 0.000 | 12 | 0 |
| musique | gemini-2.5-flash-lite | V6 | 12 | 0.002 | 0.000 | 12 | 0 |
| musique | gemini-2.5-flash-lite | P3 | 12 | 0.030 | 0.003 | 288 | 0 |
| musique | gemini-2.5-flash-lite | V1 | 12 | 0.001 | 0.000 | 12 | 0 |
| musique | gemini-2.5-flash-lite | P5 | 12 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash-lite | P1 | 12 | 0.029 | 0.002 | 276 | 0 |
| musique | gemini-2.5-flash-lite | V7 | 1 | 0.000 | 0.000 | 1 | 0 |
| musique | gemini-2.5-flash-lite | V4 | 12 | 0.007 | 0.001 | 60 | 0 |
| musique | gemini-2.5-flash-lite | V3 | 12 | 0.001 | 0.000 | 12 | 0 |
| musique | gemini-2.5-flash-lite | P4 | 12 | 0.079 | 0.007 | 756 | 0 |
| musique | gemini-2.5-flash-lite | P1.r1 | 12 | 0.030 | 0.002 | 288 | 0 |
| musique | gemini-2.5-flash-lite | V2 | 12 | 0.007 | 0.001 | 60 | 0 |
| musique | gemini-2.5-flash-lite | RM64 | 12 | 0.045 | 0.004 | 768 | 0 |
| musique | gemini-2.5-flash-lite | V5 | 12 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | P2 | 3 | 0.036 | 0.012 | 121 | 0 |
| musique | gemini-2.5-flash | LOI | 6 | 0.006 | 0.001 | 120 | 0 |
| musique | gemini-2.5-flash | V1.r1 | 6 | 0.002 | 0.000 | 6 | 0 |
| musique | gemini-2.5-flash | V6 | 6 | 0.004 | 0.001 | 6 | 0 |
| musique | gemini-2.5-flash | P3 | 6 | 0.045 | 0.007 | 144 | 0 |
| musique | gemini-2.5-flash | V1 | 6 | 0.002 | 0.000 | 6 | 0 |
| musique | gemini-2.5-flash | P5 | 6 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | P1 | 6 | 0.042 | 0.007 | 138 | 0 |
| musique | gemini-2.5-flash | V7 | 6 | 0.019 | 0.003 | 30 | 1 |
| musique | gemini-2.5-flash | V4 | 6 | 0.010 | 0.002 | 30 | 0 |
| musique | gemini-2.5-flash | V3 | 6 | 0.002 | 0.000 | 6 | 0 |
| musique | gemini-2.5-flash | P4 | 6 | 0.115 | 0.019 | 378 | 0 |
| musique | gemini-2.5-flash | P1.r1 | 6 | 0.045 | 0.007 | 144 | 0 |
| musique | gemini-2.5-flash | V2 | 6 | 0.010 | 0.002 | 30 | 0 |
| musique | gemini-2.5-flash | RM64 | 6 | 0.070 | 0.012 | 384 | 0 |
| musique | gemini-2.5-flash | V5 | 6 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6-luna | P2 | 12 | 0.052 | 0.004 | 756 | 0 |
| musique | gpt-6-luna | LOI | 12 | 0.016 | 0.001 | 240 | 2 |
| musique | gpt-6-luna | V1.r1 | 12 | 0.001 | 0.000 | 12 | 0 |
| musique | gpt-6-luna | V6 | 12 | 0.001 | 0.000 | 12 | 0 |
| musique | gpt-6-luna | P3 | 12 | 0.019 | 0.002 | 288 | 0 |
| musique | gpt-6-luna | V1 | 12 | 0.001 | 0.000 | 12 | 0 |
| musique | gpt-6-luna | P5 | 12 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6-luna | P1 | 12 | 0.020 | 0.002 | 288 | 0 |
| musique | gpt-6-luna | V7 | 12 | 0.005 | 0.000 | 60 | 0 |
| musique | gpt-6-luna | V4 | 12 | 0.004 | 0.000 | 60 | 0 |
| musique | gpt-6-luna | V3 | 12 | 0.001 | 0.000 | 12 | 0 |
| musique | gpt-6-luna | P4 | 12 | 0.049 | 0.004 | 756 | 0 |
| musique | gpt-6-luna | P1.r1 | 12 | 0.020 | 0.002 | 288 | 0 |
| musique | gpt-6-luna | V2 | 11 | 0.004 | 0.000 | 49 | 0 |
| musique | gpt-6-luna | RM64 | 12 | 0.052 | 0.004 | 768 | 0 |
| musique | gpt-6-luna | V5 | 12 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | P2 | 6 | 0.696 | 0.116 | 378 | 0 |
| musique | gpt-6.1-terra | LOI | 6 | 0.157 | 0.026 | 120 | 0 |
| musique | gpt-6.1-terra | V1.r1 | 6 | 0.012 | 0.002 | 6 | 0 |
| musique | gpt-6.1-terra | V6 | 6 | 0.014 | 0.002 | 6 | 0 |
| musique | gpt-6.1-terra | P3 | 6 | 0.260 | 0.043 | 144 | 0 |
| musique | gpt-6.1-terra | V1 | 6 | 0.012 | 0.002 | 6 | 0 |
| musique | gpt-6.1-terra | P5 | 6 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | P1 | 6 | 0.260 | 0.043 | 138 | 0 |
| musique | gpt-6.1-terra | V7 | 6 | 0.063 | 0.011 | 30 | 0 |
| musique | gpt-6.1-terra | V4 | 6 | 0.056 | 0.009 | 30 | 0 |
| musique | gpt-6.1-terra | V3 | 6 | 0.012 | 0.002 | 6 | 0 |
| musique | gpt-6.1-terra | P4 | 6 | 0.682 | 0.114 | 378 | 0 |
| musique | gpt-6.1-terra | P1.r1 | 6 | 0.262 | 0.044 | 144 | 0 |
| musique | gpt-6.1-terra | V2 | 4 | 0.031 | 0.008 | 15 | 0 |
| musique | gpt-6.1-terra | RM64 | 6 | 0.608 | 0.101 | 384 | 0 |
| musique | gpt-6.1-terra | V5 | 6 | 0.000 | 0.000 | 0 | 0 |
