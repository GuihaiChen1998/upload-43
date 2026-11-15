# Symmetric FEVER extension — raw inputs (pinned)

| File | Source | SHA-256 |
|---|---|---|
| `symmetric_v0.2/fever_symmetric_dev.jsonl` (708 rows) | github.com/TalSchuster/FeverSymmetric @ fa25d17e73ea0694edc78133ec654b9f32f6db73 | 1d43d016da9264de2139cd10edd459ffbeac84f1fd85d60b70ab6ef63d283f81 |
| `symmetric_v0.2/fever_symmetric_test.jsonl` (712 rows) | same commit | b2ff560615bd3337c858bc5b09256d04f39aaa034aaae2351bb2d6345c110f83 |
| `FeverSymmetric_DATA_LICENSE` | same commit (`DATA_LICENSE`) | — |
| `shared_task_dev.jsonl.gz` (19,998 claims) | https://fever.ai/download/fever/shared_task_dev.jsonl (gzip of the original; original SHA-256 e89865bfe1b4dd054e03dd57d7241a6fde24862905f31117cf0cd719f7c78df7) | — |
| `wiki_subset.jsonl.gz` (324 pages) | FEVER 2017 dump https://fever.ai/download/fever/wiki-pages.zip (1,713,485,474 bytes), reduced to the pages referenced by the evidence sets of the 355 Symmetric-FEVER original claims | see `../../constructed/symfever/build_info.json` |

Licences: FEVER and the Wikipedia text are CC BY-SA 3.0; see `FeverSymmetric_DATA_LICENSE`.
Families: synthetic row id = original FEVER claim id + 7-digit suffix (`0000002`–`0000004`); 177 (dev) + 178 (test) families of 4.
Build: `python scripts/26_build_symfever.py --symfever-dir data/raw/symfever --fever-dev <ungzipped shared_task_dev.jsonl> --wiki-subset data/raw/symfever/wiki_subset.jsonl.gz`
