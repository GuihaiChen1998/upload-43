# K3 k3pilot_v2 · gemini-2.5-flash-lite

## Premise (repeats 0-2)
| dataset | cond | redundancy | n_bases | n_eval_3of3 | full_3of3 | full_2of3 | full_spont_change | parse_fail | drop_ap_still_correct | drop_ap_answer_change | drop_ap_acc_drop | drop_group_still_correct | drop_group_answer_change | drop_group_acc_drop |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | F | 0 | 50 | 49 | 0.980 | 1.000 | 0.040 | 0.036 | 0.220 | 0.800 | 0.773 | 0.220 | 0.800 | 0.773 |
| hotpotqa | C | 1 | 50 | 49 | 0.980 | 0.980 | 0.020 | 0.011 | 0.973 | 0.087 | 0.007 | 0.193 | 0.807 | 0.787 |
| hotpotqa | FF | 0 | 50 | 49 | 0.980 | 1.000 | 0.080 | 0.053 | 0.173 | 0.827 | 0.820 | 0.173 | 0.827 | 0.820 |
| hotpotqa | CF | 1 | 50 | 50 | 1.000 | 1.000 | 0.040 | 0.022 | 0.993 | 0.033 | 0.007 | 0.227 | 0.787 | 0.773 |
| hotpotqa | CC | 2 | 50 | 46 | 0.920 | 0.940 | 0.160 | 0.011 | 0.973 | 0.080 | -0.027 | 0.200 | 0.833 | 0.747 |
| musique | F | 0 | 50 | 45 | 0.900 | 0.940 | 0.140 | 0.044 | 0.087 | 0.940 | 0.853 | 0.087 | 0.940 | 0.853 |
| musique | C | 1 | 50 | 49 | 0.980 | 0.980 | 0.040 | 0.024 | 0.940 | 0.100 | 0.040 | 0.100 | 0.900 | 0.880 |
| musique | FF | 0 | 50 | 47 | 0.940 | 0.940 | 0.040 | 0.031 | 0.120 | 0.920 | 0.827 | 0.120 | 0.920 | 0.827 |
| musique | CF | 1 | 50 | 48 | 0.960 | 0.980 | 0.060 | 0.022 | 0.940 | 0.093 | 0.040 | 0.080 | 0.940 | 0.900 |
| musique | CC | 2 | 50 | 48 | 0.960 | 0.960 | 0.020 | 0.029 | 0.880 | 0.140 | 0.080 | 0.087 | 0.933 | 0.873 |

## Methods (repeat 3, premise-evaluable variants of each condition)
| dataset | method | cond | n | group_top1 | group_floor | group_top1_cc | ap_top1 | gold_top1 | group_evid | nonzero_any | all_zero | pos_mass_copies | full_ctx_change_r3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | LOI | F | 49 | 0.742 | 0.091 | 0.717 | 0.742 | 0.825 | 0.837 | 0.878 | 0.122 |  |  |
| hotpotqa | LOI | C | 49 | 0.801 | 0.182 | 0.757 | 0.400 | 0.878 | 0.857 | 0.898 | 0.102 | 0.500 |  |
| hotpotqa | LOI | FF | 49 | 0.704 | 0.083 | 0.677 | 0.704 | 0.789 | 0.796 | 0.837 | 0.163 |  |  |
| hotpotqa | LOI | CF | 50 | 0.807 | 0.167 | 0.768 | 0.403 | 0.875 | 0.860 | 0.900 | 0.100 | 0.500 |  |
| hotpotqa | LOI | CC | 46 | 0.883 | 0.250 | 0.843 | 0.294 | 0.944 | 0.935 | 0.978 | 0.022 | 0.667 |  |
| hotpotqa | MEXGEN_LOO | F | 49 | 0.766 | 0.091 | 0.743 | 0.766 | 0.869 | 0.776 | 0.878 | 0.122 |  |  |
| hotpotqa | MEXGEN_LOO | C | 49 | 0.183 | 0.182 | 0.001 | 0.086 | 0.356 | 0.102 | 0.265 | 0.735 | 0.500 |  |
| hotpotqa | MEXGEN_LOO | FF | 49 | 0.713 | 0.083 | 0.686 | 0.713 | 0.820 | 0.776 | 0.857 | 0.143 |  |  |
| hotpotqa | MEXGEN_LOO | CF | 50 | 0.143 | 0.167 | -0.028 | 0.063 | 0.339 | 0.080 | 0.320 | 0.680 | 0.750 |  |
| hotpotqa | MEXGEN_LOO | CC | 46 | 0.211 | 0.250 | -0.052 | 0.064 | 0.405 | 0.109 | 0.283 | 0.717 | 0.867 |  |
| hotpotqa | P1 | F | 49 | 0.691 | 0.091 | 0.660 | 0.691 | 0.798 | 0.776 | 0.878 | 0.122 |  | 0.027 |
| hotpotqa | P1 | C | 49 | 0.164 | 0.182 | -0.022 | 0.083 | 0.334 | 0.102 | 0.265 | 0.735 | 0.500 | 0.041 |
| hotpotqa | P1 | FF | 49 | 0.653 | 0.083 | 0.622 | 0.653 | 0.755 | 0.776 | 0.857 | 0.143 |  | 0.027 |
| hotpotqa | P1 | CF | 50 | 0.143 | 0.167 | -0.028 | 0.063 | 0.339 | 0.080 | 0.320 | 0.680 | 0.750 | 0.027 |
| hotpotqa | P1 | CC | 46 | 0.225 | 0.250 | -0.033 | 0.062 | 0.422 | 0.130 | 0.304 | 0.696 | 0.889 | 0.087 |
| hotpotqa | RM64:banzhaf_exact | F | 49 | 0.857 | 0.091 | 0.843 | 0.857 | 0.959 | 0.939 | 1.000 | 0.000 |  |  |
| hotpotqa | RM64:banzhaf_exact | C | 49 | 0.857 | 0.182 | 0.825 | 0.449 | 1.000 | 0.857 | 1.000 | 0.000 | 0.479 |  |
| hotpotqa | RM64:banzhaf_exact | FF | 49 | 0.837 | 0.083 | 0.822 | 0.837 | 0.959 | 0.898 | 1.000 | 0.000 |  |  |
| hotpotqa | RM64:banzhaf_exact | CF | 50 | 0.800 | 0.167 | 0.760 | 0.450 | 0.960 | 0.900 | 1.000 | 0.000 | 0.490 |  |
| hotpotqa | RM64:banzhaf_exact | CC | 46 | 0.761 | 0.250 | 0.681 | 0.239 | 0.957 | 0.674 | 1.000 | 0.000 | 0.663 |  |
| hotpotqa | RM64:banzhaf_f1 | F | 49 | 0.837 | 0.091 | 0.820 | 0.837 | 0.959 | 0.959 | 1.000 | 0.000 |  |  |
| hotpotqa | RM64:banzhaf_f1 | C | 49 | 0.857 | 0.182 | 0.825 | 0.449 | 1.000 | 0.878 | 1.000 | 0.000 | 0.480 |  |
| hotpotqa | RM64:banzhaf_f1 | FF | 49 | 0.857 | 0.083 | 0.844 | 0.857 | 0.980 | 0.918 | 1.000 | 0.000 |  |  |
| hotpotqa | RM64:banzhaf_f1 | CF | 50 | 0.820 | 0.167 | 0.784 | 0.450 | 0.960 | 0.920 | 1.000 | 0.000 | 0.481 |  |
| hotpotqa | RM64:banzhaf_f1 | CC | 46 | 0.783 | 0.250 | 0.710 | 0.239 | 0.978 | 0.804 | 1.000 | 0.000 | 0.648 |  |
| hotpotqa | RM64:linear_exact | F | 49 | 0.857 | 0.091 | 0.843 | 0.857 | 0.959 | 0.959 | 1.000 | 0.000 |  |  |
| hotpotqa | RM64:linear_exact | C | 49 | 0.837 | 0.182 | 0.800 | 0.408 | 1.000 | 0.898 | 1.000 | 0.000 | 0.495 |  |
| hotpotqa | RM64:linear_exact | FF | 49 | 0.837 | 0.083 | 0.822 | 0.837 | 0.959 | 0.898 | 1.000 | 0.000 |  |  |
| hotpotqa | RM64:linear_exact | CF | 50 | 0.780 | 0.167 | 0.736 | 0.460 | 0.940 | 0.880 | 1.000 | 0.000 | 0.484 |  |
| hotpotqa | RM64:linear_exact | CC | 46 | 0.761 | 0.250 | 0.681 | 0.239 | 0.935 | 0.674 | 1.000 | 0.000 | 0.685 |  |
| hotpotqa | V1 | F | 49 | 0.643 | 0.091 | 0.607 | 0.643 | 0.969 | 0.980 | 1.000 | 0.000 |  |  |
| hotpotqa | V1 | C | 49 | 0.680 | 0.182 | 0.609 | 0.335 | 0.978 | 0.959 | 1.000 | 0.000 | 0.511 |  |
| hotpotqa | V1 | FF | 49 | 0.602 | 0.083 | 0.566 | 0.602 | 0.949 | 0.959 | 1.000 | 0.000 |  |  |
| hotpotqa | V1 | CF | 50 | 0.690 | 0.167 | 0.628 | 0.355 | 0.965 | 0.940 | 0.980 | 0.020 | 0.479 |  |
| hotpotqa | V1 | CC | 46 | 0.719 | 0.250 | 0.625 | 0.228 | 0.966 | 0.978 | 1.000 | 0.000 | 0.678 |  |
| musique | LOI | F | 45 | 0.681 | 0.048 | 0.664 | 0.681 | 0.750 | 0.689 | 0.711 | 0.289 |  |  |
| musique | LOI | C | 49 | 0.758 | 0.095 | 0.732 | 0.379 | 0.801 | 0.755 | 0.796 | 0.204 | 0.500 |  |
| musique | LOI | FF | 47 | 0.740 | 0.046 | 0.728 | 0.740 | 0.799 | 0.766 | 0.787 | 0.213 |  |  |
| musique | LOI | CF | 48 | 0.728 | 0.091 | 0.700 | 0.364 | 0.784 | 0.729 | 0.750 | 0.250 | 0.500 |  |
| musique | LOI | CC | 48 | 0.781 | 0.137 | 0.746 | 0.260 | 0.829 | 0.771 | 0.792 | 0.208 | 0.667 |  |
| musique | MEXGEN_LOO | F | 45 | 0.700 | 0.048 | 0.685 | 0.700 | 0.846 | 0.911 | 0.911 | 0.089 |  |  |
| musique | MEXGEN_LOO | C | 49 | 0.078 | 0.095 | -0.019 | 0.042 | 0.343 | 0.041 | 0.469 | 0.531 | 0.250 |  |
| musique | MEXGEN_LOO | FF | 47 | 0.644 | 0.046 | 0.627 | 0.644 | 0.779 | 0.872 | 0.915 | 0.085 |  |  |
| musique | MEXGEN_LOO | CF | 48 | 0.100 | 0.091 | 0.009 | 0.051 | 0.343 | 0.125 | 0.438 | 0.562 | 0.389 |  |
| musique | MEXGEN_LOO | CC | 48 | 0.089 | 0.137 | -0.055 | 0.033 | 0.328 | 0.167 | 0.479 | 0.521 | 0.583 |  |
| musique | P1 | F | 45 | 0.636 | 0.048 | 0.618 | 0.636 | 0.751 | 0.911 | 0.911 | 0.089 |  | 0.059 |
| musique | P1 | C | 49 | 0.078 | 0.095 | -0.019 | 0.042 | 0.315 | 0.041 | 0.469 | 0.531 | 0.250 | 0.048 |
| musique | P1 | FF | 47 | 0.565 | 0.046 | 0.544 | 0.565 | 0.708 | 0.872 | 0.915 | 0.085 |  | 0.014 |
| musique | P1 | CF | 48 | 0.086 | 0.091 | -0.006 | 0.037 | 0.296 | 0.125 | 0.438 | 0.562 | 0.333 | 0.076 |
| musique | P1 | CC | 48 | 0.103 | 0.137 | -0.039 | 0.036 | 0.324 | 0.167 | 0.479 | 0.521 | 0.583 | 0.042 |
| musique | RM64:banzhaf_exact | F | 45 | 0.835 | 0.048 | 0.827 | 0.835 | 0.906 | 0.867 | 0.956 | 0.044 |  |  |
| musique | RM64:banzhaf_exact | C | 49 | 0.612 | 0.095 | 0.571 | 0.367 | 0.918 | 0.898 | 1.000 | 0.000 | 0.452 |  |
| musique | RM64:banzhaf_exact | FF | 47 | 0.830 | 0.046 | 0.822 | 0.830 | 0.915 | 0.915 | 1.000 | 0.000 |  |  |
| musique | RM64:banzhaf_exact | CF | 48 | 0.583 | 0.091 | 0.542 | 0.354 | 0.875 | 0.771 | 1.000 | 0.000 | 0.467 |  |
| musique | RM64:banzhaf_exact | CC | 48 | 0.500 | 0.137 | 0.421 | 0.146 | 0.917 | 0.562 | 1.000 | 0.000 | 0.665 |  |
| musique | RM64:banzhaf_f1 | F | 45 | 0.868 | 0.048 | 0.861 | 0.868 | 0.982 | 0.956 | 0.978 | 0.022 |  |  |
| musique | RM64:banzhaf_f1 | C | 49 | 0.571 | 0.095 | 0.526 | 0.306 | 0.939 | 0.939 | 1.000 | 0.000 | 0.464 |  |
| musique | RM64:banzhaf_f1 | FF | 47 | 0.809 | 0.046 | 0.799 | 0.809 | 0.957 | 0.957 | 1.000 | 0.000 |  |  |
| musique | RM64:banzhaf_f1 | CF | 48 | 0.562 | 0.091 | 0.519 | 0.333 | 0.938 | 0.833 | 1.000 | 0.000 | 0.440 |  |
| musique | RM64:banzhaf_f1 | CC | 48 | 0.521 | 0.137 | 0.445 | 0.167 | 0.958 | 0.625 | 1.000 | 0.000 | 0.652 |  |
| musique | RM64:linear_exact | F | 45 | 0.824 | 0.048 | 0.816 | 0.824 | 0.895 | 0.867 | 0.956 | 0.044 |  |  |
| musique | RM64:linear_exact | C | 49 | 0.633 | 0.095 | 0.594 | 0.347 | 0.939 | 0.816 | 1.000 | 0.000 | 0.452 |  |
| musique | RM64:linear_exact | FF | 47 | 0.894 | 0.046 | 0.889 | 0.894 | 0.957 | 0.936 | 1.000 | 0.000 |  |  |
| musique | RM64:linear_exact | CF | 48 | 0.583 | 0.091 | 0.542 | 0.312 | 0.917 | 0.792 | 1.000 | 0.000 | 0.451 |  |
| musique | RM64:linear_exact | CC | 48 | 0.521 | 0.137 | 0.445 | 0.188 | 0.917 | 0.479 | 1.000 | 0.000 | 0.662 |  |
| musique | V1 | F | 45 | 0.413 | 0.048 | 0.384 | 0.413 | 0.917 | 0.956 | 1.000 | 0.000 |  |  |
| musique | V1 | C | 49 | 0.518 | 0.095 | 0.467 | 0.210 | 0.950 | 0.980 | 0.980 | 0.020 | 0.594 |  |
| musique | V1 | FF | 47 | 0.449 | 0.046 | 0.422 | 0.449 | 0.945 | 0.979 | 1.000 | 0.000 |  |  |
| musique | V1 | CF | 48 | 0.534 | 0.091 | 0.487 | 0.285 | 0.914 | 0.958 | 0.979 | 0.021 | 0.478 |  |
| musique | V1 | CC | 48 | 0.505 | 0.137 | 0.426 | 0.190 | 0.969 | 0.958 | 1.000 | 0.000 | 0.630 |  |

## FF / CF / CC curve on one population (bases evaluable in all three)
| dataset | method | cond | n | group_top1 | group_floor | group_top1_cc | group_evid | all_zero | pos_mass_copies |
|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | LOI | FF | 46 | 0.745 | 0.083 | 0.721 | 0.848 | 0.109 |  |
| hotpotqa | LOI | CF | 46 | 0.844 | 0.167 | 0.813 | 0.913 | 0.043 | 0.500 |
| hotpotqa | LOI | CC | 46 | 0.883 | 0.250 | 0.843 | 0.935 | 0.022 | 0.667 |
| hotpotqa | MEXGEN_LOO | FF | 46 | 0.741 | 0.083 | 0.717 | 0.783 | 0.152 |  |
| hotpotqa | MEXGEN_LOO | CF | 46 | 0.146 | 0.167 | -0.024 | 0.065 | 0.717 | 0.833 |
| hotpotqa | MEXGEN_LOO | CC | 46 | 0.211 | 0.250 | -0.052 | 0.109 | 0.717 | 0.867 |
| hotpotqa | P1 | FF | 46 | 0.679 | 0.083 | 0.650 | 0.783 | 0.152 |  |
| hotpotqa | P1 | CF | 46 | 0.146 | 0.167 | -0.024 | 0.065 | 0.717 | 0.833 |
| hotpotqa | P1 | CC | 46 | 0.225 | 0.250 | -0.033 | 0.130 | 0.696 | 0.889 |
| hotpotqa | RM64:banzhaf_exact | FF | 46 | 0.870 | 0.083 | 0.858 | 0.935 | 0.000 |  |
| hotpotqa | RM64:banzhaf_exact | CF | 46 | 0.848 | 0.167 | 0.817 | 0.935 | 0.000 | 0.490 |
| hotpotqa | RM64:banzhaf_exact | CC | 46 | 0.761 | 0.250 | 0.681 | 0.674 | 0.000 | 0.663 |
| hotpotqa | RM64:banzhaf_f1 | FF | 46 | 0.891 | 0.083 | 0.881 | 0.957 | 0.000 |  |
| hotpotqa | RM64:banzhaf_f1 | CF | 46 | 0.870 | 0.167 | 0.843 | 0.957 | 0.000 | 0.476 |
| hotpotqa | RM64:banzhaf_f1 | CC | 46 | 0.783 | 0.250 | 0.710 | 0.804 | 0.000 | 0.648 |
| hotpotqa | RM64:linear_exact | FF | 46 | 0.870 | 0.083 | 0.858 | 0.935 | 0.000 |  |
| hotpotqa | RM64:linear_exact | CF | 46 | 0.826 | 0.167 | 0.791 | 0.913 | 0.000 | 0.487 |
| hotpotqa | RM64:linear_exact | CC | 46 | 0.761 | 0.250 | 0.681 | 0.674 | 0.000 | 0.685 |
| hotpotqa | V1 | FF | 46 | 0.620 | 0.083 | 0.585 | 0.978 | 0.000 |  |
| hotpotqa | V1 | CF | 46 | 0.725 | 0.167 | 0.670 | 0.978 | 0.000 | 0.500 |
| hotpotqa | V1 | CC | 46 | 0.719 | 0.250 | 0.625 | 0.978 | 0.000 | 0.678 |
| musique | LOI | FF | 45 | 0.729 | 0.046 | 0.716 | 0.756 | 0.222 |  |
| musique | LOI | CF | 45 | 0.750 | 0.091 | 0.725 | 0.756 | 0.222 | 0.500 |
| musique | LOI | CC | 45 | 0.766 | 0.137 | 0.729 | 0.756 | 0.222 | 0.667 |
| musique | MEXGEN_LOO | FF | 45 | 0.651 | 0.046 | 0.634 | 0.867 | 0.089 |  |
| musique | MEXGEN_LOO | CF | 45 | 0.103 | 0.091 | 0.013 | 0.089 | 0.600 | 0.250 |
| musique | MEXGEN_LOO | CC | 45 | 0.091 | 0.137 | -0.053 | 0.156 | 0.556 | 0.667 |
| musique | P1 | FF | 45 | 0.567 | 0.046 | 0.547 | 0.867 | 0.089 |  |
| musique | P1 | CF | 45 | 0.087 | 0.091 | -0.004 | 0.089 | 0.600 | 0.250 |
| musique | P1 | CC | 45 | 0.106 | 0.137 | -0.035 | 0.156 | 0.556 | 0.667 |
| musique | RM64:banzhaf_exact | FF | 45 | 0.822 | 0.046 | 0.814 | 0.911 | 0.000 |  |
| musique | RM64:banzhaf_exact | CF | 45 | 0.600 | 0.091 | 0.560 | 0.800 | 0.000 | 0.488 |
| musique | RM64:banzhaf_exact | CC | 45 | 0.467 | 0.137 | 0.382 | 0.556 | 0.000 | 0.656 |
| musique | RM64:banzhaf_f1 | FF | 45 | 0.800 | 0.046 | 0.790 | 0.956 | 0.000 |  |
| musique | RM64:banzhaf_f1 | CF | 45 | 0.578 | 0.091 | 0.535 | 0.867 | 0.000 | 0.450 |
| musique | RM64:banzhaf_f1 | CC | 45 | 0.489 | 0.137 | 0.408 | 0.622 | 0.000 | 0.643 |
| musique | RM64:linear_exact | FF | 45 | 0.889 | 0.046 | 0.884 | 0.933 | 0.000 |  |
| musique | RM64:linear_exact | CF | 45 | 0.600 | 0.091 | 0.560 | 0.844 | 0.000 | 0.469 |
| musique | RM64:linear_exact | CC | 45 | 0.489 | 0.137 | 0.408 | 0.467 | 0.000 | 0.652 |
| musique | V1 | FF | 45 | 0.450 | 0.046 | 0.424 | 0.978 | 0.000 |  |
| musique | V1 | CF | 45 | 0.529 | 0.091 | 0.481 | 0.956 | 0.022 | 0.488 |
| musique | V1 | CC | 45 | 0.509 | 0.137 | 0.431 | 0.956 | 0.000 | 0.628 |

## Paired redundancy effects (base-qid bootstrap 95% CI)
| dataset | method | contrast | metric | n_base | diff | ci_lo | ci_hi |
|---|---|---|---|---|---|---|---|
| hotpotqa | LOI | CF-FF | group_evid | 49 | 0.082 | 0.020 | 0.163 |
| hotpotqa | LOI | CF-FF | all_zero | 49 | -0.082 | -0.163 | -0.020 |
| hotpotqa | LOI | CF-FF | group_top1 | 49 | 0.116 | 0.054 | 0.187 |
| hotpotqa | LOI | CF-FF | group_top1_cc | 49 | 0.106 | 0.038 | 0.185 |
| hotpotqa | LOI | CF-FF | ap_top1 | 49 | -0.294 | -0.369 | -0.213 |
| hotpotqa | LOI | CC-CF | group_evid | 46 | 0.022 | -0.043 | 0.087 |
| hotpotqa | LOI | CC-CF | all_zero | 46 | -0.022 | -0.087 | 0.043 |
| hotpotqa | LOI | CC-CF | group_top1 | 46 | 0.038 | -0.020 | 0.098 |
| hotpotqa | LOI | CC-CF | group_top1_cc | 46 | 0.030 | -0.045 | 0.104 |
| hotpotqa | LOI | CC-CF | ap_top1 | 46 | -0.128 | -0.156 | -0.097 |
| hotpotqa | LOI | CC-FF | group_evid | 46 | 0.087 | 0.022 | 0.174 |
| hotpotqa | LOI | CC-FF | all_zero | 46 | -0.087 | -0.174 | -0.022 |
| hotpotqa | LOI | CC-FF | group_top1 | 46 | 0.138 | 0.069 | 0.218 |
| hotpotqa | LOI | CC-FF | group_top1_cc | 46 | 0.122 | 0.045 | 0.210 |
| hotpotqa | LOI | CC-FF | ap_top1 | 46 | -0.450 | -0.536 | -0.363 |
| hotpotqa | LOI | C-F | group_evid | 48 | 0.021 | -0.042 | 0.104 |
| hotpotqa | LOI | C-F | all_zero | 48 | -0.021 | -0.104 | 0.042 |
| hotpotqa | LOI | C-F | group_top1 | 48 | 0.058 | -0.004 | 0.127 |
| hotpotqa | LOI | C-F | group_top1_cc | 48 | 0.041 | -0.031 | 0.120 |
| hotpotqa | LOI | C-F | ap_top1 | 48 | -0.349 | -0.420 | -0.275 |
| hotpotqa | MEXGEN_LOO | CF-FF | group_evid | 49 | -0.694 | -0.837 | -0.551 |
| hotpotqa | MEXGEN_LOO | CF-FF | all_zero | 49 | 0.531 | 0.388 | 0.673 |
| hotpotqa | MEXGEN_LOO | CF-FF | group_top1 | 49 | -0.570 | -0.672 | -0.462 |
| hotpotqa | MEXGEN_LOO | CF-FF | group_top1_cc | 49 | -0.715 | -0.827 | -0.598 |
| hotpotqa | MEXGEN_LOO | CF-FF | ap_top1 | 49 | -0.650 | -0.754 | -0.537 |
| hotpotqa | MEXGEN_LOO | CC-CF | group_evid | 46 | 0.043 | -0.043 | 0.130 |
| hotpotqa | MEXGEN_LOO | CC-CF | all_zero | 46 | 0.000 | -0.087 | 0.087 |
| hotpotqa | MEXGEN_LOO | CC-CF | group_top1 | 46 | 0.064 | 0.031 | 0.095 |
| hotpotqa | MEXGEN_LOO | CC-CF | group_top1_cc | 46 | -0.028 | -0.072 | 0.010 |
| hotpotqa | MEXGEN_LOO | CC-CF | ap_top1 | 46 | 0.000 | -0.012 | 0.010 |
| hotpotqa | MEXGEN_LOO | CC-FF | group_evid | 46 | -0.674 | -0.804 | -0.522 |
| hotpotqa | MEXGEN_LOO | CC-FF | all_zero | 46 | 0.565 | 0.413 | 0.717 |
| hotpotqa | MEXGEN_LOO | CC-FF | group_top1 | 46 | -0.530 | -0.636 | -0.409 |
| hotpotqa | MEXGEN_LOO | CC-FF | group_top1_cc | 46 | -0.770 | -0.885 | -0.639 |
| hotpotqa | MEXGEN_LOO | CC-FF | ap_top1 | 46 | -0.677 | -0.783 | -0.556 |
| hotpotqa | MEXGEN_LOO | C-F | group_evid | 48 | -0.688 | -0.812 | -0.542 |
| hotpotqa | MEXGEN_LOO | C-F | all_zero | 48 | 0.625 | 0.479 | 0.771 |
| hotpotqa | MEXGEN_LOO | C-F | group_top1 | 48 | -0.591 | -0.705 | -0.471 |
| hotpotqa | MEXGEN_LOO | C-F | group_top1_cc | 48 | -0.750 | -0.877 | -0.616 |
| hotpotqa | MEXGEN_LOO | C-F | ap_top1 | 48 | -0.689 | -0.797 | -0.566 |
| hotpotqa | P1 | CF-FF | group_evid | 49 | -0.694 | -0.837 | -0.551 |
| hotpotqa | P1 | CF-FF | all_zero | 49 | 0.531 | 0.388 | 0.673 |
| hotpotqa | P1 | CF-FF | group_top1 | 49 | -0.511 | -0.621 | -0.394 |
| hotpotqa | P1 | CF-FF | group_top1_cc | 49 | -0.651 | -0.771 | -0.525 |
| hotpotqa | P1 | CF-FF | ap_top1 | 49 | -0.590 | -0.698 | -0.477 |
| hotpotqa | P1 | CC-CF | group_evid | 46 | 0.065 | -0.022 | 0.152 |
| hotpotqa | P1 | CC-CF | all_zero | 46 | -0.022 | -0.109 | 0.065 |
| hotpotqa | P1 | CC-CF | group_top1 | 46 | 0.079 | 0.036 | 0.128 |
| hotpotqa | P1 | CC-CF | group_top1_cc | 46 | -0.009 | -0.064 | 0.056 |
| hotpotqa | P1 | CC-CF | ap_top1 | 46 | -0.002 | -0.014 | 0.010 |
| hotpotqa | P1 | CC-FF | group_evid | 46 | -0.652 | -0.783 | -0.500 |
| hotpotqa | P1 | CC-FF | all_zero | 46 | 0.543 | 0.391 | 0.696 |
| hotpotqa | P1 | CC-FF | group_top1 | 46 | -0.454 | -0.575 | -0.337 |
| hotpotqa | P1 | CC-FF | group_top1_cc | 46 | -0.683 | -0.816 | -0.552 |
| hotpotqa | P1 | CC-FF | ap_top1 | 46 | -0.617 | -0.729 | -0.500 |
| hotpotqa | P1 | C-F | group_evid | 48 | -0.688 | -0.812 | -0.542 |
| hotpotqa | P1 | C-F | all_zero | 48 | 0.625 | 0.479 | 0.771 |
| hotpotqa | P1 | C-F | group_top1 | 48 | -0.533 | -0.652 | -0.412 |
| hotpotqa | P1 | C-F | group_top1_cc | 48 | -0.689 | -0.819 | -0.554 |
| hotpotqa | P1 | C-F | ap_top1 | 48 | -0.616 | -0.734 | -0.495 |
| hotpotqa | RM64:banzhaf_exact | CF-FF | group_evid | 49 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:banzhaf_exact | CF-FF | all_zero | 49 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:banzhaf_exact | CF-FF | group_top1 | 49 | -0.041 | -0.143 | 0.061 |
| hotpotqa | RM64:banzhaf_exact | CF-FF | group_top1_cc | 49 | -0.067 | -0.187 | 0.042 |
| hotpotqa | RM64:banzhaf_exact | CF-FF | ap_top1 | 49 | -0.398 | -0.541 | -0.255 |
| hotpotqa | RM64:banzhaf_exact | CC-CF | group_evid | 46 | -0.261 | -0.391 | -0.152 |
| hotpotqa | RM64:banzhaf_exact | CC-CF | all_zero | 46 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:banzhaf_exact | CC-CF | group_top1 | 46 | -0.087 | -0.174 | -0.022 |
| hotpotqa | RM64:banzhaf_exact | CC-CF | group_top1_cc | 46 | -0.136 | -0.255 | -0.041 |
| hotpotqa | RM64:banzhaf_exact | CC-CF | ap_top1 | 46 | -0.228 | -0.348 | -0.119 |
| hotpotqa | RM64:banzhaf_exact | CC-FF | group_evid | 46 | -0.261 | -0.391 | -0.152 |
| hotpotqa | RM64:banzhaf_exact | CC-FF | all_zero | 46 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:banzhaf_exact | CC-FF | group_top1 | 46 | -0.109 | -0.239 | 0.022 |
| hotpotqa | RM64:banzhaf_exact | CC-FF | group_top1_cc | 46 | -0.177 | -0.340 | -0.029 |
| hotpotqa | RM64:banzhaf_exact | CC-FF | ap_top1 | 46 | -0.630 | -0.772 | -0.489 |
| hotpotqa | RM64:banzhaf_exact | C-F | group_evid | 48 | -0.062 | -0.146 | 0.000 |
| hotpotqa | RM64:banzhaf_exact | C-F | all_zero | 48 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:banzhaf_exact | C-F | group_top1 | 48 | 0.021 | -0.042 | 0.083 |
| hotpotqa | RM64:banzhaf_exact | C-F | group_top1_cc | 48 | 0.008 | -0.066 | 0.089 |
| hotpotqa | RM64:banzhaf_exact | C-F | ap_top1 | 48 | -0.396 | -0.531 | -0.260 |
| hotpotqa | RM64:banzhaf_f1 | CF-FF | group_evid | 49 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:banzhaf_f1 | CF-FF | all_zero | 49 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:banzhaf_f1 | CF-FF | group_top1 | 49 | -0.041 | -0.122 | 0.041 |
| hotpotqa | RM64:banzhaf_f1 | CF-FF | group_top1_cc | 49 | -0.065 | -0.163 | 0.022 |
| hotpotqa | RM64:banzhaf_f1 | CF-FF | ap_top1 | 49 | -0.418 | -0.551 | -0.286 |
| hotpotqa | RM64:banzhaf_f1 | CC-CF | group_evid | 46 | -0.152 | -0.261 | -0.065 |
| hotpotqa | RM64:banzhaf_f1 | CC-CF | all_zero | 46 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:banzhaf_f1 | CC-CF | group_top1 | 46 | -0.087 | -0.174 | -0.022 |
| hotpotqa | RM64:banzhaf_f1 | CC-CF | group_top1_cc | 46 | -0.133 | -0.246 | -0.041 |
| hotpotqa | RM64:banzhaf_f1 | CC-CF | ap_top1 | 46 | -0.228 | -0.370 | -0.087 |
| hotpotqa | RM64:banzhaf_f1 | CC-FF | group_evid | 46 | -0.152 | -0.261 | -0.065 |
| hotpotqa | RM64:banzhaf_f1 | CC-FF | all_zero | 46 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:banzhaf_f1 | CC-FF | group_top1 | 46 | -0.109 | -0.217 | 0.000 |
| hotpotqa | RM64:banzhaf_f1 | CC-FF | group_top1_cc | 46 | -0.171 | -0.311 | -0.037 |
| hotpotqa | RM64:banzhaf_f1 | CC-FF | ap_top1 | 46 | -0.652 | -0.783 | -0.522 |
| hotpotqa | RM64:banzhaf_f1 | C-F | group_evid | 48 | -0.062 | -0.146 | 0.000 |
| hotpotqa | RM64:banzhaf_f1 | C-F | all_zero | 48 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:banzhaf_f1 | C-F | group_top1 | 48 | 0.042 | 0.000 | 0.104 |
| hotpotqa | RM64:banzhaf_f1 | C-F | group_top1_cc | 48 | 0.031 | -0.020 | 0.102 |
| hotpotqa | RM64:banzhaf_f1 | C-F | ap_top1 | 48 | -0.375 | -0.510 | -0.240 |
| hotpotqa | RM64:linear_exact | CF-FF | group_evid | 49 | -0.020 | -0.061 | 0.000 |
| hotpotqa | RM64:linear_exact | CF-FF | all_zero | 49 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:linear_exact | CF-FF | group_top1 | 49 | -0.061 | -0.163 | 0.020 |
| hotpotqa | RM64:linear_exact | CF-FF | group_top1_cc | 49 | -0.091 | -0.209 | 0.007 |
| hotpotqa | RM64:linear_exact | CF-FF | ap_top1 | 49 | -0.388 | -0.551 | -0.245 |
| hotpotqa | RM64:linear_exact | CC-CF | group_evid | 46 | -0.239 | -0.348 | -0.130 |
| hotpotqa | RM64:linear_exact | CC-CF | all_zero | 46 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:linear_exact | CC-CF | group_top1 | 46 | -0.065 | -0.152 | 0.022 |
| hotpotqa | RM64:linear_exact | CC-CF | group_top1_cc | 46 | -0.110 | -0.241 | 0.003 |
| hotpotqa | RM64:linear_exact | CC-CF | ap_top1 | 46 | -0.239 | -0.391 | -0.087 |
| hotpotqa | RM64:linear_exact | CC-FF | group_evid | 46 | -0.261 | -0.391 | -0.152 |
| hotpotqa | RM64:linear_exact | CC-FF | all_zero | 46 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:linear_exact | CC-FF | group_top1 | 46 | -0.109 | -0.217 | 0.000 |
| hotpotqa | RM64:linear_exact | CC-FF | group_top1_cc | 46 | -0.177 | -0.321 | -0.047 |
| hotpotqa | RM64:linear_exact | CC-FF | ap_top1 | 46 | -0.630 | -0.761 | -0.500 |
| hotpotqa | RM64:linear_exact | C-F | group_evid | 48 | -0.042 | -0.104 | 0.000 |
| hotpotqa | RM64:linear_exact | C-F | all_zero | 48 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:linear_exact | C-F | group_top1 | 48 | 0.000 | -0.083 | 0.083 |
| hotpotqa | RM64:linear_exact | C-F | group_top1_cc | 48 | -0.018 | -0.115 | 0.076 |
| hotpotqa | RM64:linear_exact | C-F | ap_top1 | 48 | -0.438 | -0.583 | -0.292 |
| hotpotqa | V1 | CF-FF | group_evid | 49 | 0.000 | -0.061 | 0.061 |
| hotpotqa | V1 | CF-FF | all_zero | 49 | 0.000 | 0.000 | 0.000 |
| hotpotqa | V1 | CF-FF | group_top1 | 49 | 0.099 | 0.037 | 0.163 |
| hotpotqa | V1 | CF-FF | group_top1_cc | 49 | 0.075 | 0.003 | 0.147 |
| hotpotqa | V1 | CF-FF | ap_top1 | 49 | -0.241 | -0.325 | -0.160 |
| hotpotqa | V1 | CC-CF | group_evid | 46 | 0.000 | -0.065 | 0.065 |
| hotpotqa | V1 | CC-CF | all_zero | 46 | 0.000 | 0.000 | 0.000 |
| hotpotqa | V1 | CC-CF | group_top1 | 46 | -0.006 | -0.064 | 0.047 |
| hotpotqa | V1 | CC-CF | group_top1_cc | 46 | -0.044 | -0.119 | 0.023 |
| hotpotqa | V1 | CC-CF | ap_top1 | 46 | -0.135 | -0.189 | -0.078 |
| hotpotqa | V1 | CC-FF | group_evid | 46 | 0.000 | 0.000 | 0.000 |
| hotpotqa | V1 | CC-FF | all_zero | 46 | 0.000 | 0.000 | 0.000 |
| hotpotqa | V1 | CC-FF | group_top1 | 46 | 0.099 | 0.037 | 0.161 |
| hotpotqa | V1 | CC-FF | group_top1_cc | 46 | 0.040 | -0.034 | 0.114 |
| hotpotqa | V1 | CC-FF | ap_top1 | 46 | -0.392 | -0.483 | -0.297 |
| hotpotqa | V1 | C-F | group_evid | 48 | -0.021 | -0.062 | 0.000 |
| hotpotqa | V1 | C-F | all_zero | 48 | 0.000 | 0.000 | 0.000 |
| hotpotqa | V1 | C-F | group_top1 | 48 | 0.035 | -0.017 | 0.087 |
| hotpotqa | V1 | C-F | group_top1_cc | 48 | -0.001 | -0.064 | 0.062 |
| hotpotqa | V1 | C-F | ap_top1 | 48 | -0.311 | -0.378 | -0.243 |
| musique | LOI | CF-FF | group_evid | 45 | 0.000 | 0.000 | 0.000 |
| musique | LOI | CF-FF | all_zero | 45 | 0.000 | 0.000 | 0.000 |
| musique | LOI | CF-FF | group_top1 | 45 | 0.021 | 0.010 | 0.035 |
| musique | LOI | CF-FF | group_top1_cc | 45 | 0.009 | -0.001 | 0.021 |
| musique | LOI | CF-FF | ap_top1 | 45 | -0.354 | -0.415 | -0.285 |
| musique | LOI | CC-CF | group_evid | 46 | 0.000 | -0.065 | 0.065 |
| musique | LOI | CC-CF | all_zero | 46 | 0.000 | -0.065 | 0.065 |
| musique | LOI | CC-CF | group_top1 | 46 | 0.016 | -0.041 | 0.073 |
| musique | LOI | CC-CF | group_top1_cc | 46 | 0.004 | -0.060 | 0.069 |
| musique | LOI | CC-CF | ap_top1 | 46 | -0.121 | -0.149 | -0.089 |
| musique | LOI | CC-FF | group_evid | 47 | 0.000 | -0.064 | 0.064 |
| musique | LOI | CC-FF | all_zero | 47 | 0.000 | -0.064 | 0.064 |
| musique | LOI | CC-FF | group_top1 | 47 | 0.036 | -0.020 | 0.096 |
| musique | LOI | CC-FF | group_top1_cc | 47 | 0.013 | -0.049 | 0.076 |
| musique | LOI | CC-FF | ap_top1 | 47 | -0.482 | -0.564 | -0.390 |
| musique | LOI | C-F | group_evid | 44 | 0.091 | 0.023 | 0.182 |
| musique | LOI | C-F | all_zero | 44 | -0.091 | -0.182 | -0.023 |
| musique | LOI | C-F | group_top1 | 44 | 0.089 | 0.027 | 0.168 |
| musique | LOI | C-F | group_top1_cc | 44 | 0.081 | 0.014 | 0.166 |
| musique | LOI | C-F | ap_top1 | 44 | -0.298 | -0.382 | -0.205 |
| musique | MEXGEN_LOO | CF-FF | group_evid | 45 | -0.778 | -0.889 | -0.644 |
| musique | MEXGEN_LOO | CF-FF | all_zero | 45 | 0.511 | 0.356 | 0.644 |
| musique | MEXGEN_LOO | CF-FF | group_top1 | 45 | -0.548 | -0.667 | -0.418 |
| musique | MEXGEN_LOO | CF-FF | group_top1_cc | 45 | -0.621 | -0.747 | -0.482 |
| musique | MEXGEN_LOO | CF-FF | ap_top1 | 45 | -0.597 | -0.708 | -0.474 |
| musique | MEXGEN_LOO | CC-CF | group_evid | 46 | 0.065 | -0.043 | 0.174 |
| musique | MEXGEN_LOO | CC-CF | all_zero | 46 | -0.043 | -0.130 | 0.043 |
| musique | MEXGEN_LOO | CC-CF | group_top1 | 46 | -0.012 | -0.086 | 0.041 |
| musique | MEXGEN_LOO | CC-CF | group_top1_cc | 46 | -0.066 | -0.149 | -0.008 |
| musique | MEXGEN_LOO | CC-CF | ap_top1 | 46 | -0.021 | -0.071 | 0.007 |
| musique | MEXGEN_LOO | CC-FF | group_evid | 47 | -0.702 | -0.830 | -0.574 |
| musique | MEXGEN_LOO | CC-FF | all_zero | 47 | 0.447 | 0.277 | 0.596 |
| musique | MEXGEN_LOO | CC-FF | group_top1 | 47 | -0.554 | -0.655 | -0.456 |
| musique | MEXGEN_LOO | CC-FF | group_top1_cc | 47 | -0.681 | -0.786 | -0.580 |
| musique | MEXGEN_LOO | CC-FF | ap_top1 | 47 | -0.611 | -0.712 | -0.509 |
| musique | MEXGEN_LOO | C-F | group_evid | 44 | -0.886 | -0.977 | -0.795 |
| musique | MEXGEN_LOO | C-F | all_zero | 44 | 0.455 | 0.318 | 0.614 |
| musique | MEXGEN_LOO | C-F | group_top1 | 44 | -0.633 | -0.742 | -0.509 |
| musique | MEXGEN_LOO | C-F | group_top1_cc | 44 | -0.716 | -0.832 | -0.584 |
| musique | MEXGEN_LOO | C-F | ap_top1 | 44 | -0.671 | -0.773 | -0.559 |
| musique | P1 | CF-FF | group_evid | 45 | -0.778 | -0.889 | -0.644 |
| musique | P1 | CF-FF | all_zero | 45 | 0.511 | 0.356 | 0.644 |
| musique | P1 | CF-FF | group_top1 | 45 | -0.480 | -0.590 | -0.362 |
| musique | P1 | CF-FF | group_top1_cc | 45 | -0.551 | -0.667 | -0.426 |
| musique | P1 | CF-FF | ap_top1 | 45 | -0.530 | -0.637 | -0.419 |
| musique | P1 | CC-CF | group_evid | 46 | 0.065 | -0.043 | 0.174 |
| musique | P1 | CC-CF | all_zero | 46 | -0.043 | -0.130 | 0.043 |
| musique | P1 | CC-CF | group_top1 | 46 | 0.019 | -0.041 | 0.059 |
| musique | P1 | CC-CF | group_top1_cc | 46 | -0.032 | -0.097 | 0.014 |
| musique | P1 | CC-CF | ap_top1 | 46 | -0.003 | -0.013 | 0.007 |
| musique | P1 | CC-FF | group_evid | 47 | -0.702 | -0.830 | -0.574 |
| musique | P1 | CC-FF | all_zero | 47 | 0.447 | 0.277 | 0.596 |
| musique | P1 | CC-FF | group_top1 | 47 | -0.459 | -0.561 | -0.357 |
| musique | P1 | CC-FF | group_top1_cc | 47 | -0.580 | -0.687 | -0.473 |
| musique | P1 | CC-FF | ap_top1 | 47 | -0.528 | -0.631 | -0.424 |
| musique | P1 | C-F | group_evid | 44 | -0.886 | -0.977 | -0.795 |
| musique | P1 | C-F | all_zero | 44 | 0.455 | 0.318 | 0.614 |
| musique | P1 | C-F | group_top1 | 44 | -0.568 | -0.697 | -0.425 |
| musique | P1 | C-F | group_top1_cc | 44 | -0.648 | -0.784 | -0.496 |
| musique | P1 | C-F | ap_top1 | 44 | -0.606 | -0.730 | -0.475 |
| musique | RM64:banzhaf_exact | CF-FF | group_evid | 45 | -0.111 | -0.200 | -0.022 |
| musique | RM64:banzhaf_exact | CF-FF | all_zero | 45 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_exact | CF-FF | group_top1 | 45 | -0.222 | -0.356 | -0.089 |
| musique | RM64:banzhaf_exact | CF-FF | group_top1_cc | 45 | -0.254 | -0.397 | -0.115 |
| musique | RM64:banzhaf_exact | CF-FF | ap_top1 | 45 | -0.467 | -0.622 | -0.311 |
| musique | RM64:banzhaf_exact | CC-CF | group_evid | 46 | -0.261 | -0.413 | -0.109 |
| musique | RM64:banzhaf_exact | CC-CF | all_zero | 46 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_exact | CC-CF | group_top1 | 46 | -0.130 | -0.261 | 0.000 |
| musique | RM64:banzhaf_exact | CC-CF | group_top1_cc | 46 | -0.174 | -0.323 | -0.027 |
| musique | RM64:banzhaf_exact | CC-CF | ap_top1 | 46 | -0.239 | -0.370 | -0.130 |
| musique | RM64:banzhaf_exact | CC-FF | group_evid | 47 | -0.340 | -0.489 | -0.191 |
| musique | RM64:banzhaf_exact | CC-FF | all_zero | 47 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_exact | CC-FF | group_top1 | 47 | -0.340 | -0.489 | -0.191 |
| musique | RM64:banzhaf_exact | CC-FF | group_top1_cc | 47 | -0.413 | -0.583 | -0.248 |
| musique | RM64:banzhaf_exact | CC-FF | ap_top1 | 47 | -0.681 | -0.809 | -0.553 |
| musique | RM64:banzhaf_exact | C-F | group_evid | 44 | 0.045 | -0.045 | 0.136 |
| musique | RM64:banzhaf_exact | C-F | all_zero | 44 | -0.045 | -0.114 | 0.000 |
| musique | RM64:banzhaf_exact | C-F | group_top1 | 44 | -0.241 | -0.389 | -0.093 |
| musique | RM64:banzhaf_exact | C-F | group_top1_cc | 44 | -0.276 | -0.437 | -0.113 |
| musique | RM64:banzhaf_exact | C-F | ap_top1 | 44 | -0.468 | -0.628 | -0.299 |
| musique | RM64:banzhaf_f1 | CF-FF | group_evid | 45 | -0.089 | -0.178 | -0.022 |
| musique | RM64:banzhaf_f1 | CF-FF | all_zero | 45 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_f1 | CF-FF | group_top1 | 45 | -0.222 | -0.356 | -0.111 |
| musique | RM64:banzhaf_f1 | CF-FF | group_top1_cc | 45 | -0.255 | -0.398 | -0.129 |
| musique | RM64:banzhaf_f1 | CF-FF | ap_top1 | 45 | -0.467 | -0.622 | -0.333 |
| musique | RM64:banzhaf_f1 | CC-CF | group_evid | 46 | -0.261 | -0.413 | -0.109 |
| musique | RM64:banzhaf_f1 | CC-CF | all_zero | 46 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_f1 | CC-CF | group_top1 | 46 | -0.087 | -0.196 | 0.022 |
| musique | RM64:banzhaf_f1 | CC-CF | group_top1_cc | 46 | -0.125 | -0.251 | 0.002 |
| musique | RM64:banzhaf_f1 | CC-CF | ap_top1 | 46 | -0.196 | -0.326 | -0.087 |
| musique | RM64:banzhaf_f1 | CC-FF | group_evid | 47 | -0.319 | -0.447 | -0.191 |
| musique | RM64:banzhaf_f1 | CC-FF | all_zero | 47 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_f1 | CC-FF | group_top1 | 47 | -0.298 | -0.447 | -0.149 |
| musique | RM64:banzhaf_f1 | CC-FF | group_top1_cc | 47 | -0.366 | -0.534 | -0.201 |
| musique | RM64:banzhaf_f1 | CC-FF | ap_top1 | 47 | -0.638 | -0.766 | -0.511 |
| musique | RM64:banzhaf_f1 | C-F | group_evid | 44 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_f1 | C-F | all_zero | 44 | -0.023 | -0.068 | 0.000 |
| musique | RM64:banzhaf_f1 | C-F | group_top1 | 44 | -0.319 | -0.477 | -0.162 |
| musique | RM64:banzhaf_f1 | C-F | group_top1_cc | 44 | -0.361 | -0.532 | -0.192 |
| musique | RM64:banzhaf_f1 | C-F | ap_top1 | 44 | -0.569 | -0.727 | -0.412 |
| musique | RM64:linear_exact | CF-FF | group_evid | 45 | -0.089 | -0.178 | -0.022 |
| musique | RM64:linear_exact | CF-FF | all_zero | 45 | 0.000 | 0.000 | 0.000 |
| musique | RM64:linear_exact | CF-FF | group_top1 | 45 | -0.289 | -0.422 | -0.156 |
| musique | RM64:linear_exact | CF-FF | group_top1_cc | 45 | -0.324 | -0.470 | -0.179 |
| musique | RM64:linear_exact | CF-FF | ap_top1 | 45 | -0.556 | -0.689 | -0.400 |
| musique | RM64:linear_exact | CC-CF | group_evid | 46 | -0.370 | -0.522 | -0.217 |
| musique | RM64:linear_exact | CC-CF | all_zero | 46 | 0.000 | 0.000 | 0.000 |
| musique | RM64:linear_exact | CC-CF | group_top1 | 46 | -0.109 | -0.239 | 0.000 |
| musique | RM64:linear_exact | CC-CF | group_top1_cc | 46 | -0.149 | -0.293 | -0.019 |
| musique | RM64:linear_exact | CC-CF | ap_top1 | 46 | -0.152 | -0.283 | -0.022 |
| musique | RM64:linear_exact | CC-FF | group_evid | 47 | -0.447 | -0.596 | -0.298 |
| musique | RM64:linear_exact | CC-FF | all_zero | 47 | 0.000 | 0.000 | 0.000 |
| musique | RM64:linear_exact | CC-FF | group_top1 | 47 | -0.383 | -0.532 | -0.234 |
| musique | RM64:linear_exact | CC-FF | group_top1_cc | 47 | -0.455 | -0.626 | -0.281 |
| musique | RM64:linear_exact | CC-FF | ap_top1 | 47 | -0.702 | -0.830 | -0.574 |
| musique | RM64:linear_exact | C-F | group_evid | 44 | -0.045 | -0.182 | 0.068 |
| musique | RM64:linear_exact | C-F | all_zero | 44 | -0.045 | -0.114 | 0.000 |
| musique | RM64:linear_exact | C-F | group_top1 | 44 | -0.207 | -0.342 | -0.070 |
| musique | RM64:linear_exact | C-F | group_top1_cc | 44 | -0.239 | -0.387 | -0.091 |
| musique | RM64:linear_exact | C-F | ap_top1 | 44 | -0.479 | -0.637 | -0.319 |
| musique | V1 | CF-FF | group_evid | 45 | -0.022 | -0.111 | 0.044 |
| musique | V1 | CF-FF | all_zero | 45 | 0.022 | 0.000 | 0.067 |
| musique | V1 | CF-FF | group_top1 | 45 | 0.079 | 0.021 | 0.137 |
| musique | V1 | CF-FF | group_top1_cc | 45 | 0.058 | -0.005 | 0.121 |
| musique | V1 | CF-FF | ap_top1 | 45 | -0.170 | -0.229 | -0.111 |
| musique | V1 | CC-CF | group_evid | 46 | 0.000 | -0.087 | 0.087 |
| musique | V1 | CC-CF | all_zero | 46 | -0.022 | -0.065 | 0.000 |
| musique | V1 | CC-CF | group_top1 | 46 | -0.023 | -0.086 | 0.044 |
| musique | V1 | CC-CF | group_top1_cc | 46 | -0.054 | -0.125 | 0.021 |
| musique | V1 | CC-CF | ap_top1 | 46 | -0.091 | -0.148 | -0.036 |
| musique | V1 | CC-FF | group_evid | 47 | -0.021 | -0.064 | 0.000 |
| musique | V1 | CC-FF | all_zero | 47 | 0.000 | 0.000 | 0.000 |
| musique | V1 | CC-FF | group_top1 | 47 | 0.060 | 0.011 | 0.110 |
| musique | V1 | CC-FF | group_top1_cc | 47 | 0.008 | -0.049 | 0.066 |
| musique | V1 | CC-FF | ap_top1 | 47 | -0.254 | -0.318 | -0.187 |
| musique | V1 | C-F | group_evid | 44 | 0.023 | -0.045 | 0.091 |
| musique | V1 | C-F | all_zero | 44 | 0.023 | 0.000 | 0.091 |
| musique | V1 | C-F | group_top1 | 44 | 0.098 | 0.027 | 0.159 |
| musique | V1 | C-F | group_top1_cc | 44 | 0.076 | -0.001 | 0.142 |
| musique | V1 | C-F | ap_top1 | 44 | -0.200 | -0.271 | -0.138 |

## Cost
| dataset | file | calls | cost_cny |
|---|---|---|---|
| hotpotqa | P1.r3.cost.json | 3717 | 0.254 |
| hotpotqa | RM64.r3.cost.json | 8017 | 0.326 |
| hotpotqa | V1.r3.cost.json | 250 | 0.018 |
| hotpotqa | LOI.r3.cost.json | 975 | 0.015 |
| hotpotqa | premise.cost.json | 1768 | 0.121 |
| musique | P1.r3.cost.json | 6228 | 0.740 |
| musique | RM64.r3.cost.json | 11236 | 0.762 |
| musique | V1.r3.cost.json | 250 | 0.032 |
| musique | LOI.r3.cost.json | 373 | 0.005 |
| musique | premise.cost.json | 1823 | 0.216 |
