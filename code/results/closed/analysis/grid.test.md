# Phase-2 grid.test analysis

## Methods
| dataset | model | method | n | top1 | rec@g | random_top1 | all_zero | unique_max | reaches_tau | calls/inst | full_ctx_change |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | P2 | 510 | 0.873 | 0.649 | 0.200 | 0.090 | 0.645 | 0.873 | 19.880 | 0.052 |
| hotpotqa | claude-haiku-5-5 | P3 | 510 | 0.737 | 0.544 | 0.200 | 0.200 | 0.441 | 0.800 | 8.510 | 0.069 |
| hotpotqa | claude-haiku-5-5 | P4 | 510 | 0.873 | 0.649 | 0.200 | 0.090 | 0.645 | 0.873 | 20.059 | 0.052 |
| hotpotqa | claude-haiku-5-5 | P5 | 510 | 0.932 | 0.767 | 0.200 | 0.027 | 0.841 | 0.894 | 0.000 | 0.052 |
| hotpotqa | claude-haiku-5-5 | V2 | 510 | 0.977 | 0.941 | 0.200 | 0.002 | 0.175 | 0.998 | 3.039 | None |
| hotpotqa | claude-haiku-5-5 | V3 | 510 | 0.903 | 0.861 | 0.200 | 0.096 | 0.096 | 0.904 | 0.608 | None |
| hotpotqa | claude-haiku-5-5 | V4 | 510 | 0.966 | 0.928 | 0.200 | 0.012 | 0.151 | 0.988 | 3.039 | None |
| hotpotqa | claude-haiku-5-5 | V5 | 510 | 0.966 | 0.928 | 0.200 | 0.012 | 0.151 | 0.988 | 0.000 | None |
| hotpotqa | claude-haiku-5-5 | V6 | 510 | 0.970 | 0.929 | 0.200 | 0.000 | 0.096 | 1.000 | 0.608 | None |
| hotpotqa | claude-haiku-5-5 | V7 | 510 | 0.981 | 0.955 | 0.200 | 0.000 | 0.157 | 1.000 | 3.039 | None |
| hotpotqa | gemini-2.5-flash-lite | P2 | 291 | 0.790 | 0.519 | 0.201 | 0.158 | 0.636 | 0.814 | 10.258 | 0.038 |
| hotpotqa | gemini-2.5-flash-lite | P3 | 291 | 0.719 | 0.474 | 0.201 | 0.213 | 0.560 | 0.787 | 4.357 | 0.037 |
| hotpotqa | gemini-2.5-flash-lite | P4 | 291 | 0.790 | 0.519 | 0.201 | 0.158 | 0.636 | 0.814 | 10.258 | 0.038 |
| hotpotqa | gemini-2.5-flash-lite | P5 | 291 | 0.861 | 0.617 | 0.201 | 0.082 | 0.794 | 0.835 | 0.000 | 0.038 |
| hotpotqa | gemini-2.5-flash-lite | V2 | 291 | 0.971 | 0.876 | 0.201 | 0.000 | 0.323 | 1.000 | 1.564 | None |
| hotpotqa | gemini-2.5-flash-lite | V3 | 291 | 0.955 | 0.836 | 0.201 | 0.010 | 0.278 | 0.990 | 0.313 | None |
| hotpotqa | gemini-2.5-flash-lite | V4 | 291 | 0.969 | 0.875 | 0.201 | 0.003 | 0.323 | 0.997 | 1.564 | None |
| hotpotqa | gemini-2.5-flash-lite | V5 | 291 | 0.969 | 0.875 | 0.201 | 0.003 | 0.323 | 0.997 | 0.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V6 | 291 | 0.958 | 0.878 | 0.201 | 0.007 | 0.186 | 0.993 | 0.313 | None |
| hotpotqa | gemini-2.5-flash-lite | V7 | 291 | 0.969 | 0.916 | 0.201 | 0.003 | 0.313 | 0.997 | 1.564 | None |
| hotpotqa | gemini-2.5-flash | P2 | 81 | 0.732 | 0.479 | 0.200 | 0.259 | 0.605 | 0.716 | 0.000 | 0.037 |
| hotpotqa | gemini-2.5-flash | P3 | 81 | 0.683 | 0.452 | 0.200 | 0.309 | 0.519 | 0.691 | 0.000 | 0.041 |
| hotpotqa | gemini-2.5-flash | P4 | 81 | 0.732 | 0.479 | 0.200 | 0.259 | 0.605 | 0.716 | 0.000 | 0.037 |
| hotpotqa | gemini-2.5-flash | P5 | 81 | 0.869 | 0.599 | 0.200 | 0.099 | 0.815 | 0.716 | 0.000 | 0.037 |
| hotpotqa | gemini-2.5-flash | V2 | 81 | 0.990 | 0.880 | 0.200 | 0.000 | 0.358 | 1.000 | 0.000 | None |
| hotpotqa | gemini-2.5-flash | V3 | 81 | 0.986 | 0.859 | 0.200 | 0.000 | 0.284 | 1.000 | 0.000 | None |
| hotpotqa | gemini-2.5-flash | V4 | 81 | 0.970 | 0.871 | 0.200 | 0.025 | 0.333 | 0.975 | 0.000 | None |
| hotpotqa | gemini-2.5-flash | V5 | 81 | 0.970 | 0.871 | 0.200 | 0.025 | 0.333 | 0.975 | 0.000 | None |
| hotpotqa | gemini-2.5-flash | V6 | 81 | 0.996 | 0.903 | 0.200 | 0.000 | 0.210 | 1.000 | 0.000 | None |
| hotpotqa | gemini-2.5-flash | V7 | 81 | 1.000 | 0.941 | 0.200 | 0.000 | 0.333 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6-luna | P2 | 166 | 0.705 | 0.455 | 0.202 | 0.247 | 0.620 | 0.693 | 0.000 | 0.120 |
| hotpotqa | gpt-6-luna | P3 | 166 | 0.570 | 0.383 | 0.202 | 0.367 | 0.428 | 0.633 | 12.904 | 0.086 |
| hotpotqa | gpt-6-luna | P4 | 166 | 0.759 | 0.481 | 0.202 | 0.187 | 0.657 | 0.759 | 0.000 | 0.114 |
| hotpotqa | gpt-6-luna | P5 | 166 | 0.841 | 0.575 | 0.202 | 0.108 | 0.813 | 0.771 | 0.000 | 0.114 |
| hotpotqa | gpt-6-luna | V2 | 166 | 0.980 | 0.923 | 0.202 | 0.000 | 0.373 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6-luna | V3 | 166 | 0.961 | 0.860 | 0.202 | 0.024 | 0.235 | 0.976 | 0.000 | None |
| hotpotqa | gpt-6-luna | V4 | 166 | 0.977 | 0.916 | 0.202 | 0.000 | 0.373 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6-luna | V5 | 166 | 0.977 | 0.916 | 0.202 | 0.000 | 0.373 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6-luna | V6 | 166 | 0.963 | 0.874 | 0.202 | 0.000 | 0.217 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6-luna | V7 | 166 | 0.969 | 0.920 | 0.202 | 0.000 | 0.367 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6.1-terra | P2 | 64 | 0.664 | 0.420 | 0.200 | 0.359 | 0.547 | 0.562 | 0.000 | 0.036 |
| hotpotqa | gpt-6.1-terra | P3 | 64 | 0.596 | 0.388 | 0.200 | 0.453 | 0.469 | 0.547 | 0.000 | 0.021 |
| hotpotqa | gpt-6.1-terra | P4 | 64 | 0.652 | 0.409 | 0.200 | 0.406 | 0.578 | 0.484 | 0.000 | 0.010 |
| hotpotqa | gpt-6.1-terra | P5 | 64 | 0.852 | 0.611 | 0.200 | 0.141 | 0.828 | 0.547 | 0.000 | 0.010 |
| hotpotqa | gpt-6.1-terra | V2 | 64 | 0.992 | 0.921 | 0.200 | 0.000 | 0.250 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6.1-terra | V3 | 64 | 0.982 | 0.927 | 0.200 | 0.016 | 0.125 | 0.984 | 0.000 | None |
| hotpotqa | gpt-6.1-terra | V4 | 64 | 0.992 | 0.922 | 0.200 | 0.000 | 0.234 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6.1-terra | V5 | 64 | 0.992 | 0.922 | 0.200 | 0.000 | 0.234 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6.1-terra | V6 | 64 | 0.992 | 0.916 | 0.200 | 0.000 | 0.172 | 1.000 | 0.000 | None |
| hotpotqa | gpt-6.1-terra | V7 | 64 | 0.992 | 0.951 | 0.200 | 0.000 | 0.203 | 1.000 | 0.000 | None |
| musique | claude-haiku-5-5 | P2 | 750 | 0.753 | 0.590 | 0.133 | 0.013 | 0.272 | 0.983 | 45.668 | 0.251 |
| musique | claude-haiku-5-5 | P3 | 750 | 0.732 | 0.550 | 0.133 | 0.036 | 0.285 | 0.964 | 17.497 | 0.126 |
| musique | claude-haiku-5-5 | P4 | 750 | 0.753 | 0.590 | 0.133 | 0.013 | 0.272 | 0.983 | 46.527 | 0.251 |
| musique | claude-haiku-5-5 | P5 | 750 | 0.731 | 0.609 | 0.133 | 0.007 | 0.565 | 0.985 | 0.000 | 0.251 |
| musique | claude-haiku-5-5 | V2 | 750 | 0.972 | 0.926 | 0.133 | 0.004 | 0.120 | 0.996 | 3.653 | None |
| musique | claude-haiku-5-5 | V3 | 750 | 0.764 | 0.731 | 0.133 | 0.249 | 0.036 | 0.751 | 0.733 | None |
| musique | claude-haiku-5-5 | V4 | 750 | 0.917 | 0.870 | 0.133 | 0.067 | 0.081 | 0.933 | 3.633 | None |
| musique | claude-haiku-5-5 | V5 | 750 | 0.917 | 0.870 | 0.133 | 0.067 | 0.083 | 0.933 | 0.000 | None |
| musique | claude-haiku-5-5 | V6 | 750 | 0.951 | 0.896 | 0.133 | 0.009 | 0.047 | 0.991 | 0.733 | None |
| musique | claude-haiku-5-5 | V7 | 750 | 0.973 | 0.929 | 0.133 | 0.001 | 0.129 | 0.999 | 3.667 | None |
| musique | gemini-2.5-flash-lite | P2 | 774 | 0.802 | 0.488 | 0.137 | 0.035 | 0.575 | 0.955 | 46.694 | 0.055 |
| musique | gemini-2.5-flash-lite | P3 | 774 | 0.718 | 0.438 | 0.137 | 0.071 | 0.487 | 0.929 | 17.650 | 0.053 |
| musique | gemini-2.5-flash-lite | P4 | 774 | 0.802 | 0.488 | 0.137 | 0.035 | 0.575 | 0.955 | 46.694 | 0.055 |
| musique | gemini-2.5-flash-lite | P5 | 774 | 0.847 | 0.552 | 0.137 | 0.017 | 0.749 | 0.956 | 0.000 | 0.055 |
| musique | gemini-2.5-flash-lite | V2 | 774 | 0.954 | 0.832 | 0.137 | 0.001 | 0.222 | 0.999 | 3.708 | None |
| musique | gemini-2.5-flash-lite | V3 | 774 | 0.840 | 0.722 | 0.137 | 0.138 | 0.118 | 0.862 | 0.742 | None |
| musique | gemini-2.5-flash-lite | V4 | 774 | 0.891 | 0.772 | 0.137 | 0.085 | 0.189 | 0.915 | 3.708 | None |
| musique | gemini-2.5-flash-lite | V5 | 774 | 0.891 | 0.772 | 0.137 | 0.085 | 0.189 | 0.915 | 0.000 | None |
| musique | gemini-2.5-flash-lite | V6 | 774 | 0.928 | 0.810 | 0.137 | 0.035 | 0.150 | 0.965 | 0.742 | None |
| musique | gemini-2.5-flash-lite | V7 | 774 | 0.974 | 0.898 | 0.137 | 0.003 | 0.305 | 0.997 | 3.708 | None |
| musique | gemini-2.5-flash | P2 | 62 | 0.846 | 0.489 | 0.131 | 0.065 | 0.710 | 0.935 | 0.000 | 0.005 |
| musique | gemini-2.5-flash | P3 | 62 | 0.775 | 0.434 | 0.131 | 0.129 | 0.613 | 0.871 | 0.000 | 0.016 |
| musique | gemini-2.5-flash | P4 | 62 | 0.846 | 0.489 | 0.131 | 0.065 | 0.710 | 0.935 | 0.000 | 0.005 |
| musique | gemini-2.5-flash | P5 | 62 | 0.881 | 0.559 | 0.131 | 0.032 | 0.839 | 0.935 | 0.000 | 0.005 |
| musique | gemini-2.5-flash | V2 | 62 | 0.976 | 0.853 | 0.131 | 0.000 | 0.258 | 1.000 | 0.000 | None |
| musique | gemini-2.5-flash | V3 | 62 | 0.906 | 0.762 | 0.131 | 0.065 | 0.194 | 0.935 | 0.000 | None |
| musique | gemini-2.5-flash | V4 | 62 | 0.941 | 0.813 | 0.131 | 0.048 | 0.274 | 0.952 | 0.000 | None |
| musique | gemini-2.5-flash | V5 | 62 | 0.941 | 0.813 | 0.131 | 0.048 | 0.274 | 0.952 | 0.000 | None |
| musique | gemini-2.5-flash | V6 | 62 | 0.950 | 0.818 | 0.131 | 0.016 | 0.194 | 0.984 | 0.000 | None |
| musique | gemini-2.5-flash | V7 | 62 | 0.989 | 0.890 | 0.131 | 0.000 | 0.339 | 1.000 | 0.000 | None |
| musique | gpt-6-luna | P2 | 602 | 0.764 | 0.439 | 0.138 | 0.040 | 0.654 | 0.917 | 41.654 | 0.185 |
| musique | gpt-6-luna | P3 | 602 | 0.596 | 0.369 | 0.138 | 0.075 | 0.412 | 0.925 | 16.015 | 0.136 |
| musique | gpt-6-luna | P4 | 602 | 0.764 | 0.439 | 0.138 | 0.040 | 0.654 | 0.917 | 41.453 | 0.185 |
| musique | gpt-6-luna | P5 | 602 | 0.780 | 0.484 | 0.138 | 0.005 | 0.797 | 0.924 | 0.000 | 0.185 |
| musique | gpt-6-luna | V2 | 602 | 0.976 | 0.917 | 0.138 | 0.000 | 0.224 | 1.000 | 3.339 | None |
| musique | gpt-6-luna | V3 | 602 | 0.813 | 0.730 | 0.138 | 0.178 | 0.095 | 0.822 | 1.000 | None |
| musique | gpt-6-luna | V4 | 602 | 0.967 | 0.899 | 0.138 | 0.007 | 0.206 | 0.993 | 3.339 | None |
| musique | gpt-6-luna | V5 | 602 | 0.967 | 0.899 | 0.138 | 0.007 | 0.206 | 0.993 | 0.000 | None |
| musique | gpt-6-luna | V6 | 602 | 0.955 | 0.866 | 0.138 | 0.003 | 0.065 | 0.997 | 1.000 | None |
| musique | gpt-6-luna | V7 | 602 | 0.978 | 0.924 | 0.138 | 0.000 | 0.189 | 1.000 | 5.000 | None |
| musique | gpt-6.1-terra | P2 | 54 | 0.827 | 0.425 | 0.133 | 0.074 | 0.759 | 0.852 | 0.000 | 0.086 |
| musique | gpt-6.1-terra | P3 | 54 | 0.760 | 0.392 | 0.133 | 0.130 | 0.667 | 0.870 | 0.000 | 0.080 |
| musique | gpt-6.1-terra | P4 | 54 | 0.827 | 0.425 | 0.133 | 0.074 | 0.759 | 0.852 | 0.000 | 0.086 |
| musique | gpt-6.1-terra | P5 | 54 | 0.845 | 0.520 | 0.133 | 0.000 | 0.833 | 0.889 | 0.000 | 0.086 |
| musique | gpt-6.1-terra | V2 | 54 | 0.991 | 0.913 | 0.133 | 0.000 | 0.278 | 1.000 | 0.000 | None |
| musique | gpt-6.1-terra | V3 | 54 | 0.859 | 0.774 | 0.133 | 0.148 | 0.074 | 0.852 | 0.000 | None |
| musique | gpt-6.1-terra | V4 | 54 | 0.911 | 0.841 | 0.133 | 0.093 | 0.241 | 0.907 | 0.000 | None |
| musique | gpt-6.1-terra | V5 | 54 | 0.911 | 0.841 | 0.133 | 0.093 | 0.241 | 0.907 | 0.000 | None |
| musique | gpt-6.1-terra | V6 | 54 | 0.961 | 0.879 | 0.133 | 0.000 | 0.111 | 1.000 | 0.000 | None |
| musique | gpt-6.1-terra | V7 | 54 | 1.000 | 0.933 | 0.133 | 0.000 | 0.222 | 1.000 | 0.000 | None |

## Stability (repeat 1 vs 0)

## RM K-sensitivity (banzhaf, exact). k = prefix vs K_max (overlapping); halves = disjoint first vs second K/2 masks. 'argmax_agree' = tie-aware top-group Jaccard

## Projected cost of the main run (per-call cost from the pilot x formula calls x evaluable set)
| dataset | model | method | cny_per_call | calls_per_inst | cny_per_inst | n_eval | cny_total |
|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | P2 | 0.000 | 34 | 0.003 | 522 | 1.573 |
| hotpotqa | claude-haiku-5-5 | V6 | 0.000 | 1 | 0.000 | 522 | 0.064 |
| hotpotqa | claude-haiku-5-5 | P3 | 0.000 | 28 | 0.003 | 522 | 1.466 |
| hotpotqa | claude-haiku-5-5 | V7 | 0.000 | 5 | 0.001 | 522 | 0.320 |
| hotpotqa | claude-haiku-5-5 | V4 | 0.000 | 10 | 0.001 | 522 | 0.593 |
| hotpotqa | claude-haiku-5-5 | V3 | 0.000 | 2 | 0.000 | 522 | 0.120 |
| hotpotqa | claude-haiku-5-5 | P4 | 0.000 | 68 | 0.007 | 522 | 3.536 |
| hotpotqa | claude-haiku-5-5 | V2 | 0.000 | 5 | 0.000 | 522 | 0.247 |
| hotpotqa | gemini-2.5-flash-lite | P2 | 0.000 | 34 | 0.002 | 303 | 0.610 |
| hotpotqa | gemini-2.5-flash-lite | V6 | 0.000 | 1 | 0.000 | 303 | 0.029 |
| hotpotqa | gemini-2.5-flash-lite | P3 | 0.000 | 28 | 0.002 | 303 | 0.522 |
| hotpotqa | gemini-2.5-flash-lite | V7 | 0.000 | 5 | 0.000 | 303 | 0.144 |
| hotpotqa | gemini-2.5-flash-lite | V4 | 0.000 | 10 | 0.001 | 303 | 0.202 |
| hotpotqa | gemini-2.5-flash-lite | V3 | 0.000 | 2 | 0.000 | 303 | 0.041 |
| hotpotqa | gemini-2.5-flash-lite | P4 | 0.000 | 68 | 0.004 | 303 | 1.245 |
| hotpotqa | gemini-2.5-flash-lite | V2 | 0.000 | 5 | 0.000 | 303 | 0.101 |
| hotpotqa | gpt-6-luna | P3 | 0.000 | 28 | 0.003 | 178 | 0.587 |
| hotpotqa | gpt-6-luna | P4 | 0.000 | 68 | 0.016 | 178 | 2.792 |
| hotpotqa | gpt-6.1-terra | P3 | 0.001 | 28 | 0.040 | 70 | 2.793 |
| hotpotqa | gpt-6.1-terra | P4 | 0.001 | 68 | 0.097 | 70 | 6.771 |
| musique | claude-haiku-5-5 | P2 | 0.000 | 64 | 0.005 | 762 | 3.467 |
| musique | claude-haiku-5-5 | V6 | 0.000 | 1 | 0.000 | 762 | 0.081 |
| musique | claude-haiku-5-5 | P3 | 0.000 | 48 | 0.003 | 762 | 2.401 |
| musique | claude-haiku-5-5 | V7 | 0.000 | 5 | 0.001 | 762 | 0.405 |
| musique | claude-haiku-5-5 | V4 | 0.000 | 10 | 0.001 | 762 | 1.035 |
| musique | claude-haiku-5-5 | V3 | 0.000 | 2 | 0.000 | 762 | 0.286 |
| musique | claude-haiku-5-5 | P4 | 0.000 | 128 | 0.014 | 762 | 10.944 |
| musique | claude-haiku-5-5 | V2 | 0.000 | 5 | 0.001 | 762 | 0.783 |
| musique | gemini-2.5-flash-lite | P2 | 0.000 | 64 | 0.007 | 786 | 5.284 |
| musique | gemini-2.5-flash-lite | V6 | 0.000 | 1 | 0.000 | 786 | 0.124 |
| musique | gemini-2.5-flash-lite | P3 | 0.000 | 48 | 0.005 | 786 | 4.077 |
| musique | gemini-2.5-flash-lite | V7 | 0.000 | 5 | 0.001 | 786 | 0.619 |
| musique | gemini-2.5-flash-lite | V4 | 0.000 | 10 | 0.001 | 786 | 0.885 |
| musique | gemini-2.5-flash-lite | V3 | 0.000 | 2 | 0.000 | 786 | 0.177 |
| musique | gemini-2.5-flash-lite | P4 | 0.000 | 128 | 0.014 | 786 | 10.699 |
| musique | gemini-2.5-flash-lite | V2 | 0.000 | 5 | 0.001 | 786 | 0.444 |
| musique | gpt-6-luna | P2 | 0.000 | 64 | 0.018 | 614 | 11.168 |
| musique | gpt-6-luna | V6 | 0.000 | 1 | 0.000 | 614 | 0.222 |
| musique | gpt-6-luna | P3 | 0.000 | 48 | 0.013 | 614 | 7.974 |
| musique | gpt-6-luna | V7 | 0.000 | 5 | 0.002 | 614 | 1.385 |
| musique | gpt-6-luna | V4 | 0.000 | 10 | 0.003 | 614 | 1.590 |
| musique | gpt-6-luna | V3 | 0.000 | 2 | 0.000 | 614 | 0.072 |
| musique | gpt-6-luna | P4 | 0.000 | 128 | 0.036 | 614 | 22.016 |
| musique | gpt-6-luna | V2 | 0.000 | 5 | 0.001 | 614 | 0.844 |

## Cost
| dataset | model | method | n | cost_cny | cny_per_inst | calls_issued | truncated |
|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | P2 | 217 | 0.404 | 0.002 | 4562 | 0 |
| hotpotqa | claude-haiku-5-5 | V6 | 522 | 0.038 | 0.000 | 310 | 0 |
| hotpotqa | claude-haiku-5-5 | P3 | 522 | 0.435 | 0.001 | 4340 | 0 |
| hotpotqa | claude-haiku-5-5 | P5 | 522 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | claude-haiku-5-5 | V7 | 522 | 0.190 | 0.000 | 1550 | 0 |
| hotpotqa | claude-haiku-5-5 | V4 | 522 | 0.176 | 0.000 | 1550 | 0 |
| hotpotqa | claude-haiku-5-5 | V3 | 522 | 0.036 | 0.000 | 310 | 0 |
| hotpotqa | claude-haiku-5-5 | P4 | 522 | 1.019 | 0.002 | 10230 | 0 |
| hotpotqa | claude-haiku-5-5 | V2 | 522 | 0.147 | 0.000 | 1550 | 0 |
| hotpotqa | claude-haiku-5-5 | V5 | 522 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P2 | 303 | 0.177 | 0.001 | 2985 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V6 | 303 | 0.009 | 0.000 | 91 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P3 | 303 | 0.078 | 0.000 | 1268 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P5 | 303 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V7 | 303 | 0.043 | 0.000 | 455 | 1 |
| hotpotqa | gemini-2.5-flash-lite | V4 | 303 | 0.030 | 0.000 | 455 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V3 | 303 | 0.006 | 0.000 | 91 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P4 | 303 | 0.180 | 0.001 | 2985 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V2 | 303 | 0.030 | 0.000 | 455 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V5 | 303 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | P2 | 87 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | V6 | 87 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | P3 | 87 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | P5 | 87 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | V7 | 87 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | V4 | 87 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | V3 | 87 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | P4 | 87 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | V2 | 87 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gemini-2.5-flash | V5 | 87 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6-luna | P2 | 178 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6-luna | V6 | 178 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6-luna | P3 | 59 | 0.087 | 0.001 | 737 | 0 |
| hotpotqa | gpt-6-luna | P5 | 178 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6-luna | V7 | 178 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6-luna | V4 | 178 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6-luna | V3 | 178 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6-luna | P4 | 17 | 0.188 | 0.011 | 814 | 0 |
| hotpotqa | gpt-6-luna | V2 | 178 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6-luna | V5 | 178 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6.1-terra | P2 | 70 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6.1-terra | V6 | 70 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6.1-terra | P3 | 70 | 0.239 | 0.003 | 168 | 0 |
| hotpotqa | gpt-6.1-terra | P5 | 70 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6.1-terra | V7 | 70 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6.1-terra | V4 | 70 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6.1-terra | V3 | 70 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6.1-terra | P4 | 70 | 0.563 | 0.008 | 396 | 0 |
| hotpotqa | gpt-6.1-terra | V2 | 70 | 0.000 | 0.000 | 0 | 0 |
| hotpotqa | gpt-6.1-terra | V5 | 70 | 0.000 | 0.000 | 0 | 0 |
| musique | claude-haiku-5-5 | P2 | 499 | 1.450 | 0.003 | 20391 | 0 |
| musique | claude-haiku-5-5 | V6 | 762 | 0.059 | 0.000 | 550 | 0 |
| musique | claude-haiku-5-5 | P3 | 762 | 0.861 | 0.001 | 13123 | 0 |
| musique | claude-haiku-5-5 | P5 | 762 | 0.000 | 0.000 | 0 | 0 |
| musique | claude-haiku-5-5 | V7 | 762 | 0.293 | 0.000 | 2750 | 0 |
| musique | claude-haiku-5-5 | V4 | 556 | 0.256 | 0.000 | 1882 | 0 |
| musique | claude-haiku-5-5 | V3 | 163 | 0.018 | 0.000 | 94 | 0 |
| musique | claude-haiku-5-5 | P4 | 3 | 0.011 | 0.004 | 100 | 0 |
| musique | claude-haiku-5-5 | V2 | 368 | 0.231 | 0.001 | 1125 | 1 |
| musique | claude-haiku-5-5 | V5 | 762 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash-lite | P2 | 786 | 3.797 | 0.005 | 36141 | 0 |
| musique | gemini-2.5-flash-lite | V6 | 786 | 0.091 | 0.000 | 574 | 17 |
| musique | gemini-2.5-flash-lite | P3 | 466 | 0.797 | 0.002 | 7374 | 0 |
| musique | gemini-2.5-flash-lite | P5 | 786 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash-lite | V7 | 786 | 0.452 | 0.001 | 2870 | 98 |
| musique | gemini-2.5-flash-lite | V4 | 786 | 0.323 | 0.000 | 2870 | 0 |
| musique | gemini-2.5-flash-lite | V3 | 786 | 0.065 | 0.000 | 574 | 0 |
| musique | gemini-2.5-flash-lite | P4 | 786 | 3.843 | 0.005 | 36141 | 0 |
| musique | gemini-2.5-flash-lite | V2 | 786 | 0.324 | 0.000 | 2870 | 0 |
| musique | gemini-2.5-flash-lite | V5 | 786 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | P2 | 68 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | V6 | 68 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | P3 | 68 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | P5 | 68 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | V7 | 68 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | V4 | 68 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | V3 | 68 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | P4 | 68 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | V2 | 68 | 0.000 | 0.000 | 0 | 0 |
| musique | gemini-2.5-flash | V5 | 68 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6-luna | P2 | 220 | 2.278 | 0.010 | 8015 | 0 |
| musique | gpt-6-luna | V6 | 614 | 0.217 | 0.000 | 602 | 0 |
| musique | gpt-6-luna | P3 | 614 | 2.687 | 0.004 | 9929 | 0 |
| musique | gpt-6-luna | P5 | 614 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6-luna | V7 | 614 | 1.358 | 0.002 | 3010 | 0 |
| musique | gpt-6-luna | V4 | 614 | 0.536 | 0.001 | 2070 | 0 |
| musique | gpt-6-luna | V3 | 614 | 0.035 | 0.000 | 602 | 0 |
| musique | gpt-6-luna | P4 | 584 | 6.761 | 0.012 | 24136 | 0 |
| musique | gpt-6-luna | V2 | 614 | 0.569 | 0.001 | 2070 | 0 |
| musique | gpt-6-luna | V5 | 614 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | P2 | 60 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | V6 | 60 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | P3 | 60 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | P5 | 60 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | V7 | 60 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | V4 | 60 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | V3 | 60 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | P4 | 60 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | V2 | 60 | 0.000 | 0.000 | 0 | 0 |
| musique | gpt-6.1-terra | V5 | 60 | 0.000 | 0.000 | 0 | 0 |
