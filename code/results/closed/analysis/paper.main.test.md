# paper.main.test

Primary = tie-aware top-1 on the common valid set of each cell (methods V1, P1, MEXGEN_LOO, LOI, RM@k); diff/CI = paired bootstrap (2000) of method − V1. top1_e2e keeps invalid-reference rows as all-zero ties (chance floor).

## Methods

| dataset | model | method | n | n_invalid_ref | n_common | top1_common | diff_vs_V1 | ci_lo | ci_hi | top1_e2e | all_zero_valid | calls | cost | random_top1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | V1 | 510 | 0 | 510 | 0.962 |  |  |  | 0.962 | 0.008 | 1.000 | 1.000 | 0.200 |
| hotpotqa | claude-haiku-5-5 | P1 | 510 | 0 | 510 | 0.737 | -0.225 | -0.255 | -0.195 | 0.737 | 0.200 | 13.992 | 11.000 | 0.200 |
| hotpotqa | claude-haiku-5-5 | MEXGEN_LOO | 510 | 0 | 510 | 0.781 | -0.180 | -0.211 | -0.151 | 0.781 | 0.200 | 13.992 | 11.000 | 0.200 |
| hotpotqa | claude-haiku-5-5 | LOI | 510 | 0 | 510 | 0.751 | -0.211 | -0.243 | -0.178 | 0.751 | 0.247 | 10.000 | 11.000 | 0.200 |
| hotpotqa | claude-haiku-5-5 | RM@8 | 510 | 0 | 510 | 0.774 | -0.187 | -0.221 | -0.157 | 0.774 | 0.071 | 9.000 | 8.953 | 0.200 |
| hotpotqa | claude-haiku-5-5 | RM@10 | 510 | 0 | 510 | 0.830 | -0.132 | -0.162 | -0.103 | 0.830 | 0.043 | 11.000 | 10.918 | 0.200 |
| hotpotqa | claude-haiku-5-5 | RM@16 | 510 | 0 | 510 | 0.927 | -0.035 | -0.059 | -0.013 | 0.927 | 0.020 | 17.000 | 16.829 | 0.200 |
| hotpotqa | claude-haiku-5-5 | RM@32 | 510 | 0 | 510 | 0.931 | -0.031 | -0.052 | -0.010 | 0.931 | 0.014 | 33.000 | 32.447 | 0.200 |
| hotpotqa | claude-haiku-5-5 | RM64 | 510 | 0 | 510 | 0.947 | -0.015 | -0.033 | 0.002 | 0.947 | 0.008 | 60.345 | 62.949 | 0.200 |
| hotpotqa | gemini-2.5-flash-lite | V1 | 291 | 0 | 291 | 0.961 |  |  |  | 0.961 | 0.000 | 1.000 | 1.000 | 0.201 |
| hotpotqa | gemini-2.5-flash-lite | P1 | 291 | 0 | 291 | 0.719 | -0.242 | -0.288 | -0.203 | 0.719 | 0.213 | 12.931 | 10.979 | 0.201 |
| hotpotqa | gemini-2.5-flash-lite | MEXGEN_LOO | 291 | 0 | 291 | 0.774 | -0.187 | -0.230 | -0.148 | 0.774 | 0.213 | 12.931 | 10.979 | 0.201 |
| hotpotqa | gemini-2.5-flash-lite | LOI | 291 | 0 | 291 | 0.873 | -0.088 | -0.121 | -0.057 | 0.873 | 0.096 | 9.979 | 10.979 | 0.201 |
| hotpotqa | gemini-2.5-flash-lite | RM@8 | 291 | 0 | 291 | 0.788 | -0.173 | -0.217 | -0.132 | 0.788 | 0.055 | 9.000 | 8.955 | 0.201 |
| hotpotqa | gemini-2.5-flash-lite | RM@10 | 291 | 0 | 291 | 0.854 | -0.108 | -0.146 | -0.071 | 0.854 | 0.041 | 10.983 | 10.924 | 0.201 |
| hotpotqa | gemini-2.5-flash-lite | RM@16 | 291 | 0 | 291 | 0.918 | -0.043 | -0.074 | -0.016 | 0.918 | 0.027 | 17.000 | 16.859 | 0.201 |
| hotpotqa | gemini-2.5-flash-lite | RM@32 | 291 | 0 | 291 | 0.959 | -0.003 | -0.024 | 0.017 | 0.959 | 0.014 | 33.000 | 32.430 | 0.201 |
| hotpotqa | gemini-2.5-flash-lite | RM64 | 291 | 0 | 291 | 0.968 | 0.006 | -0.012 | 0.023 | 0.968 | 0.007 | 60.495 | 62.825 | 0.201 |
| hotpotqa | gemini-2.5-flash | V1 | 81 | 0 | 81 | 0.986 |  |  |  | 0.986 | 0.000 | 1.000 | 1.000 | 0.200 |
| hotpotqa | gemini-2.5-flash | P1 | 81 | 0 | 81 | 0.683 | -0.303 | -0.387 | -0.215 | 0.683 | 0.309 | 13.000 | 11.000 | 0.200 |
| hotpotqa | gemini-2.5-flash | MEXGEN_LOO | 81 | 0 | 81 | 0.713 | -0.273 | -0.358 | -0.187 | 0.713 | 0.309 | 13.000 | 11.000 | 0.200 |
| hotpotqa | gemini-2.5-flash | LOI | 81 | 0 | 81 | 0.913 | -0.073 | -0.134 | -0.021 | 0.913 | 0.099 | 10.000 | 11.000 | 0.200 |
| hotpotqa | gemini-2.5-flash | RM@8 | 81 | 0 | 81 | 0.770 | -0.216 | -0.300 | -0.135 | 0.770 | 0.074 | 9.000 | 8.951 | 0.200 |
| hotpotqa | gemini-2.5-flash | RM@10 | 81 | 0 | 81 | 0.807 | -0.179 | -0.260 | -0.105 | 0.807 | 0.062 | 11.000 | 10.901 | 0.200 |
| hotpotqa | gemini-2.5-flash | RM@16 | 81 | 0 | 81 | 0.932 | -0.053 | -0.111 | -0.002 | 0.932 | 0.000 | 17.000 | 16.840 | 0.200 |
| hotpotqa | gemini-2.5-flash | RM@32 | 81 | 0 | 81 | 0.988 | 0.002 | -0.033 | 0.029 | 0.988 | 0.000 | 33.000 | 32.531 | 0.200 |
| hotpotqa | gemini-2.5-flash | RM64 | 81 | 0 | 81 | 1.000 | 0.014 | 0.000 | 0.033 | 1.000 | 0.000 | 60.716 | 62.975 | 0.200 |
| hotpotqa | gpt-6-luna | V1 | 166 | 0 | 155 | 0.973 |  |  |  | 0.975 | 0.000 | 1.000 | 1.000 | 0.202 |
| hotpotqa | gpt-6-luna | P1 | 166 | 11 | 155 | 0.596 | -0.377 | -0.442 | -0.313 | 0.570 | 0.323 | 12.657 | 10.964 | 0.202 |
| hotpotqa | gpt-6-luna | MEXGEN_LOO | 166 | 11 | 155 | 0.634 | -0.339 | -0.403 | -0.278 | 0.605 | 0.323 | 12.657 | 10.964 | 0.202 |
| hotpotqa | gpt-6-luna | LOI | 166 | 11 | 155 | 0.713 | -0.260 | -0.313 | -0.211 | 0.679 | 0.097 | 9.964 | 10.964 | 0.202 |
| hotpotqa | gpt-6-luna | RM@8 | 166 | 11 | 155 | 0.731 | -0.242 | -0.305 | -0.186 | 0.696 | 0.123 | 12.440 | 8.946 | 0.202 |
| hotpotqa | gpt-6-luna | RM@10 | 166 | 11 | 155 | 0.740 | -0.233 | -0.297 | -0.175 | 0.705 | 0.116 | 14.283 | 10.880 | 0.202 |
| hotpotqa | gpt-6-luna | RM@16 | 166 | 11 | 155 | 0.812 | -0.161 | -0.218 | -0.111 | 0.772 | 0.084 | 19.910 | 16.783 | 0.202 |
| hotpotqa | gpt-6-luna | RM@32 | 166 | 11 | 155 | 0.868 | -0.105 | -0.157 | -0.061 | 0.824 | 0.039 | 34.849 | 32.337 | 0.202 |
| hotpotqa | gpt-6-luna | RM64 | 166 | 11 | 155 | 0.901 | -0.072 | -0.116 | -0.034 | 0.854 | 0.019 | 58.627 | 62.633 | 0.202 |
| hotpotqa | gpt-6.1-terra | V1 | 64 | 0 | 64 | 0.987 |  |  |  | 0.987 | 0.000 | 1.000 | 1.000 | 0.200 |
| hotpotqa | gpt-6.1-terra | P1 | 64 | 0 | 64 | 0.538 | -0.449 | -0.540 | -0.357 | 0.538 | 0.484 | 13.000 | 11.000 | 0.200 |
| hotpotqa | gpt-6.1-terra | MEXGEN_LOO | 64 | 0 | 64 | 0.599 | -0.388 | -0.490 | -0.291 | 0.599 | 0.484 | 13.000 | 11.000 | 0.200 |
| hotpotqa | gpt-6.1-terra | LOI | 64 | 0 | 64 | 0.866 | -0.121 | -0.186 | -0.062 | 0.866 | 0.047 | 10.000 | 11.000 | 0.200 |
| hotpotqa | gpt-6.1-terra | RM@8 | 64 | 0 | 64 | 0.691 | -0.296 | -0.395 | -0.203 | 0.691 | 0.188 | 9.000 | 8.953 | 0.200 |
| hotpotqa | gpt-6.1-terra | RM@10 | 64 | 0 | 64 | 0.701 | -0.286 | -0.389 | -0.191 | 0.701 | 0.156 | 11.000 | 10.922 | 0.200 |
| hotpotqa | gpt-6.1-terra | RM@16 | 64 | 0 | 64 | 0.809 | -0.178 | -0.275 | -0.087 | 0.809 | 0.062 | 17.000 | 16.844 | 0.200 |
| hotpotqa | gpt-6.1-terra | RM@32 | 64 | 0 | 64 | 0.971 | -0.016 | -0.057 | 0.021 | 0.971 | 0.000 | 33.000 | 32.547 | 0.200 |
| hotpotqa | gpt-6.1-terra | RM64 | 64 | 0 | 64 | 0.969 | -0.018 | -0.073 | 0.021 | 0.969 | 0.000 | 60.719 | 63.141 | 0.200 |
| musique | claude-haiku-5-5 | V1 | 750 | 0 | 747 | 0.950 |  |  |  | 0.949 | 0.017 | 1.000 | 1.000 | 0.133 |
| musique | claude-haiku-5-5 | P1 | 750 | 3 | 747 | 0.734 | -0.216 | -0.241 | -0.192 | 0.732 | 0.032 | 23.831 | 20.979 | 0.133 |
| musique | claude-haiku-5-5 | MEXGEN_LOO | 750 | 3 | 747 | 0.807 | -0.143 | -0.166 | -0.121 | 0.804 | 0.032 | 23.831 | 20.979 | 0.133 |
| musique | claude-haiku-5-5 | LOI | 750 | 3 | 747 | 0.396 | -0.554 | -0.586 | -0.522 | 0.395 | 0.671 | 19.979 | 20.979 | 0.133 |
| musique | claude-haiku-5-5 | RM@8 | 750 | 3 | 747 | 0.534 | -0.415 | -0.448 | -0.384 | 0.533 | 0.162 | 9.220 | 9.000 | 0.133 |
| musique | claude-haiku-5-5 | RM@10 | 750 | 3 | 747 | 0.613 | -0.337 | -0.369 | -0.306 | 0.611 | 0.123 | 11.212 | 11.000 | 0.133 |
| musique | claude-haiku-5-5 | RM@16 | 750 | 3 | 747 | 0.782 | -0.168 | -0.196 | -0.141 | 0.779 | 0.054 | 17.188 | 17.000 | 0.133 |
| musique | claude-haiku-5-5 | RM@20 | 750 | 3 | 747 | 0.837 | -0.112 | -0.139 | -0.087 | 0.835 | 0.044 | 21.688 | 21.000 | 0.133 |
| musique | claude-haiku-5-5 | RM@32 | 750 | 3 | 747 | 0.907 | -0.043 | -0.065 | -0.022 | 0.904 | 0.024 | 33.124 | 33.000 | 0.133 |
| musique | claude-haiku-5-5 | RM64 | 750 | 3 | 747 | 0.948 | -0.002 | -0.020 | 0.016 | 0.945 | 0.017 | 63.692 | 64.996 | 0.133 |
| musique | gemini-2.5-flash-lite | V1 | 774 | 0 | 774 | 0.934 |  |  |  | 0.934 | 0.003 | 1.000 | 1.000 | 0.137 |
| musique | gemini-2.5-flash-lite | P1 | 774 | 0 | 774 | 0.718 | -0.216 | -0.243 | -0.190 | 0.718 | 0.071 | 22.921 | 20.986 | 0.137 |
| musique | gemini-2.5-flash-lite | MEXGEN_LOO | 774 | 0 | 774 | 0.790 | -0.144 | -0.169 | -0.120 | 0.790 | 0.071 | 22.921 | 20.986 | 0.137 |
| musique | gemini-2.5-flash-lite | LOI | 774 | 0 | 774 | 0.792 | -0.142 | -0.170 | -0.115 | 0.792 | 0.214 | 19.968 | 20.986 | 0.137 |
| musique | gemini-2.5-flash-lite | RM@8 | 774 | 0 | 774 | 0.708 | -0.226 | -0.257 | -0.196 | 0.708 | 0.066 | 9.000 | 9.000 | 0.137 |
| musique | gemini-2.5-flash-lite | RM@10 | 774 | 0 | 774 | 0.768 | -0.166 | -0.195 | -0.137 | 0.768 | 0.043 | 11.000 | 11.000 | 0.137 |
| musique | gemini-2.5-flash-lite | RM@16 | 774 | 0 | 774 | 0.889 | -0.045 | -0.069 | -0.022 | 0.889 | 0.017 | 17.000 | 17.000 | 0.137 |
| musique | gemini-2.5-flash-lite | RM@20 | 774 | 0 | 774 | 0.916 | -0.017 | -0.040 | 0.004 | 0.916 | 0.012 | 21.500 | 21.000 | 0.137 |
| musique | gemini-2.5-flash-lite | RM@32 | 774 | 0 | 774 | 0.951 | 0.017 | -0.002 | 0.034 | 0.951 | 0.008 | 33.000 | 33.000 | 0.137 |
| musique | gemini-2.5-flash-lite | RM64 | 774 | 0 | 774 | 0.980 | 0.047 | 0.032 | 0.060 | 0.980 | 0.003 | 63.996 | 64.997 | 0.137 |
| musique | gemini-2.5-flash | V1 | 62 | 0 | 62 | 0.953 |  |  |  | 0.953 | 0.000 | 1.000 | 1.000 | 0.131 |
| musique | gemini-2.5-flash | P1 | 62 | 0 | 62 | 0.775 | -0.178 | -0.264 | -0.098 | 0.775 | 0.129 | 22.984 | 20.984 | 0.131 |
| musique | gemini-2.5-flash | MEXGEN_LOO | 62 | 0 | 62 | 0.810 | -0.143 | -0.226 | -0.064 | 0.810 | 0.129 | 22.984 | 20.984 | 0.131 |
| musique | gemini-2.5-flash | LOI | 62 | 0 | 62 | 0.867 | -0.086 | -0.163 | -0.013 | 0.867 | 0.113 | 19.984 | 20.984 | 0.131 |
| musique | gemini-2.5-flash | RM@8 | 62 | 0 | 62 | 0.695 | -0.258 | -0.359 | -0.161 | 0.695 | 0.032 | 9.000 | 9.000 | 0.131 |
| musique | gemini-2.5-flash | RM@10 | 62 | 0 | 62 | 0.782 | -0.171 | -0.259 | -0.086 | 0.782 | 0.000 | 11.000 | 11.000 | 0.131 |
| musique | gemini-2.5-flash | RM@16 | 62 | 0 | 62 | 0.895 | -0.058 | -0.118 | -0.004 | 0.895 | 0.000 | 17.000 | 17.000 | 0.131 |
| musique | gemini-2.5-flash | RM@20 | 62 | 0 | 62 | 0.911 | -0.042 | -0.095 | 0.005 | 0.911 | 0.000 | 21.694 | 21.000 | 0.131 |
| musique | gemini-2.5-flash | RM@32 | 62 | 0 | 62 | 0.944 | -0.009 | -0.047 | 0.024 | 0.944 | 0.000 | 33.000 | 33.000 | 0.131 |
| musique | gemini-2.5-flash | RM64 | 62 | 0 | 62 | 0.968 | 0.015 | -0.023 | 0.052 | 0.968 | 0.000 | 63.984 | 65.000 | 0.131 |
| musique | gpt-6-luna | V1 | 602 | 0 | 602 | 0.952 |  |  |  | 0.952 | 0.005 | 1.000 | 1.000 | 0.138 |
| musique | gpt-6-luna | P1 | 602 | 0 | 602 | 0.596 | -0.357 | -0.389 | -0.324 | 0.596 | 0.075 | 23.900 | 20.987 | 0.138 |
| musique | gpt-6-luna | MEXGEN_LOO | 602 | 0 | 602 | 0.676 | -0.276 | -0.308 | -0.243 | 0.676 | 0.075 | 23.900 | 20.987 | 0.138 |
| musique | gpt-6-luna | LOI | 602 | 0 | 602 | 0.749 | -0.203 | -0.235 | -0.174 | 0.749 | 0.113 | 19.914 | 20.987 | 0.138 |
| musique | gpt-6-luna | RM@8 | 602 | 0 | 602 | 0.673 | -0.280 | -0.312 | -0.246 | 0.673 | 0.076 | 9.000 | 9.000 | 0.138 |
| musique | gpt-6-luna | RM@10 | 602 | 0 | 602 | 0.716 | -0.236 | -0.270 | -0.201 | 0.716 | 0.060 | 11.000 | 11.000 | 0.138 |
| musique | gpt-6-luna | RM@16 | 602 | 0 | 602 | 0.817 | -0.135 | -0.165 | -0.105 | 0.817 | 0.022 | 17.000 | 17.000 | 0.138 |
| musique | gpt-6-luna | RM@20 | 602 | 0 | 602 | 0.844 | -0.109 | -0.137 | -0.079 | 0.844 | 0.020 | 21.429 | 21.000 | 0.138 |
| musique | gpt-6-luna | RM@32 | 602 | 0 | 602 | 0.863 | -0.089 | -0.116 | -0.062 | 0.863 | 0.010 | 33.000 | 33.000 | 0.138 |
| musique | gpt-6-luna | RM64 | 602 | 0 | 602 | 0.890 | -0.062 | -0.086 | -0.036 | 0.890 | 0.008 | 63.017 | 64.997 | 0.138 |
| musique | gpt-6.1-terra | V1 | 54 | 0 | 54 | 0.975 |  |  |  | 0.975 | 0.000 | 1.000 | 1.000 | 0.133 |
| musique | gpt-6.1-terra | P1 | 54 | 0 | 54 | 0.760 | -0.215 | -0.323 | -0.116 | 0.760 | 0.130 | 23.000 | 21.000 | 0.133 |
| musique | gpt-6.1-terra | MEXGEN_LOO | 54 | 0 | 54 | 0.793 | -0.183 | -0.286 | -0.092 | 0.793 | 0.130 | 23.000 | 21.000 | 0.133 |
| musique | gpt-6.1-terra | LOI | 54 | 0 | 54 | 0.880 | -0.096 | -0.180 | -0.015 | 0.880 | 0.093 | 20.000 | 21.000 | 0.133 |
| musique | gpt-6.1-terra | RM@8 | 54 | 0 | 54 | 0.717 | -0.259 | -0.372 | -0.146 | 0.717 | 0.037 | 9.000 | 9.000 | 0.133 |
| musique | gpt-6.1-terra | RM@10 | 54 | 0 | 54 | 0.763 | -0.213 | -0.330 | -0.105 | 0.763 | 0.019 | 11.000 | 11.000 | 0.133 |
| musique | gpt-6.1-terra | RM@16 | 54 | 0 | 54 | 0.870 | -0.105 | -0.198 | -0.019 | 0.870 | 0.000 | 17.000 | 17.000 | 0.133 |
| musique | gpt-6.1-terra | RM@20 | 54 | 0 | 54 | 0.944 | -0.031 | -0.102 | 0.034 | 0.944 | 0.000 | 21.000 | 21.000 | 0.133 |
| musique | gpt-6.1-terra | RM@32 | 54 | 0 | 54 | 0.963 | -0.012 | -0.074 | 0.040 | 0.963 | 0.000 | 33.000 | 33.000 | 0.133 |
| musique | gpt-6.1-terra | RM64 | 54 | 0 | 54 | 0.981 | 0.006 | -0.040 | 0.046 | 0.981 | 0.000 | 61.407 | 65.000 | 0.133 |
| qasper | claude-haiku-5-5 | V1 | 294 | 0 | 294 | 0.866 |  |  |  | 0.866 | 0.000 | 1.000 | 1.000 | 0.100 |
| qasper | claude-haiku-5-5 | P1 | 294 | 0 | 294 | 0.505 | -0.361 | -0.401 | -0.318 | 0.505 | 0.082 | 13.000 | 11.000 | 0.100 |
| qasper | claude-haiku-5-5 | MEXGEN_LOO | 294 | 0 | 294 | 0.749 | -0.117 | -0.155 | -0.082 | 0.749 | 0.092 | 13.000 | 11.000 | 0.100 |
| qasper | claude-haiku-5-5 | LOI | 294 | 0 | 294 | 0.661 | -0.205 | -0.255 | -0.157 | 0.661 | 0.289 | 10.000 | 11.000 | 0.100 |
| qasper | claude-haiku-5-5 | RM@8 | 294 | 0 | 294 | 0.583 | -0.283 | -0.335 | -0.233 | 0.583 | 0.235 | 9.000 | 8.949 | 0.100 |
| qasper | claude-haiku-5-5 | RM@10 | 294 | 0 | 294 | 0.610 | -0.256 | -0.306 | -0.208 | 0.610 | 0.207 | 11.000 | 10.929 | 0.100 |
| qasper | claude-haiku-5-5 | RM@16 | 294 | 0 | 294 | 0.678 | -0.189 | -0.238 | -0.140 | 0.678 | 0.160 | 17.000 | 16.884 | 0.100 |
| qasper | claude-haiku-5-5 | RM@32 | 294 | 0 | 294 | 0.750 | -0.117 | -0.164 | -0.072 | 0.750 | 0.133 | 33.000 | 32.480 | 0.100 |
| qasper | claude-haiku-5-5 | RM64 | 294 | 0 | 294 | 0.768 | -0.099 | -0.144 | -0.055 | 0.768 | 0.109 | 59.231 | 62.969 | 0.100 |
| qasper | gemini-2.5-flash-lite | V1 | 304 | 0 | 304 | 0.935 |  |  |  | 0.935 | 0.000 | 1.000 | 1.000 | 0.100 |
| qasper | gemini-2.5-flash-lite | P1 | 304 | 0 | 304 | 0.603 | -0.333 | -0.380 | -0.291 | 0.603 | 0.069 | 13.000 | 11.000 | 0.100 |
| qasper | gemini-2.5-flash-lite | MEXGEN_LOO | 304 | 0 | 304 | 0.782 | -0.153 | -0.192 | -0.116 | 0.782 | 0.076 | 13.000 | 11.000 | 0.100 |
| qasper | gemini-2.5-flash-lite | LOI | 304 | 0 | 304 | 0.739 | -0.197 | -0.242 | -0.151 | 0.739 | 0.197 | 10.000 | 11.000 | 0.100 |
| qasper | gemini-2.5-flash-lite | RM@8 | 304 | 0 | 304 | 0.738 | -0.197 | -0.242 | -0.152 | 0.738 | 0.079 | 9.000 | 8.957 | 0.100 |
| qasper | gemini-2.5-flash-lite | RM@10 | 304 | 0 | 304 | 0.779 | -0.157 | -0.200 | -0.114 | 0.779 | 0.062 | 11.000 | 10.951 | 0.100 |
| qasper | gemini-2.5-flash-lite | RM@16 | 304 | 0 | 304 | 0.828 | -0.107 | -0.147 | -0.067 | 0.828 | 0.043 | 17.000 | 16.891 | 0.100 |
| qasper | gemini-2.5-flash-lite | RM@32 | 304 | 0 | 304 | 0.853 | -0.083 | -0.122 | -0.046 | 0.853 | 0.023 | 33.000 | 32.487 | 0.100 |
| qasper | gemini-2.5-flash-lite | RM64 | 304 | 0 | 304 | 0.875 | -0.060 | -0.099 | -0.022 | 0.875 | 0.016 | 60.780 | 62.977 | 0.100 |
| qasper | gemini-2.5-flash | V1 | 296 | 0 | 296 | 0.950 |  |  |  | 0.950 | 0.000 | 1.000 | 1.000 | 0.100 |
| qasper | gemini-2.5-flash | P1 | 296 | 0 | 296 | 0.617 | -0.333 | -0.381 | -0.286 | 0.617 | 0.078 | 13.000 | 11.000 | 0.100 |
| qasper | gemini-2.5-flash | MEXGEN_LOO | 296 | 0 | 296 | 0.773 | -0.177 | -0.219 | -0.138 | 0.773 | 0.084 | 13.000 | 11.000 | 0.100 |
| qasper | gemini-2.5-flash | LOI | 296 | 0 | 296 | 0.751 | -0.199 | -0.245 | -0.154 | 0.751 | 0.193 | 10.000 | 11.000 | 0.100 |
| qasper | gemini-2.5-flash | RM@8 | 296 | 0 | 296 | 0.737 | -0.213 | -0.258 | -0.170 | 0.737 | 0.078 | 9.000 | 8.959 | 0.100 |
| qasper | gemini-2.5-flash | RM@10 | 296 | 0 | 296 | 0.789 | -0.162 | -0.202 | -0.121 | 0.789 | 0.061 | 11.000 | 10.953 | 0.100 |
| qasper | gemini-2.5-flash | RM@16 | 296 | 0 | 296 | 0.846 | -0.105 | -0.146 | -0.067 | 0.846 | 0.037 | 17.000 | 16.892 | 0.100 |
| qasper | gemini-2.5-flash | RM@32 | 296 | 0 | 296 | 0.867 | -0.083 | -0.121 | -0.048 | 0.867 | 0.024 | 33.000 | 32.500 | 0.100 |
| qasper | gemini-2.5-flash | RM64 | 296 | 0 | 296 | 0.881 | -0.069 | -0.105 | -0.034 | 0.881 | 0.014 | 59.328 | 63.010 | 0.100 |
| qasper | gpt-6-luna | V1 | 260 | 0 | 260 | 0.892 |  |  |  | 0.892 | 0.004 | 1.000 | 1.000 | 0.100 |
| qasper | gpt-6-luna | P1 | 260 | 0 | 260 | 0.518 | -0.373 | -0.421 | -0.328 | 0.518 | 0.096 | 13.000 | 11.000 | 0.100 |
| qasper | gpt-6-luna | MEXGEN_LOO | 260 | 0 | 260 | 0.770 | -0.122 | -0.168 | -0.078 | 0.770 | 0.100 | 13.000 | 11.000 | 0.100 |
| qasper | gpt-6-luna | LOI | 260 | 0 | 260 | 0.628 | -0.263 | -0.315 | -0.216 | 0.628 | 0.296 | 10.000 | 11.000 | 0.100 |
| qasper | gpt-6-luna | RM@8 | 260 | 0 | 260 | 0.616 | -0.276 | -0.330 | -0.223 | 0.616 | 0.108 | 9.000 | 8.942 | 0.100 |
| qasper | gpt-6-luna | RM@10 | 260 | 0 | 260 | 0.655 | -0.236 | -0.289 | -0.188 | 0.655 | 0.092 | 11.000 | 10.931 | 0.100 |
| qasper | gpt-6-luna | RM@16 | 260 | 0 | 260 | 0.748 | -0.144 | -0.194 | -0.100 | 0.748 | 0.069 | 17.000 | 16.877 | 0.100 |
| qasper | gpt-6-luna | RM@32 | 260 | 0 | 260 | 0.807 | -0.085 | -0.131 | -0.045 | 0.807 | 0.046 | 33.000 | 32.500 | 0.100 |
| qasper | gpt-6-luna | RM64 | 260 | 0 | 260 | 0.832 | -0.060 | -0.103 | -0.021 | 0.832 | 0.027 | 60.842 | 62.988 | 0.100 |
| qasper | gpt-6.1-terra | V1 | 258 | 0 | 258 | 0.868 |  |  |  | 0.868 | 0.004 | 1.000 | 1.000 | 0.100 |
| qasper | gpt-6.1-terra | P1 | 258 | 0 | 258 | 0.487 | -0.381 | -0.427 | -0.331 | 0.487 | 0.105 | 13.000 | 11.000 | 0.100 |
| qasper | gpt-6.1-terra | MEXGEN_LOO | 258 | 0 | 258 | 0.730 | -0.138 | -0.185 | -0.093 | 0.730 | 0.116 | 13.000 | 11.000 | 0.100 |
| qasper | gpt-6.1-terra | LOI | 258 | 0 | 258 | 0.639 | -0.229 | -0.281 | -0.176 | 0.639 | 0.279 | 9.922 | 11.000 | 0.100 |
| qasper | gpt-6.1-terra | RM@8 | 258 | 0 | 258 | 0.590 | -0.278 | -0.332 | -0.224 | 0.590 | 0.217 | 9.000 | 8.950 | 0.100 |
| qasper | gpt-6.1-terra | RM@10 | 258 | 0 | 258 | 0.618 | -0.250 | -0.301 | -0.197 | 0.618 | 0.182 | 11.000 | 10.942 | 0.100 |
| qasper | gpt-6.1-terra | RM@16 | 258 | 0 | 258 | 0.702 | -0.166 | -0.216 | -0.115 | 0.702 | 0.124 | 17.000 | 16.872 | 0.100 |
| qasper | gpt-6.1-terra | RM@32 | 258 | 0 | 258 | 0.715 | -0.153 | -0.205 | -0.103 | 0.715 | 0.093 | 33.000 | 32.488 | 0.100 |
| qasper | gpt-6.1-terra | RM64 | 258 | 0 | 258 | 0.776 | -0.093 | -0.142 | -0.046 | 0.776 | 0.081 | 60.810 | 63.004 | 0.100 |

## Coverage / fidelity (common valid set)

| dataset | model | method | n_common | coverage | fidelity | V1_on_covered | V1_on_uncovered | unique_max_share | top1_unique | top1_tied | spontaneous_change | gap_vs_V1 | share_gap_all_zero |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | P1 | 510 | 0.800 | 0.871 | 0.978 | 0.898 | 0.551 | 0.987 | 0.728 | 0.069 | 0.225 | 0.620 |
| hotpotqa | claude-haiku-5-5 | LOI | 510 | 0.753 | 0.932 | 0.959 | 0.970 | 0.742 | 0.979 | 0.796 | nan | 0.211 | 0.903 |
| hotpotqa | claude-haiku-5-5 | MEXGEN_LOO | 510 | 0.800 | 0.927 | 0.978 | 0.898 | 0.684 | 0.975 | 0.822 | 0.069 | 0.180 | 0.774 |
| hotpotqa | gemini-2.5-flash-lite | P1 | 291 | 0.787 | 0.858 | 0.964 | 0.950 | 0.712 | 0.988 | 0.538 | 0.037 | 0.242 | 0.655 |
| hotpotqa | gemini-2.5-flash-lite | LOI | 291 | 0.904 | 0.945 | 0.960 | 0.976 | 0.726 | 0.990 | 0.827 | nan | 0.088 | 0.849 |
| hotpotqa | gemini-2.5-flash-lite | MEXGEN_LOO | 291 | 0.787 | 0.928 | 0.964 | 0.950 | 0.825 | 0.989 | 0.638 | 0.037 | 0.187 | 0.847 |
| hotpotqa | gemini-2.5-flash | P1 | 81 | 0.691 | 0.898 | 0.979 | 1.000 | 0.750 | 1.000 | 0.594 | 0.041 | 0.303 | 0.816 |
| hotpotqa | gemini-2.5-flash | LOI | 81 | 0.901 | 0.991 | 0.984 | 1.000 | 0.603 | 1.000 | 0.977 | nan | 0.073 | 1.085 |
| hotpotqa | gemini-2.5-flash | MEXGEN_LOO | 81 | 0.691 | 0.942 | 0.979 | 1.000 | 0.839 | 1.000 | 0.636 | 0.041 | 0.273 | 0.905 |
| hotpotqa | gpt-6-luna | P1 | 155 | 0.677 | 0.781 | 0.976 | 0.967 | 0.676 | 0.986 | 0.354 | 0.086 | 0.377 | 0.650 |
| hotpotqa | gpt-6-luna | LOI | 155 | 0.903 | 0.768 | 0.970 | 1.000 | 0.521 | 1.000 | 0.515 | nan | 0.260 | 0.297 |
| hotpotqa | gpt-6-luna | MEXGEN_LOO | 155 | 0.677 | 0.838 | 0.976 | 0.967 | 0.800 | 0.964 | 0.331 | 0.086 | 0.339 | 0.723 |
| hotpotqa | gpt-6.1-terra | P1 | 64 | 0.516 | 0.856 | 0.990 | 0.984 | 0.788 | 1.000 | 0.321 | 0.068 | 0.449 | 0.846 |
| hotpotqa | gpt-6.1-terra | LOI | 64 | 0.953 | 0.899 | 0.986 | 1.000 | 0.361 | 1.000 | 0.842 | nan | 0.121 | 0.310 |
| hotpotqa | gpt-6.1-terra | MEXGEN_LOO | 64 | 0.516 | 0.973 | 0.990 | 0.984 | 0.970 | 1.000 | 0.111 | 0.068 | 0.388 | 0.978 |
| musique | claude-haiku-5-5 | P1 | 747 | 0.968 | 0.754 | 0.955 | 0.801 | 0.296 | 0.981 | 0.659 | 0.126 | 0.216 | 0.099 |
| musique | claude-haiku-5-5 | LOI | 747 | 0.329 | 0.927 | 0.921 | 0.964 | 0.939 | 0.961 | 0.400 | nan | 0.554 | 1.003 |
| musique | claude-haiku-5-5 | MEXGEN_LOO | 747 | 0.968 | 0.829 | 0.955 | 0.801 | 0.372 | 0.974 | 0.743 | 0.126 | 0.143 | 0.149 |
| musique | gemini-2.5-flash-lite | P1 | 774 | 0.929 | 0.763 | 0.938 | 0.874 | 0.524 | 0.987 | 0.516 | 0.053 | 0.216 | 0.245 |
| musique | gemini-2.5-flash-lite | LOI | 774 | 0.786 | 0.972 | 0.931 | 0.945 | 0.924 | 0.989 | 0.760 | nan | 0.142 | 1.229 |
| musique | gemini-2.5-flash-lite | MEXGEN_LOO | 774 | 0.929 | 0.840 | 0.938 | 0.874 | 0.652 | 0.979 | 0.580 | 0.053 | 0.144 | 0.367 |
| musique | gemini-2.5-flash | P1 | 62 | 0.871 | 0.872 | 0.965 | 0.875 | 0.704 | 1.000 | 0.569 | 0.016 | 0.178 | 0.548 |
| musique | gemini-2.5-flash | LOI | 62 | 0.887 | 0.964 | 0.953 | 0.952 | 0.873 | 1.000 | 0.714 | nan | 0.086 | 1.109 |
| musique | gemini-2.5-flash | MEXGEN_LOO | 62 | 0.871 | 0.913 | 0.965 | 0.875 | 0.759 | 1.000 | 0.637 | 0.016 | 0.143 | 0.684 |
| musique | gpt-6-luna | P1 | 602 | 0.925 | 0.631 | 0.955 | 0.922 | 0.445 | 0.964 | 0.365 | 0.136 | 0.357 | 0.161 |
| musique | gpt-6-luna | LOI | 602 | 0.887 | 0.826 | 0.950 | 0.968 | 0.695 | 0.941 | 0.566 | nan | 0.203 | 0.458 |
| musique | gpt-6-luna | MEXGEN_LOO | 602 | 0.925 | 0.719 | 0.955 | 0.922 | 0.580 | 0.963 | 0.381 | 0.136 | 0.276 | 0.208 |
| musique | gpt-6.1-terra | P1 | 54 | 0.870 | 0.851 | 0.972 | 1.000 | 0.766 | 1.000 | 0.364 | 0.080 | 0.215 | 0.512 |
| musique | gpt-6.1-terra | LOI | 54 | 0.907 | 0.959 | 0.973 | 1.000 | 0.857 | 1.000 | 0.714 | nan | 0.096 | 0.871 |
| musique | gpt-6.1-terra | MEXGEN_LOO | 54 | 0.870 | 0.888 | 0.972 | 1.000 | 0.809 | 1.000 | 0.417 | 0.080 | 0.183 | 0.603 |
| qasper | claude-haiku-5-5 | P1 | 294 | 0.918 | 0.541 | 0.883 | 0.681 | 0.426 | 0.965 | 0.227 | 0.232 | 0.361 | 0.131 |
| qasper | claude-haiku-5-5 | LOI | 294 | 0.711 | 0.889 | 0.885 | 0.820 | 0.885 | 0.957 | 0.370 | nan | 0.205 | 1.015 |
| qasper | claude-haiku-5-5 | MEXGEN_LOO | 294 | 0.908 | 0.815 | 0.887 | 0.660 | 0.839 | 0.933 | 0.201 | 0.232 | 0.117 | 0.441 |
| qasper | gemini-2.5-flash-lite | P1 | 304 | 0.931 | 0.640 | 0.954 | 0.683 | 0.534 | 0.967 | 0.266 | 0.138 | 0.333 | 0.121 |
| qasper | gemini-2.5-flash-lite | LOI | 304 | 0.803 | 0.896 | 0.928 | 0.967 | 0.893 | 0.954 | 0.407 | nan | 0.197 | 0.870 |
| qasper | gemini-2.5-flash-lite | MEXGEN_LOO | 304 | 0.924 | 0.838 | 0.956 | 0.681 | 0.840 | 0.949 | 0.257 | 0.138 | 0.153 | 0.288 |
| qasper | gemini-2.5-flash | P1 | 296 | 0.922 | 0.661 | 0.961 | 0.826 | 0.590 | 0.950 | 0.245 | 0.116 | 0.333 | 0.169 |
| qasper | gemini-2.5-flash | LOI | 296 | 0.807 | 0.907 | 0.941 | 0.991 | 0.904 | 0.958 | 0.422 | nan | 0.199 | 0.862 |
| qasper | gemini-2.5-flash | MEXGEN_LOO | 296 | 0.916 | 0.835 | 0.963 | 0.813 | 0.856 | 0.940 | 0.215 | 0.116 | 0.177 | 0.340 |
| qasper | gpt-6-luna | P1 | 260 | 0.904 | 0.563 | 0.901 | 0.800 | 0.438 | 0.951 | 0.260 | 0.219 | 0.373 | 0.180 |
| qasper | gpt-6-luna | LOI | 260 | 0.704 | 0.851 | 0.900 | 0.871 | 0.820 | 0.947 | 0.414 | nan | 0.263 | 0.867 |
| qasper | gpt-6-luna | MEXGEN_LOO | 260 | 0.900 | 0.844 | 0.901 | 0.808 | 0.906 | 0.906 | 0.253 | 0.219 | 0.122 | 0.581 |
| qasper | gpt-6.1-terra | P1 | 258 | 0.895 | 0.532 | 0.883 | 0.741 | 0.433 | 0.930 | 0.228 | 0.251 | 0.381 | 0.176 |
| qasper | gpt-6.1-terra | LOI | 258 | 0.721 | 0.848 | 0.872 | 0.857 | 0.849 | 0.930 | 0.380 | nan | 0.229 | 0.922 |
| qasper | gpt-6.1-terra | MEXGEN_LOO | 258 | 0.884 | 0.813 | 0.886 | 0.733 | 0.829 | 0.931 | 0.242 | 0.251 | 0.138 | 0.535 |

## Routing: cheap estimator, escalate to RM when uninformative

| dataset | model | route | rule | top1 | calls | cost | escalated | n_common |
|---|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | P1->RM@16 | all_zero | 0.881 | 17.192 | 14.145 | 0.200 | 510 |
| hotpotqa | claude-haiku-5-5 | P1->RM@16 | no_unique_max | 0.932 | 22.933 | 19.827 | 0.559 | 510 |
| hotpotqa | claude-haiku-5-5 | P1->RM@32 | all_zero | 0.876 | 20.392 | 17.273 | 0.200 | 510 |
| hotpotqa | claude-haiku-5-5 | P1->RM@32 | no_unique_max | 0.932 | 31.875 | 28.565 | 0.559 | 510 |
| hotpotqa | claude-haiku-5-5 | P1->RM64 | all_zero | 0.875 | 25.857 | 23.363 | 0.200 | 510 |
| hotpotqa | claude-haiku-5-5 | P1->RM64 | no_unique_max | 0.943 | 47.218 | 45.627 | 0.559 | 510 |
| hotpotqa | claude-haiku-5-5 | LOI->RM@16 | all_zero | 0.907 | 13.953 | 14.927 | 0.247 | 510 |
| hotpotqa | claude-haiku-5-5 | LOI->RM@16 | no_unique_max | 0.927 | 17.059 | 17.978 | 0.441 | 510 |
| hotpotqa | claude-haiku-5-5 | LOI->RM@32 | all_zero | 0.917 | 17.906 | 18.798 | 0.247 | 510 |
| hotpotqa | claude-haiku-5-5 | LOI->RM@32 | no_unique_max | 0.935 | 24.118 | 24.884 | 0.441 | 510 |
| hotpotqa | claude-haiku-5-5 | LOI->RM64 | all_zero | 0.929 | 24.682 | 26.298 | 0.247 | 510 |
| hotpotqa | claude-haiku-5-5 | LOI->RM64 | no_unique_max | 0.942 | 36.080 | 38.324 | 0.441 | 510 |
| hotpotqa | gemini-2.5-flash-lite | P1->RM@16 | all_zero | 0.851 | 16.340 | 14.340 | 0.213 | 291 |
| hotpotqa | gemini-2.5-flash-lite | P1->RM@16 | no_unique_max | 0.918 | 19.969 | 17.942 | 0.440 | 291 |
| hotpotqa | gemini-2.5-flash-lite | P1->RM@32 | all_zero | 0.873 | 19.749 | 17.615 | 0.213 | 291 |
| hotpotqa | gemini-2.5-flash-lite | P1->RM@32 | no_unique_max | 0.959 | 27.007 | 24.777 | 0.440 | 291 |
| hotpotqa | gemini-2.5-flash-lite | P1->RM64 | all_zero | 0.869 | 25.419 | 23.986 | 0.213 | 291 |
| hotpotqa | gemini-2.5-flash-lite | P1->RM64 | no_unique_max | 0.964 | 38.966 | 38.079 | 0.440 | 291 |
| hotpotqa | gemini-2.5-flash-lite | LOI->RM@16 | all_zero | 0.939 | 11.519 | 12.509 | 0.096 | 291 |
| hotpotqa | gemini-2.5-flash-lite | LOI->RM@16 | no_unique_max | 0.935 | 15.478 | 16.412 | 0.344 | 291 |
| hotpotqa | gemini-2.5-flash-lite | LOI->RM@32 | all_zero | 0.945 | 13.058 | 14.021 | 0.096 | 291 |
| hotpotqa | gemini-2.5-flash-lite | LOI->RM@32 | no_unique_max | 0.959 | 20.976 | 21.763 | 0.344 | 291 |
| hotpotqa | gemini-2.5-flash-lite | LOI->RM64 | all_zero | 0.949 | 15.698 | 16.959 | 0.096 | 291 |
| hotpotqa | gemini-2.5-flash-lite | LOI->RM64 | no_unique_max | 0.964 | 30.285 | 32.158 | 0.344 | 291 |
| hotpotqa | gemini-2.5-flash | P1->RM@16 | all_zero | 0.893 | 17.938 | 15.889 | 0.309 | 81 |
| hotpotqa | gemini-2.5-flash | P1->RM@16 | no_unique_max | 0.932 | 20.704 | 18.630 | 0.481 | 81 |
| hotpotqa | gemini-2.5-flash | P1->RM@32 | all_zero | 0.930 | 22.877 | 20.753 | 0.309 | 81 |
| hotpotqa | gemini-2.5-flash | P1->RM@32 | no_unique_max | 0.988 | 28.407 | 26.185 | 0.481 | 81 |
| hotpotqa | gemini-2.5-flash | P1->RM64 | all_zero | 0.930 | 31.420 | 30.136 | 0.309 | 81 |
| hotpotqa | gemini-2.5-flash | P1->RM64 | no_unique_max | 1.000 | 41.728 | 40.864 | 0.481 | 81 |
| hotpotqa | gemini-2.5-flash | LOI->RM@16 | all_zero | 0.973 | 11.580 | 12.580 | 0.099 | 81 |
| hotpotqa | gemini-2.5-flash | LOI->RM@16 | no_unique_max | 0.957 | 17.309 | 18.235 | 0.457 | 81 |
| hotpotqa | gemini-2.5-flash | LOI->RM@32 | all_zero | 0.979 | 13.160 | 14.123 | 0.099 | 81 |
| hotpotqa | gemini-2.5-flash | LOI->RM@32 | no_unique_max | 0.988 | 24.617 | 25.432 | 0.457 | 81 |
| hotpotqa | gemini-2.5-flash | LOI->RM64 | all_zero | 0.992 | 15.864 | 17.160 | 0.099 | 81 |
| hotpotqa | gemini-2.5-flash | LOI->RM64 | no_unique_max | 1.000 | 37.272 | 39.383 | 0.457 | 81 |
| hotpotqa | gpt-6-luna | P1->RM@16 | all_zero | 0.748 | 18.645 | 16.039 | 0.323 | 155 |
| hotpotqa | gpt-6-luna | P1->RM@16 | no_unique_max | 0.817 | 22.155 | 19.510 | 0.542 | 155 |
| hotpotqa | gpt-6-luna | P1->RM@32 | all_zero | 0.784 | 23.806 | 21.032 | 0.323 | 155 |
| hotpotqa | gpt-6-luna | P1->RM@32 | no_unique_max | 0.868 | 30.826 | 27.955 | 0.542 | 155 |
| hotpotqa | gpt-6-luna | P1->RM64 | all_zero | 0.802 | 31.935 | 30.697 | 0.323 | 155 |
| hotpotqa | gpt-6-luna | P1->RM64 | no_unique_max | 0.894 | 44.368 | 44.245 | 0.542 | 155 |
| hotpotqa | gpt-6-luna | LOI->RM@16 | all_zero | 0.773 | 11.510 | 12.490 | 0.097 | 155 |
| hotpotqa | gpt-6-luna | LOI->RM@16 | no_unique_max | 0.842 | 18.426 | 19.310 | 0.529 | 155 |
| hotpotqa | gpt-6-luna | LOI->RM@32 | all_zero | 0.780 | 13.058 | 14.006 | 0.097 | 155 |
| hotpotqa | gpt-6-luna | LOI->RM@32 | no_unique_max | 0.889 | 26.890 | 27.471 | 0.529 | 155 |
| hotpotqa | gpt-6-luna | LOI->RM64 | all_zero | 0.773 | 15.677 | 16.935 | 0.097 | 155 |
| hotpotqa | gpt-6-luna | LOI->RM64 | no_unique_max | 0.914 | 40.245 | 43.394 | 0.529 | 155 |
| hotpotqa | gpt-6.1-terra | P1->RM@16 | all_zero | 0.807 | 20.750 | 18.672 | 0.484 | 64 |
| hotpotqa | gpt-6.1-terra | P1->RM@16 | no_unique_max | 0.853 | 22.500 | 20.406 | 0.594 | 64 |
| hotpotqa | gpt-6.1-terra | P1->RM@32 | all_zero | 0.905 | 28.500 | 26.359 | 0.484 | 64 |
| hotpotqa | gpt-6.1-terra | P1->RM@32 | no_unique_max | 0.971 | 32.000 | 29.797 | 0.594 | 64 |
| hotpotqa | gpt-6.1-terra | P1->RM64 | all_zero | 0.894 | 41.828 | 41.109 | 0.484 | 64 |
| hotpotqa | gpt-6.1-terra | P1->RM64 | no_unique_max | 0.969 | 48.406 | 47.938 | 0.594 | 64 |
| hotpotqa | gpt-6.1-terra | LOI->RM@16 | all_zero | 0.891 | 10.750 | 11.750 | 0.047 | 64 |
| hotpotqa | gpt-6.1-terra | LOI->RM@16 | no_unique_max | 0.853 | 20.500 | 21.422 | 0.656 | 64 |
| hotpotqa | gpt-6.1-terra | LOI->RM@32 | all_zero | 0.896 | 11.500 | 12.453 | 0.047 | 64 |
| hotpotqa | gpt-6.1-terra | LOI->RM@32 | no_unique_max | 0.971 | 31.000 | 31.750 | 0.656 | 64 |
| hotpotqa | gpt-6.1-terra | LOI->RM64 | all_zero | 0.904 | 12.781 | 13.891 | 0.047 | 64 |
| hotpotqa | gpt-6.1-terra | LOI->RM64 | no_unique_max | 0.969 | 49.047 | 51.719 | 0.656 | 64 |
| musique | claude-haiku-5-5 | P1->RM@16 | all_zero | 0.757 | 24.436 | 21.493 | 0.032 | 747 |
| musique | claude-haiku-5-5 | P1->RM@16 | no_unique_max | 0.798 | 35.339 | 32.395 | 0.714 | 747 |
| musique | claude-haiku-5-5 | P1->RM@32 | all_zero | 0.759 | 24.950 | 22.007 | 0.032 | 747 |
| musique | claude-haiku-5-5 | P1->RM@32 | no_unique_max | 0.903 | 46.755 | 43.811 | 0.714 | 747 |
| musique | claude-haiku-5-5 | P1->RM64 | all_zero | 0.758 | 25.906 | 23.035 | 0.032 | 747 |
| musique | claude-haiku-5-5 | P1->RM64 | no_unique_max | 0.945 | 68.565 | 66.640 | 0.714 | 747 |
| musique | claude-haiku-5-5 | LOI->RM@16 | all_zero | 0.790 | 30.710 | 31.710 | 0.671 | 747 |
| musique | claude-haiku-5-5 | LOI->RM@16 | no_unique_max | 0.791 | 31.031 | 32.031 | 0.691 | 747 |
| musique | claude-haiku-5-5 | LOI->RM@32 | all_zero | 0.903 | 41.440 | 42.440 | 0.671 | 747 |
| musique | claude-haiku-5-5 | LOI->RM@32 | no_unique_max | 0.904 | 42.083 | 43.083 | 0.691 | 747 |
| musique | claude-haiku-5-5 | LOI->RM64 | all_zero | 0.943 | 62.047 | 63.898 | 0.671 | 747 |
| musique | claude-haiku-5-5 | LOI->RM64 | no_unique_max | 0.944 | 63.312 | 65.183 | 0.691 | 747 |
| musique | gemini-2.5-flash-lite | P1->RM@16 | all_zero | 0.770 | 24.058 | 22.123 | 0.071 | 774 |
| musique | gemini-2.5-flash-lite | P1->RM@16 | no_unique_max | 0.909 | 31.128 | 29.193 | 0.513 | 774 |
| musique | gemini-2.5-flash-lite | P1->RM@32 | all_zero | 0.774 | 25.195 | 23.260 | 0.071 | 774 |
| musique | gemini-2.5-flash-lite | P1->RM@32 | no_unique_max | 0.949 | 39.335 | 37.399 | 0.513 | 774 |
| musique | gemini-2.5-flash-lite | P1->RM64 | all_zero | 0.776 | 27.397 | 25.534 | 0.071 | 774 |
| musique | gemini-2.5-flash-lite | P1->RM64 | no_unique_max | 0.977 | 55.231 | 53.810 | 0.513 | 774 |
| musique | gemini-2.5-flash-lite | LOI->RM@16 | all_zero | 0.926 | 23.399 | 24.417 | 0.214 | 774 |
| musique | gemini-2.5-flash-lite | LOI->RM@16 | no_unique_max | 0.925 | 24.350 | 25.368 | 0.274 | 774 |
| musique | gemini-2.5-flash-lite | LOI->RM@32 | all_zero | 0.952 | 26.831 | 27.849 | 0.214 | 774 |
| musique | gemini-2.5-flash-lite | LOI->RM@32 | no_unique_max | 0.958 | 28.733 | 29.751 | 0.274 | 774 |
| musique | gemini-2.5-flash-lite | LOI->RM64 | all_zero | 0.966 | 33.479 | 34.712 | 0.214 | 774 |
| musique | gemini-2.5-flash-lite | LOI->RM64 | no_unique_max | 0.977 | 37.224 | 38.516 | 0.274 | 774 |
| musique | gemini-2.5-flash | P1->RM@16 | all_zero | 0.848 | 25.048 | 23.048 | 0.129 | 62 |
| musique | gemini-2.5-flash | P1->RM@16 | no_unique_max | 0.911 | 29.177 | 27.177 | 0.387 | 62 |
| musique | gemini-2.5-flash | P1->RM@32 | all_zero | 0.856 | 27.113 | 25.113 | 0.129 | 62 |
| musique | gemini-2.5-flash | P1->RM@32 | no_unique_max | 0.944 | 35.371 | 33.371 | 0.387 | 62 |
| musique | gemini-2.5-flash | P1->RM64 | all_zero | 0.873 | 31.097 | 29.242 | 0.129 | 62 |
| musique | gemini-2.5-flash | P1->RM64 | no_unique_max | 0.968 | 47.355 | 45.758 | 0.387 | 62 |
| musique | gemini-2.5-flash | LOI->RM@16 | all_zero | 0.952 | 21.790 | 22.790 | 0.113 | 62 |
| musique | gemini-2.5-flash | LOI->RM@16 | no_unique_max | 0.952 | 23.597 | 24.597 | 0.226 | 62 |
| musique | gemini-2.5-flash | LOI->RM@32 | all_zero | 0.960 | 23.597 | 24.597 | 0.113 | 62 |
| musique | gemini-2.5-flash | LOI->RM@32 | no_unique_max | 0.960 | 27.210 | 28.210 | 0.226 | 62 |
| musique | gemini-2.5-flash | LOI->RM64 | all_zero | 0.968 | 27.097 | 28.210 | 0.113 | 62 |
| musique | gemini-2.5-flash | LOI->RM64 | no_unique_max | 0.968 | 34.210 | 35.435 | 0.226 | 62 |
| musique | gpt-6-luna | P1->RM@16 | all_zero | 0.642 | 25.096 | 22.183 | 0.075 | 602 |
| musique | gpt-6-luna | P1->RM@16 | no_unique_max | 0.822 | 33.309 | 30.395 | 0.588 | 602 |
| musique | gpt-6-luna | P1->RM@32 | all_zero | 0.651 | 26.292 | 23.379 | 0.075 | 602 |
| musique | gpt-6-luna | P1->RM@32 | no_unique_max | 0.858 | 42.718 | 39.804 | 0.588 | 602 |
| musique | gpt-6-luna | P1->RM64 | all_zero | 0.654 | 28.412 | 25.771 | 0.075 | 602 |
| musique | gpt-6-luna | P1->RM64 | no_unique_max | 0.882 | 60.156 | 58.621 | 0.588 | 602 |
| musique | gpt-6-luna | LOI->RM@16 | all_zero | 0.796 | 21.721 | 22.794 | 0.113 | 602 |
| musique | gpt-6-luna | LOI->RM@16 | no_unique_max | 0.830 | 26.053 | 27.126 | 0.384 | 602 |
| musique | gpt-6-luna | LOI->RM@32 | all_zero | 0.812 | 23.528 | 24.601 | 0.113 | 602 |
| musique | gpt-6-luna | LOI->RM@32 | no_unique_max | 0.868 | 32.193 | 33.266 | 0.384 | 602 |
| musique | gpt-6-luna | LOI->RM64 | all_zero | 0.816 | 26.822 | 28.216 | 0.113 | 602 |
| musique | gpt-6-luna | LOI->RM64 | no_unique_max | 0.890 | 43.610 | 45.542 | 0.384 | 602 |
| musique | gpt-6.1-terra | P1->RM@16 | all_zero | 0.852 | 25.074 | 23.074 | 0.130 | 54 |
| musique | gpt-6.1-terra | P1->RM@16 | no_unique_max | 0.907 | 28.333 | 26.333 | 0.333 | 54 |
| musique | gpt-6.1-terra | P1->RM@32 | all_zero | 0.870 | 27.148 | 25.148 | 0.130 | 54 |
| musique | gpt-6.1-terra | P1->RM@32 | no_unique_max | 0.981 | 33.667 | 31.667 | 0.333 | 54 |
| musique | gpt-6.1-terra | P1->RM64 | all_zero | 0.870 | 31.167 | 29.296 | 0.130 | 54 |
| musique | gpt-6.1-terra | P1->RM64 | no_unique_max | 0.981 | 44.000 | 42.333 | 0.333 | 54 |
| musique | gpt-6.1-terra | LOI->RM@16 | all_zero | 0.889 | 21.481 | 22.481 | 0.093 | 54 |
| musique | gpt-6.1-terra | LOI->RM@16 | no_unique_max | 0.898 | 23.556 | 24.556 | 0.222 | 54 |
| musique | gpt-6.1-terra | LOI->RM@32 | all_zero | 0.944 | 22.963 | 23.963 | 0.093 | 54 |
| musique | gpt-6.1-terra | LOI->RM@32 | no_unique_max | 0.963 | 27.111 | 28.111 | 0.222 | 54 |
| musique | gpt-6.1-terra | LOI->RM64 | all_zero | 0.944 | 25.833 | 26.926 | 0.093 | 54 |
| musique | gpt-6.1-terra | LOI->RM64 | no_unique_max | 0.981 | 33.204 | 35.222 | 0.222 | 54 |
| qasper | claude-haiku-5-5 | P1->RM@16 | all_zero | 0.528 | 14.306 | 12.293 | 0.082 | 294 |
| qasper | claude-haiku-5-5 | P1->RM@16 | no_unique_max | 0.702 | 22.741 | 20.670 | 0.609 | 294 |
| qasper | claude-haiku-5-5 | P1->RM@32 | all_zero | 0.543 | 15.612 | 13.558 | 0.082 | 294 |
| qasper | claude-haiku-5-5 | P1->RM@32 | no_unique_max | 0.764 | 32.483 | 30.139 | 0.609 | 294 |
| qasper | claude-haiku-5-5 | P1->RM64 | all_zero | 0.540 | 17.677 | 16.031 | 0.082 | 294 |
| qasper | claude-haiku-5-5 | P1->RM64 | no_unique_max | 0.779 | 48.180 | 48.684 | 0.609 | 294 |
| qasper | claude-haiku-5-5 | LOI->RM@16 | all_zero | 0.773 | 14.626 | 15.595 | 0.289 | 294 |
| qasper | claude-haiku-5-5 | LOI->RM@16 | no_unique_max | 0.773 | 15.932 | 16.891 | 0.371 | 294 |
| qasper | claude-haiku-5-5 | LOI->RM@32 | all_zero | 0.804 | 19.252 | 20.126 | 0.289 | 294 |
| qasper | claude-haiku-5-5 | LOI->RM@32 | no_unique_max | 0.812 | 21.864 | 22.680 | 0.371 | 294 |
| qasper | claude-haiku-5-5 | LOI->RM64 | all_zero | 0.809 | 26.578 | 28.935 | 0.289 | 294 |
| qasper | claude-haiku-5-5 | LOI->RM64 | no_unique_max | 0.822 | 31.449 | 33.993 | 0.371 | 294 |
| qasper | gemini-2.5-flash-lite | P1->RM@16 | all_zero | 0.643 | 14.105 | 12.102 | 0.069 | 304 |
| qasper | gemini-2.5-flash-lite | P1->RM@16 | no_unique_max | 0.828 | 21.053 | 19.000 | 0.503 | 304 |
| qasper | gemini-2.5-flash-lite | P1->RM@32 | all_zero | 0.634 | 15.211 | 13.181 | 0.069 | 304 |
| qasper | gemini-2.5-flash-lite | P1->RM@32 | no_unique_max | 0.853 | 29.105 | 26.868 | 0.503 | 304 |
| qasper | gemini-2.5-flash-lite | P1->RM64 | all_zero | 0.638 | 17.135 | 15.293 | 0.069 | 304 |
| qasper | gemini-2.5-flash-lite | P1->RM64 | no_unique_max | 0.875 | 43.092 | 42.220 | 0.503 | 304 |
| qasper | gemini-2.5-flash-lite | LOI->RM@16 | all_zero | 0.831 | 13.158 | 14.132 | 0.197 | 304 |
| qasper | gemini-2.5-flash-lite | LOI->RM@16 | no_unique_max | 0.831 | 14.526 | 15.497 | 0.283 | 304 |
| qasper | gemini-2.5-flash-lite | LOI->RM@32 | all_zero | 0.856 | 16.316 | 17.204 | 0.197 | 304 |
| qasper | gemini-2.5-flash-lite | LOI->RM@32 | no_unique_max | 0.849 | 19.053 | 19.898 | 0.283 | 304 |
| qasper | gemini-2.5-flash-lite | LOI->RM64 | all_zero | 0.864 | 21.796 | 23.207 | 0.197 | 304 |
| qasper | gemini-2.5-flash-lite | LOI->RM64 | no_unique_max | 0.862 | 26.875 | 28.493 | 0.283 | 304 |
| qasper | gemini-2.5-flash | P1->RM@16 | all_zero | 0.669 | 14.243 | 12.240 | 0.078 | 296 |
| qasper | gemini-2.5-flash | P1->RM@16 | no_unique_max | 0.839 | 20.297 | 18.260 | 0.456 | 296 |
| qasper | gemini-2.5-flash | P1->RM@32 | all_zero | 0.659 | 15.486 | 13.446 | 0.078 | 296 |
| qasper | gemini-2.5-flash | P1->RM@32 | no_unique_max | 0.857 | 27.595 | 25.399 | 0.456 | 296 |
| qasper | gemini-2.5-flash | P1->RM64 | all_zero | 0.664 | 17.568 | 15.818 | 0.078 | 296 |
| qasper | gemini-2.5-flash | P1->RM64 | no_unique_max | 0.873 | 39.318 | 39.321 | 0.456 | 296 |
| qasper | gemini-2.5-flash | LOI->RM@16 | all_zero | 0.849 | 13.081 | 14.057 | 0.193 | 296 |
| qasper | gemini-2.5-flash | LOI->RM@16 | no_unique_max | 0.855 | 14.324 | 15.297 | 0.270 | 296 |
| qasper | gemini-2.5-flash | LOI->RM@32 | all_zero | 0.865 | 16.162 | 17.091 | 0.193 | 296 |
| qasper | gemini-2.5-flash | LOI->RM@32 | no_unique_max | 0.867 | 18.649 | 19.544 | 0.270 | 296 |
| qasper | gemini-2.5-flash | LOI->RM64 | all_zero | 0.875 | 20.733 | 22.966 | 0.193 | 296 |
| qasper | gemini-2.5-flash | LOI->RM64 | no_unique_max | 0.881 | 25.243 | 27.777 | 0.270 | 296 |
| qasper | gpt-6-luna | P1->RM@16 | all_zero | 0.565 | 14.538 | 12.527 | 0.096 | 260 |
| qasper | gpt-6-luna | P1->RM@16 | no_unique_max | 0.755 | 22.662 | 20.562 | 0.604 | 260 |
| qasper | gpt-6-luna | P1->RM@32 | all_zero | 0.565 | 16.077 | 14.042 | 0.096 | 260 |
| qasper | gpt-6-luna | P1->RM@32 | no_unique_max | 0.810 | 32.323 | 29.985 | 0.604 | 260 |
| qasper | gpt-6-luna | P1->RM64 | all_zero | 0.570 | 18.765 | 16.981 | 0.096 | 260 |
| qasper | gpt-6-luna | P1->RM64 | no_unique_max | 0.835 | 49.035 | 48.373 | 0.604 | 260 |
| qasper | gpt-6-luna | LOI->RM@16 | all_zero | 0.747 | 14.738 | 15.704 | 0.296 | 260 |
| qasper | gpt-6-luna | LOI->RM@16 | no_unique_max | 0.762 | 16.769 | 17.715 | 0.423 | 260 |
| qasper | gpt-6-luna | LOI->RM@32 | all_zero | 0.795 | 19.477 | 20.354 | 0.296 | 260 |
| qasper | gpt-6-luna | LOI->RM@32 | no_unique_max | 0.817 | 23.538 | 24.365 | 0.423 | 260 |
| qasper | gpt-6-luna | LOI->RM64 | all_zero | 0.807 | 27.715 | 29.373 | 0.296 | 260 |
| qasper | gpt-6-luna | LOI->RM64 | no_unique_max | 0.835 | 35.312 | 37.242 | 0.423 | 260 |
| qasper | gpt-6.1-terra | P1->RM@16 | all_zero | 0.533 | 14.674 | 12.663 | 0.105 | 258 |
| qasper | gpt-6.1-terra | P1->RM@16 | no_unique_max | 0.700 | 22.798 | 20.713 | 0.612 | 258 |
| qasper | gpt-6.1-terra | P1->RM@32 | all_zero | 0.529 | 16.349 | 14.295 | 0.105 | 258 |
| qasper | gpt-6.1-terra | P1->RM@32 | no_unique_max | 0.711 | 32.597 | 30.264 | 0.612 | 258 |
| qasper | gpt-6.1-terra | P1->RM64 | all_zero | 0.527 | 19.248 | 17.481 | 0.105 | 258 |
| qasper | gpt-6.1-terra | P1->RM64 | no_unique_max | 0.764 | 49.500 | 48.895 | 0.612 | 258 |
| qasper | gpt-6.1-terra | LOI->RM@16 | all_zero | 0.725 | 14.388 | 15.430 | 0.279 | 258 |
| qasper | gpt-6.1-terra | LOI->RM@16 | no_unique_max | 0.730 | 16.124 | 17.147 | 0.388 | 258 |
| qasper | gpt-6.1-terra | LOI->RM@32 | all_zero | 0.723 | 18.853 | 19.775 | 0.279 | 258 |
| qasper | gpt-6.1-terra | LOI->RM@32 | no_unique_max | 0.733 | 22.326 | 23.209 | 0.388 | 258 |
| qasper | gpt-6.1-terra | LOI->RM64 | all_zero | 0.768 | 26.609 | 28.283 | 0.279 | 258 |
| qasper | gpt-6.1-terra | LOI->RM64 | no_unique_max | 0.778 | 33.062 | 35.000 | 0.388 | 258 |
