# Drop-all-gold oracle (original presentation, repeats 0-2)

survive = answer still correct with every gold passage removed (>=2/3 repeats; 3/3 in brackets). ABD = some non-gold passage contains a gold answer string.

| dataset | model | n | survive | ABD share | survive ABD | survive no-ABD | survive context_dep | survive abstained_correct | P1 rows | P1 all-zero | survive among P1 all-zero | survive among P1 non-zero |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | 522 | 0.071 [0.054] | 0.239 | 0.256 (n=125) | 0.013 (n=397) | 0.090 (n=145) | 0.064 (n=377) | 522 (main) | 0.201 (n=522) | 0.219 (n=105) | 0.034 (n=417) |
| hotpotqa | gemini-2.5-flash-lite | 303 | 0.079 [0.076] | 0.201 | 0.311 (n=61) | 0.021 (n=242) | 0.086 (n=255) | 0.042 (n=48) | 303 (main) | 0.215 (n=303) | 0.277 (n=65) | 0.025 (n=238) |
| hotpotqa | gemini-2.5-flash | 87 | 0.057 [0.057] | 0.172 | 0.267 (n=15) | 0.014 (n=72) | 0.070 (n=71) | 0.000 (n=16) | 87 (main) | 0.322 (n=87) | 0.143 (n=28) | 0.017 (n=59) |
| hotpotqa | gpt-6.1-terra | 70 | 0.129 [0.086] | 0.186 | 0.615 (n=13) | 0.018 (n=57) | 0.131 (n=61) | 0.111 (n=9) | 70 (main) | 0.443 (n=70) | 0.290 (n=31) | 0.000 (n=39) |
| musique | claude-haiku-5-5 | 762 | 0.012 [0.009] | 0.100 | 0.079 (n=76) | 0.004 (n=686) | 0.023 (n=217) | 0.007 (n=545) | 759 (main) | 0.032 (n=759) | 0.250 (n=24) | 0.004 (n=735) |
| musique | gemini-2.5-flash-lite | 786 | 0.034 [0.025] | 0.104 | 0.220 (n=82) | 0.013 (n=704) | 0.052 (n=440) | 0.012 (n=346) | 786 (main) | 0.070 (n=786) | 0.164 (n=55) | 0.025 (n=731) |
| musique | gemini-2.5-flash | 68 | 0.074 [0.059] | 0.118 | 0.125 (n=8) | 0.067 (n=60) | 0.111 (n=45) | 0.000 (n=23) | 68 (main) | 0.118 (n=68) | 0.250 (n=8) | 0.050 (n=60) |
| musique | gpt-6.1-terra | 60 | 0.033 [0.017] | 0.083 | 0.000 (n=5) | 0.036 (n=55) | 0.021 (n=47) | 0.077 (n=13) | 60 (main) | 0.133 (n=60) | 0.125 (n=8) | 0.019 (n=52) |

Total cost ≈ ¥1.57
