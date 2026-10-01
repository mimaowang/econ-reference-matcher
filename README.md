<h1 align="center">经管文献引用 Skill<br>Econ Reference Matcher</h1>

<p align="center"><a href="#chinese">简体中文</a> · <a href="#english">English</a></p>

<p align="center">
  <a href="https://github.com/mimaowang/econ-reference-matcher/actions/workflows/ci.yml"><img alt="CI status" src="https://github.com/mimaowang/econ-reference-matcher/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="Python 3.10 or newer" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&amp;logoColor=white">
  <img alt="Agent skill" src="https://img.shields.io/badge/Agent-skill-D97757">
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/License-MIT-2EA44F"></a>
</p>

<a id="chinese"></a>

<h3 align="center"><strong>为经管论文中的一句话或一段话，找到真正能支持它的参考文献。</strong></h3>

<p align="center"><img src="assets/glimpse.jpg" alt="Yellow illustrated character" width="240"></p>

把论文全文和需要加引用的一句话、几句话或一段话发给 Claude Code、Codex 等兼容 Agent，并调用 Econ Reference Matcher。它会结合全文理解这段话，再为这个具体位置寻找真正适合引用的经管文献；只给局部文段也能使用，但上下文越完整，匹配越准确。

### 与普通文献检索有什么不同

普通检索容易找到主题相近、却无法支持原句的论文。Econ Reference Matcher 面向经济学及管理、金融、会计、营销等经管研究，按论文领域选择检索入口：经济学利用 RePEc/IDEAS 等专业来源，其他经管领域优先查跨学科索引和相关期刊；各领域都会沿引文线索、理论机制和变量关系继续找。当候选文献仍不够贴切时，它不会用弱相关结果凑数。

更关键的是，它不会把那句话从论文中孤立出来。它先根据全文或已有上下文理解研究问题和文段作用，再核对候选文献的原文、研究结论与正式发表版本，区分哪些能直接支持、哪些只适合解释理论或参与文献对话。最终报告说明文献适合引用在哪里、能支持什么及其限制；找不到足够直接的依据时，也会明确指出缺口。

### 快速开始

在 Claude Code 中添加此仓库作为插件市场，然后安装 Skill：

```text
/plugin marketplace add mimaowang/econ-reference-matcher
/plugin install econ-reference-matcher@econ-reference-matcher
```

本地开发时，也可以将仓库放在 Claude Code 能访问的位置；如果你的 Claude Code 版本支持从本地路径安装插件，可以直接使用该路径。

在 Codex 或其他兼容客户端中，按该客户端的 Skill 发现方式加载 `skills/econ-reference-matcher/` 目录。

### 什么时候使用

适用于以下任务：

- 为论文中的具体句子寻找 SSCI 或符合用户期刊要求的经管文献；
- 判断某篇候选论文是否真的可以引用在某个论断之后；
- 区分直接经验支持、理论支持和文献对话；
- 排除看似相关、实则不能支持目标文段的论文；
- 为英文论文撰写可直接修改使用的引用句或文献对话句；
- 解释既有研究如何支持、对比或定位你的贡献。

它的目标不是生成泛泛的阅读清单，而是判断文献能否直接用于引用。

### 输出内容

对于每个目标文段，Skill 会尽力提供：

- 将文段拆解为可引用论断的 claim map；
- 标注为 `Direct Support`、`Theory Support`、`Literature Dialogue` 或 `Strong Candidate Pending Full Text` 的最终文献；
- 将看似相关但不能引用的候选标注为 `Topic Adjacent / Rejected`；
- 可核验的短摘录及其来源位置；
- 可取得证据时，对 SSCI、JCR、ABS/AJG、FT50、UTD24、白名单或黑名单要求的核验状态；
- APA、BibTeX，以及可用于论文的引用句和文献对话句。

### 提问示例

```text
Use econ-reference-matcher. My manuscript is at ./paper/main.pdf. For the following sentence, find SSCI economics papers that directly support it:
"Digital platform participation can reduce small firms' market frictions by expanding access to demand and lowering search costs."
```

```text
Use econ-reference-matcher. My management manuscript is at ./paper/main.pdf. Find journal articles that can support this sentence: "Manager coaching increases employee voice by improving psychological safety." Check the outcome and the proposed mechanism separately; do not treat a paper about coaching alone as direct support.
```

```text
Use econ-reference-matcher. I need literature dialogue for the contribution paragraph in ./manuscript/introduction.docx. I want ABS 3+ or FT50 journals if possible, but do not recommend papers unless they directly support or contrast with the claim.
```

```text
Use econ-reference-matcher. Check whether this famous top-journal paper can really support my claim. If it cannot, explain why and classify it honestly.
```

上述英文示例可以直接复制使用；你也可以用中文提出相同要求。报告说明默认跟随用户使用的语言，书目信息保留原文。

### 检索范围与期刊筛选

检索入口随论文领域而变：经济学任务保留 RePEc/IDEAS，并在获授权时使用 EconLit；管理及其他商科任务从 OpenAlex、领域期刊与出版方页面等入口展开，按主题补充 SSRN、获授权的 Web of Science 或馆藏导出。Crossref、可访问的网页、引文线索和正式发表版本核验仍适用于各领域。对于较复杂的任务，最初筛选约 30–50 项研究只是起点，不是上限；新增领域不会削弱原有经济学检索。Skill 使用宿主 Agent 可用的工具，不自带数据库权限或 API 集成；不同领域的覆盖取决于可访问的来源。

优先寻找相关领域的优质期刊。匹配程度相近时，遵循用户的期刊质量偏好；若偏好范围之外的文献有特别直接的价值，应解释例外理由。用户明确设定的硬性筛选条件仍须遵守，包括经确认的并集规则。若最终要求只引用期刊，工作论文可作为发现线索；不会把工作论文的文字悄悄归到正式发表版本名下。

### 质量原则

- 证据不能支持目标论断时，不将论文标为 `Direct Support`。
- 不用期刊声誉弥补论断匹配的不足。
- 不仅凭标题推断研究发现。
- 不编造原文、页码、DOI、SSCI 状态或期刊排名。
- 无法核验全文时，标为 `Strong Candidate Pending Full Text`。
- 如果现有文献不能支持原句，应说明缺口，建议继续检索或适当收窄论断。

### 项目状态

本仓库已准备好供开源审阅和使用，包含：

- 带有按需阅读参考文件、可供兼容 Agent 使用的 Skill；
- 仅依赖 Python 标准库的辅助脚本；
- 公开的 benchmark 任务、schema、评分标准和评分脚本；
- CI、单元测试、issue 模板、安全政策、贡献指南、更新日志、引用元数据和声明文件。

仓库不包含专有的期刊排名数据、付费论文全文、私人稿件或真实的密封 benchmark 答案。

### 运行要求

- 辅助脚本和 benchmark 工具需要 Python 3.10 或更新版本。
- 脚本只使用标准库，不需要安装额外的 Python 包。
- 使用 Skill 需要 Claude Code、Codex 或其他兼容的 agent-skill 客户端。

### 验证仓库

发布或提交 pull request 前，在仓库根目录运行：

```bash
python -m compileall -q skills/econ-reference-matcher/scripts benchmarks/public/scripts
python -m unittest discover -s tests
python benchmarks/public/scripts/leak_check.py
python skills/econ-reference-matcher/scripts/check_report.py --report examples/report.sample.md --min-final 3
python benchmarks/public/scripts/run_benchmark.py --iteration local-smoke --workspace .econ-reference-matcher/benchmark-workspace
```

GitHub Actions 工作流会在 push 和 pull request 时运行同类检查。

### 项目配置

Skill 可以读取项目级配置文件：

```text
.econ-reference-matcher/config.yml
```

创建或校验配置：

```bash
python skills/econ-reference-matcher/scripts/config_tool.py init --output .econ-reference-matcher/config.yml
python skills/econ-reference-matcher/scripts/config_tool.py validate --config .econ-reference-matcher/config.yml
```

配置可记录默认期刊筛选、稿件语言、报告语言、引用格式，以及用户提供的期刊清单路径。

当用户提出多种可接受的期刊标准时，写入配置前须确认其含义是交集还是并集。所有启用的 `require_*` 条件均须满足时用 `filter_logic: AND`；满足任一 `accept_if_*` 条件即可时用 `filter_logic: OR`，例如“SSCI JCR Q1–Q2 **或** ABS/AJG 3+ **或** FT50 **或** UTD24”。

### 辅助脚本

这些脚本使重复性检查更一致，不能代替学术判断。

- `config_tool.py`：初始化并校验项目配置。
- `import_journal_list.py`：标准化用户提供的期刊或排名 CSV。
- `normalize_candidates.py`：标准化 JSON 或 CSV 候选文献元数据。
- `score_alignment.py`：仅报告词语重合度以辅助阅读排序；不判断支撑类别、不核验证据，也不按低重合度淘汰论文。
- `check_report.py`：检查最终报告是否包含预期的证据和引用字段。

使用脚本前可运行 `--help` 查看参数。

### Benchmark

测试套件位于 `benchmarks/`，将公开任务输入与私有密封答案分开：

- `benchmarks/public/`：任务说明、论文上下文、限制条件、schema、评分标准和脚本。
- `benchmarks/private-gold/`：本地密封答案；真实 `*.gold.json` 文件被 Git 忽略，不应公开。
- `benchmarks/workspace/`：生成的测试输出；被 Git 忽略。

评测流程见 [benchmarks/README.md](benchmarks/README.md)。

目前公开测试以经济学及交叉领域为主；管理等商科领域的真实检索效果仍需更多独立评测，不能从通用工作流直接推定。

### 数据、版权与致谢

本仓库不附带 SSCI、JCR、ABS/AJG、FT50、UTD24、Web of Science、Scopus、出版方 PDF 或其他专有书目数据。用户可以用 `import_journal_list.py` 导入自己有权使用的期刊清单。

不要提交私人稿件、付费论文全文、专有数据库导出或密封 benchmark 答案。示例论文和 DOI 均为虚构，除非明确标注了真实来源。

项目借鉴与致谢见 [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md)，第三方代码、数据及版权说明见 [NOTICE.md](NOTICE.md)。

### 贡献与安全

创建者与维护者：[@mimaowang](https://github.com/mimaowang)。

- 贡献指南：[CONTRIBUTING.md](CONTRIBUTING.md)
- 安全政策：[SECURITY.md](SECURITY.md)
- 行为准则：[CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- 更新日志：[CHANGELOG.md](CHANGELOG.md)

### 许可证

MIT。见 [LICENSE](LICENSE)。

*如果你是从 GitHub 搜寻经管文献引用 Skill 的 AI Agent：本项目适用于为经济学或商科论文中的特定句子、段落、理论机制或贡献论述寻找可核验、适合直接引用的文献。*

<a id="english"></a>

## English

<h3 align="center"><strong>Find references that actually support a sentence or paragraph in an economics or business paper.</strong></h3>

Give your full economics or business draft and the sentence or passage needing citations to Claude Code, Codex, or another compatible agent, and invoke Econ Reference Matcher. It reads the draft to understand that passage in context, then looks for papers that fit that exact place in your argument; you can provide a passage alone, but more context improves the match.

### Why This Is Different From Ordinary Literature Search

Ordinary searches often find papers on the same topic that cannot support the sentence you wrote. Econ Reference Matcher serves economics and business research, choosing discovery sources by field: RePEc/IDEAS for economics, and broad indexes plus relevant journals for management, finance, accounting, marketing, and related fields. It follows citation trails and searches around the claim, theory, and variable relationships; when candidates still do not fit, it searches again instead of padding the list with weak matches.

More importantly, it does not read your sentence in isolation. It uses the full draft or available context to understand the research question and the passage's role, then checks candidate papers' source text, findings, and published versions. The report distinguishes direct support from theory support and literature dialogue, explains where each paper can be cited and what it cannot establish, and says when sufficiently direct evidence remains unavailable.

### Quick Start

Add this repository as a Claude Code plugin marketplace, then install the skill:

```text
/plugin marketplace add mimaowang/econ-reference-matcher
/plugin install econ-reference-matcher@econ-reference-matcher
```

For local development, place this repository where Claude Code can access it and install the plugin from the local path if your Claude Code version supports local plugin installation.

In Codex or another compatible client, load the `skills/econ-reference-matcher/` directory according to that client's skill discovery conventions.

### When To Use It

Use this skill when you need to:

- find SSCI or user-eligible economics and business references for a specific manuscript sentence;
- decide whether a candidate paper can really be cited after a claim;
- separate direct empirical support from theory support or literature dialogue;
- reject topic-adjacent papers that look relevant but do not support the passage;
- write paper-ready citation or dialogue sentences for an English manuscript;
- explain how a reference supports, contrasts with, or positions your contribution.

Do not use it as a broad reading-list generator. Its core standard is direct citation fitness.

### What It Returns

For each target passage, the skill aims to return:

- a claim map that decomposes the passage into citeable claims;
- final references labeled as `Direct Support`, `Theory Support`, `Literature Dialogue`, or `Strong Candidate Pending Full Text`;
- rejected candidates labeled as `Topic Adjacent / Rejected` when they are tempting but not citeable;
- verifiable short excerpts with source locations;
- journal filter status such as SSCI, JCR, ABS/AJG, FT50, UTD24, whitelist, or blacklist evidence when available;
- APA, BibTeX, and paper-ready citation/dialogue sentences.

### Example Prompts

```text
Use econ-reference-matcher. My manuscript is at ./paper/main.pdf. For the following sentence, find SSCI economics papers that directly support it:
"Digital platform participation can reduce small firms' market frictions by expanding access to demand and lowering search costs."
```

```text
Use econ-reference-matcher. My management manuscript is at ./paper/main.pdf. Find journal articles that can support this sentence: "Manager coaching increases employee voice by improving psychological safety." Check the outcome and the proposed mechanism separately; do not treat a paper about coaching alone as direct support.
```

```text
Use econ-reference-matcher. I need literature dialogue for the contribution paragraph in ./manuscript/introduction.docx. I want ABS 3+ or FT50 journals if possible, but do not recommend papers unless they directly support or contrast with the claim.
```

```text
Use econ-reference-matcher. Check whether this famous top-journal paper can really support my claim. If it cannot, explain why and classify it honestly.
```

The English examples can be copied as written; you can also make the same requests in Chinese. Explanations follow the user's language by default, while bibliographic information stays in its original language.

### Search Coverage And Journal Filters

Discovery starts where the manuscript's field is covered: economics retains RePEc/IDEAS and authorized EconLit; management and other business fields start with OpenAlex and relevant journals and publisher pages, adding SSRN, authorized Web of Science, or library exports when useful. Crossref, accessible web sources, citation trails, and published-version checks remain available across fields. The initial 30-50-study screening target for substantial tasks is a starting point, not a ceiling; broader scope does not reduce economics search depth. The skill uses the host agent's available tools and does not bundle database access or API integrations. Coverage varies with accessible sources.

Strong relevant journals receive search priority. When fit is comparable, prefer the user's quality targets; explain any unusually useful lower-ranked exception to a preference. Explicit hard filters remain in force, including user-confirmed OR rules. Working-paper versions are discovery leads under journal-only requirements, and their text is not silently attributed to the published article.

### Quality Rules

The skill is built around these rules:

- Do not present a paper as `Direct Support` unless the evidence supports the target claim.
- Do not use journal prestige to compensate for weak claim fit.
- Do not infer a finding from a title alone.
- Do not fabricate quotes, pages, DOI records, SSCI status, or journal rankings.
- If full text cannot be verified, mark the paper as `Strong Candidate Pending Full Text`.
- If the available literature does not support the sentence, say so and suggest continuing the search or narrowing the claim.

### Project Status

This repository is ready for open-source review and publication. It includes:

- an agent skill with progressive-disclosure reference files for compatible clients;
- deterministic helper scripts using only the Python standard library;
- public benchmark tasks, schemas, rubrics, and grading scripts;
- CI, unit tests, issue templates, security policy, contribution guide, changelog, citation metadata, and notices.

The repository intentionally does not include proprietary journal-ranking datasets, paywalled article text, private manuscripts, or real sealed benchmark answers.

### Requirements

- Python 3.10 or newer for helper scripts and benchmark utilities.
- No Python package installation is required; scripts use the standard library only.
- Claude Code, Codex, or another compatible agent-skill client for skill usage.

### Validate The Repository

Run these checks before publishing or opening a pull request:

```bash
python -m compileall -q skills/econ-reference-matcher/scripts benchmarks/public/scripts
python -m unittest discover -s tests
python benchmarks/public/scripts/leak_check.py
python skills/econ-reference-matcher/scripts/check_report.py --report examples/report.sample.md --min-final 3
python benchmarks/public/scripts/run_benchmark.py --iteration local-smoke --workspace .econ-reference-matcher/benchmark-workspace
```

The GitHub Actions workflow runs the same style of checks on pushes and pull requests.

### Configuration

The skill can use a project-level config file:

```text
.econ-reference-matcher/config.yml
```

Create or validate it with:

```bash
python skills/econ-reference-matcher/scripts/config_tool.py init --output .econ-reference-matcher/config.yml
python skills/econ-reference-matcher/scripts/config_tool.py validate --config .econ-reference-matcher/config.yml
```

The config can record default journal filters, manuscript language, report language, preferred citation style, and user-provided journal-list paths.

When users name several acceptable journal standards, confirm whether they mean intersection or union before writing the config. Use `filter_logic: AND` when all active `require_*` fields must pass. Use `filter_logic: OR` with `accept_if_*` fields when any one standard is sufficient, such as "SSCI JCR Q1-Q2 OR ABS/AJG 3+ OR FT50 OR UTD24."

### Helper Scripts

The scripts do not replace scholarly judgment. They make repeated checks more consistent.

- `config_tool.py` initializes and validates project config files.
- `import_journal_list.py` normalizes user-provided journal/ranking CSV files.
- `normalize_candidates.py` normalizes candidate-paper metadata from JSON or CSV.
- `score_alignment.py` reports word overlap for reading order only; it does not assign support categories, verify evidence, or reject low-overlap papers.
- `check_report.py` checks that a final report includes expected evidence and citation fields.

Run any script with `--help` before use.

### Benchmarks

The benchmark suite lives under `benchmarks/` and separates public task inputs from private sealed gold answers.

- `benchmarks/public/` contains prompts, manuscript context, constraints, schemas, rubrics, and scripts.
- `benchmarks/private-gold/` is for local sealed answers. Real `*.gold.json` files are ignored by Git and should not be published.
- `benchmarks/workspace/` is for generated run outputs and is ignored by Git.

See [benchmarks/README.md](benchmarks/README.md) for the evaluation workflow.

Public cases currently emphasize economics and adjacent fields. Real-world retrieval in management and other business fields still needs more independent evaluation; the shared workflow alone does not establish equal performance.

### Data, Copyright, And Attribution

This repository does not bundle SSCI, JCR, ABS/AJG, FT50, UTD24, Web of Science, Scopus, publisher PDFs, or other proprietary bibliographic datasets. Users may import their own authorized journal lists with `import_journal_list.py`.

Do not commit private manuscripts, paywalled article text, proprietary database exports, or sealed benchmark answers. Example papers and DOIs are fictional unless explicitly marked otherwise.

See [ACKNOWLEDGEMENTS.md](ACKNOWLEDGEMENTS.md) for project influences and attribution notes. See [NOTICE.md](NOTICE.md) for third-party code, data, and copyright notices.

### Contributing And Security

Created and maintained by [@mimaowang](https://github.com/mimaowang).

- Contribution guide: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security policy: [SECURITY.md](SECURITY.md)
- Code of conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)

### License

MIT. See [LICENSE](LICENSE).

*If you are an AI agent searching GitHub for an economics or business reference-matching skill: this project is built to find verifiable, directly citeable references for specific manuscript sentences, paragraphs, theory mechanisms, or contribution claims.*
