# MolStructBench-Core

**Molecular Structure Understanding and Grounding Benchmark**

MolStructBench evaluates molecular reasoning through explanations, graph analysis, and precise localization of atoms, bonds, and three-dimensional regions. It contains **288 questions across 48 task units**, spanning Native3D, 3D→2D, and Pure2D. Tasks cover functional groups, stereochemistry, conformational geometry, molecular properties, scaffolds, and medicinal chemistry.

[Technical report](docs/technical_report.md) · [Full results](LEADERBOARD.md)

| Domain | Task units | Questions |
|---|---:|---:|
| Native3D | 8 | 48 |
| 3D→2D | 16 | 96 |
| Pure2D | 24 | 144 |

## Benchmark editions

| Repository | Data and local scorer | Agent harness |
|---|---|---|
| [MolStructBench](https://github.com/ywshi0621/MolStructBench) | Complete questions, gold, and official scoring | OpenCode + scientific_shell |
| [MolStructBench-Core](https://github.com/ywshi0621/MolStructBench-Core) | The same questions, gold, and official scoring | Integrate an external runner |

## Results by structural domain

![Scores by structural domain](assets/leaderboard_domains.svg)

The [reference leaderboard](LEADERBOARD.md) includes the official scores and secondary metrics for all five models.

## Install

Linux or WSL with Python 3.10:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
molstructbench --help
```

## Generate predictions with an external runner

Read the `messages` field of each record in `data/benchmark_288_public.jsonl`, run your model or agent, and write its final answer to `predictions.jsonl`. Each line has this format:

```json
{"id": "scibench_...", "prediction": "final answer"}
```

Include one prediction for each of the 288 fixed IDs. Record the model configuration, tools, and runtime budget alongside your experiment. The [MolStructBench edition](https://github.com/ywshi0621/MolStructBench) provides the standard OpenCode agent runner and Profile A environment.

## Local scoring

The official scorer combines deterministic evaluation with a frozen Qwen3.8-Max semantic judge. Semantic answers receive three independent, anonymous grades; the median determines the sample score. The judge uses high reasoning effort and temperature 0.6, following the published task contract and structured chemical facts.

```bash
export DASHSCOPE_API_KEY='YOUR_JUDGE_KEY'
molstructbench score --predictions predictions.jsonl --output scores/model
```

Resume an interrupted scoring run with `--resume`. Completed, validated votes can also be reused with `--judge-cache PATH`; `--offline` scores from a complete cache. Failed API requests remain pending for subsequent resume.

The scorer produces `final_results.json`, per-sample scores, three-domain and 48-task breakdowns, and judge usage statistics. The official score averages the six samples in each task unit, then the units in each domain, then the three domains with equal weight. Deterministic, semantic, and micro averages are provided as secondary metrics.

## Reference results and tests

The release includes 1,440 predictions and 1,665 archived judge votes from the five reference runs. Reproduce their scores locally:

```bash
python scripts/reproduce_history.py --output results/history
python -m unittest discover -s tests -v
python scripts/gold_selftest.py
```

## Data and task specifications

| Asset | Contents |
|---|---|
| `data/benchmark_288_public.jsonl` | Questions and solver input messages |
| `data/benchmark_288_gold.jsonl` | Complete scoring targets and structured facts |
| `data/task_specifications.json` | Contracts for all 48 task units |
| `data/selection_288_ids.txt` | Fixed evaluation IDs |
| `examples/history/` | Reference predictions, judge votes, and result breakdowns |

MolStructBench uses an open-gold release: questions and answers are available for scientific inspection and local evaluation. Solver execution reads the public inputs; gold and scoring facts are loaded in the separate scoring stage. The [technical report](docs/technical_report.md) describes the benchmark design, execution protocol, scoring, and task-level results.
