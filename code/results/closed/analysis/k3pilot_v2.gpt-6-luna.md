# K3 k3pilot_v2 · gpt-6-luna

## Premise (repeats 0-2)
| dataset | cond | redundancy | n_bases | n_eval_3of3 | full_3of3 | full_2of3 | full_spont_change | parse_fail | drop_ap_still_correct | drop_ap_answer_change | drop_ap_acc_drop | drop_group_still_correct | drop_group_answer_change | drop_group_acc_drop |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | F | 0 | 50 | 44 | 0.880 | 0.980 | 0.140 | 0.000 | 0.253 | 0.767 | 0.700 | 0.253 | 0.767 | 0.700 |
| hotpotqa | C | 1 | 50 | 46 | 0.920 | 0.980 | 0.140 | 0.000 | 0.927 | 0.113 | 0.033 | 0.320 | 0.720 | 0.640 |
| hotpotqa | FF | 0 | 50 | 45 | 0.900 | 0.940 | 0.160 | 0.000 | 0.267 | 0.747 | 0.680 | 0.267 | 0.747 | 0.680 |
| hotpotqa | CF | 1 | 50 | 45 | 0.900 | 0.920 | 0.140 | 0.000 | 0.933 | 0.100 | -0.013 | 0.287 | 0.733 | 0.633 |
| hotpotqa | CC | 2 | 50 | 46 | 0.920 | 0.980 | 0.100 | 0.000 | 0.947 | 0.107 | 0.020 | 0.320 | 0.713 | 0.647 |
| musique | F | 0 | 50 | 43 | 0.860 | 0.900 | 0.180 | 0.004 | 0.340 | 0.727 | 0.567 | 0.340 | 0.727 | 0.567 |
| musique | C | 1 | 50 | 45 | 0.900 | 0.940 | 0.140 | 0.000 | 0.913 | 0.107 | 0.033 | 0.267 | 0.800 | 0.680 |
| musique | FF | 0 | 50 | 42 | 0.840 | 0.960 | 0.180 | 0.000 | 0.367 | 0.720 | 0.560 | 0.367 | 0.720 | 0.560 |
| musique | CF | 1 | 50 | 43 | 0.860 | 0.900 | 0.180 | 0.000 | 0.913 | 0.140 | -0.007 | 0.273 | 0.793 | 0.633 |
| musique | CC | 2 | 50 | 42 | 0.840 | 0.940 | 0.160 | 0.000 | 0.907 | 0.107 | 0.013 | 0.280 | 0.773 | 0.640 |

## Methods (repeat 3, premise-evaluable variants of each condition)
| dataset | method | cond | n | group_top1 | group_floor | group_top1_cc | ap_top1 | gold_top1 | group_evid | nonzero_any | all_zero | pos_mass_copies | full_ctx_change_r3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | LOI | F | 44 | 0.606 | 0.091 | 0.566 | 0.606 | 0.695 | 0.795 | 0.841 | 0.159 |  |  |
| hotpotqa | LOI | C | 46 | 0.663 | 0.182 | 0.588 | 0.332 | 0.730 | 0.783 | 0.826 | 0.174 | 0.500 |  |
| hotpotqa | LOI | FF | 45 | 0.637 | 0.083 | 0.604 | 0.637 | 0.719 | 0.867 | 0.889 | 0.111 |  |  |
| hotpotqa | LOI | CF | 45 | 0.723 | 0.167 | 0.668 | 0.362 | 0.768 | 0.867 | 0.867 | 0.133 | 0.500 |  |
| hotpotqa | LOI | CC | 46 | 0.819 | 0.250 | 0.759 | 0.273 | 0.855 | 0.913 | 0.913 | 0.087 | 0.667 |  |
| hotpotqa | MEXGEN_LOO | F | 44 | 0.636 | 0.091 | 0.600 | 0.636 | 0.714 | 0.750 | 0.795 | 0.205 |  |  |
| hotpotqa | MEXGEN_LOO | C | 46 | 0.182 | 0.182 | 0.000 | 0.112 | 0.322 | 0.196 | 0.326 | 0.674 | 0.561 |  |
| hotpotqa | MEXGEN_LOO | FF | 45 | 0.673 | 0.083 | 0.643 | 0.673 | 0.757 | 0.711 | 0.822 | 0.178 |  |  |
| hotpotqa | MEXGEN_LOO | CF | 45 | 0.190 | 0.167 | 0.028 | 0.090 | 0.262 | 0.200 | 0.289 | 0.711 | 0.500 |  |
| hotpotqa | MEXGEN_LOO | CC | 46 | 0.268 | 0.250 | 0.024 | 0.073 | 0.410 | 0.174 | 0.304 | 0.696 | 0.792 |  |
| hotpotqa | P1 | F | 44 | 0.568 | 0.091 | 0.524 | 0.568 | 0.641 | 0.750 | 0.818 | 0.182 |  | 0.140 |
| hotpotqa | P1 | C | 46 | 0.191 | 0.182 | 0.011 | 0.114 | 0.334 | 0.196 | 0.326 | 0.674 | 0.556 | 0.130 |
| hotpotqa | P1 | FF | 45 | 0.574 | 0.083 | 0.536 | 0.574 | 0.668 | 0.711 | 0.822 | 0.178 |  | 0.111 |
| hotpotqa | P1 | CF | 45 | 0.188 | 0.167 | 0.026 | 0.091 | 0.261 | 0.200 | 0.311 | 0.689 | 0.500 | 0.133 |
| hotpotqa | P1 | CC | 46 | 0.250 | 0.250 | -0.000 | 0.075 | 0.394 | 0.174 | 0.304 | 0.696 | 0.729 | 0.094 |
| hotpotqa | RM64:banzhaf_exact | F | 44 | 0.854 | 0.091 | 0.840 | 0.854 | 0.936 | 0.886 | 0.977 | 0.023 |  |  |
| hotpotqa | RM64:banzhaf_exact | C | 46 | 0.707 | 0.182 | 0.641 | 0.359 | 0.859 | 0.826 | 1.000 | 0.000 | 0.511 |  |
| hotpotqa | RM64:banzhaf_exact | FF | 45 | 0.802 | 0.083 | 0.784 | 0.802 | 0.937 | 0.867 | 0.978 | 0.022 |  |  |
| hotpotqa | RM64:banzhaf_exact | CF | 45 | 0.759 | 0.167 | 0.711 | 0.335 | 0.850 | 0.822 | 0.978 | 0.022 | 0.499 |  |
| hotpotqa | RM64:banzhaf_exact | CC | 46 | 0.723 | 0.250 | 0.630 | 0.168 | 0.848 | 0.717 | 0.935 | 0.065 | 0.675 |  |
| hotpotqa | RM64:banzhaf_f1 | F | 44 | 0.909 | 0.091 | 0.900 | 0.909 | 0.966 | 0.932 | 1.000 | 0.000 |  |  |
| hotpotqa | RM64:banzhaf_f1 | C | 46 | 0.793 | 0.182 | 0.748 | 0.359 | 0.902 | 0.870 | 1.000 | 0.000 | 0.521 |  |
| hotpotqa | RM64:banzhaf_f1 | FF | 45 | 0.844 | 0.083 | 0.830 | 0.844 | 0.978 | 0.911 | 1.000 | 0.000 |  |  |
| hotpotqa | RM64:banzhaf_f1 | CF | 45 | 0.826 | 0.167 | 0.791 | 0.335 | 0.894 | 0.889 | 0.978 | 0.022 | 0.521 |  |
| hotpotqa | RM64:banzhaf_f1 | CC | 46 | 0.766 | 0.250 | 0.688 | 0.190 | 0.891 | 0.761 | 0.935 | 0.065 | 0.678 |  |
| hotpotqa | RM64:linear_exact | F | 44 | 0.798 | 0.091 | 0.777 | 0.798 | 0.913 | 0.886 | 0.977 | 0.023 |  |  |
| hotpotqa | RM64:linear_exact | C | 46 | 0.761 | 0.182 | 0.708 | 0.370 | 0.891 | 0.848 | 1.000 | 0.000 | 0.528 |  |
| hotpotqa | RM64:linear_exact | FF | 45 | 0.780 | 0.083 | 0.760 | 0.780 | 0.915 | 0.867 | 0.978 | 0.022 |  |  |
| hotpotqa | RM64:linear_exact | CF | 45 | 0.804 | 0.167 | 0.764 | 0.357 | 0.894 | 0.822 | 0.978 | 0.022 | 0.514 |  |
| hotpotqa | RM64:linear_exact | CC | 46 | 0.690 | 0.250 | 0.587 | 0.179 | 0.913 | 0.717 | 0.935 | 0.065 | 0.671 |  |
| hotpotqa | V1 | F | 44 | 0.578 | 0.091 | 0.535 | 0.578 | 0.973 | 0.977 | 1.000 | 0.000 |  |  |
| hotpotqa | V1 | C | 46 | 0.565 | 0.182 | 0.469 | 0.286 | 0.957 | 0.957 | 1.000 | 0.000 | 0.511 |  |
| hotpotqa | V1 | FF | 45 | 0.598 | 0.083 | 0.562 | 0.598 | 0.974 | 0.978 | 1.000 | 0.000 |  |  |
| hotpotqa | V1 | CF | 45 | 0.565 | 0.167 | 0.478 | 0.296 | 0.941 | 0.978 | 1.000 | 0.000 | 0.489 |  |
| hotpotqa | V1 | CC | 46 | 0.583 | 0.250 | 0.444 | 0.216 | 0.982 | 1.000 | 1.000 | 0.000 | 0.652 |  |
| musique | LOI | F | 43 | 0.703 | 0.048 | 0.688 | 0.703 | 0.797 | 0.930 | 0.977 | 0.023 |  |  |
| musique | LOI | C | 45 | 0.778 | 0.095 | 0.755 | 0.389 | 0.863 | 0.933 | 0.978 | 0.022 | 0.500 |  |
| musique | LOI | FF | 42 | 0.649 | 0.045 | 0.632 | 0.649 | 0.742 | 0.857 | 0.905 | 0.095 |  |  |
| musique | LOI | CF | 43 | 0.688 | 0.091 | 0.657 | 0.344 | 0.757 | 0.837 | 0.884 | 0.116 | 0.500 |  |
| musique | LOI | CC | 42 | 0.803 | 0.136 | 0.772 | 0.268 | 0.864 | 0.929 | 0.976 | 0.024 | 0.667 |  |
| musique | MEXGEN_LOO | F | 43 | 0.587 | 0.048 | 0.567 | 0.587 | 0.687 | 0.767 | 0.860 | 0.140 |  |  |
| musique | MEXGEN_LOO | C | 45 | 0.083 | 0.095 | -0.014 | 0.034 | 0.272 | 0.133 | 0.489 | 0.511 | 0.583 |  |
| musique | MEXGEN_LOO | FF | 42 | 0.643 | 0.045 | 0.626 | 0.643 | 0.786 | 0.833 | 0.905 | 0.095 |  |  |
| musique | MEXGEN_LOO | CF | 43 | 0.108 | 0.091 | 0.018 | 0.036 | 0.386 | 0.233 | 0.535 | 0.465 | 0.742 |  |
| musique | MEXGEN_LOO | CC | 42 | 0.122 | 0.136 | -0.016 | 0.023 | 0.366 | 0.119 | 0.524 | 0.476 | 0.933 |  |
| musique | P1 | F | 43 | 0.559 | 0.048 | 0.537 | 0.559 | 0.656 | 0.767 | 0.860 | 0.140 |  | 0.031 |
| musique | P1 | C | 45 | 0.092 | 0.095 | -0.004 | 0.039 | 0.281 | 0.133 | 0.489 | 0.511 | 0.583 | 0.030 |
| musique | P1 | FF | 42 | 0.539 | 0.045 | 0.517 | 0.539 | 0.666 | 0.833 | 0.905 | 0.095 |  | 0.048 |
| musique | P1 | CF | 43 | 0.109 | 0.091 | 0.019 | 0.031 | 0.365 | 0.233 | 0.535 | 0.465 | 0.750 | 0.062 |
| musique | P1 | CC | 42 | 0.126 | 0.136 | -0.011 | 0.023 | 0.348 | 0.119 | 0.524 | 0.476 | 0.933 | 0.071 |
| musique | RM64:banzhaf_exact | F | 43 | 0.814 | 0.048 | 0.805 | 0.814 | 0.907 | 0.884 | 1.000 | 0.000 |  |  |
| musique | RM64:banzhaf_exact | C | 45 | 0.722 | 0.095 | 0.693 | 0.244 | 0.878 | 0.911 | 1.000 | 0.000 | 0.526 |  |
| musique | RM64:banzhaf_exact | FF | 42 | 0.881 | 0.045 | 0.875 | 0.881 | 0.952 | 0.952 | 1.000 | 0.000 |  |  |
| musique | RM64:banzhaf_exact | CF | 43 | 0.723 | 0.091 | 0.695 | 0.373 | 0.865 | 0.767 | 0.977 | 0.023 | 0.518 |  |
| musique | RM64:banzhaf_exact | CC | 42 | 0.679 | 0.136 | 0.628 | 0.214 | 0.821 | 0.690 | 1.000 | 0.000 | 0.674 |  |
| musique | RM64:banzhaf_f1 | F | 43 | 0.767 | 0.048 | 0.756 | 0.767 | 0.907 | 0.907 | 1.000 | 0.000 |  |  |
| musique | RM64:banzhaf_f1 | C | 45 | 0.722 | 0.095 | 0.693 | 0.311 | 0.856 | 0.889 | 1.000 | 0.000 | 0.521 |  |
| musique | RM64:banzhaf_f1 | FF | 42 | 0.857 | 0.045 | 0.850 | 0.857 | 0.952 | 0.952 | 1.000 | 0.000 |  |  |
| musique | RM64:banzhaf_f1 | CF | 43 | 0.721 | 0.091 | 0.693 | 0.326 | 0.907 | 0.791 | 1.000 | 0.000 | 0.511 |  |
| musique | RM64:banzhaf_f1 | CC | 42 | 0.679 | 0.136 | 0.628 | 0.214 | 0.821 | 0.714 | 1.000 | 0.000 | 0.664 |  |
| musique | RM64:linear_exact | F | 43 | 0.767 | 0.048 | 0.756 | 0.767 | 0.907 | 0.907 | 1.000 | 0.000 |  |  |
| musique | RM64:linear_exact | C | 45 | 0.756 | 0.095 | 0.730 | 0.356 | 0.911 | 0.822 | 1.000 | 0.000 | 0.528 |  |
| musique | RM64:linear_exact | FF | 42 | 0.881 | 0.045 | 0.875 | 0.881 | 0.952 | 0.952 | 1.000 | 0.000 |  |  |
| musique | RM64:linear_exact | CF | 43 | 0.700 | 0.091 | 0.670 | 0.303 | 0.888 | 0.814 | 0.977 | 0.023 | 0.517 |  |
| musique | RM64:linear_exact | CC | 42 | 0.667 | 0.136 | 0.614 | 0.286 | 0.833 | 0.643 | 1.000 | 0.000 | 0.669 |  |
| musique | V1 | F | 43 | 0.422 | 0.048 | 0.394 | 0.422 | 0.952 | 0.953 | 1.000 | 0.000 |  |  |
| musique | V1 | C | 45 | 0.387 | 0.095 | 0.323 | 0.185 | 0.939 | 0.889 | 1.000 | 0.000 | 0.575 |  |
| musique | V1 | FF | 42 | 0.397 | 0.045 | 0.368 | 0.397 | 0.952 | 0.952 | 1.000 | 0.000 |  |  |
| musique | V1 | CF | 43 | 0.419 | 0.091 | 0.360 | 0.275 | 0.965 | 0.930 | 1.000 | 0.000 | 0.338 |  |
| musique | V1 | CC | 42 | 0.411 | 0.136 | 0.318 | 0.177 | 0.968 | 0.929 | 1.000 | 0.000 | 0.581 |  |

## FF / CF / CC curve on one population (bases evaluable in all three)
| dataset | method | cond | n | group_top1 | group_floor | group_top1_cc | group_evid | all_zero | pos_mass_copies |
|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | LOI | FF | 43 | 0.663 | 0.083 | 0.632 | 0.907 | 0.070 |  |
| hotpotqa | LOI | CF | 43 | 0.710 | 0.167 | 0.653 | 0.860 | 0.140 | 0.500 |
| hotpotqa | LOI | CC | 43 | 0.824 | 0.250 | 0.766 | 0.930 | 0.070 | 0.667 |
| hotpotqa | MEXGEN_LOO | FF | 43 | 0.681 | 0.083 | 0.652 | 0.721 | 0.186 |  |
| hotpotqa | MEXGEN_LOO | CF | 43 | 0.193 | 0.167 | 0.031 | 0.186 | 0.721 | 0.438 |
| hotpotqa | MEXGEN_LOO | CC | 43 | 0.277 | 0.250 | 0.036 | 0.163 | 0.721 | 0.762 |
| hotpotqa | P1 | FF | 43 | 0.578 | 0.083 | 0.539 | 0.721 | 0.186 |  |
| hotpotqa | P1 | CF | 43 | 0.191 | 0.167 | 0.029 | 0.186 | 0.698 | 0.438 |
| hotpotqa | P1 | CC | 43 | 0.257 | 0.250 | 0.010 | 0.163 | 0.721 | 0.690 |
| hotpotqa | RM64:banzhaf_exact | FF | 43 | 0.816 | 0.083 | 0.799 | 0.884 | 0.023 |  |
| hotpotqa | RM64:banzhaf_exact | CF | 43 | 0.771 | 0.167 | 0.726 | 0.837 | 0.023 | 0.499 |
| hotpotqa | RM64:banzhaf_exact | CC | 43 | 0.727 | 0.250 | 0.636 | 0.721 | 0.070 | 0.685 |
| hotpotqa | RM64:banzhaf_f1 | FF | 43 | 0.860 | 0.083 | 0.848 | 0.930 | 0.000 |  |
| hotpotqa | RM64:banzhaf_f1 | CF | 43 | 0.841 | 0.167 | 0.809 | 0.907 | 0.023 | 0.509 |
| hotpotqa | RM64:banzhaf_f1 | CC | 43 | 0.773 | 0.250 | 0.698 | 0.767 | 0.070 | 0.687 |
| hotpotqa | RM64:linear_exact | FF | 43 | 0.793 | 0.083 | 0.774 | 0.884 | 0.023 |  |
| hotpotqa | RM64:linear_exact | CF | 43 | 0.818 | 0.167 | 0.781 | 0.837 | 0.023 | 0.513 |
| hotpotqa | RM64:linear_exact | CC | 43 | 0.692 | 0.250 | 0.589 | 0.744 | 0.070 | 0.682 |
| hotpotqa | V1 | FF | 43 | 0.614 | 0.083 | 0.579 | 1.000 | 0.000 |  |
| hotpotqa | V1 | CF | 43 | 0.568 | 0.167 | 0.481 | 0.977 | 0.000 | 0.512 |
| hotpotqa | V1 | CC | 43 | 0.578 | 0.250 | 0.437 | 1.000 | 0.000 | 0.674 |
| musique | LOI | FF | 38 | 0.685 | 0.045 | 0.670 | 0.868 | 0.079 |  |
| musique | LOI | CF | 38 | 0.700 | 0.091 | 0.670 | 0.842 | 0.105 | 0.500 |
| musique | LOI | CC | 38 | 0.832 | 0.136 | 0.806 | 0.947 | 0.000 | 0.667 |
| musique | MEXGEN_LOO | FF | 38 | 0.605 | 0.045 | 0.586 | 0.816 | 0.105 |  |
| musique | MEXGEN_LOO | CF | 38 | 0.106 | 0.091 | 0.017 | 0.237 | 0.474 | 0.769 |
| musique | MEXGEN_LOO | CC | 38 | 0.127 | 0.136 | -0.010 | 0.105 | 0.500 | 1.000 |
| musique | P1 | FF | 38 | 0.513 | 0.045 | 0.489 | 0.816 | 0.105 |  |
| musique | P1 | CF | 38 | 0.108 | 0.091 | 0.018 | 0.237 | 0.474 | 0.778 |
| musique | P1 | CC | 38 | 0.132 | 0.136 | -0.005 | 0.105 | 0.500 | 1.000 |
| musique | RM64:banzhaf_exact | FF | 38 | 0.868 | 0.045 | 0.862 | 0.947 | 0.000 |  |
| musique | RM64:banzhaf_exact | CF | 38 | 0.739 | 0.091 | 0.713 | 0.789 | 0.026 | 0.519 |
| musique | RM64:banzhaf_exact | CC | 38 | 0.697 | 0.136 | 0.650 | 0.711 | 0.000 | 0.668 |
| musique | RM64:banzhaf_f1 | FF | 38 | 0.842 | 0.045 | 0.835 | 0.947 | 0.000 |  |
| musique | RM64:banzhaf_f1 | CF | 38 | 0.737 | 0.091 | 0.711 | 0.816 | 0.000 | 0.511 |
| musique | RM64:banzhaf_f1 | CC | 38 | 0.697 | 0.136 | 0.650 | 0.737 | 0.000 | 0.674 |
| musique | RM64:linear_exact | FF | 38 | 0.868 | 0.045 | 0.862 | 0.947 | 0.000 |  |
| musique | RM64:linear_exact | CF | 38 | 0.739 | 0.091 | 0.713 | 0.816 | 0.026 | 0.503 |
| musique | RM64:linear_exact | CC | 38 | 0.684 | 0.136 | 0.634 | 0.658 | 0.000 | 0.662 |
| musique | V1 | FF | 38 | 0.388 | 0.045 | 0.359 | 0.947 | 0.000 |  |
| musique | V1 | CF | 38 | 0.386 | 0.091 | 0.325 | 0.921 | 0.000 | 0.343 |
| musique | V1 | CC | 38 | 0.399 | 0.136 | 0.304 | 0.921 | 0.000 | 0.562 |

## Paired redundancy effects (base-qid bootstrap 95% CI)
| dataset | method | contrast | metric | n_base | diff | ci_lo | ci_hi |
|---|---|---|---|---|---|---|---|
| hotpotqa | LOI | CF-FF | group_evid | 43 | -0.047 | -0.163 | 0.047 |
| hotpotqa | LOI | CF-FF | all_zero | 43 | 0.070 | -0.023 | 0.163 |
| hotpotqa | LOI | CF-FF | group_top1 | 43 | 0.048 | -0.043 | 0.135 |
| hotpotqa | LOI | CF-FF | group_top1_cc | 43 | 0.021 | -0.082 | 0.120 |
| hotpotqa | LOI | CF-FF | ap_top1 | 43 | -0.307 | -0.395 | -0.222 |
| hotpotqa | LOI | CC-CF | group_evid | 45 | 0.067 | -0.022 | 0.178 |
| hotpotqa | LOI | CC-CF | all_zero | 45 | -0.067 | -0.178 | 0.022 |
| hotpotqa | LOI | CC-CF | group_top1 | 45 | 0.109 | 0.037 | 0.188 |
| hotpotqa | LOI | CC-CF | group_top1_cc | 45 | 0.108 | 0.018 | 0.206 |
| hotpotqa | LOI | CC-CF | ap_top1 | 45 | -0.084 | -0.120 | -0.046 |
| hotpotqa | LOI | CC-FF | group_evid | 44 | 0.023 | 0.000 | 0.068 |
| hotpotqa | LOI | CC-FF | all_zero | 44 | 0.000 | 0.000 | 0.000 |
| hotpotqa | LOI | CC-FF | group_top1 | 44 | 0.162 | 0.104 | 0.227 |
| hotpotqa | LOI | CC-FF | group_top1_cc | 44 | 0.131 | 0.070 | 0.203 |
| hotpotqa | LOI | CC-FF | ap_top1 | 44 | -0.379 | -0.467 | -0.286 |
| hotpotqa | LOI | C-F | group_evid | 42 | 0.000 | -0.095 | 0.095 |
| hotpotqa | LOI | C-F | all_zero | 42 | 0.000 | -0.095 | 0.095 |
| hotpotqa | LOI | C-F | group_top1 | 42 | 0.062 | -0.013 | 0.138 |
| hotpotqa | LOI | C-F | group_top1_cc | 42 | 0.027 | -0.059 | 0.113 |
| hotpotqa | LOI | C-F | ap_top1 | 42 | -0.273 | -0.355 | -0.187 |
| hotpotqa | MEXGEN_LOO | CF-FF | group_evid | 43 | -0.535 | -0.721 | -0.349 |
| hotpotqa | MEXGEN_LOO | CF-FF | all_zero | 43 | 0.535 | 0.372 | 0.698 |
| hotpotqa | MEXGEN_LOO | CF-FF | group_top1 | 43 | -0.489 | -0.637 | -0.331 |
| hotpotqa | MEXGEN_LOO | CF-FF | group_top1_cc | 43 | -0.621 | -0.786 | -0.443 |
| hotpotqa | MEXGEN_LOO | CF-FF | ap_top1 | 43 | -0.589 | -0.726 | -0.437 |
| hotpotqa | MEXGEN_LOO | CC-CF | group_evid | 45 | -0.022 | -0.111 | 0.044 |
| hotpotqa | MEXGEN_LOO | CC-CF | all_zero | 45 | 0.000 | -0.111 | 0.111 |
| hotpotqa | MEXGEN_LOO | CC-CF | group_top1 | 45 | 0.084 | -0.001 | 0.162 |
| hotpotqa | MEXGEN_LOO | CC-CF | group_top1_cc | 45 | 0.004 | -0.103 | 0.105 |
| hotpotqa | MEXGEN_LOO | CC-CF | ap_top1 | 45 | -0.016 | -0.067 | 0.018 |
| hotpotqa | MEXGEN_LOO | CC-FF | group_evid | 44 | -0.568 | -0.727 | -0.409 |
| hotpotqa | MEXGEN_LOO | CC-FF | all_zero | 44 | 0.523 | 0.364 | 0.659 |
| hotpotqa | MEXGEN_LOO | CC-FF | group_top1 | 44 | -0.418 | -0.552 | -0.276 |
| hotpotqa | MEXGEN_LOO | CC-FF | group_top1_cc | 44 | -0.633 | -0.784 | -0.465 |
| hotpotqa | MEXGEN_LOO | CC-FF | ap_top1 | 44 | -0.614 | -0.733 | -0.489 |
| hotpotqa | MEXGEN_LOO | C-F | group_evid | 42 | -0.571 | -0.738 | -0.405 |
| hotpotqa | MEXGEN_LOO | C-F | all_zero | 42 | 0.500 | 0.333 | 0.643 |
| hotpotqa | MEXGEN_LOO | C-F | group_top1 | 42 | -0.455 | -0.590 | -0.309 |
| hotpotqa | MEXGEN_LOO | C-F | group_top1_cc | 42 | -0.599 | -0.749 | -0.434 |
| hotpotqa | MEXGEN_LOO | C-F | ap_top1 | 42 | -0.526 | -0.663 | -0.379 |
| hotpotqa | P1 | CF-FF | group_evid | 43 | -0.535 | -0.721 | -0.349 |
| hotpotqa | P1 | CF-FF | all_zero | 43 | 0.512 | 0.349 | 0.674 |
| hotpotqa | P1 | CF-FF | group_top1 | 43 | -0.387 | -0.543 | -0.226 |
| hotpotqa | P1 | CF-FF | group_top1_cc | 43 | -0.510 | -0.683 | -0.332 |
| hotpotqa | P1 | CF-FF | ap_top1 | 43 | -0.485 | -0.635 | -0.341 |
| hotpotqa | P1 | CC-CF | group_evid | 45 | -0.022 | -0.111 | 0.044 |
| hotpotqa | P1 | CC-CF | all_zero | 45 | 0.022 | -0.089 | 0.133 |
| hotpotqa | P1 | CC-CF | group_top1 | 45 | 0.067 | -0.010 | 0.134 |
| hotpotqa | P1 | CC-CF | group_top1_cc | 45 | -0.019 | -0.117 | 0.066 |
| hotpotqa | P1 | CC-CF | ap_top1 | 45 | -0.014 | -0.065 | 0.021 |
| hotpotqa | P1 | CC-FF | group_evid | 44 | -0.568 | -0.727 | -0.409 |
| hotpotqa | P1 | CC-FF | all_zero | 44 | 0.523 | 0.364 | 0.659 |
| hotpotqa | P1 | CC-FF | group_top1 | 44 | -0.336 | -0.475 | -0.179 |
| hotpotqa | P1 | CC-FF | group_top1_cc | 44 | -0.548 | -0.707 | -0.376 |
| hotpotqa | P1 | CC-FF | ap_top1 | 44 | -0.511 | -0.638 | -0.376 |
| hotpotqa | P1 | C-F | group_evid | 42 | -0.571 | -0.738 | -0.405 |
| hotpotqa | P1 | C-F | all_zero | 42 | 0.524 | 0.380 | 0.667 |
| hotpotqa | P1 | C-F | group_top1 | 42 | -0.378 | -0.528 | -0.225 |
| hotpotqa | P1 | C-F | group_top1_cc | 42 | -0.514 | -0.682 | -0.345 |
| hotpotqa | P1 | C-F | ap_top1 | 42 | -0.455 | -0.605 | -0.304 |
| hotpotqa | RM64:banzhaf_exact | CF-FF | group_evid | 43 | -0.047 | -0.140 | 0.047 |
| hotpotqa | RM64:banzhaf_exact | CF-FF | all_zero | 43 | 0.000 | -0.070 | 0.070 |
| hotpotqa | RM64:banzhaf_exact | CF-FF | group_top1 | 43 | -0.045 | -0.136 | 0.045 |
| hotpotqa | RM64:banzhaf_exact | CF-FF | group_top1_cc | 43 | -0.074 | -0.178 | 0.027 |
| hotpotqa | RM64:banzhaf_exact | CF-FF | ap_top1 | 43 | -0.465 | -0.614 | -0.326 |
| hotpotqa | RM64:banzhaf_exact | CC-CF | group_evid | 45 | -0.089 | -0.244 | 0.067 |
| hotpotqa | RM64:banzhaf_exact | CC-CF | all_zero | 45 | 0.044 | 0.000 | 0.111 |
| hotpotqa | RM64:banzhaf_exact | CC-CF | group_top1 | 45 | -0.020 | -0.133 | 0.098 |
| hotpotqa | RM64:banzhaf_exact | CC-CF | group_top1_cc | 45 | -0.059 | -0.204 | 0.090 |
| hotpotqa | RM64:banzhaf_exact | CC-CF | ap_top1 | 45 | -0.163 | -0.298 | -0.022 |
| hotpotqa | RM64:banzhaf_exact | CC-FF | group_evid | 44 | -0.182 | -0.318 | -0.045 |
| hotpotqa | RM64:banzhaf_exact | CC-FF | all_zero | 44 | 0.045 | -0.045 | 0.136 |
| hotpotqa | RM64:banzhaf_exact | CC-FF | group_top1 | 44 | -0.110 | -0.223 | -0.006 |
| hotpotqa | RM64:banzhaf_exact | CC-FF | group_top1_cc | 44 | -0.190 | -0.339 | -0.059 |
| hotpotqa | RM64:banzhaf_exact | CC-FF | ap_top1 | 44 | -0.667 | -0.803 | -0.526 |
| hotpotqa | RM64:banzhaf_exact | C-F | group_evid | 42 | -0.048 | -0.143 | 0.048 |
| hotpotqa | RM64:banzhaf_exact | C-F | all_zero | 42 | -0.024 | -0.071 | 0.000 |
| hotpotqa | RM64:banzhaf_exact | C-F | group_top1 | 42 | -0.145 | -0.264 | -0.026 |
| hotpotqa | RM64:banzhaf_exact | C-F | group_top1_cc | 42 | -0.196 | -0.340 | -0.052 |
| hotpotqa | RM64:banzhaf_exact | C-F | ap_top1 | 42 | -0.502 | -0.657 | -0.347 |
| hotpotqa | RM64:banzhaf_f1 | CF-FF | group_evid | 43 | -0.023 | -0.093 | 0.047 |
| hotpotqa | RM64:banzhaf_f1 | CF-FF | all_zero | 43 | 0.023 | 0.000 | 0.070 |
| hotpotqa | RM64:banzhaf_f1 | CF-FF | group_top1 | 43 | -0.019 | -0.093 | 0.050 |
| hotpotqa | RM64:banzhaf_f1 | CF-FF | group_top1_cc | 43 | -0.038 | -0.125 | 0.046 |
| hotpotqa | RM64:banzhaf_f1 | CF-FF | ap_top1 | 43 | -0.510 | -0.661 | -0.370 |
| hotpotqa | RM64:banzhaf_f1 | CC-CF | group_evid | 45 | -0.111 | -0.244 | 0.022 |
| hotpotqa | RM64:banzhaf_f1 | CC-CF | all_zero | 45 | 0.044 | 0.000 | 0.111 |
| hotpotqa | RM64:banzhaf_f1 | CC-CF | group_top1 | 45 | -0.043 | -0.152 | 0.063 |
| hotpotqa | RM64:banzhaf_f1 | CC-CF | group_top1_cc | 45 | -0.080 | -0.221 | 0.050 |
| hotpotqa | RM64:banzhaf_f1 | CC-CF | ap_top1 | 45 | -0.141 | -0.287 | 0.004 |
| hotpotqa | RM64:banzhaf_f1 | CC-FF | group_evid | 44 | -0.182 | -0.318 | -0.068 |
| hotpotqa | RM64:banzhaf_f1 | CC-FF | all_zero | 44 | 0.068 | 0.000 | 0.159 |
| hotpotqa | RM64:banzhaf_f1 | CC-FF | group_top1 | 44 | -0.108 | -0.216 | -0.006 |
| hotpotqa | RM64:banzhaf_f1 | CC-FF | group_top1_cc | 44 | -0.177 | -0.317 | -0.049 |
| hotpotqa | RM64:banzhaf_f1 | CC-FF | ap_top1 | 44 | -0.688 | -0.816 | -0.542 |
| hotpotqa | RM64:banzhaf_f1 | C-F | group_evid | 42 | -0.048 | -0.143 | 0.048 |
| hotpotqa | RM64:banzhaf_f1 | C-F | all_zero | 42 | 0.000 | 0.000 | 0.000 |
| hotpotqa | RM64:banzhaf_f1 | C-F | group_top1 | 42 | -0.107 | -0.226 | 0.000 |
| hotpotqa | RM64:banzhaf_f1 | C-F | group_top1_cc | 42 | -0.143 | -0.285 | -0.013 |
| hotpotqa | RM64:banzhaf_f1 | C-F | ap_top1 | 42 | -0.536 | -0.679 | -0.381 |
| hotpotqa | RM64:linear_exact | CF-FF | group_evid | 43 | -0.047 | -0.140 | 0.047 |
| hotpotqa | RM64:linear_exact | CF-FF | all_zero | 43 | 0.000 | -0.070 | 0.070 |
| hotpotqa | RM64:linear_exact | CF-FF | group_top1 | 43 | 0.025 | -0.072 | 0.124 |
| hotpotqa | RM64:linear_exact | CF-FF | group_top1_cc | 43 | 0.008 | -0.109 | 0.119 |
| hotpotqa | RM64:linear_exact | CF-FF | ap_top1 | 43 | -0.419 | -0.558 | -0.277 |
| hotpotqa | RM64:linear_exact | CC-CF | group_evid | 45 | -0.089 | -0.244 | 0.067 |
| hotpotqa | RM64:linear_exact | CC-CF | all_zero | 45 | 0.044 | 0.000 | 0.111 |
| hotpotqa | RM64:linear_exact | CC-CF | group_top1 | 45 | -0.098 | -0.250 | 0.054 |
| hotpotqa | RM64:linear_exact | CC-CF | group_top1_cc | 45 | -0.157 | -0.357 | 0.036 |
| hotpotqa | RM64:linear_exact | CC-CF | ap_top1 | 45 | -0.174 | -0.330 | -0.020 |
| hotpotqa | RM64:linear_exact | CC-FF | group_evid | 44 | -0.159 | -0.318 | -0.023 |
| hotpotqa | RM64:linear_exact | CC-FF | all_zero | 44 | 0.045 | -0.045 | 0.136 |
| hotpotqa | RM64:linear_exact | CC-FF | group_top1 | 44 | -0.121 | -0.273 | 0.027 |
| hotpotqa | RM64:linear_exact | CC-FF | group_top1_cc | 44 | -0.211 | -0.395 | -0.027 |
| hotpotqa | RM64:linear_exact | CC-FF | ap_top1 | 44 | -0.633 | -0.771 | -0.487 |
| hotpotqa | RM64:linear_exact | C-F | group_evid | 42 | -0.024 | -0.119 | 0.048 |
| hotpotqa | RM64:linear_exact | C-F | all_zero | 42 | -0.024 | -0.071 | 0.000 |
| hotpotqa | RM64:linear_exact | C-F | group_top1 | 42 | -0.026 | -0.123 | 0.071 |
| hotpotqa | RM64:linear_exact | C-F | group_top1_cc | 42 | -0.058 | -0.177 | 0.066 |
| hotpotqa | RM64:linear_exact | C-F | ap_top1 | 42 | -0.407 | -0.552 | -0.262 |
| hotpotqa | V1 | CF-FF | group_evid | 43 | -0.023 | -0.070 | 0.000 |
| hotpotqa | V1 | CF-FF | all_zero | 43 | 0.000 | 0.000 | 0.000 |
| hotpotqa | V1 | CF-FF | group_top1 | 43 | -0.047 | -0.105 | 0.008 |
| hotpotqa | V1 | CF-FF | group_top1_cc | 43 | -0.098 | -0.163 | -0.036 |
| hotpotqa | V1 | CF-FF | ap_top1 | 43 | -0.328 | -0.430 | -0.231 |
| hotpotqa | V1 | CC-CF | group_evid | 45 | 0.022 | 0.000 | 0.067 |
| hotpotqa | V1 | CC-CF | all_zero | 45 | 0.000 | 0.000 | 0.000 |
| hotpotqa | V1 | CC-CF | group_top1 | 45 | 0.020 | -0.026 | 0.074 |
| hotpotqa | V1 | CC-CF | group_top1_cc | 45 | -0.031 | -0.090 | 0.038 |
| hotpotqa | V1 | CC-CF | ap_top1 | 45 | -0.076 | -0.150 | -0.004 |
| hotpotqa | V1 | CC-FF | group_evid | 44 | 0.000 | 0.000 | 0.000 |
| hotpotqa | V1 | CC-FF | all_zero | 44 | 0.000 | 0.000 | 0.000 |
| hotpotqa | V1 | CC-FF | group_top1 | 44 | -0.036 | -0.102 | 0.027 |
| hotpotqa | V1 | CC-FF | group_top1_cc | 44 | -0.142 | -0.219 | -0.067 |
| hotpotqa | V1 | CC-FF | ap_top1 | 44 | -0.420 | -0.521 | -0.328 |
| hotpotqa | V1 | C-F | group_evid | 42 | -0.024 | -0.071 | 0.000 |
| hotpotqa | V1 | C-F | all_zero | 42 | 0.000 | 0.000 | 0.000 |
| hotpotqa | V1 | C-F | group_top1 | 42 | -0.010 | -0.069 | 0.050 |
| hotpotqa | V1 | C-F | group_top1_cc | 42 | -0.062 | -0.131 | 0.007 |
| hotpotqa | V1 | C-F | ap_top1 | 42 | -0.292 | -0.385 | -0.198 |
| musique | LOI | CF-FF | group_evid | 40 | -0.025 | -0.125 | 0.050 |
| musique | LOI | CF-FF | all_zero | 40 | 0.025 | -0.050 | 0.125 |
| musique | LOI | CF-FF | group_top1 | 40 | 0.017 | -0.065 | 0.084 |
| musique | LOI | CF-FF | group_top1_cc | 40 | 0.001 | -0.087 | 0.072 |
| musique | LOI | CF-FF | ap_top1 | 40 | -0.322 | -0.408 | -0.242 |
| musique | LOI | CC-CF | group_evid | 40 | 0.075 | -0.025 | 0.175 |
| musique | LOI | CC-CF | all_zero | 40 | -0.075 | -0.175 | 0.025 |
| musique | LOI | CC-CF | group_top1 | 40 | 0.107 | 0.016 | 0.205 |
| musique | LOI | CC-CF | group_top1_cc | 40 | 0.106 | 0.004 | 0.216 |
| musique | LOI | CC-CF | ap_top1 | 40 | -0.082 | -0.125 | -0.035 |
| musique | LOI | CC-FF | group_evid | 40 | 0.075 | 0.000 | 0.175 |
| musique | LOI | CC-FF | all_zero | 40 | -0.075 | -0.175 | 0.000 |
| musique | LOI | CC-FF | group_top1 | 40 | 0.153 | 0.090 | 0.231 |
| musique | LOI | CC-FF | group_top1_cc | 40 | 0.141 | 0.073 | 0.223 |
| musique | LOI | CC-FF | ap_top1 | 40 | -0.397 | -0.488 | -0.299 |
| musique | LOI | C-F | group_evid | 43 | 0.000 | -0.070 | 0.070 |
| musique | LOI | C-F | all_zero | 43 | 0.000 | -0.070 | 0.070 |
| musique | LOI | C-F | group_top1 | 43 | 0.065 | -0.014 | 0.137 |
| musique | LOI | C-F | group_top1_cc | 43 | 0.055 | -0.029 | 0.132 |
| musique | LOI | C-F | ap_top1 | 43 | -0.319 | -0.396 | -0.239 |
| musique | MEXGEN_LOO | CF-FF | group_evid | 40 | -0.575 | -0.725 | -0.425 |
| musique | MEXGEN_LOO | CF-FF | all_zero | 40 | 0.375 | 0.225 | 0.525 |
| musique | MEXGEN_LOO | CF-FF | group_top1 | 40 | -0.511 | -0.639 | -0.376 |
| musique | MEXGEN_LOO | CF-FF | group_top1_cc | 40 | -0.582 | -0.716 | -0.440 |
| musique | MEXGEN_LOO | CF-FF | ap_top1 | 40 | -0.588 | -0.715 | -0.461 |
| musique | MEXGEN_LOO | CC-CF | group_evid | 40 | -0.100 | -0.250 | 0.050 |
| musique | MEXGEN_LOO | CC-CF | all_zero | 40 | 0.000 | -0.100 | 0.100 |
| musique | MEXGEN_LOO | CC-CF | group_top1 | 40 | 0.022 | -0.044 | 0.094 |
| musique | MEXGEN_LOO | CC-CF | group_top1_cc | 40 | -0.027 | -0.101 | 0.056 |
| musique | MEXGEN_LOO | CC-CF | ap_top1 | 40 | -0.009 | -0.025 | 0.002 |
| musique | MEXGEN_LOO | CC-FF | group_evid | 40 | -0.725 | -0.875 | -0.550 |
| musique | MEXGEN_LOO | CC-FF | all_zero | 40 | 0.400 | 0.250 | 0.550 |
| musique | MEXGEN_LOO | CC-FF | group_top1 | 40 | -0.500 | -0.631 | -0.372 |
| musique | MEXGEN_LOO | CC-FF | group_top1_cc | 40 | -0.621 | -0.759 | -0.484 |
| musique | MEXGEN_LOO | CC-FF | ap_top1 | 40 | -0.602 | -0.721 | -0.469 |
| musique | MEXGEN_LOO | C-F | group_evid | 43 | -0.651 | -0.814 | -0.465 |
| musique | MEXGEN_LOO | C-F | all_zero | 43 | 0.395 | 0.233 | 0.558 |
| musique | MEXGEN_LOO | C-F | group_top1 | 43 | -0.501 | -0.632 | -0.366 |
| musique | MEXGEN_LOO | C-F | group_top1_cc | 43 | -0.576 | -0.715 | -0.434 |
| musique | MEXGEN_LOO | C-F | ap_top1 | 43 | -0.551 | -0.680 | -0.424 |
| musique | P1 | CF-FF | group_evid | 40 | -0.575 | -0.725 | -0.425 |
| musique | P1 | CF-FF | all_zero | 40 | 0.375 | 0.225 | 0.525 |
| musique | P1 | CF-FF | group_top1 | 40 | -0.402 | -0.544 | -0.267 |
| musique | P1 | CF-FF | group_top1_cc | 40 | -0.467 | -0.617 | -0.325 |
| musique | P1 | CF-FF | ap_top1 | 40 | -0.484 | -0.616 | -0.361 |
| musique | P1 | CC-CF | group_evid | 40 | -0.100 | -0.250 | 0.050 |
| musique | P1 | CC-CF | all_zero | 40 | 0.000 | -0.100 | 0.100 |
| musique | P1 | CC-CF | group_top1 | 40 | 0.025 | -0.040 | 0.097 |
| musique | P1 | CC-CF | group_top1_cc | 40 | -0.023 | -0.097 | 0.060 |
| musique | P1 | CC-CF | ap_top1 | 40 | -0.004 | -0.013 | 0.003 |
| musique | P1 | CC-FF | group_evid | 40 | -0.725 | -0.875 | -0.550 |
| musique | P1 | CC-FF | all_zero | 40 | 0.400 | 0.250 | 0.550 |
| musique | P1 | CC-FF | group_top1 | 40 | -0.408 | -0.543 | -0.269 |
| musique | P1 | CC-FF | group_top1_cc | 40 | -0.524 | -0.668 | -0.373 |
| musique | P1 | CC-FF | ap_top1 | 40 | -0.514 | -0.634 | -0.391 |
| musique | P1 | C-F | group_evid | 43 | -0.651 | -0.814 | -0.465 |
| musique | P1 | C-F | all_zero | 43 | 0.395 | 0.233 | 0.558 |
| musique | P1 | C-F | group_top1 | 43 | -0.472 | -0.600 | -0.341 |
| musique | P1 | C-F | group_top1_cc | 43 | -0.547 | -0.681 | -0.408 |
| musique | P1 | C-F | ap_top1 | 43 | -0.523 | -0.644 | -0.400 |
| musique | RM64:banzhaf_exact | CF-FF | group_evid | 40 | -0.150 | -0.251 | -0.050 |
| musique | RM64:banzhaf_exact | CF-FF | all_zero | 40 | 0.025 | 0.000 | 0.075 |
| musique | RM64:banzhaf_exact | CF-FF | group_top1 | 40 | -0.123 | -0.248 | 0.000 |
| musique | RM64:banzhaf_exact | CF-FF | group_top1_cc | 40 | -0.142 | -0.278 | -0.010 |
| musique | RM64:banzhaf_exact | CF-FF | ap_top1 | 40 | -0.474 | -0.636 | -0.311 |
| musique | RM64:banzhaf_exact | CC-CF | group_evid | 40 | -0.075 | -0.200 | 0.075 |
| musique | RM64:banzhaf_exact | CC-CF | all_zero | 40 | -0.025 | -0.075 | 0.000 |
| musique | RM64:banzhaf_exact | CC-CF | group_top1 | 40 | -0.040 | -0.165 | 0.095 |
| musique | RM64:banzhaf_exact | CC-CF | group_top1_cc | 40 | -0.063 | -0.206 | 0.089 |
| musique | RM64:banzhaf_exact | CC-CF | ap_top1 | 40 | -0.189 | -0.326 | -0.028 |
| musique | RM64:banzhaf_exact | CC-FF | group_evid | 40 | -0.225 | -0.350 | -0.100 |
| musique | RM64:banzhaf_exact | CC-FF | all_zero | 40 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_exact | CC-FF | group_top1 | 40 | -0.163 | -0.300 | -0.037 |
| musique | RM64:banzhaf_exact | CC-FF | group_top1_cc | 40 | -0.202 | -0.362 | -0.057 |
| musique | RM64:banzhaf_exact | CC-FF | ap_top1 | 40 | -0.650 | -0.800 | -0.500 |
| musique | RM64:banzhaf_exact | C-F | group_evid | 43 | 0.023 | -0.047 | 0.093 |
| musique | RM64:banzhaf_exact | C-F | all_zero | 43 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_exact | C-F | group_top1 | 43 | -0.081 | -0.186 | 0.023 |
| musique | RM64:banzhaf_exact | C-F | group_top1_cc | 43 | -0.100 | -0.215 | 0.012 |
| musique | RM64:banzhaf_exact | C-F | ap_top1 | 43 | -0.558 | -0.698 | -0.419 |
| musique | RM64:banzhaf_f1 | CF-FF | group_evid | 40 | -0.125 | -0.225 | -0.025 |
| musique | RM64:banzhaf_f1 | CF-FF | all_zero | 40 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_f1 | CF-FF | group_top1 | 40 | -0.100 | -0.225 | 0.000 |
| musique | RM64:banzhaf_f1 | CF-FF | group_top1_cc | 40 | -0.118 | -0.253 | -0.005 |
| musique | RM64:banzhaf_f1 | CF-FF | ap_top1 | 40 | -0.500 | -0.662 | -0.338 |
| musique | RM64:banzhaf_f1 | CC-CF | group_evid | 40 | -0.075 | -0.200 | 0.050 |
| musique | RM64:banzhaf_f1 | CC-CF | all_zero | 40 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_f1 | CC-CF | group_top1 | 40 | -0.037 | -0.163 | 0.100 |
| musique | RM64:banzhaf_f1 | CC-CF | group_top1_cc | 40 | -0.061 | -0.213 | 0.093 |
| musique | RM64:banzhaf_f1 | CC-CF | ap_top1 | 40 | -0.138 | -0.287 | 0.000 |
| musique | RM64:banzhaf_f1 | CC-FF | group_evid | 40 | -0.200 | -0.325 | -0.075 |
| musique | RM64:banzhaf_f1 | CC-FF | all_zero | 40 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_f1 | CC-FF | group_top1 | 40 | -0.138 | -0.287 | 0.000 |
| musique | RM64:banzhaf_f1 | CC-FF | group_top1_cc | 40 | -0.176 | -0.344 | -0.019 |
| musique | RM64:banzhaf_f1 | CC-FF | ap_top1 | 40 | -0.625 | -0.775 | -0.475 |
| musique | RM64:banzhaf_f1 | C-F | group_evid | 43 | -0.023 | -0.116 | 0.070 |
| musique | RM64:banzhaf_f1 | C-F | all_zero | 43 | 0.000 | 0.000 | 0.000 |
| musique | RM64:banzhaf_f1 | C-F | group_top1 | 43 | -0.035 | -0.116 | 0.047 |
| musique | RM64:banzhaf_f1 | C-F | group_top1_cc | 43 | -0.051 | -0.145 | 0.037 |
| musique | RM64:banzhaf_f1 | C-F | ap_top1 | 43 | -0.442 | -0.593 | -0.302 |
| musique | RM64:linear_exact | CF-FF | group_evid | 40 | -0.125 | -0.225 | -0.025 |
| musique | RM64:linear_exact | CF-FF | all_zero | 40 | 0.025 | 0.000 | 0.075 |
| musique | RM64:linear_exact | CF-FF | group_top1 | 40 | -0.148 | -0.275 | -0.025 |
| musique | RM64:linear_exact | CF-FF | group_top1_cc | 40 | -0.169 | -0.312 | -0.035 |
| musique | RM64:linear_exact | CF-FF | ap_top1 | 40 | -0.549 | -0.723 | -0.375 |
| musique | RM64:linear_exact | CC-CF | group_evid | 40 | -0.175 | -0.350 | 0.000 |
| musique | RM64:linear_exact | CC-CF | all_zero | 40 | -0.025 | -0.075 | 0.000 |
| musique | RM64:linear_exact | CC-CF | group_top1 | 40 | -0.052 | -0.175 | 0.064 |
| musique | RM64:linear_exact | CC-CF | group_top1_cc | 40 | -0.078 | -0.219 | 0.053 |
| musique | RM64:linear_exact | CC-CF | ap_top1 | 40 | -0.076 | -0.226 | 0.074 |
| musique | RM64:linear_exact | CC-FF | group_evid | 40 | -0.275 | -0.450 | -0.125 |
| musique | RM64:linear_exact | CC-FF | all_zero | 40 | 0.000 | 0.000 | 0.000 |
| musique | RM64:linear_exact | CC-FF | group_top1 | 40 | -0.175 | -0.325 | -0.025 |
| musique | RM64:linear_exact | CC-FF | group_top1_cc | 40 | -0.216 | -0.387 | -0.045 |
| musique | RM64:linear_exact | CC-FF | ap_top1 | 40 | -0.575 | -0.725 | -0.425 |
| musique | RM64:linear_exact | C-F | group_evid | 43 | -0.093 | -0.209 | 0.000 |
| musique | RM64:linear_exact | C-F | all_zero | 43 | 0.000 | 0.000 | 0.000 |
| musique | RM64:linear_exact | C-F | group_top1 | 43 | 0.000 | -0.116 | 0.116 |
| musique | RM64:linear_exact | C-F | group_top1_cc | 43 | -0.013 | -0.139 | 0.111 |
| musique | RM64:linear_exact | C-F | ap_top1 | 43 | -0.395 | -0.558 | -0.233 |
| musique | V1 | CF-FF | group_evid | 40 | -0.025 | -0.075 | 0.000 |
| musique | V1 | CF-FF | all_zero | 40 | 0.000 | 0.000 | 0.000 |
| musique | V1 | CF-FF | group_top1 | 40 | -0.002 | -0.048 | 0.042 |
| musique | V1 | CF-FF | group_top1_cc | 40 | -0.034 | -0.082 | 0.014 |
| musique | V1 | CF-FF | ap_top1 | 40 | -0.144 | -0.227 | -0.067 |
| musique | V1 | CC-CF | group_evid | 40 | 0.000 | 0.000 | 0.000 |
| musique | V1 | CC-CF | all_zero | 40 | 0.000 | 0.000 | 0.000 |
| musique | V1 | CC-CF | group_top1 | 40 | 0.013 | -0.029 | 0.058 |
| musique | V1 | CC-CF | group_top1_cc | 40 | -0.020 | -0.068 | 0.035 |
| musique | V1 | CC-CF | ap_top1 | 40 | -0.090 | -0.171 | -0.019 |
| musique | V1 | CC-FF | group_evid | 40 | -0.025 | -0.075 | 0.000 |
| musique | V1 | CC-FF | all_zero | 40 | 0.000 | 0.000 | 0.000 |
| musique | V1 | CC-FF | group_top1 | 40 | 0.010 | -0.027 | 0.048 |
| musique | V1 | CC-FF | group_top1_cc | 40 | -0.056 | -0.099 | -0.011 |
| musique | V1 | CC-FF | ap_top1 | 40 | -0.210 | -0.273 | -0.146 |
| musique | V1 | C-F | group_evid | 43 | -0.047 | -0.116 | 0.000 |
| musique | V1 | C-F | all_zero | 43 | 0.000 | 0.000 | 0.000 |
| musique | V1 | C-F | group_top1 | 43 | -0.029 | -0.091 | 0.033 |
| musique | V1 | C-F | group_top1_cc | 43 | -0.064 | -0.130 | 0.002 |
| musique | V1 | C-F | ap_top1 | 43 | -0.229 | -0.316 | -0.143 |

## Cost
| dataset | file | calls | cost_cny |
|---|---|---|---|
| hotpotqa | P1.r3.cost.json | 3736 | 0.697 |
| hotpotqa | RM64.r3.cost.json | 2579 | 0.511 |
| hotpotqa | V1.r3.cost.json | 250 | 0.009 |
| hotpotqa | LOI.r3.cost.json | 1437 | 0.473 |
| hotpotqa | premise.cost.json | 371 | 0.104 |
| musique | P1.r3.cost.json | 5539 | 0.677 |
| musique | RM64.r3.cost.json | 11144 | 1.434 |
| musique | V1.r3.cost.json | 250 | 0.028 |
| musique | LOI.r3.cost.json | 2632 | 0.260 |
| musique | premise.cost.json | 643 | 0.239 |
