# Phase-2 grid_sub analysis

## Methods
| dataset | model | method | n | top1 | rec@g | random_top1 | all_zero | unique_max | reaches_tau | calls/inst | full_ctx_change |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | P2 | 200 | 0.892 | 0.667 | 0.200 | 0.080 | 0.660 | 0.900 | 33.000 | 0.055 |
| hotpotqa | claude-haiku-5-5 | P3 | 200 | 0.731 | 0.547 | 0.200 | 0.195 | 0.420 | 0.805 | 14.000 | 0.072 |
| hotpotqa | claude-haiku-5-5 | P4 | 200 | 0.892 | 0.667 | 0.200 | 0.080 | 0.660 | 0.900 | 33.000 | 0.055 |
| hotpotqa | claude-haiku-5-5 | P5 | 200 | 0.952 | 0.782 | 0.200 | 0.020 | 0.870 | 0.915 | 0.000 | 0.055 |
| hotpotqa | claude-haiku-5-5 | V2 | 200 | 0.984 | 0.943 | 0.200 | 0.005 | 0.180 | 0.995 | 5.000 | None |
| hotpotqa | claude-haiku-5-5 | V3 | 200 | 0.926 | 0.881 | 0.200 | 0.075 | 0.100 | 0.925 | 1.000 | None |
| hotpotqa | claude-haiku-5-5 | V4 | 200 | 0.980 | 0.940 | 0.200 | 0.005 | 0.145 | 0.995 | 5.000 | None |
| hotpotqa | claude-haiku-5-5 | V5 | 200 | 0.980 | 0.940 | 0.200 | 0.005 | 0.145 | 0.995 | 0.000 | None |
| hotpotqa | claude-haiku-5-5 | V6 | 200 | 0.978 | 0.934 | 0.200 | 0.000 | 0.105 | 1.000 | 1.000 | None |
| hotpotqa | claude-haiku-5-5 | V7 | 200 | 0.991 | 0.958 | 0.200 | 0.000 | 0.150 | 1.000 | 5.000 | None |
| hotpotqa | gemini-2.5-flash-lite | P2 | 200 | 0.795 | 0.529 | 0.200 | 0.160 | 0.630 | 0.805 | 33.000 | 0.030 |
| hotpotqa | gemini-2.5-flash-lite | P3 | 200 | 0.716 | 0.477 | 0.200 | 0.230 | 0.545 | 0.770 | 14.000 | 0.025 |
| hotpotqa | gemini-2.5-flash-lite | P4 | 200 | 0.795 | 0.529 | 0.200 | 0.160 | 0.630 | 0.805 | 33.000 | 0.030 |
| hotpotqa | gemini-2.5-flash-lite | P5 | 200 | 0.865 | 0.619 | 0.200 | 0.085 | 0.795 | 0.835 | 0.000 | 0.030 |
| hotpotqa | gemini-2.5-flash-lite | V2 | 200 | 0.969 | 0.884 | 0.200 | 0.000 | 0.300 | 1.000 | 5.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V3 | 200 | 0.952 | 0.837 | 0.200 | 0.010 | 0.265 | 0.990 | 1.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V4 | 200 | 0.966 | 0.882 | 0.200 | 0.005 | 0.300 | 0.995 | 5.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V5 | 200 | 0.966 | 0.882 | 0.200 | 0.005 | 0.300 | 0.995 | 0.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V6 | 200 | 0.959 | 0.876 | 0.200 | 0.010 | 0.185 | 0.990 | 1.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V7 | 200 | 0.967 | 0.918 | 0.200 | 0.005 | 0.305 | 0.995 | 5.000 | None |
| hotpotqa | gemini-2.5-flash | P2 | 81 | 0.732 | 0.479 | 0.200 | 0.259 | 0.605 | 0.716 | 33.000 | 0.037 |
| hotpotqa | gemini-2.5-flash | P3 | 81 | 0.683 | 0.452 | 0.200 | 0.309 | 0.519 | 0.691 | 14.000 | 0.041 |
| hotpotqa | gemini-2.5-flash | P4 | 81 | 0.732 | 0.479 | 0.200 | 0.259 | 0.605 | 0.716 | 33.000 | 0.037 |
| hotpotqa | gemini-2.5-flash | P5 | 81 | 0.869 | 0.599 | 0.200 | 0.099 | 0.815 | 0.716 | 0.000 | 0.037 |
| hotpotqa | gemini-2.5-flash | V2 | 81 | 0.990 | 0.880 | 0.200 | 0.000 | 0.358 | 1.000 | 5.000 | None |
| hotpotqa | gemini-2.5-flash | V3 | 81 | 0.986 | 0.859 | 0.200 | 0.000 | 0.284 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash | V4 | 81 | 0.970 | 0.871 | 0.200 | 0.025 | 0.333 | 0.975 | 5.000 | None |
| hotpotqa | gemini-2.5-flash | V5 | 81 | 0.970 | 0.871 | 0.200 | 0.025 | 0.333 | 0.975 | 0.000 | None |
| hotpotqa | gemini-2.5-flash | V6 | 81 | 0.996 | 0.903 | 0.200 | 0.000 | 0.210 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash | V7 | 81 | 1.000 | 0.941 | 0.200 | 0.000 | 0.333 | 1.000 | 5.000 | None |
| hotpotqa | gpt-6-luna | P2 | 166 | 0.705 | 0.455 | 0.202 | 0.247 | 0.620 | 0.693 | 30.120 | 0.120 |
| hotpotqa | gpt-6-luna | P3 | 166 | 0.570 | 0.383 | 0.202 | 0.367 | 0.428 | 0.633 | 12.904 | 0.086 |
| hotpotqa | gpt-6-luna | P4 | 166 | 0.759 | 0.481 | 0.202 | 0.187 | 0.657 | 0.759 | 67.078 | 0.114 |
| hotpotqa | gpt-6-luna | P5 | 166 | 0.841 | 0.575 | 0.202 | 0.108 | 0.813 | 0.771 | 0.000 | 0.114 |
| hotpotqa | gpt-6-luna | V2 | 166 | 0.980 | 0.923 | 0.202 | 0.000 | 0.373 | 1.000 | 5.000 | None |
| hotpotqa | gpt-6-luna | V3 | 166 | 0.961 | 0.860 | 0.202 | 0.024 | 0.235 | 0.976 | 1.000 | None |
| hotpotqa | gpt-6-luna | V4 | 166 | 0.977 | 0.916 | 0.202 | 0.000 | 0.373 | 1.000 | 4.946 | None |
| hotpotqa | gpt-6-luna | V5 | 166 | 0.977 | 0.916 | 0.202 | 0.000 | 0.373 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6-luna | V6 | 166 | 0.963 | 0.874 | 0.202 | 0.000 | 0.217 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6-luna | V7 | 166 | 0.969 | 0.920 | 0.202 | 0.000 | 0.367 | 1.000 | 5.000 | None |
| hotpotqa | gpt-6.1-terra | P2 | 64 | 0.664 | 0.420 | 0.200 | 0.359 | 0.547 | 0.562 | 31.359 | 0.036 |
| hotpotqa | gpt-6.1-terra | P3 | 64 | 0.596 | 0.388 | 0.200 | 0.453 | 0.469 | 0.547 | 21.438 | 0.021 |
| hotpotqa | gpt-6.1-terra | P4 | 64 | 0.652 | 0.409 | 0.200 | 0.406 | 0.578 | 0.484 | 66.000 | 0.010 |
| hotpotqa | gpt-6.1-terra | P5 | 64 | 0.852 | 0.611 | 0.200 | 0.141 | 0.828 | 0.547 | 0.000 | 0.010 |
| hotpotqa | gpt-6.1-terra | V2 | 64 | 0.992 | 0.921 | 0.200 | 0.000 | 0.250 | 1.000 | 3.750 | None |
| hotpotqa | gpt-6.1-terra | V3 | 64 | 0.982 | 0.927 | 0.200 | 0.016 | 0.125 | 0.984 | 1.000 | None |
| hotpotqa | gpt-6.1-terra | V4 | 64 | 0.992 | 0.922 | 0.200 | 0.000 | 0.234 | 1.000 | 5.469 | None |
| hotpotqa | gpt-6.1-terra | V5 | 64 | 0.992 | 0.922 | 0.200 | 0.000 | 0.234 | 1.000 | 0.625 | None |
| hotpotqa | gpt-6.1-terra | V6 | 64 | 0.992 | 0.916 | 0.200 | 0.000 | 0.172 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6.1-terra | V7 | 64 | 0.992 | 0.951 | 0.200 | 0.000 | 0.203 | 1.000 | 4.969 | None |
| musique | claude-haiku-5-5 | P2 | 200 | 0.870 | 0.673 | 0.150 | 0.005 | 0.295 | 0.990 | 61.330 | 0.137 |
| musique | claude-haiku-5-5 | P3 | 200 | 0.703 | 0.516 | 0.150 | 0.030 | 0.245 | 0.970 | 23.960 | 0.145 |
| musique | claude-haiku-5-5 | P4 | 200 | 0.870 | 0.673 | 0.150 | 0.005 | 0.295 | 0.990 | 61.015 | 0.137 |
| musique | claude-haiku-5-5 | P5 | 200 | 0.873 | 0.717 | 0.150 | 0.000 | 0.560 | 0.995 | 0.000 | 0.137 |
| musique | claude-haiku-5-5 | V2 | 200 | 0.975 | 0.927 | 0.150 | 0.010 | 0.100 | 0.990 | 5.000 | None |
| musique | claude-haiku-5-5 | V3 | 200 | 0.737 | 0.703 | 0.150 | 0.300 | 0.015 | 0.700 | 1.000 | None |
| musique | claude-haiku-5-5 | V4 | 200 | 0.894 | 0.836 | 0.150 | 0.110 | 0.055 | 0.890 | 5.000 | None |
| musique | claude-haiku-5-5 | V5 | 200 | 0.894 | 0.834 | 0.150 | 0.110 | 0.055 | 0.890 | 0.000 | None |
| musique | claude-haiku-5-5 | V6 | 200 | 0.966 | 0.905 | 0.150 | 0.010 | 0.020 | 0.990 | 1.000 | None |
| musique | claude-haiku-5-5 | V7 | 200 | 0.983 | 0.939 | 0.150 | 0.005 | 0.070 | 0.995 | 5.000 | None |
| musique | gemini-2.5-flash-lite | P2 | 200 | 0.782 | 0.456 | 0.150 | 0.035 | 0.575 | 0.955 | 62.940 | 0.045 |
| musique | gemini-2.5-flash-lite | P3 | 200 | 0.706 | 0.419 | 0.150 | 0.060 | 0.470 | 0.940 | 23.980 | 0.058 |
| musique | gemini-2.5-flash-lite | P4 | 200 | 0.782 | 0.456 | 0.150 | 0.035 | 0.575 | 0.955 | 62.940 | 0.045 |
| musique | gemini-2.5-flash-lite | P5 | 200 | 0.818 | 0.522 | 0.150 | 0.010 | 0.705 | 0.955 | 0.000 | 0.045 |
| musique | gemini-2.5-flash-lite | V2 | 200 | 0.960 | 0.819 | 0.150 | 0.005 | 0.160 | 0.995 | 5.000 | None |
| musique | gemini-2.5-flash-lite | V3 | 200 | 0.830 | 0.705 | 0.150 | 0.150 | 0.090 | 0.850 | 1.000 | None |
| musique | gemini-2.5-flash-lite | V4 | 200 | 0.898 | 0.761 | 0.150 | 0.075 | 0.140 | 0.925 | 5.000 | None |
| musique | gemini-2.5-flash-lite | V5 | 200 | 0.898 | 0.761 | 0.150 | 0.075 | 0.140 | 0.925 | 0.000 | None |
| musique | gemini-2.5-flash-lite | V6 | 200 | 0.921 | 0.798 | 0.150 | 0.050 | 0.130 | 0.950 | 1.000 | None |
| musique | gemini-2.5-flash-lite | V7 | 200 | 0.972 | 0.892 | 0.150 | 0.000 | 0.260 | 1.000 | 5.000 | None |
| musique | gemini-2.5-flash | P2 | 62 | 0.846 | 0.489 | 0.131 | 0.065 | 0.710 | 0.935 | 62.952 | 0.005 |
| musique | gemini-2.5-flash | P3 | 62 | 0.775 | 0.434 | 0.131 | 0.129 | 0.613 | 0.871 | 23.984 | 0.016 |
| musique | gemini-2.5-flash | P4 | 62 | 0.846 | 0.489 | 0.131 | 0.065 | 0.710 | 0.935 | 60.790 | 0.005 |
| musique | gemini-2.5-flash | P5 | 62 | 0.881 | 0.559 | 0.131 | 0.032 | 0.839 | 0.935 | 0.000 | 0.005 |
| musique | gemini-2.5-flash | V2 | 62 | 0.976 | 0.853 | 0.131 | 0.000 | 0.258 | 1.000 | 5.000 | None |
| musique | gemini-2.5-flash | V3 | 62 | 0.906 | 0.762 | 0.131 | 0.065 | 0.194 | 0.935 | 1.000 | None |
| musique | gemini-2.5-flash | V4 | 62 | 0.941 | 0.813 | 0.131 | 0.048 | 0.274 | 0.952 | 5.000 | None |
| musique | gemini-2.5-flash | V5 | 62 | 0.941 | 0.813 | 0.131 | 0.048 | 0.274 | 0.952 | 0.000 | None |
| musique | gemini-2.5-flash | V6 | 62 | 0.950 | 0.818 | 0.131 | 0.016 | 0.194 | 0.984 | 1.000 | None |
| musique | gemini-2.5-flash | V7 | 62 | 0.989 | 0.890 | 0.131 | 0.000 | 0.339 | 1.000 | 5.000 | None |
| musique | gpt-6-luna | P2 | 200 | 0.779 | 0.430 | 0.150 | 0.040 | 0.660 | 0.915 | 61.245 | 0.168 |
| musique | gpt-6-luna | P3 | 200 | 0.598 | 0.360 | 0.150 | 0.090 | 0.415 | 0.910 | 23.995 | 0.167 |
| musique | gpt-6-luna | P4 | 200 | 0.779 | 0.430 | 0.150 | 0.040 | 0.660 | 0.915 | 61.870 | 0.168 |
| musique | gpt-6-luna | P5 | 200 | 0.794 | 0.474 | 0.150 | 0.000 | 0.845 | 0.925 | 0.000 | 0.168 |
| musique | gpt-6-luna | V2 | 200 | 0.970 | 0.908 | 0.150 | 0.000 | 0.220 | 1.000 | 5.000 | None |
| musique | gpt-6-luna | V3 | 200 | 0.813 | 0.733 | 0.150 | 0.180 | 0.085 | 0.820 | 1.000 | None |
| musique | gpt-6-luna | V4 | 200 | 0.967 | 0.889 | 0.150 | 0.000 | 0.210 | 1.000 | 5.000 | None |
| musique | gpt-6-luna | V5 | 200 | 0.967 | 0.889 | 0.150 | 0.000 | 0.210 | 1.000 | 0.000 | None |
| musique | gpt-6-luna | V6 | 200 | 0.963 | 0.859 | 0.150 | 0.000 | 0.060 | 1.000 | 1.000 | None |
| musique | gpt-6-luna | V7 | 200 | 0.983 | 0.919 | 0.150 | 0.000 | 0.200 | 1.000 | 5.000 | None |
| musique | gpt-6.1-terra | P2 | 54 | 0.827 | 0.425 | 0.133 | 0.074 | 0.759 | 0.852 | 63.000 | 0.086 |
| musique | gpt-6.1-terra | P3 | 54 | 0.760 | 0.392 | 0.133 | 0.130 | 0.667 | 0.870 | 24.000 | 0.080 |
| musique | gpt-6.1-terra | P4 | 54 | 0.827 | 0.425 | 0.133 | 0.074 | 0.759 | 0.852 | 63.000 | 0.086 |
| musique | gpt-6.1-terra | P5 | 54 | 0.845 | 0.520 | 0.133 | 0.000 | 0.833 | 0.889 | 0.000 | 0.086 |
| musique | gpt-6.1-terra | V2 | 54 | 0.991 | 0.913 | 0.133 | 0.000 | 0.278 | 1.000 | 5.000 | None |
| musique | gpt-6.1-terra | V3 | 54 | 0.859 | 0.774 | 0.133 | 0.148 | 0.074 | 0.852 | 1.000 | None |
| musique | gpt-6.1-terra | V4 | 54 | 0.911 | 0.841 | 0.133 | 0.093 | 0.241 | 0.907 | 5.000 | None |
| musique | gpt-6.1-terra | V5 | 54 | 0.911 | 0.841 | 0.133 | 0.093 | 0.241 | 0.907 | 0.000 | None |
| musique | gpt-6.1-terra | V6 | 54 | 0.961 | 0.879 | 0.133 | 0.000 | 0.111 | 1.000 | 1.000 | None |
| musique | gpt-6.1-terra | V7 | 54 | 1.000 | 0.933 | 0.133 | 0.000 | 0.222 | 1.000 | 5.000 | None |

## Stability (repeat 1 vs 0)

## RM K-sensitivity (banzhaf, exact). k = prefix vs K_max (overlapping); halves = disjoint first vs second K/2 masks. 'argmax_agree' = tie-aware top-group Jaccard

## Projected cost of the main run (per-call cost from the pilot x formula calls x evaluable set)
| dataset | model | method | cny_per_call | calls_per_inst | cny_per_inst | n_eval | cny_total |
|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | P2 | 0.000 | 34 | 0.003 | 522 | 1.542 |
| hotpotqa | claude-haiku-5-5 | V6 | 0.000 | 1 | 0.000 | 522 | 0.065 |
| hotpotqa | claude-haiku-5-5 | P3 | 0.000 | 28 | 0.003 | 522 | 1.465 |
| hotpotqa | claude-haiku-5-5 | V7 | 0.000 | 5 | 0.001 | 522 | 0.319 |
| hotpotqa | claude-haiku-5-5 | V4 | 0.000 | 10 | 0.001 | 522 | 0.589 |
| hotpotqa | claude-haiku-5-5 | V3 | 0.000 | 2 | 0.000 | 522 | 0.119 |
| hotpotqa | claude-haiku-5-5 | P4 | 0.000 | 68 | 0.007 | 522 | 3.545 |
| hotpotqa | claude-haiku-5-5 | V2 | 0.000 | 5 | 0.000 | 522 | 0.250 |
| hotpotqa | gemini-2.5-flash-lite | P2 | 0.000 | 34 | 0.002 | 303 | 0.612 |
| hotpotqa | gemini-2.5-flash-lite | V6 | 0.000 | 1 | 0.000 | 303 | 0.028 |
| hotpotqa | gemini-2.5-flash-lite | P3 | 0.000 | 28 | 0.002 | 303 | 0.524 |
| hotpotqa | gemini-2.5-flash-lite | V7 | 0.000 | 5 | 0.000 | 303 | 0.143 |
| hotpotqa | gemini-2.5-flash-lite | V4 | 0.000 | 10 | 0.001 | 303 | 0.204 |
| hotpotqa | gemini-2.5-flash-lite | V3 | 0.000 | 2 | 0.000 | 303 | 0.041 |
| hotpotqa | gemini-2.5-flash-lite | P4 | 0.000 | 68 | 0.004 | 303 | 1.252 |
| hotpotqa | gemini-2.5-flash-lite | V2 | 0.000 | 5 | 0.000 | 303 | 0.102 |
| hotpotqa | gemini-2.5-flash | P2 | 0.000 | 34 | 0.006 | 87 | 0.522 |
| hotpotqa | gemini-2.5-flash | V6 | 0.000 | 1 | 0.000 | 87 | 0.031 |
| hotpotqa | gemini-2.5-flash | P3 | 0.000 | 28 | 0.005 | 87 | 0.435 |
| hotpotqa | gemini-2.5-flash | V7 | 0.000 | 5 | 0.002 | 87 | 0.153 |
| hotpotqa | gemini-2.5-flash | V4 | 0.000 | 10 | 0.002 | 87 | 0.172 |
| hotpotqa | gemini-2.5-flash | V3 | 0.000 | 2 | 0.000 | 87 | 0.034 |
| hotpotqa | gemini-2.5-flash | P4 | 0.000 | 68 | 0.012 | 87 | 1.049 |
| hotpotqa | gemini-2.5-flash | V2 | 0.000 | 5 | 0.001 | 87 | 0.089 |
| hotpotqa | gpt-6-luna | P2 | 0.000 | 34 | 0.005 | 178 | 0.859 |
| hotpotqa | gpt-6-luna | V6 | 0.000 | 1 | 0.000 | 178 | 0.048 |
| hotpotqa | gpt-6-luna | V7 | 0.000 | 5 | 0.002 | 178 | 0.299 |
| hotpotqa | gpt-6-luna | V4 | 0.000 | 10 | 0.001 | 178 | 0.216 |
| hotpotqa | gpt-6-luna | V3 | 0.000 | 2 | 0.000 | 178 | 0.073 |
| hotpotqa | gpt-6-luna | P4 | 0.000 | 68 | 0.018 | 178 | 3.155 |
| hotpotqa | gpt-6-luna | V2 | 0.000 | 5 | 0.001 | 178 | 0.102 |
| hotpotqa | gpt-6.1-terra | P2 | 0.001 | 34 | 0.049 | 70 | 3.456 |
| hotpotqa | gpt-6.1-terra | V6 | 0.002 | 1 | 0.002 | 70 | 0.107 |
| hotpotqa | gpt-6.1-terra | P3 | 0.001 | 28 | 0.041 | 70 | 2.840 |
| hotpotqa | gpt-6.1-terra | V7 | 0.002 | 5 | 0.008 | 70 | 0.537 |
| hotpotqa | gpt-6.1-terra | V4 | 0.001 | 10 | 0.015 | 70 | 1.036 |
| hotpotqa | gpt-6.1-terra | V3 | 0.001 | 2 | 0.003 | 70 | 0.208 |
| hotpotqa | gpt-6.1-terra | P4 | 0.001 | 68 | 0.098 | 70 | 6.881 |
| hotpotqa | gpt-6.1-terra | V2 | 0.001 | 5 | 0.007 | 70 | 0.520 |
| hotpotqa | gpt-6.1-terra | V5 | 0.001 | 10 | 0.015 | 70 | 1.024 |
| musique | claude-haiku-5-5 | P2 | 0.000 | 64 | 0.016 | 762 | 12.285 |
| musique | claude-haiku-5-5 | V6 | 0.000 | 1 | 0.000 | 762 | 0.152 |
| musique | claude-haiku-5-5 | P3 | 0.000 | 48 | 0.008 | 762 | 6.160 |
| musique | claude-haiku-5-5 | V7 | 0.000 | 5 | 0.001 | 762 | 0.751 |
| musique | claude-haiku-5-5 | V4 | 0.000 | 10 | 0.002 | 762 | 1.338 |
| musique | claude-haiku-5-5 | V3 | 0.000 | 2 | 0.000 | 762 | 0.269 |
| musique | claude-haiku-5-5 | P4 | 0.000 | 128 | 0.023 | 762 | 17.262 |
| musique | claude-haiku-5-5 | V2 | 0.000 | 5 | 0.001 | 762 | 0.729 |
| musique | gemini-2.5-flash-lite | P2 | 0.000 | 64 | 0.007 | 786 | 5.313 |
| musique | gemini-2.5-flash-lite | V6 | 0.000 | 1 | 0.000 | 786 | 0.128 |
| musique | gemini-2.5-flash-lite | P3 | 0.000 | 48 | 0.005 | 786 | 4.050 |
| musique | gemini-2.5-flash-lite | V7 | 0.000 | 5 | 0.001 | 786 | 0.642 |
| musique | gemini-2.5-flash-lite | V4 | 0.000 | 10 | 0.001 | 786 | 0.887 |
| musique | gemini-2.5-flash-lite | V3 | 0.000 | 2 | 0.000 | 786 | 0.178 |
| musique | gemini-2.5-flash-lite | P4 | 0.000 | 128 | 0.014 | 786 | 10.734 |
| musique | gemini-2.5-flash-lite | V2 | 0.000 | 5 | 0.001 | 786 | 0.446 |
| musique | gemini-2.5-flash | P2 | 0.000 | 64 | 0.020 | 68 | 1.337 |
| musique | gemini-2.5-flash | V6 | 0.001 | 1 | 0.001 | 68 | 0.037 |
| musique | gemini-2.5-flash | P3 | 0.000 | 48 | 0.015 | 68 | 1.015 |
| musique | gemini-2.5-flash | V7 | 0.001 | 5 | 0.003 | 68 | 0.183 |
| musique | gemini-2.5-flash | V4 | 0.000 | 10 | 0.003 | 68 | 0.223 |
| musique | gemini-2.5-flash | V3 | 0.000 | 2 | 0.001 | 68 | 0.045 |
| musique | gemini-2.5-flash | P4 | 0.000 | 128 | 0.047 | 68 | 3.169 |
| musique | gemini-2.5-flash | V2 | 0.000 | 5 | 0.002 | 68 | 0.114 |
| musique | gpt-6-luna | P2 | 0.000 | 64 | 0.016 | 614 | 9.960 |
| musique | gpt-6-luna | V6 | 0.000 | 1 | 0.000 | 614 | 0.156 |
| musique | gpt-6-luna | P3 | 0.000 | 48 | 0.013 | 614 | 8.232 |
| musique | gpt-6-luna | V7 | 0.000 | 5 | 0.001 | 614 | 0.800 |
| musique | gpt-6-luna | V4 | 0.000 | 10 | 0.002 | 614 | 1.487 |
| musique | gpt-6-luna | V3 | 0.000 | 2 | 0.001 | 614 | 0.321 |
| musique | gpt-6-luna | P4 | 0.000 | 128 | 0.036 | 614 | 22.165 |
| musique | gpt-6-luna | V2 | 0.000 | 5 | 0.001 | 614 | 0.815 |
| musique | gpt-6.1-terra | P2 | 0.002 | 64 | 0.111 | 60 | 6.660 |
| musique | gpt-6.1-terra | V6 | 0.002 | 1 | 0.002 | 60 | 0.112 |
| musique | gpt-6.1-terra | P3 | 0.002 | 48 | 0.083 | 60 | 4.969 |
| musique | gpt-6.1-terra | V7 | 0.002 | 5 | 0.009 | 60 | 0.559 |
| musique | gpt-6.1-terra | V4 | 0.002 | 10 | 0.017 | 60 | 1.048 |
| musique | gpt-6.1-terra | V3 | 0.002 | 2 | 0.004 | 60 | 0.210 |
| musique | gpt-6.1-terra | P4 | 0.002 | 128 | 0.220 | 60 | 13.225 |
| musique | gpt-6.1-terra | V2 | 0.002 | 5 | 0.009 | 60 | 0.539 |

## Cost
| dataset | model | method | n | cost_cny | cny_per_inst | calls_issued | truncated |
|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | P2 | 200 | 0.574 | 0.003 | 6600 | 0 |
| hotpotqa | claude-haiku-5-5 | V6 | 200 | 0.025 | 0.000 | 200 | 0 |
| hotpotqa | claude-haiku-5-5 | P3 | 200 | 0.281 | 0.001 | 2800 | 0 |
| hotpotqa | claude-haiku-5-5 | P5 | 200 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | claude-haiku-5-5 | V7 | 200 | 0.122 | 0.001 | 1000 | 0 |
| hotpotqa | claude-haiku-5-5 | V4 | 200 | 0.113 | 0.001 | 1000 | 0 |
| hotpotqa | claude-haiku-5-5 | V3 | 200 | 0.023 | 0.000 | 200 | 0 |
| hotpotqa | claude-haiku-5-5 | P4 | 200 | 0.659 | 0.003 | 6600 | 0 |
| hotpotqa | claude-haiku-5-5 | V2 | 200 | 0.096 | 0.000 | 1000 | 0 |
| hotpotqa | claude-haiku-5-5 | V5 | 200 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P2 | 200 | 0.392 | 0.002 | 6600 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V6 | 200 | 0.019 | 0.000 | 200 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P3 | 200 | 0.173 | 0.001 | 2800 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P5 | 200 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V7 | 200 | 0.095 | 0.000 | 1000 | 4 |
| hotpotqa | gemini-2.5-flash-lite | V4 | 200 | 0.067 | 0.000 | 1000 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V3 | 200 | 0.013 | 0.000 | 200 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P4 | 200 | 0.401 | 0.002 | 6600 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V2 | 200 | 0.067 | 0.000 | 1000 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V5 | 200 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | P2 | 81 | 0.471 | 0.006 | 2673 | 0 |
| hotpotqa | gemini-2.5-flash | V6 | 81 | 0.029 | 0.000 | 81 | 0 |
| hotpotqa | gemini-2.5-flash | P3 | 81 | 0.203 | 0.003 | 1134 | 0 |
| hotpotqa | gemini-2.5-flash | P5 | 81 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | V7 | 81 | 0.143 | 0.002 | 405 | 0 |
| hotpotqa | gemini-2.5-flash | V4 | 81 | 0.080 | 0.001 | 405 | 0 |
| hotpotqa | gemini-2.5-flash | V3 | 81 | 0.016 | 0.000 | 81 | 0 |
| hotpotqa | gemini-2.5-flash | P4 | 81 | 0.474 | 0.006 | 2673 | 0 |
| hotpotqa | gemini-2.5-flash | V2 | 81 | 0.083 | 0.001 | 405 | 0 |
| hotpotqa | gemini-2.5-flash | V5 | 81 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6-luna | P2 | 68 | 0.305 | 0.004 | 2147 | 0 |
| hotpotqa | gpt-6-luna | V6 | 166 | 0.045 | 0.000 | 166 | 0 |
| hotpotqa | gpt-6-luna | P5 | 166 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6-luna | V7 | 166 | 0.279 | 0.002 | 830 | 0 |
| hotpotqa | gpt-6-luna | V4 | 51 | 0.030 | 0.001 | 246 | 0 |
| hotpotqa | gpt-6-luna | V3 | 166 | 0.034 | 0.000 | 166 | 0 |
| hotpotqa | gpt-6-luna | P4 | 166 | 2.931 | 0.018 | 11246 | 0 |
| hotpotqa | gpt-6-luna | V2 | 166 | 0.095 | 0.001 | 830 | 0 |
| hotpotqa | gpt-6-luna | V5 | 166 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6.1-terra | P2 | 47 | 2.099 | 0.045 | 1446 | 0 |
| hotpotqa | gpt-6.1-terra | V6 | 64 | 0.098 | 0.002 | 64 | 0 |
| hotpotqa | gpt-6.1-terra | P3 | 64 | 1.988 | 0.031 | 1372 | 0 |
| hotpotqa | gpt-6.1-terra | P5 | 64 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6.1-terra | V7 | 64 | 0.491 | 0.008 | 320 | 0 |
| hotpotqa | gpt-6.1-terra | V4 | 64 | 0.518 | 0.008 | 350 | 0 |
| hotpotqa | gpt-6.1-terra | V3 | 64 | 0.095 | 0.001 | 64 | 0 |
| hotpotqa | gpt-6.1-terra | P4 | 64 | 6.106 | 0.095 | 4224 | 0 |
| hotpotqa | gpt-6.1-terra | V2 | 64 | 0.371 | 0.006 | 250 | 0 |
| hotpotqa | gpt-6.1-terra | V5 | 64 | 0.058 | 0.001 | 40 | 0 |
| musique | claude-haiku-5-5 | P2 | 6 | 0.017 | 0.003 | 68 | 0 |
| musique | claude-haiku-5-5 | V6 | 200 | 0.040 | 0.000 | 200 | 0 |
| musique | claude-haiku-5-5 | P3 | 200 | 0.807 | 0.004 | 4792 | 0 |
| musique | claude-haiku-5-5 | P5 | 200 | 0.000 | 0.000 | 0 | 0 |
| musique | claude-haiku-5-5 | V7 | 200 | 0.197 | 0.001 | 1000 | 0 |
| musique | claude-haiku-5-5 | V4 | 200 | 0.176 | 0.001 | 1000 | 0 |
| musique | claude-haiku-5-5 | V3 | 200 | 0.035 | 0.000 | 200 | 0 |
| musique | claude-haiku-5-5 | P4 | 113 | 1.191 | 0.011 | 6731 | 0 |
| musique | claude-haiku-5-5 | V2 | 200 | 0.191 | 0.001 | 1000 | 2 |
| musique | claude-haiku-5-5 | V5 | 200 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash-lite | P2 | 200 | 1.329 | 0.007 | 12588 | 0 |
| musique | gemini-2.5-flash-lite | V6 | 200 | 0.033 | 0.000 | 200 | 10 |
| musique | gemini-2.5-flash-lite | P3 | 200 | 0.515 | 0.003 | 4796 | 0 |
| musique | gemini-2.5-flash-lite | P5 | 200 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash-lite | V7 | 200 | 0.163 | 0.001 | 1000 | 35 |
| musique | gemini-2.5-flash-lite | V4 | 200 | 0.113 | 0.001 | 1000 | 0 |
| musique | gemini-2.5-flash-lite | V3 | 200 | 0.023 | 0.000 | 200 | 0 |
| musique | gemini-2.5-flash-lite | P4 | 200 | 1.343 | 0.007 | 12588 | 0 |
| musique | gemini-2.5-flash-lite | V2 | 200 | 0.113 | 0.001 | 1000 | 0 |
| musique | gemini-2.5-flash-lite | V5 | 200 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | P2 | 62 | 1.199 | 0.019 | 3903 | 0 |
| musique | gemini-2.5-flash | V6 | 62 | 0.033 | 0.001 | 62 | 0 |
| musique | gemini-2.5-flash | P3 | 62 | 0.462 | 0.007 | 1487 | 0 |
| musique | gemini-2.5-flash | P5 | 62 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | V7 | 62 | 0.167 | 0.003 | 310 | 3 |
| musique | gemini-2.5-flash | V4 | 62 | 0.101 | 0.002 | 310 | 0 |
| musique | gemini-2.5-flash | V3 | 62 | 0.020 | 0.000 | 62 | 0 |
| musique | gemini-2.5-flash | P4 | 5 | 0.066 | 0.013 | 181 | 0 |
| musique | gemini-2.5-flash | V2 | 62 | 0.104 | 0.002 | 310 | 0 |
| musique | gemini-2.5-flash | V5 | 62 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6-luna | P2 | 200 | 3.193 | 0.016 | 12597 | 0 |
| musique | gpt-6-luna | V6 | 200 | 0.051 | 0.000 | 200 | 0 |
| musique | gpt-6-luna | P3 | 200 | 1.340 | 0.007 | 4799 | 0 |
| musique | gpt-6-luna | P5 | 200 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6-luna | V7 | 200 | 0.260 | 0.001 | 1000 | 0 |
| musique | gpt-6-luna | V4 | 200 | 0.242 | 0.001 | 1000 | 0 |
| musique | gpt-6-luna | V3 | 200 | 0.052 | 0.000 | 200 | 0 |
| musique | gpt-6-luna | P4 | 47 | 0.772 | 0.016 | 2738 | 0 |
| musique | gpt-6-luna | V2 | 200 | 0.266 | 0.001 | 1000 | 0 |
| musique | gpt-6-luna | V5 | 200 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | P2 | 54 | 5.900 | 0.109 | 3402 | 0 |
| musique | gpt-6.1-terra | V6 | 54 | 0.100 | 0.002 | 54 | 0 |
| musique | gpt-6.1-terra | P3 | 54 | 2.236 | 0.041 | 1296 | 0 |
| musique | gpt-6.1-terra | P5 | 54 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | V7 | 54 | 0.503 | 0.009 | 270 | 0 |
| musique | gpt-6.1-terra | V4 | 54 | 0.472 | 0.009 | 270 | 0 |
| musique | gpt-6.1-terra | V3 | 54 | 0.095 | 0.002 | 54 | 0 |
| musique | gpt-6.1-terra | P4 | 54 | 5.858 | 0.108 | 3402 | 0 |
| musique | gpt-6.1-terra | V2 | 54 | 0.485 | 0.009 | 270 | 0 |
| musique | gpt-6.1-terra | V5 | 54 | 0.000 | 0.000 | 0 | 0 |
