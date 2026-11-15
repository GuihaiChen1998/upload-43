# paper.main.all.symfever.full_correct

Primary = tie-aware top-1 on the common valid set of each cell (methods V1, P1, MEXGEN_LOO, LOI, RM@k); diff/CI = paired bootstrap (2000) of method − V1. top1_e2e keeps invalid-reference rows as all-zero ties (chance floor).

## Methods

| dataset | model | method | n | n_invalid_ref | n_common | top1_common | diff_vs_V1 | ci_lo | ci_hi | top1_e2e | all_zero_valid | calls | cost | random_top1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| symfever | claude-haiku-5-5 | V1 | 1022 | 0 | 1022 | 0.945 |  |  |  | 0.945 | 0.011 | 0.992 | 0.992 | 0.100 |
| symfever | claude-haiku-5-5 | P1 | 1022 | 0 | 1022 | 0.825 | -0.120 | -0.143 | -0.098 | 0.825 | 0.101 | 12.776 | 11.000 | 0.100 |
| symfever | claude-haiku-5-5 | MEXGEN_LOO | 1022 | 0 | 1022 | 0.825 | -0.120 | -0.143 | -0.098 | 0.825 | 0.101 | 12.776 | 11.000 | 0.100 |
| symfever | claude-haiku-5-5 | LOI | 1022 | 0 | 1022 | 0.892 | -0.053 | -0.071 | -0.035 | 0.892 | 0.048 | 9.660 | 11.000 | 0.100 |
| symfever | claude-haiku-5-5 | RM@8 | 1022 | 0 | 1022 | 0.853 | -0.092 | -0.113 | -0.071 | 0.853 | 0.044 | 9.000 | 8.959 | 0.100 |
| symfever | claude-haiku-5-5 | RM@10 | 1022 | 0 | 1022 | 0.871 | -0.074 | -0.094 | -0.054 | 0.871 | 0.031 | 11.000 | 10.938 | 0.100 |
| symfever | claude-haiku-5-5 | RM@16 | 1022 | 0 | 1022 | 0.906 | -0.039 | -0.058 | -0.022 | 0.906 | 0.013 | 17.000 | 16.854 | 0.100 |
| symfever | claude-haiku-5-5 | RM@32 | 1022 | 0 | 1022 | 0.939 | -0.006 | -0.022 | 0.009 | 0.939 | 0.003 | 33.000 | 32.481 | 0.100 |
| symfever | claude-haiku-5-5 | RM64 | 1022 | 0 | 1022 | 0.947 | 0.002 | -0.014 | 0.017 | 0.947 | 0.001 | 59.854 | 63.031 | 0.100 |
| symfever | gemini-2.5-flash-lite | V1 | 1061 | 0 | 1061 | 0.978 |  |  |  | 0.978 | 0.000 | 0.992 | 0.992 | 0.100 |
| symfever | gemini-2.5-flash-lite | P1 | 1061 | 0 | 1061 | 0.830 | -0.148 | -0.171 | -0.125 | 0.830 | 0.113 | 12.739 | 11.000 | 0.100 |
| symfever | gemini-2.5-flash-lite | MEXGEN_LOO | 1061 | 0 | 1061 | 0.830 | -0.148 | -0.171 | -0.125 | 0.830 | 0.113 | 12.739 | 11.000 | 0.100 |
| symfever | gemini-2.5-flash-lite | LOI | 1061 | 0 | 1061 | 0.883 | -0.095 | -0.111 | -0.078 | 0.883 | 0.019 | 9.157 | 11.000 | 0.100 |
| symfever | gemini-2.5-flash-lite | RM@8 | 1061 | 0 | 1061 | 0.872 | -0.106 | -0.127 | -0.087 | 0.872 | 0.034 | 9.000 | 8.960 | 0.100 |
| symfever | gemini-2.5-flash-lite | RM@10 | 1061 | 0 | 1061 | 0.899 | -0.079 | -0.098 | -0.061 | 0.899 | 0.021 | 11.000 | 10.942 | 0.100 |
| symfever | gemini-2.5-flash-lite | RM@16 | 1061 | 0 | 1061 | 0.928 | -0.050 | -0.067 | -0.034 | 0.928 | 0.008 | 17.000 | 16.859 | 0.100 |
| symfever | gemini-2.5-flash-lite | RM@32 | 1061 | 0 | 1061 | 0.945 | -0.033 | -0.047 | -0.018 | 0.945 | 0.004 | 33.000 | 32.484 | 0.100 |
| symfever | gemini-2.5-flash-lite | RM64 | 1061 | 0 | 1061 | 0.945 | -0.033 | -0.048 | -0.017 | 0.945 | 0.001 | 59.680 | 63.026 | 0.100 |
| symfever | gemini-2.5-flash | V1 | 1064 | 0 | 1064 | 0.978 |  |  |  | 0.978 | 0.000 | 1.000 | 1.000 | 0.100 |
| symfever | gemini-2.5-flash | P1 | 1064 | 0 | 1064 | 0.825 | -0.153 | -0.176 | -0.131 | 0.825 | 0.114 | 12.914 | 11.000 | 0.100 |
| symfever | gemini-2.5-flash | MEXGEN_LOO | 1064 | 0 | 1064 | 0.825 | -0.153 | -0.176 | -0.131 | 0.825 | 0.114 | 12.914 | 11.000 | 0.100 |
| symfever | gemini-2.5-flash | LOI | 1064 | 0 | 1064 | 0.884 | -0.094 | -0.111 | -0.078 | 0.884 | 0.017 | 9.514 | 11.000 | 0.100 |
| symfever | gpt-6-luna | V1 | 764 | 0 | 764 | 0.979 |  |  |  | 0.979 | 0.000 | 0.993 | 0.993 | 0.100 |
| symfever | gpt-6-luna | P1 | 764 | 0 | 764 | 0.844 | -0.135 | -0.159 | -0.113 | 0.844 | 0.045 | 12.508 | 11.000 | 0.100 |
| symfever | gpt-6-luna | MEXGEN_LOO | 764 | 0 | 764 | 0.844 | -0.135 | -0.159 | -0.113 | 0.844 | 0.045 | 12.508 | 11.000 | 0.100 |
| symfever | gpt-6-luna | LOI | 764 | 0 | 764 | 0.922 | -0.057 | -0.073 | -0.041 | 0.922 | 0.054 | 7.492 | 11.000 | 0.100 |
| symfever | gpt-6-luna | RM@8 | 764 | 0 | 764 | 0.879 | -0.100 | -0.121 | -0.079 | 0.879 | 0.048 | 9.000 | 8.963 | 0.100 |
| symfever | gpt-6-luna | RM@10 | 764 | 0 | 764 | 0.901 | -0.078 | -0.098 | -0.059 | 0.901 | 0.039 | 11.000 | 10.944 | 0.100 |
| symfever | gpt-6-luna | RM@16 | 764 | 0 | 764 | 0.929 | -0.049 | -0.068 | -0.032 | 0.929 | 0.027 | 17.000 | 16.855 | 0.100 |
| symfever | gpt-6-luna | RM@32 | 764 | 0 | 764 | 0.946 | -0.033 | -0.047 | -0.019 | 0.946 | 0.012 | 33.000 | 32.479 | 0.100 |
| symfever | gpt-6-luna | RM64 | 764 | 0 | 764 | 0.962 | -0.017 | -0.031 | -0.003 | 0.962 | 0.009 | 57.988 | 63.001 | 0.100 |
| symfever | gpt-6.1-terra | V1 | 1047 | 0 | 1047 | 0.957 |  |  |  | 0.957 | 0.011 | 0.992 | 0.992 | 0.100 |
| symfever | gpt-6.1-terra | P1 | 1047 | 0 | 1047 | 0.819 | -0.138 | -0.160 | -0.116 | 0.819 | 0.099 | 12.732 | 11.000 | 0.100 |
| symfever | gpt-6.1-terra | MEXGEN_LOO | 1047 | 0 | 1047 | 0.819 | -0.138 | -0.160 | -0.116 | 0.819 | 0.099 | 12.732 | 11.000 | 0.100 |
| symfever | gpt-6.1-terra | LOI | 1047 | 0 | 1047 | 0.894 | -0.063 | -0.079 | -0.047 | 0.894 | 0.044 | 9.108 | 11.000 | 0.100 |

## Coverage / fidelity (common valid set)

| dataset | model | method | n_common | coverage | fidelity | V1_on_covered | V1_on_uncovered | unique_max_share | top1_unique | top1_tied | spontaneous_change | gap_vs_V1 | share_gap_all_zero |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| symfever | claude-haiku-5-5 | P1 | 1022 | 0.899 | 0.906 | 0.959 | 0.819 | 0.873 | 0.996 | 0.290 | 0.026 | 0.120 | 0.604 |
| symfever | claude-haiku-5-5 | LOI | 1022 | 0.952 | 0.932 | 0.949 | 0.874 | 0.890 | 0.997 | 0.410 | nan | 0.053 | 0.702 |
| symfever | claude-haiku-5-5 | MEXGEN_LOO | 1022 | 0.899 | 0.906 | 0.959 | 0.819 | 0.873 | 0.996 | 0.290 | 0.026 | 0.120 | 0.604 |
| symfever | gemini-2.5-flash-lite | P1 | 1061 | 0.887 | 0.923 | 0.989 | 0.887 | 0.887 | 0.996 | 0.343 | 0.012 | 0.148 | 0.601 |
| symfever | gemini-2.5-flash-lite | LOI | 1061 | 0.981 | 0.898 | 0.979 | 0.942 | 0.838 | 0.994 | 0.403 | nan | 0.095 | 0.167 |
| symfever | gemini-2.5-flash-lite | MEXGEN_LOO | 1061 | 0.887 | 0.923 | 0.989 | 0.887 | 0.887 | 0.996 | 0.343 | 0.012 | 0.148 | 0.601 |
| symfever | gemini-2.5-flash | P1 | 1064 | 0.886 | 0.918 | 0.990 | 0.889 | 0.883 | 0.995 | 0.334 | 0.016 | 0.153 | 0.586 |
| symfever | gemini-2.5-flash | LOI | 1064 | 0.983 | 0.898 | 0.978 | 0.963 | 0.834 | 0.995 | 0.407 | nan | 0.094 | 0.155 |
| symfever | gemini-2.5-flash | MEXGEN_LOO | 1064 | 0.886 | 0.918 | 0.990 | 0.889 | 0.883 | 0.995 | 0.334 | 0.016 | 0.153 | 0.586 |
| symfever | gpt-6-luna | P1 | 764 | 0.955 | 0.879 | 0.986 | 0.821 | 0.837 | 0.997 | 0.272 | 0.067 | 0.135 | 0.238 |
| symfever | gpt-6-luna | LOI | 764 | 0.946 | 0.969 | 0.981 | 0.947 | 0.949 | 0.999 | 0.412 | nan | 0.057 | 0.800 |
| symfever | gpt-6-luna | MEXGEN_LOO | 764 | 0.955 | 0.879 | 0.986 | 0.821 | 0.837 | 0.997 | 0.272 | 0.067 | 0.135 | 0.238 |
| symfever | gpt-6.1-terra | P1 | 1047 | 0.901 | 0.899 | 0.973 | 0.808 | 0.861 | 0.994 | 0.309 | 0.046 | 0.138 | 0.511 |
| symfever | gpt-6.1-terra | LOI | 1047 | 0.956 | 0.931 | 0.961 | 0.878 | 0.884 | 0.995 | 0.436 | nan | 0.063 | 0.544 |
| symfever | gpt-6.1-terra | MEXGEN_LOO | 1047 | 0.901 | 0.899 | 0.973 | 0.808 | 0.861 | 0.994 | 0.309 | 0.046 | 0.138 | 0.511 |

## Routing: cheap estimator, escalate to RM when uninformative

| dataset | model | route | rule | top1 | calls | cost | escalated | n_common |
|---|---|---|---|---|---|---|---|---|
| symfever | claude-haiku-5-5 | P1->RM@16 | all_zero | 0.862 | 14.388 | 12.604 | 0.101 | 1022 |
| symfever | claude-haiku-5-5 | P1->RM@16 | no_unique_max | 0.908 | 16.220 | 14.419 | 0.215 | 1022 |
| symfever | claude-haiku-5-5 | P1->RM@32 | all_zero | 0.873 | 16.001 | 14.179 | 0.101 | 1022 |
| symfever | claude-haiku-5-5 | P1->RM@32 | no_unique_max | 0.941 | 19.664 | 17.774 | 0.215 | 1022 |
| symfever | claude-haiku-5-5 | P1->RM64 | all_zero | 0.878 | 18.815 | 17.270 | 0.101 | 1022 |
| symfever | claude-haiku-5-5 | P1->RM64 | no_unique_max | 0.948 | 25.382 | 24.330 | 0.215 | 1022 |
| symfever | claude-haiku-5-5 | LOI->RM@16 | all_zero | 0.915 | 10.428 | 11.760 | 0.048 | 1022 |
| symfever | claude-haiku-5-5 | LOI->RM@16 | no_unique_max | 0.925 | 12.103 | 13.425 | 0.153 | 1022 |
| symfever | claude-haiku-5-5 | LOI->RM@32 | all_zero | 0.927 | 11.195 | 12.515 | 0.048 | 1022 |
| symfever | claude-haiku-5-5 | LOI->RM@32 | no_unique_max | 0.945 | 14.545 | 15.816 | 0.153 | 1022 |
| symfever | claude-haiku-5-5 | LOI->RM64 | all_zero | 0.929 | 12.387 | 13.971 | 0.048 | 1022 |
| symfever | claude-haiku-5-5 | LOI->RM64 | no_unique_max | 0.950 | 18.599 | 20.477 | 0.153 | 1022 |
| symfever | gemini-2.5-flash-lite | P1->RM@16 | all_zero | 0.875 | 14.549 | 12.792 | 0.113 | 1061 |
| symfever | gemini-2.5-flash-lite | P1->RM@16 | no_unique_max | 0.932 | 16.147 | 14.376 | 0.213 | 1061 |
| symfever | gemini-2.5-flash-lite | P1->RM@32 | all_zero | 0.886 | 16.358 | 14.557 | 0.113 | 1061 |
| symfever | gemini-2.5-flash-lite | P1->RM@32 | no_unique_max | 0.947 | 19.555 | 17.703 | 0.213 | 1061 |
| symfever | gemini-2.5-flash-lite | P1->RM64 | all_zero | 0.885 | 19.339 | 18.026 | 0.113 | 1061 |
| symfever | gemini-2.5-flash-lite | P1->RM64 | no_unique_max | 0.947 | 25.197 | 24.205 | 0.213 | 1061 |
| symfever | gemini-2.5-flash-lite | LOI->RM@16 | all_zero | 0.896 | 9.459 | 11.297 | 0.019 | 1061 |
| symfever | gemini-2.5-flash-lite | LOI->RM@16 | no_unique_max | 0.930 | 12.008 | 13.827 | 0.178 | 1061 |
| symfever | gemini-2.5-flash-lite | LOI->RM@32 | all_zero | 0.898 | 9.761 | 11.592 | 0.019 | 1061 |
| symfever | gemini-2.5-flash-lite | LOI->RM@32 | no_unique_max | 0.945 | 14.858 | 16.616 | 0.178 | 1061 |
| symfever | gemini-2.5-flash-lite | LOI->RM64 | all_zero | 0.898 | 10.228 | 12.165 | 0.019 | 1061 |
| symfever | gemini-2.5-flash-lite | LOI->RM64 | no_unique_max | 0.945 | 19.540 | 22.074 | 0.178 | 1061 |
| symfever | gpt-6-luna | P1->RM@16 | all_zero | 0.862 | 13.220 | 11.707 | 0.045 | 764 |
| symfever | gpt-6-luna | P1->RM@16 | no_unique_max | 0.937 | 15.712 | 14.175 | 0.200 | 764 |
| symfever | gpt-6-luna | P1->RM@32 | all_zero | 0.862 | 13.932 | 12.399 | 0.045 | 764 |
| symfever | gpt-6-luna | P1->RM@32 | no_unique_max | 0.951 | 18.916 | 17.302 | 0.200 | 764 |
| symfever | gpt-6-luna | P1->RM64 | all_zero | 0.867 | 15.153 | 13.763 | 0.045 | 764 |
| symfever | gpt-6-luna | P1->RM64 | no_unique_max | 0.965 | 23.880 | 23.423 | 0.200 | 764 |
| symfever | gpt-6-luna | LOI->RM@16 | all_zero | 0.946 | 8.351 | 11.851 | 0.054 | 764 |
| symfever | gpt-6-luna | LOI->RM@16 | no_unique_max | 0.948 | 9.126 | 12.620 | 0.102 | 764 |
| symfever | gpt-6-luna | LOI->RM@32 | all_zero | 0.953 | 9.209 | 12.688 | 0.054 | 764 |
| symfever | gpt-6-luna | LOI->RM@32 | no_unique_max | 0.955 | 10.759 | 14.219 | 0.102 | 764 |
| symfever | gpt-6-luna | LOI->RM64 | all_zero | 0.957 | 10.401 | 14.330 | 0.054 | 764 |
| symfever | gpt-6-luna | LOI->RM64 | no_unique_max | 0.965 | 13.283 | 17.347 | 0.102 | 764 |
