# paper.main.test.qasper

Primary = tie-aware top-1 on the common valid set of each cell (methods V1, P1, MEXGEN_LOO, LOI, RM@k); diff/CI = paired bootstrap (2000) of method − V1. top1_e2e keeps invalid-reference rows as all-zero ties (chance floor).

## Methods

| dataset | model | method | n | n_invalid_ref | n_common | top1_common | diff_vs_V1 | ci_lo | ci_hi | top1_e2e | all_zero_valid | calls | cost | random_top1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
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
