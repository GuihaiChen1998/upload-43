# Phase-2 main.test analysis

## Methods
| dataset | model | method | n | top1 | rec@g | random_top1 | all_zero | unique_max | reaches_tau | calls/inst | full_ctx_change |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | LOI | 510 | 0.751 | 0.509 | 0.200 | 0.247 | 0.559 | 0.753 | 10.000 | None |
| hotpotqa | claude-haiku-5-5 | MEXGEN_LOO | 510 | 0.781 | 0.560 | 0.200 | 0.200 | 0.547 | 0.778 | 0.000 | None |
| hotpotqa | claude-haiku-5-5 | P1 | 510 | 0.737 | 0.544 | 0.200 | 0.200 | 0.441 | 0.800 | 13.992 | 0.069 |
| hotpotqa | claude-haiku-5-5 | P1.r1 | 510 | 0.729 | 0.531 | 0.200 | 0.208 | 0.453 | 0.792 | 14.000 | None |
| hotpotqa | claude-haiku-5-5 | RM64 | 510 | 0.947 | 0.721 | 0.200 | 0.008 | 0.976 | 0.825 | 60.345 | None |
| hotpotqa | claude-haiku-5-5 | RM64:banzhaf_exact | 510 | 0.947 | 0.721 | 0.200 | 0.008 | 0.976 | 0.825 | 60.345 | None |
| hotpotqa | claude-haiku-5-5 | RM64:banzhaf_f1 | 510 | 0.963 | 0.736 | 0.200 | 0.004 | 0.986 | 0.853 | 60.345 | None |
| hotpotqa | claude-haiku-5-5 | RM64:linear_exact | 510 | 0.955 | 0.756 | 0.200 | 0.008 | 0.992 | 0.771 | 60.345 | None |
| hotpotqa | claude-haiku-5-5 | RM64:linear_f1 | 510 | 0.964 | 0.770 | 0.200 | 0.004 | 0.996 | 0.798 | 60.345 | None |
| hotpotqa | claude-haiku-5-5 | RM@16 | 510 | 0.927 | 0.628 | 0.200 | 0.020 | 0.914 | 0.833 | 17.000 | None |
| hotpotqa | claude-haiku-5-5 | RM@32 | 510 | 0.931 | 0.683 | 0.200 | 0.014 | 0.971 | 0.825 | 33.000 | None |
| hotpotqa | claude-haiku-5-5 | RM@8 | 510 | 0.774 | 0.547 | 0.200 | 0.071 | 0.778 | 0.880 | 9.000 | None |
| hotpotqa | claude-haiku-5-5 | V1 | 510 | 0.962 | 0.914 | 0.200 | 0.008 | 0.110 | 0.992 | 1.000 | None |
| hotpotqa | claude-haiku-5-5 | V1.r1 | 510 | 0.963 | 0.910 | 0.200 | 0.014 | 0.122 | 0.986 | 1.000 | None |
| hotpotqa | gemini-2.5-flash-lite | LOI | 291 | 0.873 | 0.585 | 0.201 | 0.096 | 0.656 | 0.904 | 9.979 | None |
| hotpotqa | gemini-2.5-flash-lite | MEXGEN_LOO | 291 | 0.774 | 0.495 | 0.201 | 0.213 | 0.649 | 0.735 | 0.000 | None |
| hotpotqa | gemini-2.5-flash-lite | P1 | 291 | 0.719 | 0.474 | 0.201 | 0.213 | 0.560 | 0.787 | 12.931 | 0.037 |
| hotpotqa | gemini-2.5-flash-lite | P1.r1 | 291 | 0.711 | 0.472 | 0.201 | 0.234 | 0.543 | 0.766 | 13.787 | None |
| hotpotqa | gemini-2.5-flash-lite | RM64 | 291 | 0.968 | 0.670 | 0.201 | 0.007 | 0.986 | 0.828 | 60.495 | None |
| hotpotqa | gemini-2.5-flash-lite | RM64:banzhaf_exact | 291 | 0.968 | 0.670 | 0.201 | 0.007 | 0.986 | 0.828 | 60.495 | None |
| hotpotqa | gemini-2.5-flash-lite | RM64:banzhaf_f1 | 291 | 0.967 | 0.684 | 0.201 | 0.007 | 0.993 | 0.859 | 60.495 | None |
| hotpotqa | gemini-2.5-flash-lite | RM64:linear_exact | 291 | 0.960 | 0.697 | 0.201 | 0.007 | 0.993 | 0.808 | 60.495 | None |
| hotpotqa | gemini-2.5-flash-lite | RM64:linear_f1 | 291 | 0.964 | 0.733 | 0.201 | 0.007 | 0.993 | 0.832 | 60.495 | None |
| hotpotqa | gemini-2.5-flash-lite | RM@16 | 291 | 0.918 | 0.599 | 0.201 | 0.027 | 0.924 | 0.900 | 17.000 | None |
| hotpotqa | gemini-2.5-flash-lite | RM@32 | 291 | 0.959 | 0.621 | 0.201 | 0.014 | 0.969 | 0.863 | 33.000 | None |
| hotpotqa | gemini-2.5-flash-lite | RM@8 | 291 | 0.788 | 0.516 | 0.201 | 0.055 | 0.842 | 0.907 | 9.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V1 | 291 | 0.961 | 0.840 | 0.201 | 0.000 | 0.282 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash-lite | V1.r1 | 291 | 0.965 | 0.851 | 0.201 | 0.000 | 0.261 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash | LOI | 81 | 0.913 | 0.671 | 0.200 | 0.099 | 0.543 | 0.901 | 10.000 | None |
| hotpotqa | gemini-2.5-flash | MEXGEN_LOO | 81 | 0.713 | 0.467 | 0.200 | 0.309 | 0.580 | 0.630 | 0.000 | None |
| hotpotqa | gemini-2.5-flash | P1 | 81 | 0.683 | 0.452 | 0.200 | 0.309 | 0.519 | 0.691 | 13.000 | 0.041 |
| hotpotqa | gemini-2.5-flash | P1.r1 | 81 | 0.675 | 0.441 | 0.200 | 0.309 | 0.543 | 0.691 | 14.000 | None |
| hotpotqa | gemini-2.5-flash | RM64 | 81 | 1.000 | 0.704 | 0.200 | 0.000 | 1.000 | 0.852 | 60.716 | None |
| hotpotqa | gemini-2.5-flash | RM64:banzhaf_exact | 81 | 1.000 | 0.704 | 0.200 | 0.000 | 1.000 | 0.852 | 60.716 | None |
| hotpotqa | gemini-2.5-flash | RM64:banzhaf_f1 | 81 | 1.000 | 0.710 | 0.200 | 0.000 | 1.000 | 0.889 | 60.716 | None |
| hotpotqa | gemini-2.5-flash | RM64:linear_exact | 81 | 0.988 | 0.747 | 0.200 | 0.000 | 1.000 | 0.827 | 60.716 | None |
| hotpotqa | gemini-2.5-flash | RM64:linear_f1 | 81 | 0.988 | 0.747 | 0.200 | 0.000 | 1.000 | 0.864 | 60.716 | None |
| hotpotqa | gemini-2.5-flash | RM@16 | 81 | 0.932 | 0.651 | 0.200 | 0.000 | 0.938 | 0.926 | 17.000 | None |
| hotpotqa | gemini-2.5-flash | RM@32 | 81 | 0.988 | 0.679 | 0.200 | 0.000 | 0.951 | 0.889 | 33.000 | None |
| hotpotqa | gemini-2.5-flash | RM@8 | 81 | 0.770 | 0.534 | 0.200 | 0.074 | 0.815 | 0.877 | 9.000 | None |
| hotpotqa | gemini-2.5-flash | V1 | 81 | 0.986 | 0.859 | 0.200 | 0.000 | 0.284 | 1.000 | 1.000 | None |
| hotpotqa | gemini-2.5-flash | V1.r1 | 81 | 0.990 | 0.853 | 0.200 | 0.000 | 0.309 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6-luna | LOI | 166 | 0.679 | 0.483 | 0.202 | 0.157 | 0.440 | 0.843 | 9.964 | None |
| hotpotqa | gpt-6-luna | MEXGEN_LOO | 166 | 0.605 | 0.395 | 0.202 | 0.367 | 0.506 | 0.602 | 0.000 | None |
| hotpotqa | gpt-6-luna | P1 | 166 | 0.570 | 0.383 | 0.202 | 0.367 | 0.428 | 0.633 | 12.657 | 0.086 |
| hotpotqa | gpt-6-luna | P1.r1 | 166 | 0.613 | 0.410 | 0.202 | 0.277 | 0.464 | 0.723 | 13.669 | None |
| hotpotqa | gpt-6-luna | RM64 | 166 | 0.854 | 0.597 | 0.202 | 0.084 | 0.904 | 0.627 | 58.627 | None |
| hotpotqa | gpt-6-luna | RM64:banzhaf_exact | 155 | 0.901 | 0.625 | 0.202 | 0.019 | 0.968 | 0.671 | 58.465 | None |
| hotpotqa | gpt-6-luna | RM64:banzhaf_f1 | 155 | 0.919 | 0.656 | 0.202 | 0.013 | 0.974 | 0.671 | 58.465 | None |
| hotpotqa | gpt-6-luna | RM64:linear_exact | 155 | 0.881 | 0.636 | 0.202 | 0.019 | 0.981 | 0.665 | 58.465 | None |
| hotpotqa | gpt-6-luna | RM64:linear_f1 | 155 | 0.899 | 0.670 | 0.202 | 0.013 | 0.987 | 0.626 | 58.465 | None |
| hotpotqa | gpt-6-luna | RM@16 | 155 | 0.812 | 0.546 | 0.202 | 0.084 | 0.871 | 0.729 | 17.000 | None |
| hotpotqa | gpt-6-luna | RM@32 | 155 | 0.868 | 0.587 | 0.202 | 0.039 | 0.916 | 0.710 | 33.000 | None |
| hotpotqa | gpt-6-luna | RM@8 | 155 | 0.731 | 0.479 | 0.202 | 0.123 | 0.742 | 0.781 | 9.000 | None |
| hotpotqa | gpt-6-luna | V1 | 166 | 0.975 | 0.874 | 0.202 | 0.000 | 0.235 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6-luna | V1.r1 | 166 | 0.963 | 0.874 | 0.202 | 0.000 | 0.223 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6.1-terra | LOI | 64 | 0.866 | 0.713 | 0.200 | 0.047 | 0.344 | 0.953 | 10.000 | None |
| hotpotqa | gpt-6.1-terra | MEXGEN_LOO | 64 | 0.599 | 0.376 | 0.200 | 0.484 | 0.500 | 0.484 | 0.000 | None |
| hotpotqa | gpt-6.1-terra | P1 | 64 | 0.538 | 0.358 | 0.200 | 0.484 | 0.406 | 0.516 | 13.000 | 0.068 |
| hotpotqa | gpt-6.1-terra | P1.r1 | 64 | 0.564 | 0.370 | 0.200 | 0.484 | 0.438 | 0.516 | 14.000 | None |
| hotpotqa | gpt-6.1-terra | RM64 | 64 | 0.969 | 0.727 | 0.200 | 0.000 | 1.000 | 0.641 | 60.719 | None |
| hotpotqa | gpt-6.1-terra | RM64:banzhaf_exact | 64 | 0.969 | 0.727 | 0.200 | 0.000 | 1.000 | 0.641 | 60.719 | None |
| hotpotqa | gpt-6.1-terra | RM64:banzhaf_f1 | 64 | 0.953 | 0.734 | 0.200 | 0.000 | 1.000 | 0.656 | 60.719 | None |
| hotpotqa | gpt-6.1-terra | RM64:linear_exact | 64 | 0.938 | 0.742 | 0.200 | 0.000 | 1.000 | 0.625 | 60.719 | None |
| hotpotqa | gpt-6.1-terra | RM64:linear_f1 | 64 | 0.938 | 0.773 | 0.200 | 0.000 | 1.000 | 0.578 | 60.719 | None |
| hotpotqa | gpt-6.1-terra | RM@16 | 64 | 0.809 | 0.596 | 0.200 | 0.062 | 0.859 | 0.750 | 17.000 | None |
| hotpotqa | gpt-6.1-terra | RM@32 | 64 | 0.971 | 0.698 | 0.200 | 0.000 | 0.938 | 0.719 | 33.000 | None |
| hotpotqa | gpt-6.1-terra | RM@8 | 64 | 0.691 | 0.495 | 0.200 | 0.188 | 0.703 | 0.766 | 9.000 | None |
| hotpotqa | gpt-6.1-terra | V1 | 64 | 0.987 | 0.931 | 0.200 | 0.000 | 0.125 | 1.000 | 1.000 | None |
| hotpotqa | gpt-6.1-terra | V1.r1 | 64 | 0.992 | 0.930 | 0.200 | 0.000 | 0.141 | 1.000 | 1.000 | None |
| musique | claude-haiku-5-5 | LOI | 750 | 0.395 | 0.238 | 0.133 | 0.672 | 0.308 | 0.328 | 19.979 | None |
| musique | claude-haiku-5-5 | MEXGEN_LOO | 750 | 0.804 | 0.590 | 0.133 | 0.036 | 0.359 | 0.951 | 0.000 | None |
| musique | claude-haiku-5-5 | P1 | 750 | 0.732 | 0.550 | 0.133 | 0.036 | 0.285 | 0.964 | 23.831 | 0.126 |
| musique | claude-haiku-5-5 | P1.r1 | 750 | 0.722 | 0.551 | 0.133 | 0.053 | 0.251 | 0.947 | 23.729 | None |
| musique | claude-haiku-5-5 | RM64 | 750 | 0.945 | 0.727 | 0.133 | 0.021 | 0.944 | 0.557 | 63.692 | None |
| musique | claude-haiku-5-5 | RM64:banzhaf_exact | 747 | 0.948 | 0.729 | 0.133 | 0.017 | 0.948 | 0.560 | 63.691 | None |
| musique | claude-haiku-5-5 | RM64:banzhaf_f1 | 747 | 0.956 | 0.738 | 0.133 | 0.003 | 0.967 | 0.574 | 63.691 | None |
| musique | claude-haiku-5-5 | RM64:linear_exact | 747 | 0.942 | 0.735 | 0.133 | 0.017 | 0.983 | 0.443 | 63.691 | None |
| musique | claude-haiku-5-5 | RM64:linear_f1 | 747 | 0.954 | 0.749 | 0.133 | 0.003 | 0.997 | 0.466 | 63.691 | None |
| musique | claude-haiku-5-5 | RM@16 | 747 | 0.782 | 0.562 | 0.133 | 0.054 | 0.774 | 0.633 | 17.000 | None |
| musique | claude-haiku-5-5 | RM@32 | 747 | 0.907 | 0.665 | 0.133 | 0.024 | 0.906 | 0.581 | 33.000 | None |
| musique | claude-haiku-5-5 | RM@8 | 747 | 0.534 | 0.409 | 0.133 | 0.162 | 0.569 | 0.764 | 9.000 | None |
| musique | claude-haiku-5-5 | V1 | 750 | 0.949 | 0.893 | 0.133 | 0.017 | 0.048 | 0.983 | 1.000 | None |
| musique | claude-haiku-5-5 | V1.r1 | 750 | 0.936 | 0.879 | 0.133 | 0.032 | 0.053 | 0.968 | 1.000 | None |
| musique | gemini-2.5-flash-lite | LOI | 774 | 0.792 | 0.391 | 0.137 | 0.214 | 0.726 | 0.786 | 19.968 | None |
| musique | gemini-2.5-flash-lite | MEXGEN_LOO | 774 | 0.790 | 0.465 | 0.137 | 0.071 | 0.606 | 0.904 | 0.000 | None |
| musique | gemini-2.5-flash-lite | P1 | 774 | 0.718 | 0.438 | 0.137 | 0.071 | 0.487 | 0.929 | 22.921 | 0.053 |
| musique | gemini-2.5-flash-lite | P1.r1 | 774 | 0.722 | 0.437 | 0.137 | 0.068 | 0.497 | 0.932 | 23.820 | None |
| musique | gemini-2.5-flash-lite | RM64 | 774 | 0.980 | 0.570 | 0.137 | 0.003 | 0.990 | 0.828 | 63.996 | None |
| musique | gemini-2.5-flash-lite | RM64:banzhaf_exact | 774 | 0.980 | 0.570 | 0.137 | 0.003 | 0.990 | 0.828 | 63.996 | None |
| musique | gemini-2.5-flash-lite | RM64:banzhaf_f1 | 774 | 0.991 | 0.584 | 0.137 | 0.000 | 0.996 | 0.846 | 63.996 | None |
| musique | gemini-2.5-flash-lite | RM64:linear_exact | 774 | 0.969 | 0.593 | 0.137 | 0.003 | 0.997 | 0.767 | 63.996 | None |
| musique | gemini-2.5-flash-lite | RM64:linear_f1 | 774 | 0.979 | 0.619 | 0.137 | 0.000 | 1.000 | 0.787 | 63.996 | None |
| musique | gemini-2.5-flash-lite | RM@16 | 774 | 0.889 | 0.486 | 0.137 | 0.017 | 0.911 | 0.832 | 17.000 | None |
| musique | gemini-2.5-flash-lite | RM@32 | 774 | 0.951 | 0.536 | 0.137 | 0.008 | 0.968 | 0.814 | 33.000 | None |
| musique | gemini-2.5-flash-lite | RM@8 | 774 | 0.708 | 0.408 | 0.137 | 0.066 | 0.735 | 0.893 | 9.000 | None |
| musique | gemini-2.5-flash-lite | V1 | 774 | 0.934 | 0.798 | 0.137 | 0.003 | 0.141 | 0.997 | 1.000 | None |
| musique | gemini-2.5-flash-lite | V1.r1 | 774 | 0.930 | 0.786 | 0.137 | 0.004 | 0.156 | 0.996 | 1.000 | None |
| musique | gemini-2.5-flash | LOI | 62 | 0.867 | 0.440 | 0.131 | 0.113 | 0.774 | 0.887 | 19.984 | None |
| musique | gemini-2.5-flash | MEXGEN_LOO | 62 | 0.810 | 0.454 | 0.131 | 0.129 | 0.661 | 0.839 | 0.000 | None |
| musique | gemini-2.5-flash | P1 | 62 | 0.775 | 0.434 | 0.131 | 0.129 | 0.613 | 0.871 | 22.984 | 0.016 |
| musique | gemini-2.5-flash | P1.r1 | 62 | 0.763 | 0.432 | 0.131 | 0.145 | 0.597 | 0.855 | 23.984 | None |
| musique | gemini-2.5-flash | RM64 | 62 | 0.968 | 0.524 | 0.131 | 0.000 | 1.000 | 0.919 | 63.984 | None |
| musique | gemini-2.5-flash | RM64:banzhaf_exact | 62 | 0.968 | 0.524 | 0.131 | 0.000 | 1.000 | 0.919 | 63.984 | None |
| musique | gemini-2.5-flash | RM64:banzhaf_f1 | 62 | 0.968 | 0.528 | 0.131 | 0.000 | 1.000 | 0.919 | 63.984 | None |
| musique | gemini-2.5-flash | RM64:linear_exact | 62 | 0.968 | 0.570 | 0.131 | 0.000 | 1.000 | 0.855 | 63.984 | None |
| musique | gemini-2.5-flash | RM64:linear_f1 | 62 | 0.968 | 0.583 | 0.131 | 0.000 | 1.000 | 0.887 | 63.984 | None |
| musique | gemini-2.5-flash | RM@16 | 62 | 0.895 | 0.505 | 0.131 | 0.000 | 0.952 | 0.935 | 17.000 | None |
| musique | gemini-2.5-flash | RM@32 | 62 | 0.944 | 0.555 | 0.131 | 0.000 | 0.984 | 0.887 | 33.000 | None |
| musique | gemini-2.5-flash | RM@8 | 62 | 0.695 | 0.451 | 0.131 | 0.032 | 0.790 | 0.935 | 9.000 | None |
| musique | gemini-2.5-flash | V1 | 62 | 0.953 | 0.808 | 0.131 | 0.000 | 0.194 | 1.000 | 1.000 | None |
| musique | gemini-2.5-flash | V1.r1 | 62 | 0.961 | 0.836 | 0.131 | 0.000 | 0.161 | 1.000 | 1.000 | None |
| musique | gpt-6-luna | LOI | 602 | 0.749 | 0.420 | 0.138 | 0.113 | 0.616 | 0.887 | 19.914 | None |
| musique | gpt-6-luna | MEXGEN_LOO | 602 | 0.676 | 0.395 | 0.138 | 0.075 | 0.537 | 0.890 | 0.000 | None |
| musique | gpt-6-luna | P1 | 602 | 0.596 | 0.369 | 0.138 | 0.075 | 0.412 | 0.925 | 23.900 | 0.136 |
| musique | gpt-6-luna | P1.r1 | 602 | 0.572 | 0.359 | 0.138 | 0.088 | 0.372 | 0.912 | 23.751 | None |
| musique | gpt-6-luna | RM64 | 602 | 0.890 | 0.478 | 0.138 | 0.008 | 0.980 | 0.762 | 63.017 | None |
| musique | gpt-6-luna | RM64:banzhaf_exact | 602 | 0.890 | 0.478 | 0.138 | 0.008 | 0.980 | 0.762 | 63.017 | None |
| musique | gpt-6-luna | RM64:banzhaf_f1 | 602 | 0.906 | 0.499 | 0.138 | 0.003 | 0.993 | 0.746 | 63.017 | None |
| musique | gpt-6-luna | RM64:linear_exact | 602 | 0.873 | 0.503 | 0.138 | 0.008 | 0.992 | 0.738 | 63.017 | None |
| musique | gpt-6-luna | RM64:linear_f1 | 602 | 0.898 | 0.522 | 0.138 | 0.003 | 0.997 | 0.711 | 63.017 | None |
| musique | gpt-6-luna | RM@16 | 602 | 0.817 | 0.427 | 0.138 | 0.022 | 0.900 | 0.812 | 17.000 | None |
| musique | gpt-6-luna | RM@32 | 602 | 0.863 | 0.464 | 0.138 | 0.010 | 0.978 | 0.776 | 33.000 | None |
| musique | gpt-6-luna | RM@8 | 602 | 0.673 | 0.383 | 0.138 | 0.076 | 0.728 | 0.895 | 9.000 | None |
| musique | gpt-6-luna | V1 | 602 | 0.952 | 0.843 | 0.138 | 0.005 | 0.091 | 0.995 | 1.000 | None |
| musique | gpt-6-luna | V1.r1 | 602 | 0.948 | 0.844 | 0.138 | 0.002 | 0.091 | 0.998 | 1.000 | None |
| musique | gpt-6.1-terra | LOI | 54 | 0.880 | 0.440 | 0.133 | 0.093 | 0.778 | 0.907 | 20.000 | None |
| musique | gpt-6.1-terra | MEXGEN_LOO | 54 | 0.793 | 0.407 | 0.133 | 0.130 | 0.704 | 0.870 | 0.000 | None |
| musique | gpt-6.1-terra | P1 | 54 | 0.760 | 0.392 | 0.133 | 0.130 | 0.667 | 0.870 | 23.000 | 0.080 |
| musique | gpt-6.1-terra | P1.r1 | 54 | 0.831 | 0.420 | 0.133 | 0.074 | 0.741 | 0.926 | 24.000 | None |
| musique | gpt-6.1-terra | RM64 | 54 | 0.981 | 0.546 | 0.133 | 0.000 | 1.000 | 0.815 | 61.407 | None |
| musique | gpt-6.1-terra | RM64:banzhaf_exact | 54 | 0.981 | 0.546 | 0.133 | 0.000 | 1.000 | 0.815 | 61.407 | None |
| musique | gpt-6.1-terra | RM64:banzhaf_f1 | 54 | 0.981 | 0.535 | 0.133 | 0.000 | 1.000 | 0.778 | 61.407 | None |
| musique | gpt-6.1-terra | RM64:linear_exact | 54 | 0.981 | 0.590 | 0.133 | 0.000 | 1.000 | 0.796 | 61.407 | None |
| musique | gpt-6.1-terra | RM64:linear_f1 | 54 | 0.981 | 0.594 | 0.133 | 0.000 | 1.000 | 0.778 | 61.407 | None |
| musique | gpt-6.1-terra | RM@16 | 54 | 0.870 | 0.459 | 0.133 | 0.000 | 0.944 | 0.833 | 17.000 | None |
| musique | gpt-6.1-terra | RM@32 | 54 | 0.963 | 0.517 | 0.133 | 0.000 | 1.000 | 0.852 | 33.000 | None |
| musique | gpt-6.1-terra | RM@8 | 54 | 0.717 | 0.405 | 0.133 | 0.037 | 0.759 | 0.870 | 9.000 | None |
| musique | gpt-6.1-terra | V1 | 54 | 0.975 | 0.879 | 0.133 | 0.000 | 0.074 | 1.000 | 1.000 | None |
| musique | gpt-6.1-terra | V1.r1 | 54 | 0.966 | 0.890 | 0.133 | 0.000 | 0.093 | 1.000 | 1.000 | None |

## Stability (repeat 1 vs 0)
| dataset | model | method | n | identical_phi | per_source_agree | n_same_a0 | per_source_agree_same_a0 | top_group_jaccard | spearman_tie_preserving | n_rho_defined |
|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | V1 | 510 | 0.916 | 0.989 | 0 | nan | 0.957 | 0.972 | 502 |
| hotpotqa | claude-haiku-5-5 | P1 | 510 | 0.584 | 0.903 | 476 | 0.936 | 0.716 | 0.750 | 372 |
| hotpotqa | gemini-2.5-flash-lite | V1 | 291 | 0.893 | 0.989 | 0 | nan | 0.951 | 0.966 | 291 |
| hotpotqa | gemini-2.5-flash-lite | P1 | 291 | 0.729 | 0.932 | 274 | 0.964 | 0.821 | 0.851 | 210 |
| hotpotqa | gemini-2.5-flash | V1 | 81 | 0.938 | 0.994 | 0 | nan | 0.971 | 0.981 | 81 |
| hotpotqa | gemini-2.5-flash | P1 | 81 | 0.778 | 0.944 | 78 | 0.974 | 0.856 | 0.877 | 52 |
| hotpotqa | gpt-6-luna | V1 | 166 | 0.849 | 0.981 | 0 | nan | 0.917 | 0.935 | 166 |
| hotpotqa | gpt-6-luna | P1 | 166 | 0.608 | 0.884 | 128 | 0.954 | 0.727 | 0.697 | 99 |
| hotpotqa | gpt-6.1-terra | V1 | 64 | 0.906 | 0.991 | 0 | nan | 0.956 | 0.970 | 64 |
| hotpotqa | gpt-6.1-terra | P1 | 64 | 0.797 | 0.928 | 57 | 0.967 | 0.836 | 0.822 | 28 |
| musique | claude-haiku-5-5 | V1 | 750 | 0.827 | 0.986 | 0 | nan | 0.911 | 0.958 | 718 |
| musique | claude-haiku-5-5 | P1 | 750 | 0.397 | 0.856 | 641 | 0.913 | 0.623 | 0.626 | 680 |
| musique | gemini-2.5-flash-lite | V1 | 774 | 0.857 | 0.990 | 0 | nan | 0.940 | 0.960 | 770 |
| musique | gemini-2.5-flash-lite | P1 | 774 | 0.610 | 0.921 | 734 | 0.955 | 0.781 | 0.797 | 696 |
| musique | gemini-2.5-flash | V1 | 62 | 0.871 | 0.994 | 0 | nan | 0.953 | 0.971 | 62 |
| musique | gemini-2.5-flash | P1 | 62 | 0.710 | 0.973 | 61 | 0.973 | 0.837 | 0.911 | 51 |
| musique | gpt-6-luna | V1 | 602 | 0.703 | 0.977 | 0 | nan | 0.856 | 0.899 | 598 |
| musique | gpt-6-luna | P1 | 602 | 0.372 | 0.819 | 499 | 0.898 | 0.593 | 0.540 | 517 |
| musique | gpt-6.1-terra | V1 | 54 | 0.759 | 0.987 | 0 | nan | 0.906 | 0.940 | 54 |
| musique | gpt-6.1-terra | P1 | 54 | 0.630 | 0.881 | 48 | 0.963 | 0.729 | 0.803 | 43 |

## RM K-sensitivity (banzhaf, exact). k = prefix vs K_max (overlapping); halves = disjoint first vs second K/2 masks. 'argmax_agree' = tie-aware top-group Jaccard
| dataset | model | k | spearman_vs_Kmax | argmax_agree | unique_masks_min | unique_masks_mean |
|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | halves | 0.384 | 0.803 | 57 | 62.016 |
| hotpotqa | claude-haiku-5-5 | 8 | 0.549 | 0.654 | None | None |
| hotpotqa | claude-haiku-5-5 | 16 | 0.654 | 0.806 | None | None |
| hotpotqa | claude-haiku-5-5 | 32 | 0.785 | 0.886 | None | None |
| hotpotqa | gemini-2.5-flash-lite | halves | 0.337 | 0.855 | 16 | 61.887 |
| hotpotqa | gemini-2.5-flash-lite | 8 | 0.513 | 0.718 | None | None |
| hotpotqa | gemini-2.5-flash-lite | 16 | 0.620 | 0.878 | None | None |
| hotpotqa | gemini-2.5-flash-lite | 32 | 0.756 | 0.953 | None | None |
| hotpotqa | gemini-2.5-flash | halves | 0.343 | 0.833 | 57 | 62.037 |
| hotpotqa | gemini-2.5-flash | 8 | 0.514 | 0.651 | None | None |
| hotpotqa | gemini-2.5-flash | 16 | 0.625 | 0.821 | None | None |
| hotpotqa | gemini-2.5-flash | 32 | 0.766 | 0.926 | None | None |
| hotpotqa | gpt-6-luna | halves | 0.389 | 0.773 | 16 | 61.677 |
| hotpotqa | gpt-6-luna | 8 | 0.533 | 0.682 | None | None |
| hotpotqa | gpt-6-luna | 16 | 0.641 | 0.779 | None | None |
| hotpotqa | gpt-6-luna | 32 | 0.774 | 0.864 | None | None |
| hotpotqa | gpt-6.1-terra | halves | 0.332 | 0.790 | 57 | 62.203 |
| hotpotqa | gpt-6.1-terra | 8 | 0.555 | 0.558 | None | None |
| hotpotqa | gpt-6.1-terra | 16 | 0.664 | 0.686 | None | None |
| hotpotqa | gpt-6.1-terra | 32 | 0.754 | 0.919 | None | None |
| musique | claude-haiku-5-5 | halves | 0.231 | 0.617 | 63 | 63.996 |
| musique | claude-haiku-5-5 | 8 | 0.451 | 0.415 | None | None |
| musique | claude-haiku-5-5 | 16 | 0.566 | 0.632 | None | None |
| musique | claude-haiku-5-5 | 32 | 0.733 | 0.789 | None | None |
| musique | gemini-2.5-flash-lite | halves | 0.200 | 0.847 | 63 | 63.997 |
| musique | gemini-2.5-flash-lite | 8 | 0.434 | 0.644 | None | None |
| musique | gemini-2.5-flash-lite | 16 | 0.558 | 0.835 | None | None |
| musique | gemini-2.5-flash-lite | 32 | 0.724 | 0.912 | None | None |
| musique | gemini-2.5-flash | halves | 0.134 | 0.871 | 64 | 64.000 |
| musique | gemini-2.5-flash | 8 | 0.397 | 0.630 | None | None |
| musique | gemini-2.5-flash | 16 | 0.565 | 0.855 | None | None |
| musique | gemini-2.5-flash | 32 | 0.702 | 0.911 | None | None |
| musique | gpt-6-luna | halves | 0.183 | 0.823 | 63 | 63.997 |
| musique | gpt-6-luna | 8 | 0.416 | 0.635 | None | None |
| musique | gpt-6-luna | 16 | 0.546 | 0.812 | None | None |
| musique | gpt-6-luna | 32 | 0.727 | 0.900 | None | None |
| musique | gpt-6.1-terra | halves | 0.174 | 0.852 | 64 | 64.000 |
| musique | gpt-6.1-terra | 8 | 0.385 | 0.647 | None | None |
| musique | gpt-6.1-terra | 16 | 0.504 | 0.852 | None | None |
| musique | gpt-6.1-terra | 32 | 0.710 | 0.963 | None | None |

## Projected cost of the main run (per-call cost from the pilot x formula calls x evaluable set)
| dataset | model | method | cny_per_call | calls_per_inst | cny_per_inst | n_eval | cny_total |
|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | LOI | 0.000 | 11 | 0.000 | 522 | 0.231 |
| hotpotqa | claude-haiku-5-5 | V1.r1 | 0.000 | 1 | 0.000 | 522 | 0.049 |
| hotpotqa | claude-haiku-5-5 | V1 | 0.000 | 1 | 0.000 | 522 | 0.049 |
| hotpotqa | claude-haiku-5-5 | P1 | 0.000 | 14 | 0.001 | 522 | 0.633 |
| hotpotqa | claude-haiku-5-5 | P1.r1 | 0.000 | 14 | 0.001 | 522 | 0.634 |
| hotpotqa | claude-haiku-5-5 | RM32 | 0.000 | 33 | 0.002 | 522 | 1.298 |
| hotpotqa | gemini-2.5-flash-lite | LOI | 0.000 | 11 | 0.000 | 303 | 0.048 |
| hotpotqa | gemini-2.5-flash-lite | V1.r1 | 0.000 | 1 | 0.000 | 303 | 0.020 |
| hotpotqa | gemini-2.5-flash-lite | V1 | 0.000 | 1 | 0.000 | 303 | 0.020 |
| hotpotqa | gemini-2.5-flash-lite | P1 | 0.000 | 14 | 0.001 | 303 | 0.255 |
| hotpotqa | gemini-2.5-flash-lite | P1.r1 | 0.000 | 14 | 0.001 | 303 | 0.257 |
| hotpotqa | gemini-2.5-flash-lite | RM32 | 0.000 | 33 | 0.001 | 303 | 0.356 |
| hotpotqa | gemini-2.5-flash | LOI | 0.000 | 11 | 0.001 | 87 | 0.049 |
| hotpotqa | gemini-2.5-flash | V1.r1 | 0.000 | 1 | 0.000 | 87 | 0.019 |
| hotpotqa | gemini-2.5-flash | V1 | 0.000 | 1 | 0.000 | 87 | 0.019 |
| hotpotqa | gemini-2.5-flash | P1 | 0.000 | 14 | 0.003 | 87 | 0.231 |
| hotpotqa | gemini-2.5-flash | P1.r1 | 0.000 | 14 | 0.003 | 87 | 0.232 |
| hotpotqa | gemini-2.5-flash | RM32 | 0.000 | 33 | 0.004 | 87 | 0.333 |
| hotpotqa | gpt-6-luna | LOI | 0.000 | 11 | 0.000 | 178 | 0.011 |
| hotpotqa | gpt-6-luna | V1.r1 | 0.000 | 1 | 0.000 | 178 | 0.013 |
| hotpotqa | gpt-6-luna | V1 | 0.000 | 1 | 0.000 | 178 | 0.039 |
| hotpotqa | gpt-6-luna | P1 | 0.000 | 14 | 0.001 | 178 | 0.250 |
| hotpotqa | gpt-6-luna | P1.r1 | 0.000 | 14 | 0.002 | 178 | 0.428 |
| hotpotqa | gpt-6-luna | RM32 | 0.000 | 33 | 0.004 | 178 | 0.623 |
| hotpotqa | gpt-6.1-terra | LOI | 0.001 | 11 | 0.011 | 70 | 0.749 |
| hotpotqa | gpt-6.1-terra | V1.r1 | 0.001 | 1 | 0.001 | 70 | 0.092 |
| hotpotqa | gpt-6.1-terra | V1 | 0.001 | 1 | 0.001 | 70 | 0.095 |
| hotpotqa | gpt-6.1-terra | P1 | 0.001 | 14 | 0.019 | 70 | 1.324 |
| hotpotqa | gpt-6.1-terra | P1.r1 | 0.001 | 14 | 0.014 | 70 | 1.007 |
| hotpotqa | gpt-6.1-terra | RM32 | 0.001 | 33 | 0.042 | 70 | 2.936 |
| musique | claude-haiku-5-5 | LOI | 0.000 | 21 | 0.001 | 762 | 0.730 |
| musique | claude-haiku-5-5 | V1.r1 | 0.000 | 1 | 0.000 | 762 | 0.153 |
| musique | claude-haiku-5-5 | V1 | 0.000 | 1 | 0.000 | 762 | 0.136 |
| musique | claude-haiku-5-5 | P1 | 0.000 | 24 | 0.004 | 762 | 2.989 |
| musique | claude-haiku-5-5 | P1.r1 | 0.000 | 24 | 0.004 | 762 | 2.985 |
| musique | claude-haiku-5-5 | RM32 | 0.000 | 33 | 0.004 | 762 | 3.012 |
| musique | gemini-2.5-flash-lite | LOI | 0.000 | 21 | 0.000 | 786 | 0.232 |
| musique | gemini-2.5-flash-lite | V1.r1 | 0.000 | 1 | 0.000 | 786 | 0.089 |
| musique | gemini-2.5-flash-lite | V1 | 0.000 | 1 | 0.000 | 786 | 0.089 |
| musique | gemini-2.5-flash-lite | P1 | 0.000 | 24 | 0.003 | 786 | 1.992 |
| musique | gemini-2.5-flash-lite | P1.r1 | 0.000 | 24 | 0.003 | 786 | 2.007 |
| musique | gemini-2.5-flash-lite | RM32 | 0.000 | 33 | 0.002 | 786 | 1.551 |
| musique | gemini-2.5-flash | LOI | 0.000 | 21 | 0.001 | 68 | 0.072 |
| musique | gemini-2.5-flash | V1.r1 | 0.000 | 1 | 0.000 | 68 | 0.024 |
| musique | gemini-2.5-flash | V1 | 0.000 | 1 | 0.000 | 68 | 0.024 |
| musique | gemini-2.5-flash | P1 | 0.000 | 24 | 0.008 | 68 | 0.527 |
| musique | gemini-2.5-flash | P1.r1 | 0.000 | 24 | 0.008 | 68 | 0.526 |
| musique | gemini-2.5-flash | RM32 | 0.000 | 33 | 0.006 | 68 | 0.421 |
| musique | gpt-6-luna | LOI | 0.000 | 21 | 0.002 | 614 | 1.293 |
| musique | gpt-6-luna | V1.r1 | 0.000 | 1 | 0.000 | 614 | 0.079 |
| musique | gpt-6-luna | V1 | 0.000 | 1 | 0.000 | 614 | 0.070 |
| musique | gpt-6-luna | P1 | 0.000 | 24 | 0.003 | 614 | 1.757 |
| musique | gpt-6-luna | P1.r1 | 0.000 | 24 | 0.003 | 614 | 1.871 |
| musique | gpt-6-luna | RM32 | 0.000 | 33 | 0.004 | 614 | 2.698 |
| musique | gpt-6.1-terra | LOI | 0.001 | 21 | 0.021 | 60 | 1.235 |
| musique | gpt-6.1-terra | V1.r1 | 0.002 | 1 | 0.002 | 60 | 0.110 |
| musique | gpt-6.1-terra | V1 | 0.002 | 1 | 0.002 | 60 | 0.108 |
| musique | gpt-6.1-terra | P1 | 0.002 | 24 | 0.038 | 60 | 2.256 |
| musique | gpt-6.1-terra | P1.r1 | 0.002 | 24 | 0.043 | 60 | 2.572 |
| musique | gpt-6.1-terra | RM32 | 0.001 | 33 | 0.038 | 60 | 2.268 |

## Cost
| dataset | model | method | n | cost_cny | cny_per_inst | calls_issued | truncated |
|---|---|---|---|---|---|---|---|
| hotpotqa | claude-haiku-5-5 | LOI | 522 | 0.205 | 0.000 | 5100 | 0 |
| hotpotqa | claude-haiku-5-5 | V1.r1 | 522 | 0.048 | 0.000 | 510 | 0 |
| hotpotqa | claude-haiku-5-5 | V1 | 522 | 0.048 | 0.000 | 510 | 0 |
| hotpotqa | claude-haiku-5-5 | P1 | 522 | 0.618 | 0.001 | 7136 | 0 |
| hotpotqa | claude-haiku-5-5 | P1.r1 | 522 | 0.620 | 0.001 | 7140 | 0 |
| hotpotqa | claude-haiku-5-5 | RM64 | 159 | 0.695 | 0.004 | 9220 | 0 |
| hotpotqa | gemini-2.5-flash-lite | LOI | 303 | 0.042 | 0.000 | 2904 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V1.r1 | 303 | 0.019 | 0.000 | 291 | 0 |
| hotpotqa | gemini-2.5-flash-lite | V1 | 303 | 0.019 | 0.000 | 291 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P1 | 303 | 0.227 | 0.001 | 3763 | 0 |
| hotpotqa | gemini-2.5-flash-lite | P1.r1 | 303 | 0.243 | 0.001 | 4012 | 0 |
| hotpotqa | gemini-2.5-flash-lite | RM64 | 303 | 0.627 | 0.002 | 17604 | 0 |
| hotpotqa | gemini-2.5-flash | LOI | 87 | 0.042 | 0.000 | 810 | 0 |
| hotpotqa | gemini-2.5-flash | V1.r1 | 87 | 0.018 | 0.000 | 81 | 0 |
| hotpotqa | gemini-2.5-flash | V1 | 87 | 0.017 | 0.000 | 81 | 0 |
| hotpotqa | gemini-2.5-flash | P1 | 87 | 0.199 | 0.002 | 1053 | 0 |
| hotpotqa | gemini-2.5-flash | P1.r1 | 87 | 0.216 | 0.002 | 1134 | 0 |
| hotpotqa | gemini-2.5-flash | RM64 | 87 | 0.570 | 0.007 | 4918 | 0 |
| hotpotqa | gpt-6-luna | LOI | 178 | 0.010 | 0.000 | 1654 | 0 |
| hotpotqa | gpt-6-luna | V1.r1 | 178 | 0.012 | 0.000 | 166 | 0 |
| hotpotqa | gpt-6-luna | V1 | 178 | 0.037 | 0.000 | 166 | 0 |
| hotpotqa | gpt-6-luna | P1 | 35 | 0.045 | 0.001 | 443 | 0 |
| hotpotqa | gpt-6-luna | P1.r1 | 178 | 0.390 | 0.002 | 2269 | 0 |
| hotpotqa | gpt-6-luna | RM64 | 32 | 0.184 | 0.006 | 1732 | 0 |
| hotpotqa | gpt-6.1-terra | LOI | 70 | 0.623 | 0.009 | 640 | 0 |
| hotpotqa | gpt-6.1-terra | V1.r1 | 70 | 0.084 | 0.001 | 64 | 0 |
| hotpotqa | gpt-6.1-terra | V1 | 70 | 0.087 | 0.001 | 64 | 0 |
| hotpotqa | gpt-6.1-terra | P1 | 70 | 1.124 | 0.016 | 832 | 0 |
| hotpotqa | gpt-6.1-terra | P1.r1 | 70 | 0.921 | 0.013 | 896 | 0 |
| hotpotqa | gpt-6.1-terra | RM64 | 70 | 4.940 | 0.071 | 3886 | 0 |
| musique | claude-haiku-5-5 | LOI | 762 | 0.683 | 0.001 | 14984 | 0 |
| musique | claude-haiku-5-5 | V1.r1 | 387 | 0.076 | 0.000 | 379 | 1 |
| musique | claude-haiku-5-5 | V1 | 762 | 0.134 | 0.000 | 750 | 1 |
| musique | claude-haiku-5-5 | P1 | 762 | 2.922 | 0.004 | 17873 | 3 |
| musique | claude-haiku-5-5 | P1.r1 | 762 | 2.913 | 0.004 | 17846 | 2 |
| musique | claude-haiku-5-5 | RM64 | 601 | 4.511 | 0.008 | 37658 | 3 |
| musique | gemini-2.5-flash-lite | LOI | 786 | 0.217 | 0.000 | 15455 | 0 |
| musique | gemini-2.5-flash-lite | V1.r1 | 786 | 0.088 | 0.000 | 774 | 0 |
| musique | gemini-2.5-flash-lite | V1 | 786 | 0.088 | 0.000 | 774 | 0 |
| musique | gemini-2.5-flash-lite | P1 | 786 | 1.873 | 0.002 | 17741 | 0 |
| musique | gemini-2.5-flash-lite | P1.r1 | 353 | 0.872 | 0.002 | 8191 | 0 |
| musique | gemini-2.5-flash-lite | RM64 | 786 | 2.962 | 0.004 | 49533 | 2 |
| musique | gemini-2.5-flash | LOI | 68 | 0.062 | 0.001 | 1239 | 0 |
| musique | gemini-2.5-flash | V1.r1 | 68 | 0.022 | 0.000 | 62 | 0 |
| musique | gemini-2.5-flash | V1 | 68 | 0.022 | 0.000 | 62 | 0 |
| musique | gemini-2.5-flash | P1 | 68 | 0.460 | 0.007 | 1425 | 0 |
| musique | gemini-2.5-flash | P1.r1 | 68 | 0.480 | 0.007 | 1487 | 0 |
| musique | gemini-2.5-flash | RM64 | 68 | 0.744 | 0.011 | 3967 | 0 |
| musique | gpt-6-luna | LOI | 296 | 0.589 | 0.002 | 5871 | 1 |
| musique | gpt-6-luna | V1.r1 | 614 | 0.079 | 0.000 | 614 | 0 |
| musique | gpt-6-luna | V1 | 614 | 0.070 | 0.000 | 614 | 0 |
| musique | gpt-6-luna | P1 | 614 | 1.750 | 0.003 | 14674 | 0 |
| musique | gpt-6-luna | P1.r1 | 28 | 0.074 | 0.003 | 580 | 0 |
| musique | gpt-6-luna | RM64 | 215 | 1.799 | 0.008 | 13507 | 0 |
| musique | gpt-6.1-terra | LOI | 60 | 1.058 | 0.018 | 1080 | 0 |
| musique | gpt-6.1-terra | V1.r1 | 60 | 0.099 | 0.002 | 54 | 0 |
| musique | gpt-6.1-terra | V1 | 60 | 0.097 | 0.002 | 54 | 0 |
| musique | gpt-6.1-terra | P1 | 60 | 1.946 | 0.032 | 1242 | 0 |
| musique | gpt-6.1-terra | P1.r1 | 60 | 2.315 | 0.039 | 1296 | 0 |
| musique | gpt-6.1-terra | RM64 | 17 | 0.939 | 0.055 | 820 | 0 |
