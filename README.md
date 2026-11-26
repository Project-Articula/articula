[English](README.md) · [繁體中文](README.zh-TW.md)

# Articula

An open research-engineering project that starts from one question:

> **Can an artificial will be built as a body — not just as a model?**

Articula tries to build both halves at once: a *brain* (awareness, subconscious,
collective subconscious) and a *shell* (an artificial body the brain can inhabit,
move, and be changed by). They are designed together because we do not believe a
disembodied model can become a self.

**Status: design phase (v0.1). There is no implementation yet.** This repository
currently holds the project skeleton, the licence and the working policies. Design
notes will be published in batches once edited for public reading.

## Design principles (working hypotheses)

These are hypotheses, not settled science, and they are listed so they can be
criticised.

- **Emotion is multidimensional prediction error**, not a list of discrete labels.
- **Reward is reward prediction error (RPE) — and it carries no punishment.**
  Not receiving a reward is not a punishment; behaviour is shaped by prediction,
  not by fear.
- **Interoception comes first.** Five modules (relay, drive, alarm, insula,
  empathy sandbox) give the brain a body to feel before it has a world to see.
- **A router with adapters sits between brain and shell.** Modules communicate
  only through the router; state does not leak across module boundaries.
- **Self-reference has three layers**: subjecthood (M6), a default-mode network,
  and a hard reality-check gate.
- **Training is stratified**: organ-level training may be strict; individual-level
  training must not be alienating.

## What is and is not here

| | |
|---|---|
| ✅ | Project infrastructure: public repository, AGPLv3, review policy |
| ⬜ | Design notes (in editorial preparation) |
| ⬜ | Implementation, training, models, shell/body code |

## Repository layout

```
README.md      this file
LICENSE        GNU AGPL v3.0
SECURITY.md    how to report vulnerabilities and prompt-injection attempts
AGENTS.md      rules of engagement for AI agents working in this repository
docs/          design notes (published in batches)
devlog/        short public development log
```

## Why publish

The project sits at the intersection of software, neuroscience, psychology and
philosophy, and it is being built by someone who is not a professional in any of
those fields. Keeping that private would guarantee that its mistakes are never
corrected. Publishing it means the strongest criticism arrives while the design
is still cheap to change.

The downside is that ideas can be taken. That is a price we are willing to pay,
and the AGPLv3 licence is the concrete form of the trade: the source and the
notes stay open, including for anyone who offers a modified version as a network
service.

## AI involvement

This project is produced with heavy AI assistance. Day-to-day repository
maintenance is performed by an AI agent account, `@articula-agent` (display name
"Articula"), operating under the supervision of the human owner,
`@ADHDinosaur`. The agent may create branches and pull requests, but **only the
human owner merges**. Its rules of engagement are in [AGENTS.md](AGENTS.md).

We state this plainly because readers deserve to know who wrote what, and
because the experiment itself is part of the project: an AI that helps build the
thing that is supposed to become it would be a strange thing to hide.

## Contributing

Criticism is more useful than agreement. Open an issue if you think a design
principle is wrong, under-specified, or borrowed without credit. Pull requests
are welcome; they are reviewed by the human owner, never merged automatically.

## Licence

Copyright (C) 2026 ADHDinosaur.

Articula is free software: you can redistribute it and/or modify it under the
terms of the **GNU Affero General Public License** as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version. See [LICENSE](LICENSE).

`SPDX-License-Identifier: AGPL-3.0-or-later`

The licence applies to the documentation in this repository as well. We chose a
network copyleft licence deliberately: this work is not meant to become a closed
product.
