# Requested temperature vs observed behaviour

## Reasoning tokens per issued call (all runs)

| model | calls | reasoning tokens / call | completion tokens / call |
|---|---|---|---|
| claude-haiku-5-5 | 339257 | 0.0 | 241.1 |
| gpt-6-luna | 203257 | 124.9 | 141.8 |
| gpt-6.1-terra | 77524 | 38.0 | 50.2 |
| gemini-2.5-flash-lite | 390436 | 0.0 | 18.6 |
| gemini-2.5-flash | 80801 | 0.0 | 14.6 |

## Draw diversity of the full-context prompt (same questions)

| dataset | model | n | any answer disagreement: 5 draws @0.7 (V2) | 4 draws @0.01 (P1) | per-draw change @0.01 (P1) | per-draw change @0.7 (P2) |
|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | 522 | 0.123 | 0.115 | 0.068 | 0.052 |
| hotpotqa | gpt-6-luna | 164 | 0.226 | 0.134 | 0.081 | 0.118 |
| hotpotqa | gpt-6.1-terra | 70 | 0.029 | 0.086 | 0.062 | 0.033 |
| hotpotqa | gemini-2.5-flash-lite | 303 | 0.106 | 0.076 | 0.042 | 0.044 |
| hotpotqa | gemini-2.5-flash | 87 | 0.023 | 0.057 | 0.038 | 0.034 |
| musique | claude-haiku-5-5 | 758 | 0.257 | 0.198 | 0.126 | 0.248 |
| musique | gpt-6-luna | 614 | 0.248 | 0.220 | 0.135 | 0.186 |
| musique | gpt-6.1-terra | 60 | 0.150 | 0.117 | 0.083 | 0.111 |
| musique | gemini-2.5-flash-lite | 785 | 0.132 | 0.088 | 0.053 | 0.055 |
| musique | gemini-2.5-flash | 68 | 0.044 | 0.044 | 0.015 | 0.005 |
