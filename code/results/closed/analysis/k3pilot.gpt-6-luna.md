# K3 k3pilot · gpt-6-luna

## Premise (repeats 0-2)
| dataset | cond | redundancy | n_bases | n_eval_3of3 | full_3of3 | full_2of3 | full_spont_change | parse_fail | drop_ap_still_correct | drop_ap_answer_change | drop_ap_acc_drop | drop_group_still_correct | drop_group_answer_change | drop_group_acc_drop |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hotpotqa | F | 0 | 50 | 40 | 0.889 | 0.978 | 0.133 | 0.000 | 0.237 | 0.785 | 0.719 | 0.237 | 0.785 | 0.719 |
| hotpotqa | C | 1 | 50 | 42 | 0.913 | 0.978 | 0.130 | 0.000 | 0.920 | 0.109 | 0.036 | 0.283 | 0.754 | 0.674 |
| hotpotqa | FF | 0 | 50 | 41 | 0.891 | 0.935 | 0.174 | 0.000 | 0.246 | 0.768 | 0.696 | 0.246 | 0.768 | 0.696 |
| hotpotqa | CF | 1 | 50 | 42 | 0.913 | 0.957 | 0.152 | 0.000 | 0.913 | 0.123 | 0.036 | 0.232 | 0.797 | 0.717 |
| hotpotqa | CC | 2 | 50 | 42 | 0.913 | 0.978 | 0.109 | 0.000 | 0.942 | 0.109 | 0.022 | 0.304 | 0.732 | 0.659 |
| musique | F | 0 | 50 | 31 | 0.886 | 0.943 | 0.171 | 0.006 | 0.410 | 0.714 | 0.524 | 0.410 | 0.714 | 0.524 |
| musique | C | 1 | 50 | 34 | 0.944 | 0.972 | 0.111 | 0.000 | 0.944 | 0.083 | 0.028 | 0.352 | 0.713 | 0.620 |
| musique | FF | 0 | 50 | 31 | 0.886 | 0.943 | 0.143 | 0.000 | 0.457 | 0.667 | 0.476 | 0.457 | 0.667 | 0.476 |
| musique | CF | 1 | 50 | 31 | 0.912 | 0.971 | 0.147 | 0.000 | 0.990 | 0.098 | -0.029 | 0.402 | 0.706 | 0.559 |
| musique | CC | 2 | 50 | 32 | 0.889 | 0.944 | 0.111 | 0.000 | 0.926 | 0.074 | 0.009 | 0.352 | 0.713 | 0.583 |

## Methods (repeat 3, premise-evaluable variants of each condition)
(none)

## FF / CF / CC curve on one population (bases evaluable in all three)
(none)

## Paired redundancy effects (base-qid bootstrap 95% CI)
(none)

## Cost
(none)
