# MolStructBench

**Molecular Structure Understanding and Grounding Benchmark** · 分子结构理解与定位评测

v1.0 · 不带 Harness 数据与评分版 · open-gold · 本地自动评分

覆盖 Native3D、3D→2D、Pure2D，固定 288 道题、48 个 dataset×task units、每 unit 6 题。
包含分子属性、功能团、结构定位/grounding、立体化学、药化与结构知识任务。
本次只改发布名称和工程打包；题目、gold、选样、科学评分规则与五模型历史答案均不变。

[English technical report](docs/technical_report.md) · [Reference leaderboard](LEADERBOARD.md)

## 选择版本

| 版本 | 数据/gold/官方 Scorer | OpenCode Agent + scientific_shell |
|---|---|---|
| WITH_HARNESS | 完整 | 包含 |
| WITHOUT_HARNESS | 完整 | 不包含，接入自己的框架 |

两版的科学数据与评分相同，分别使用独立虚拟环境。详见 docs/EDITION.md。

## 安装（Linux / WSL，Python 3.10）

解压 ZIP 或 clone 相应仓库后进入目录。带 Harness 版须安装 python3.10-venv、
bubblewrap 和 curl；安装依赖需要网络。评分版只需 Python 依赖，无维护者评分服务。

```bash
python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
molstructbench --help
python scripts/verify_release.py
```

## 使用外部运行框架

本版有完整题目和官方 Scorer，没有 OpenCode、Agent loop、scientific_shell、
provider adapters 或运行环境，命令不包含 eval。不安装 bubblewrap、OpenCode
或科学工具环境。用自己的 API/框架仅从 data/benchmark_288_public.jsonl 的
messages 生成最终答案；禁止把 gold 或评分 facts 发送给 Solver。

输出每行仅 {"id":"scibench_...","prediction":"final answer"} 的 predictions.jsonl，
正式评分要求 288 个固定唯一 ID。外部框架的工具和预算须自行披露，不能把不同
执行条件标为标准 Profile A 历史实验。使用标准运行请选 WITH_HARNESS 版。

## 本地官方评分

```bash
export DASHSCOPE_API_KEY='YOUR_JUDGE_KEY'
molstructbench score --predictions predictions.jsonl --output scores/model
# 自动恢复同输入 checkpoint，只补缺失票
molstructbench score --predictions predictions.jsonl --output scores/model --resume
```

Deterministic 本地运行；semantic 使用冻结 qwen3.8-max、high reasoning、temperature
0.6、固定 prompt，三次独立匿名 Judge 取中位数。用户使用自己的 key，不需要官方
URL、token 或联系维护者。Judge 不看模型身份、轨迹、reasoning 或 tool history。
任务依据、等价表达、额外正确事实与矛盾处理遵守原冻结协议。

支持 --judge-cache PATH 和 --offline；缓存严格校验 request / prompt / 参数 hash，
失败 pending、不记 0。完整成功返回 0，pending 返回 3、官方总分 null，输入/hash
错误返回 2。输入改变须使用新输出目录。输出 final_results.json、per_sample_scores.jsonl、
48-task 和三数据集 breakdown、Judge 使用统计。

官方 headline：task-unit mean → dataset mean → 三 dataset 等权平均；
deterministic、semantic、micro 仅作 secondary metrics。

## 测试与历史复现（不调用任何 Solver 或付费 Judge）

```bash
python -m unittest discover -s tests -v
python scripts/gold_selftest.py
python scripts/reproduce_history.py --output results/history
```

包内 1440 条历史预测、1665 个原始 Judge 票可由同一 scorer 复现。expected 文件仅用于
结果比较，不作为计算输入。历史数据中的 scibench_ IDs、dataset IDs、Python 内部包名
与 scibench 命令别名保留兼容性，不改变 frozen prompt 或历史 request hash。

## 数据与评分隔离

完整 gold 在 data/benchmark_288_gold.jsonl；accepted variants、48-task specs、固定
selection、Judge public-evidence 快照和 hashes 全部包含。gold 公开后不再是隐藏测试集。
Solver 阶段只读取 public input；gold 和评分事实仅在本地评分阶段使用。
本仓库不附个人运行目录、缓存、机器日志或身份映射。

公开交付物经过姓名/账号/机器路径/API 密钥清理与扫描；通用 sandbox 路径如 /workspace
和 /home/agent 为运行协议，不是个人路径。详情见 docs/PRIVACY_AUDIT.json。
见 docs/technical_report.md、docs/ACCEPTANCE.json、PUBLIC_HASHES.json 和 SCORER_FREEZE.json。
软件源代码 MIT；第三方与数据权利说明见 LICENSE / NOTICE。
