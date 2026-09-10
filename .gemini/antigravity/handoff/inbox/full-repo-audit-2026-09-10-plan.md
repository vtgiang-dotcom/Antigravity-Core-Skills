---
slug: full-repo-audit-2026-09-10
created: 2026-09-10
from: claude
status: pending
---

# Task

Do a broad health/consistency audit of this repo and report every issue you find. This is a **read-only investigation** — your only deliverable is one report file. Do not fix anything, do not propose you'll fix it "if given the go-ahead" — just report.

## Why now

Since the last clean audit (`.gemini/antigravity/handoff/outbox/audit-2026-09-04-report.md`, 2026-09-04, all gates green at that time), the tree has changed a lot and is currently **uncommitted**:
- Two new skills ported from Anthropic's official skills repo into `.kilo/skill/`: `claude-api` (multi-language: python/typescript/java/go/ruby/csharp/php/curl) and `mcp-builder` (python + node/typescript). Both mirrored into `.claude/`, `.copilot/`, `.gemini/antigravity/skills/`, `.opencode/`.
- `tools/config/lint-budget.json` budget raised 60 -> 75 to accommodate 3 bandit/BLE findings x 5 mirrored copies of `mcp-builder/scripts/evaluation.py`.
- Several harness-generated files touched by `tools/generate_harness.py --harness all` (agents, commands, rulebooks, plugin manifests).
- Earlier in the week: OpenCode engine reintroduced, Gemini/Antigravity IDE discovery enhancements, a deploy stale-file-cleanup fix.

Nobody has independently re-verified this batch of changes yet. Treat every claim in this plan and in commit messages as **unverified until you run the command yourself.**

## Context — harness architecture (read this before diving in)

- `.kilo/` is the single source of truth. `tools/generate_harness.py --harness all` generates/mirrors it into `.claude/` (Claude Code), `.opencode/` (OpenCode), and syncs skill-body content into `.copilot/skill/` and `.gemini/antigravity/skills/` for skills that already exist there as directories (it does **not** auto-create new mirror directories — those must be `cp -r`'d by hand, which is exactly the kind of step that's easy to forget or get half-right).
- `agent.yaml` is hand-maintained (not generated) — an alphabetically-sorted `skills:` list. Easy to drift from `.kilo/skill/`'s actual directory listing.
- `tools/garden.py` is the drift detector between `.kilo/` and all mirrors, plus doc-count checks (skill/agent counts hardcoded in `AGENTS.md`, `README.md`, `.github/copilot-instructions.md`, `.gemini/antigravity/AGENTS.md`, `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`) and manifest sync (`agent.yaml`).
- `tools/check_lint_budget.py` is a ratchet for the `S` (bandit) + `BLE` (blind-except) rule families that `.ruff.toml`'s `select` list deliberately omits — `ruff check .` alone will NOT catch these.
- `.harness.lock` is the authoritative boundary list between harness files and project files.

## Scope — what to check

1. **Run every verification gate yourself and report the raw output**, don't trust that they pass because a commit message says so:
   - `python .github/scripts/checklist.py .`
   - `python -m pytest tools/ -q`
   - `python tools/garden.py`
   - `python tools/validate_schemas.py`
   - `python tools/check_lint_budget.py`
   - `python .github/scripts/security_scan.py .`
2. **Skill parity audit**: for `claude-api` and `mcp-builder` specifically, diff `.kilo/skill/<name>/` against `.claude/skills/<name>/`, `.copilot/skill/<name>/`, `.gemini/antigravity/skills/<name>/`, `.opencode/skills/<name>/`. Report any file present in one mirror but missing (or differing) in another. `garden.py` claims 0 drift — verify that claim independently with a real `diff -r`, don't just trust its exit code.
3. **Dangling/broken cross-references**: search the whole repo (not just the two new skills) for references to files that don't exist — e.g. old plan called for excluding `shared/admin-api.md`, `shared/prompt-audit.md`, `shared/platform-availability.md`, `shared/claude-platform-on-aws.md`, and all `shared/managed-agents-*.md` from `claude-api` — confirm no remaining `.md` file under `.kilo/skill/claude-api/` or its 4 mirrors links to one of those non-existent paths. Same check for any `{lang}/managed-agents/` directory reference.
4. **Stale hardcoded counts**: re-run the same class of check as the 2026-07-26 `stale-counts-audit` (skills/agents/commands/instructions counts in docs) — ground truth is the filesystem count in `.kilo/skill/`, `.kilo/agents/`, `.kilo/command/`, `.kilo/instruction/`. Skill count should now be 52 project-wide (was 50 before this session's two additions) — confirm every doc that states a skill count agrees, and flag any that don't.
5. **Lint-budget honesty**: `tools/config/lint-budget.json`'s comment claims the 60->75 raise is entirely `mcp-builder/scripts/evaluation.py` x5 mirrors (15 findings: S314 xml parse + 2x BLE001, per copy). Run `python tools/check_lint_budget.py --list` and confirm the actual finding list matches that claim — flag anything unexplained.
6. **General sweep** (same spirit as the 2026-09-04 audit, but don't just re-check the same five gates and call it done): look for anything else that looks broken, inconsistent, or half-finished — orphaned files, TODO/FIXME markers in shipped (non-test) code under `tools/` or `.kilo/`, `.claude/hooks/*.py` behavior that doesn't match what `CLAUDE.md`/`AGENTS.md` claims about it, skills with frontmatter that doesn't match their actual content, or anything in `git status` that looks like it shouldn't be there (e.g. a file that should have been gitignored, or an untracked directory left over from earlier work).

## Constraints (IMPORTANT — follow exactly)

- **Do NOT modify any file** except the one report file named below. Do not "helpfully" fix anything you find, even something tiny — report it, I decide what to fix.
- Do not create scratch/temp files inside the repository (use your own workspace/scratch area if you need intermediate notes).
- **Never commit, push, or run any destructive command.** Leave the working tree exactly as you found it (it is currently dirty/uncommitted — that is expected, do not stage or revert anything).
- If two engines/tools might be editing the same tree concurrently, check `tools/shared_state.py` locks first; if this audit is read-only (it is), you don't need to take a lock, but don't write anywhere outside the one report path below.
- If you are unsure whether something is a real issue, include it anyway and say you're unsure. Do not silently drop ambiguous findings.

## Expected report format — evidence, not confidence

Write to `.gemini/antigravity/handoff/outbox/full-repo-audit-2026-09-10-report.md` with this frontmatter:

```
---
slug: full-repo-audit-2026-09-10
completed: <ISO date>
from: gemini
---
```

Then, for **every gate in Scope item 1**, a row in:

| Gate | Command run | Output (trimmed) | Pass/Fail |

For every other finding, one row in:

| Area | File | Claim/Expectation | What you found | Command run to verify |

Do not write a row you didn't run a command for. If you couldn't verify something (e.g. a tool unavailable in your environment), say so as its own row with an empty "Command run" cell — don't skip it silently and don't write an unearned "confident: yes".

End with a short **Summary** (bullet list, max 10 bullets): what's actually broken vs. what's fine vs. what's ambiguous and needs a human decision.

Keep the report under 250 lines. Do not paste large file excerpts — cite `file:line` instead.
