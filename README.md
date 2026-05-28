# diff-reviewer

`diff-reviewer` is an LLM-assisted pull request diff reviewer that chunks large diffs, routes them through multiple review agents, aggregates structured findings, and benchmarks the output on real GitHub pull requests.

## What it does

- Parses unified git diffs into file and hunk structures.
- Chunks large diffs to stay within model context limits.
- Runs parallel review agents for bug risk, security risk, and style quality.
- Produces structured findings with severity, category, confidence, and file scope.
- Aggregates findings into a calibrated total risk score and rating.
- Supports a PR-Agent-style command router for PR-specific workflows.
- Benchmarks the reviewer against real public PR diffs.

## PR-Agent-style flow

The project now follows a PR-Agent-inspired flow:

1. `Digest`
   - PR status detection
   - Hunk and file prioritization
   - Detection of `CONTRIBUTING.md` and `guidelines.md` as `FUTURE` support docs
2. `Planning`
   - Token-aware compression and prioritization
   - User-request analysis
   - `/reflect` emits a PR comment that waits for user response
3. `Routing`
   - The request is routed to a command-specific tool

## Supported commands

| Command | Result type |
| --- | --- |
| `review` | PR comment |
| `describe` | PR description |
| `ask` | PR comment |
| `generate_labels` | PR labels |
| `improve` | PR inline code suggestions |
| `update_changelog` | Update changelog |
| `add_doc` | PR inline code suggestions |
| `similar_issue` | PR comment |
| `reflect` | PR comment waiting for user response |
| `command` | Empty Result (`FUTURE`) |

## Installation

Create a virtual environment and install the project:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Or install it as a package:

```bash
.venv/bin/pip install -e .
```

## Configuration

Copy `.env.example` to `.env` and fill in your provider credentials.

Supported providers:

- `gemini`
- `openai`

Important environment variables:

- `LLM_PROVIDER`
- `GEMINI_API_KEYS`
- `GEMINI_MODEL`
- `OPENAI_API_KEY`
- `OPENAI_MODEL`
- `MAX_TOKENS`
- `ENABLE_COMPRESSION`
- `LLM_TIMEOUT_SECONDS`
- `LOG_LEVEL`

## Usage

Review a diff file as text:

```bash
.venv/bin/python -m src.cli test.diff --command review
```

Review a diff file as JSON:

```bash
.venv/bin/python -m src.cli test.diff --command describe --format json
```

Ask a PR question:

```bash
.venv/bin/python -m src.cli test.diff --command ask --request "What is the main operational risk?"
```

Trigger the reflection/planning step:

```bash
.venv/bin/python -m src.cli test.diff --command reflect --format json
```

Run the benchmark on real public PRs:

```bash
.venv/bin/python scripts/benchmark_real_prs.py --output benchmark_results.json
```

## Testing

```bash
.venv/bin/pytest -q
```

## Output model

Each finding contains:

- `severity`
- `category`
- `title`
- `details`
- `confidence`
- `file_path`

The final review also includes:

- `total_score`
- `rating`

## Current limitations

- The model prompts are heuristic and need a labeled benchmark set for serious quality evaluation.
- Scoring is calibrated but still rule-based rather than learned from historical reviewer outcomes.
- Provider-side quota and rate limits can affect benchmark runs.
- `similar_issue` and support-doc enrichment are scaffolded locally and need real issue-tracker and repository-guideline integrations to match full PR-Agent depth.
