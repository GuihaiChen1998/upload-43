# Qasper v0.3 (raw)

- Source: official release, https://qasper-dataset.s3.us-west-2.amazonaws.com/ (downloaded 2026-11-04):
  `qasper-train-dev-v0.3.tgz`, `qasper-test-and-evaluator-v0.3.tgz` (kept here as downloaded).
- Paper: Dasigi et al., "A Dataset of Information-Seeking Questions and Answers Anchored in Research Papers", NAACL 2021.
- License: CC BY 4.0 (per the dataset card / paper).
- `scripts/33_build_qasper.py` reads `qasper-dev-v0.3.json` and `qasper-test-v0.3.json`, extracted from the archives
  (`tar xzf qasper-train-dev-v0.3.tgz qasper-dev-v0.3.json; tar xzf qasper-test-and-evaluator-v0.3.tgz qasper-test-v0.3.json`);
  the extracted JSON files are not committed.

SHA-256:
```
72a52a41193e2838b8074f80ac074b94f956b84886c36a61c58a7df4171bdd72  qasper-test-and-evaluator-v0.3.tgz
a28fdf966db827bcee3d873107d6b6669864fb7ca8fbf73a192f5e39191bdb5a  qasper-train-dev-v0.3.tgz
2ae7ee62a65b1c4225791c70de80c2aad4e8998cf1fd4f09a53103db4f21af93  qasper-dev-v0.3.json
6e29ad410e6e39aa1936017fb965b30a20eb2e7751997f55b97c9d281aa884e5  qasper-test-v0.3.json
```
