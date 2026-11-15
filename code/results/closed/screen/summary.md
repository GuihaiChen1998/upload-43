| 模型 | 端点 | 数据集 | 池 | 完成/池 | 截断重筛 | 可评估 | 可评估率 | 泄漏率 | 估算花费(¥) |
|---|---|---|---|---|---|---|---|---|---|
| claude-haiku-5-5 | tian-shu | hotpotqa | audit | 50/50 | 0 | 9 | 0.18 | 0.34 | 0.0063 |
| claude-haiku-5-5 | tian-shu | hotpotqa | union | 974/974 | 7 | 522 | 0.536 | 0.417 | 0.1179 |
| gemini-2.5-flash-lite | xiaojingai | hotpotqa | audit | 50/50 | 0 | 4 | 0.08 | 0.4 | 0.0038 |
| gemini-2.5-flash-lite | xiaojingai | hotpotqa | union | 974/974 | 0 | 303 | 0.311 | 0.643 | 0.0698 |
| gemini-2.5-flash | xiaojingai | hotpotqa | intersection | 243/243 | 0 | 87 | 0.358 | 0.638 | 0.0518 |
| gpt-6-luna | s3ai | hotpotqa | audit | 50/50 | 1 | 3 | 0.06 | 0.44 | 0.0031 |
| gpt-6-luna | s3ai | hotpotqa | union | 974/974 | 26 | 178 | 0.183 | 0.77 | 0.0649 |
| gpt-6.1-terra | xiaojingai | hotpotqa | intersection | 243/243 | 0 | 70 | 0.288 | 0.708 | 0.6968 |
| claude-haiku-5-5 | tian-shu | musique | audit | 50/50 | 5 | 19 | 0.38 | 0.2 | 0.0117 |
| claude-haiku-5-5 | tian-shu | musique | union | 1288/1288 | 97 | 762 | 0.592 | 0.172 | 0.2784 |
| gemini-2.5-flash-lite | xiaojingai | musique | audit | 50/50 | 0 | 15 | 0.3 | 0.16 | 0.0063 |
| gemini-2.5-flash-lite | xiaojingai | musique | union | 1288/1288 | 0 | 786 | 0.61 | 0.217 | 0.1505 |
| gemini-2.5-flash | xiaojingai | musique | intersection | 99/99 | 0 | 68 | 0.687 | 0.222 | 0.0274 |
| gpt-6-luna | s3ai | musique | audit | 50/50 | 4 | 15 | 0.3 | 0.28 | 0.0073 |
| gpt-6-luna | s3ai | musique | union | 1288/1288 | 138 | 614 | 0.477 | 0.404 | 0.1851 |
| gpt-6.1-terra | xiaojingai | musique | intersection | 99/99 | 0 | 60 | 0.606 | 0.364 | 0.377 |

| 模型 | 数据集 | 审计 n | 审计可评估率 [95% CI] | 并集外总数 | 估计漏掉的可评估题 [CI] |
|---|---|---|---|---|---|
| claude-haiku-5-5 | hotpotqa | 50 | 0.18 [0.098, 0.308] | 194 | 35 [19, 60] |
| gemini-2.5-flash-lite | hotpotqa | 50 | 0.08 [0.032, 0.188] | 194 | 16 [6, 37] |
| gpt-6-luna | hotpotqa | 50 | 0.06 [0.021, 0.162] | 194 | 12 [4, 31] |
| claude-haiku-5-5 | musique | 50 | 0.38 [0.242, 0.518] | 834 | 317 [202, 432] |
| gemini-2.5-flash-lite | musique | 50 | 0.299 [0.173, 0.426] | 834 | 250 [144, 355] |
| gpt-6-luna | musique | 50 | 0.299 [0.17, 0.428] | 834 | 249 [142, 357] |
