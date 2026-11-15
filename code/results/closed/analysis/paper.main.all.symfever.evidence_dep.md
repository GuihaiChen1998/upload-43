# paper.main.all.symfever.evidence_dep

Primary = tie-aware top-1 on the common valid set of each cell (methods V1, P1, MEXGEN_LOO, LOI, RM@k); diff/CI = paired bootstrap (2000) of method − V1. top1_e2e keeps invalid-reference rows as all-zero ties (chance floor).

## Methods

| dataset | model | method | n | n_invalid_ref | n_common | top1_common | diff_vs_V1 | ci_lo | ci_hi | top1_e2e | all_zero_valid | calls | cost | random_top1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| symfever | claude-haiku-5-5 | V1 | 678 | 0 | 678 | 0.973 |  |  |  | 0.973 | 0.006 | 0.994 | 0.994 | 0.100 |
| symfever | claude-haiku-5-5 | P1 | 678 | 0 | 678 | 0.882 | -0.091 | -0.115 | -0.067 | 0.882 | 0.031 | 12.739 | 11.000 | 0.100 |
| symfever | claude-haiku-5-5 | MEXGEN_LOO | 678 | 0 | 678 | 0.882 | -0.091 | -0.115 | -0.067 | 0.882 | 0.031 | 12.739 | 11.000 | 0.100 |
| symfever | claude-haiku-5-5 | LOI | 678 | 0 | 678 | 0.928 | -0.044 | -0.063 | -0.026 | 0.928 | 0.056 | 9.550 | 11.000 | 0.100 |
| symfever | claude-haiku-5-5 | RM@8 | 678 | 0 | 678 | 0.894 | -0.079 | -0.102 | -0.058 | 0.894 | 0.032 | 9.000 | 8.954 | 0.100 |
| symfever | claude-haiku-5-5 | RM@10 | 678 | 0 | 678 | 0.913 | -0.059 | -0.082 | -0.040 | 0.913 | 0.021 | 11.000 | 10.935 | 0.100 |
| symfever | claude-haiku-5-5 | RM@16 | 678 | 0 | 678 | 0.943 | -0.029 | -0.048 | -0.013 | 0.943 | 0.007 | 17.000 | 16.855 | 0.100 |
| symfever | claude-haiku-5-5 | RM@32 | 678 | 0 | 678 | 0.969 | -0.004 | -0.019 | 0.010 | 0.969 | 0.001 | 33.000 | 32.472 | 0.100 |
| symfever | claude-haiku-5-5 | RM64 | 678 | 0 | 678 | 0.978 | 0.005 | -0.008 | 0.019 | 0.978 | 0.001 | 59.662 | 63.022 | 0.100 |
| symfever | gemini-2.5-flash-lite | V1 | 742 | 0 | 742 | 0.990 |  |  |  | 0.990 | 0.000 | 0.992 | 0.992 | 0.100 |
| symfever | gemini-2.5-flash-lite | P1 | 742 | 0 | 742 | 0.883 | -0.108 | -0.131 | -0.086 | 0.883 | 0.043 | 12.662 | 11.000 | 0.100 |
| symfever | gemini-2.5-flash-lite | MEXGEN_LOO | 742 | 0 | 742 | 0.883 | -0.108 | -0.131 | -0.086 | 0.883 | 0.043 | 12.662 | 11.000 | 0.100 |
| symfever | gemini-2.5-flash-lite | LOI | 742 | 0 | 742 | 0.927 | -0.063 | -0.081 | -0.047 | 0.927 | 0.020 | 8.829 | 11.000 | 0.100 |
| symfever | gemini-2.5-flash-lite | RM@8 | 742 | 0 | 742 | 0.912 | -0.079 | -0.100 | -0.059 | 0.912 | 0.020 | 9.000 | 8.961 | 0.100 |
| symfever | gemini-2.5-flash-lite | RM@10 | 742 | 0 | 742 | 0.941 | -0.049 | -0.067 | -0.033 | 0.941 | 0.012 | 11.000 | 10.942 | 0.100 |
| symfever | gemini-2.5-flash-lite | RM@16 | 742 | 0 | 742 | 0.969 | -0.021 | -0.034 | -0.009 | 0.969 | 0.005 | 17.000 | 16.858 | 0.100 |
| symfever | gemini-2.5-flash-lite | RM@32 | 742 | 0 | 742 | 0.979 | -0.011 | -0.023 | 0.000 | 0.979 | 0.003 | 33.000 | 32.488 | 0.100 |
| symfever | gemini-2.5-flash-lite | RM64 | 742 | 0 | 742 | 0.979 | -0.012 | -0.023 | -0.001 | 0.979 | 0.001 | 59.336 | 63.018 | 0.100 |
| symfever | gemini-2.5-flash | V1 | 750 | 0 | 750 | 0.991 |  |  |  | 0.991 | 0.000 | 1.000 | 1.000 | 0.100 |
| symfever | gemini-2.5-flash | P1 | 750 | 0 | 750 | 0.871 | -0.120 | -0.143 | -0.097 | 0.871 | 0.047 | 12.879 | 11.000 | 0.100 |
| symfever | gemini-2.5-flash | MEXGEN_LOO | 750 | 0 | 750 | 0.871 | -0.120 | -0.143 | -0.097 | 0.871 | 0.047 | 12.879 | 11.000 | 0.100 |
| symfever | gemini-2.5-flash | LOI | 750 | 0 | 750 | 0.929 | -0.062 | -0.079 | -0.045 | 0.929 | 0.019 | 9.317 | 11.000 | 0.100 |
| symfever | gpt-6-luna | V1 | 764 | 0 | 764 | 0.979 |  |  |  | 0.979 | 0.000 | 0.993 | 0.993 | 0.100 |
| symfever | gpt-6-luna | P1 | 764 | 0 | 764 | 0.844 | -0.135 | -0.159 | -0.113 | 0.844 | 0.045 | 12.508 | 11.000 | 0.100 |
| symfever | gpt-6-luna | MEXGEN_LOO | 764 | 0 | 764 | 0.844 | -0.135 | -0.159 | -0.113 | 0.844 | 0.045 | 12.508 | 11.000 | 0.100 |
| symfever | gpt-6-luna | LOI | 764 | 0 | 764 | 0.922 | -0.057 | -0.073 | -0.041 | 0.922 | 0.054 | 7.492 | 11.000 | 0.100 |
| symfever | gpt-6-luna | RM@8 | 764 | 0 | 764 | 0.879 | -0.100 | -0.121 | -0.079 | 0.879 | 0.048 | 9.000 | 8.963 | 0.100 |
| symfever | gpt-6-luna | RM@10 | 764 | 0 | 764 | 0.901 | -0.078 | -0.098 | -0.059 | 0.901 | 0.039 | 11.000 | 10.944 | 0.100 |
| symfever | gpt-6-luna | RM@16 | 764 | 0 | 764 | 0.929 | -0.049 | -0.068 | -0.032 | 0.929 | 0.027 | 17.000 | 16.855 | 0.100 |
| symfever | gpt-6-luna | RM@32 | 764 | 0 | 764 | 0.946 | -0.033 | -0.047 | -0.019 | 0.946 | 0.012 | 33.000 | 32.479 | 0.100 |
| symfever | gpt-6-luna | RM64 | 764 | 0 | 764 | 0.962 | -0.017 | -0.031 | -0.003 | 0.962 | 0.009 | 57.988 | 63.001 | 0.100 |
| symfever | gpt-6.1-terra | V1 | 722 | 0 | 722 | 0.969 |  |  |  | 0.969 | 0.014 | 0.990 | 0.990 | 0.100 |
| symfever | gpt-6.1-terra | P1 | 722 | 0 | 722 | 0.859 | -0.110 | -0.134 | -0.086 | 0.859 | 0.037 | 12.629 | 11.000 | 0.100 |
| symfever | gpt-6.1-terra | MEXGEN_LOO | 722 | 0 | 722 | 0.859 | -0.110 | -0.134 | -0.086 | 0.859 | 0.037 | 12.629 | 11.000 | 0.100 |
| symfever | gpt-6.1-terra | LOI | 722 | 0 | 722 | 0.924 | -0.045 | -0.064 | -0.027 | 0.924 | 0.048 | 8.758 | 11.000 | 0.100 |

## Coverage / fidelity (common valid set)

| dataset | model | method | n_common | coverage | fidelity | V1_on_covered | V1_on_uncovered | unique_max_share | top1_unique | top1_tied | spontaneous_change | gap_vs_V1 | share_gap_all_zero |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| symfever | claude-haiku-5-5 | P1 | 678 | 0.969 | 0.907 | 0.975 | 0.905 | 0.868 | 1.000 | 0.299 | 0.029 | 0.091 | 0.275 |
| symfever | claude-haiku-5-5 | LOI | 678 | 0.944 | 0.978 | 0.975 | 0.928 | 0.961 | 1.000 | 0.427 | nan | 0.044 | 1.048 |
| symfever | claude-haiku-5-5 | MEXGEN_LOO | 678 | 0.969 | 0.907 | 0.975 | 0.905 | 0.868 | 1.000 | 0.299 | 0.029 | 0.091 | 0.275 |
| symfever | gemini-2.5-flash-lite | P1 | 742 | 0.957 | 0.918 | 0.993 | 0.938 | 0.875 | 1.000 | 0.345 | 0.015 | 0.108 | 0.336 |
| symfever | gemini-2.5-flash-lite | LOI | 742 | 0.980 | 0.944 | 0.991 | 0.967 | 0.908 | 0.998 | 0.405 | nan | 0.063 | 0.276 |
| symfever | gemini-2.5-flash-lite | MEXGEN_LOO | 742 | 0.957 | 0.918 | 0.993 | 0.938 | 0.875 | 1.000 | 0.345 | 0.015 | 0.108 | 0.336 |
| symfever | gemini-2.5-flash | P1 | 750 | 0.953 | 0.909 | 0.995 | 0.914 | 0.866 | 0.998 | 0.333 | 0.022 | 0.120 | 0.318 |
| symfever | gemini-2.5-flash | LOI | 750 | 0.981 | 0.945 | 0.991 | 1.000 | 0.906 | 1.000 | 0.412 | nan | 0.062 | 0.272 |
| symfever | gemini-2.5-flash | MEXGEN_LOO | 750 | 0.953 | 0.909 | 0.995 | 0.914 | 0.866 | 0.998 | 0.333 | 0.022 | 0.120 | 0.318 |
| symfever | gpt-6-luna | P1 | 764 | 0.955 | 0.879 | 0.986 | 0.821 | 0.837 | 0.997 | 0.272 | 0.067 | 0.135 | 0.238 |
| symfever | gpt-6-luna | LOI | 764 | 0.946 | 0.969 | 0.981 | 0.947 | 0.949 | 0.999 | 0.412 | nan | 0.057 | 0.800 |
| symfever | gpt-6-luna | MEXGEN_LOO | 764 | 0.955 | 0.879 | 0.986 | 0.821 | 0.837 | 0.997 | 0.272 | 0.067 | 0.135 | 0.238 |
| symfever | gpt-6.1-terra | P1 | 722 | 0.963 | 0.889 | 0.975 | 0.833 | 0.840 | 0.998 | 0.312 | 0.056 | 0.110 | 0.249 |
| symfever | gpt-6.1-terra | LOI | 722 | 0.952 | 0.966 | 0.974 | 0.883 | 0.939 | 1.000 | 0.450 | nan | 0.045 | 0.845 |
| symfever | gpt-6.1-terra | MEXGEN_LOO | 722 | 0.963 | 0.889 | 0.975 | 0.833 | 0.840 | 0.998 | 0.312 | 0.056 | 0.110 | 0.249 |

## Routing: cheap estimator, escalate to RM when uninformative

| dataset | model | route | rule | top1 | calls | cost | escalated | n_common |
|---|---|---|---|---|---|---|---|---|
| symfever | claude-haiku-5-5 | P1->RM@16 | all_zero | 0.894 | 13.235 | 11.496 | 0.031 | 678 |
| symfever | claude-haiku-5-5 | P1->RM@16 | no_unique_max | 0.946 | 15.288 | 13.531 | 0.159 | 678 |
| symfever | claude-haiku-5-5 | P1->RM@32 | all_zero | 0.897 | 13.730 | 11.976 | 0.031 | 678 |
| symfever | claude-haiku-5-5 | P1->RM@32 | no_unique_max | 0.972 | 17.836 | 16.013 | 0.159 | 678 |
| symfever | claude-haiku-5-5 | P1->RM64 | all_zero | 0.900 | 14.577 | 12.928 | 0.031 | 678 |
| symfever | claude-haiku-5-5 | P1->RM64 | no_unique_max | 0.979 | 22.022 | 20.851 | 0.159 | 678 |
| symfever | claude-haiku-5-5 | LOI->RM@16 | all_zero | 0.957 | 10.447 | 11.888 | 0.056 | 678 |
| symfever | claude-haiku-5-5 | LOI->RM@16 | no_unique_max | 0.964 | 11.037 | 12.476 | 0.093 | 678 |
| symfever | claude-haiku-5-5 | LOI->RM@32 | all_zero | 0.969 | 11.344 | 12.770 | 0.056 | 678 |
| symfever | claude-haiku-5-5 | LOI->RM@32 | no_unique_max | 0.976 | 12.524 | 13.931 | 0.093 | 678 |
| symfever | claude-haiku-5-5 | LOI->RM64 | all_zero | 0.973 | 12.774 | 14.469 | 0.056 | 678 |
| symfever | claude-haiku-5-5 | LOI->RM64 | no_unique_max | 0.982 | 14.957 | 16.757 | 0.093 | 678 |
| symfever | gemini-2.5-flash-lite | P1->RM@16 | all_zero | 0.904 | 13.352 | 11.683 | 0.043 | 742 |
| symfever | gemini-2.5-flash-lite | P1->RM@16 | no_unique_max | 0.973 | 15.271 | 13.585 | 0.163 | 742 |
| symfever | gemini-2.5-flash-lite | P1->RM@32 | all_zero | 0.908 | 14.042 | 12.356 | 0.043 | 742 |
| symfever | gemini-2.5-flash-lite | P1->RM@32 | no_unique_max | 0.981 | 17.880 | 16.132 | 0.163 | 742 |
| symfever | gemini-2.5-flash-lite | P1->RM64 | all_zero | 0.904 | 15.086 | 13.686 | 0.043 | 742 |
| symfever | gemini-2.5-flash-lite | P1->RM64 | no_unique_max | 0.980 | 22.093 | 21.101 | 0.163 | 742 |
| symfever | gemini-2.5-flash-lite | LOI->RM@16 | all_zero | 0.940 | 9.152 | 11.321 | 0.020 | 742 |
| symfever | gemini-2.5-flash-lite | LOI->RM@16 | no_unique_max | 0.974 | 10.597 | 12.755 | 0.111 | 742 |
| symfever | gemini-2.5-flash-lite | LOI->RM@32 | all_zero | 0.941 | 9.476 | 11.637 | 0.020 | 742 |
| symfever | gemini-2.5-flash-lite | LOI->RM@32 | no_unique_max | 0.981 | 12.365 | 14.487 | 0.111 | 742 |
| symfever | gemini-2.5-flash-lite | LOI->RM64 | all_zero | 0.942 | 9.961 | 12.251 | 0.020 | 742 |
| symfever | gemini-2.5-flash-lite | LOI->RM64 | no_unique_max | 0.979 | 15.119 | 17.879 | 0.111 | 742 |
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
