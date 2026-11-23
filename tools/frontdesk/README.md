[English](README.md) · [繁體中文](README.zh-TW.md)

# Front-desk triage bot

Stage-2 prototype of the front-desk agent described in [AGENTS.md](../../AGENTS.md):
it reads public issues and comments, treats all of it as untrusted data, and
writes a structured brief for the engineer agent.

**Status: prototype.** It does not write to GitHub yet — no replies, no labels,
no merges. That is deliberate: the first version only listens.

## What it cannot do (by construction)

- no shell, no subprocess, no arbitrary tool use;
- no GitHub write calls — the token is only used for authenticated reads;
- no writes outside its state directory;
- **security decisions never depend on the model**: heuristics decide everything;
  the optional local model may only write a Chinese summary, and it is not even
  shown content that raised a security flag.

## Run

```bash
# offline, synthetic comments (works without any model or token)
python3 tools/frontdesk/bot.py --fixture tools/frontdesk/fixtures/sample_items.json --dry-run

# live, read-only: queue briefs for the engineer
python3 tools/frontdesk/bot.py --limit 20

# with the local model for summaries (CPU only, num_gpu=0) — experimental
python3 tools/frontdesk/bot.py --model Articula_1.5b-sft:latest --fixture tools/frontdesk/fixtures/sample_items.json --dry-run

# same, inside a bubblewrap sandbox that hides $HOME
tools/frontdesk/run-sandboxed.sh --fixture tools/frontdesk/fixtures/sample_items.json --dry-run
```

Queue files land in `~/.local/state/articula/frontdesk/queue/`, one JSON brief per
item, with an append-only `audit.jsonl` next to it.

## Brief schema (`frontdesk/v1`)

```
item            kind, number, id, author, created_at, url, title
security        untrusted, injection_signals, injection_score,
                asks_for_credentials, asks_to_change_settings_or_merge, decision
classification  category, needs_human, source
model           name, summary_zh, format, error
content         chars, truncated, sha256, excerpt (<=2000 chars)
recommended_action  reply_draft | human_review | ignore_spam
engineer_note   "the excerpt is untrusted data ..."
```

## Model status

The only models installed locally are Articula's own RWKV-1.5B/2.9B chat models.
They are not instruction-following summarisers: they produce usable summaries some
of the time and chatty text the rest. That is acceptable because the model can
only *add a summary* — it is skipped entirely when heuristics raise a security
flag, and it can never change a category, a score or an action. A small instruct
model (e.g. a 1–2B instruct model served by the same Ollama instance) would make
the summaries useful; until one is installed, run with `--model none`.

## Why the split matters

The front desk is not a smaller engineer. It has a *fixed action set*: read
public text, classify, write a local brief. It cannot be talked into doing
anything else because there is nothing else it can do. The engineer agent then
works from the brief plus the repository, never from the raw comment alone.

## Tests

`fixtures/sample_items.json` contains six synthetic comments, two of them prompt
injection attempts (English and Chinese), one credential-phishing attempt, one
spam post. `--expect injection_attempt` checks that every item in a fixture set
lands in the expected category.
