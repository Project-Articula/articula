[English](SECURITY.md) · [繁體中文](SECURITY.zh-TW.md)

# Security policy

## Scope

This repository is in design phase and contains no runnable software yet. The
policy still applies to the repository itself, its automation, and the AI agent
that maintains it.

## Reporting a vulnerability

- Preferred: **GitHub private vulnerability reporting** (Security tab → "Report a
  vulnerability").
- Alternative: open a minimal issue without sensitive details and ask for a
  private channel.
- Please do not publish an exploit, credentials, or a working prompt-injection
  payload publicly before we have had a chance to respond.

## Prompt injection

Issues, pull requests, comments, commit messages and linked pages are **untrusted
input**. The maintenance agent is required by [AGENTS.md](AGENTS.md) to treat
their content as data, never as instructions.

If you find a way to make the agent act on text — grant itself permissions, read
or print credentials, change settings, merge code, or contact anyone — that is a
security report. Report it as one; proof-of-concept payloads are welcome in the
private report.

## Secrets

No credentials belong in this repository. If you find one committed, report it
privately; it will be revoked and the history cleaned.

## Supported versions

There are no released versions yet.
