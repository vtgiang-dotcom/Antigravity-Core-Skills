---
slug: full-repo-audit-2026-09-10
completed: 2026-09-10
from: gemini
---

# Full Repository Health & Consistency Audit

Audit conducted on 2026-09-10 across all 5 harness engines (`.kilo`, `.claude`, `.copilot`, `.gemini`, `.opencode`).

---

## 1. Verification Gates (Scope 1)

| Gate | Command run | Output (trimmed) | Pass/Fail |
|---|---|---|---|
| **Master Checklist** | `python .github/scripts/checklist.py .` | `Total: 5 \| Passed: 4 \| Failed: 1 (Ruff Linter: FAILED)` | **FAIL** |
| **Ruff Linter** | `ruff check .` | `Found 10 errors (5x I001 unsorted imports, 5x B905 zip missing strict=)` | **FAIL** |
| **Pytest Suite** | `python -m pytest tools/ -q` | `457 passed, 3 skipped in 44.54s` | **PASS** |
| **Garden Drift Audit** | `python tools/garden.py` | `Total drift issues: 0 / Garden is clean — no drift detected.` | **PASS** |
| **Schema Validation** | `python tools/validate_schemas.py` | `Files checked: 66 / Errors: 0 / All schemas valid.` | **PASS** |
| **Lint Budget Gate** | `python tools/check_lint_budget.py` | `Extra rule families: S,BLE / Findings: 75 / Budget: 75 [OK] At budget.` | **PASS** |
| **Secret Scan** | `python .github/scripts/security_scan.py .` | `Files scanned: 950 / No issues found.` | **PASS** |

---

## 2. Findings & Detailed Verifications (Scope 2 – 6)

| Area | File | Claim/Expectation | What you found | Command run to verify |
|---|---|---|---|---|
| **Code Quality (Ruff)** | `*/mcp-builder/scripts/evaluation.py:6` (all 5 mirrors) | `checklist.py` passes | `I001` unformatted/unsorted import block across all 5 copies of `evaluation.py` | `ruff check .` |
| **Code Quality (Ruff)** | `*/mcp-builder/scripts/evaluation.py:269` (all 5 mirrors) | `checklist.py` passes | `B905` `zip()` without explicit `strict=` parameter across all 5 copies | `ruff check .` |
| **Skill Parity** | `.copilot/skill/claude-api/SKILL.md` & `.gemini/antigravity/skills/claude-api/SKILL.md` | Content identical to `.kilo/skill/claude-api/SKILL.md` | Frontmatter description diverged: adds `(Python)`, omits `MCP, agents,` | `git diff --no-index .kilo/skill/claude-api/SKILL.md .copilot/skill/claude-api/SKILL.md` |
| **Skill Parity** | `.copilot/skill/claude-api/shared/anthropic-cli.md:159-228` & `.gemini/...` | Content identical to `.kilo/skill/claude-api/shared/anthropic-cli.md` | Copilot & Gemini copies have 70 extra lines (`Version-controlled Managed Agents resources`) linking to deleted docs | `git diff --no-index .kilo/skill/claude-api/shared/anthropic-cli.md .copilot/skill/claude-api/shared/anthropic-cli.md` |
| **Garden Audit Blindspot** | `tools/garden.py:200-208` | `garden.py` detects content drift across skill mirrors | `check_skills_content_drift()` strips frontmatter and only compares `SKILL.md` body; completely ignores subdirectories (`shared/`) and frontmatter drift | `python -c "import tools.garden"` |
| **Dangling Refs** | `.kilo/skill/claude-api/shared/cost-optimization.md:12,47,77,122` | References resolve to existing files | Cites excluded non-existent `shared/prompt-audit.md`, `shared/claude-platform-on-aws.md`, `shared/platform-availability.md` | `python -c "..."` (rglob regex search) |
| **Dangling Refs** | `.kilo/skill/claude-api/shared/model-migration.md:461,523,529,1601,1843` | References resolve to existing files | Cites excluded `prompt-audit.md`, `platform-availability.md`, `claude-platform-on-aws.md` | `python -c "..."` (rglob regex search) |
| **Dangling Refs** | `.kilo/skill/claude-api/shared/models.md:73`, `prompt-caching.md:174,176,206`, `tool-use-concepts.md:277,303,362,403` | References resolve to existing files | Cites excluded `shared/platform-availability.md` and `shared/managed-agents-*.md` | `python -c "..."` (rglob regex search) |
| **Dangling Refs** | `.kilo/skill/claude-api/shared/live-sources.md:93` | References resolve to existing files/dirs | Cites non-existent `shared/managed-agents-*.md` and `{lang}/managed-agents/README.md` | `python -c "..."` (rglob regex search) |
| **Dangling Refs** | `.kilo/skill/claude-api/python/claude-api/sdk-upgrade.md:172` | References resolve to existing files | Cites excluded `shared/prompt-audit.md` | `python -c "..."` (rglob regex search) |
| **Doc Counts** | Core docs (`AGENTS.md`, `CLAUDE.md`, `.claude-plugin/`, `agent.yaml`) | Ground truth: 52 skills, 14 agents, 14 commands, 10 instructions | All core doc counts match ground truth (52 skills, 14 agents); `agent.yaml` has exactly 52 sorted entries | `python -c "..."` (filesystem vs doc counts) |
| **Doc Counts (Example)** | `SPEC.md:201` | Ground truth matching | Contains historical error example string "32 skills, 15 agents" (benign table row) | `git grep "15 agents" SPEC.md` |
| **Lint Budget Honesty** | `tools/config/lint-budget.json` | 60 -> 75 raise explained solely by `evaluation.py` x5 mirrors | Verified exact: 15 findings across 5 mirrors (1x S314 XML parse + 2x BLE001 per copy = 15) | `python tools/check_lint_budget.py --list` |
| **Hook Behavior Drift** | `.claude/hooks/guard.py:354` | Recommends current primary executor | Hint message still recommends fallback `python tools/kilo_cli_delegate.py` instead of primary `opencode_delegate.py` | `git grep -n "kilo_cli_delegate" .claude/hooks/` |
| **Code Markers** | `tools/*.py` (shipped non-test code) | No unaddressed TODO/FIXME markers | 0 TODO/FIXME/HACK/XXX markers found in non-test `tools/*.py` | `python -c "..."` (tools/ scan) |
| **Working Tree** | Repository working directory | Clean or expected uncommitted batch | 37 tracked files modified, 11 untracked directories (both ported skills across all mirrors) | `git status --short` |

---

## 3. Summary

- **Actually Broken (Immediate Blocker)**:
  1. `python .github/scripts/checklist.py .` fails on Ruff: 10 errors across all 5 mirrored copies of `mcp-builder/scripts/evaluation.py` (5x `I001` unsorted imports, 5x `B905` `zip()` missing `strict=True`).
  2. `claude-api` parity drift: `.copilot/` and `.gemini/` copies of `shared/anthropic-cli.md` retain 70 lines (L159–228) referencing deleted `managed-agents` docs, while `.kilo/`, `.claude/`, and `.opencode/` already had them trimmed.
  3. `claude-api` SKILL.md frontmatter drift: `.copilot/` and `.gemini/` have an older description header mentioning `(Python)` and omitting `MCP, agents,`.
  4. 51 dangling cross-references in `claude-api`: Files across `shared/` (`cost-optimization.md`, `model-migration.md`, `models.md`, `prompt-caching.md`, `tool-use-concepts.md`, `live-sources.md`) and `python/.../sdk-upgrade.md` still cite excluded paths (`prompt-audit.md`, `platform-availability.md`, `claude-platform-on-aws.md`, `shared/managed-agents-*.md`, `{lang}/managed-agents/README.md`).

- **Verified Fine & Fully Compliant**:
  1. Pytest suite: 457 passed, 3 skipped (0 regressions).
  2. Lint budget honesty: The 60 -> 75 increase perfectly matches the 15 bandit/BLE findings in `evaluation.py` x5 copies.
  3. Hardcoded counts: All primary documentation (`AGENTS.md`, `CLAUDE.md`, `.claude-plugin/`, `agent.yaml`) correctly reflect 52 skills and 14 agents.
  4. Schemas & Security: `validate_schemas.py` (66 files) and `security_scan.py` (950 files) both passed cleanly.
  5. Code cleanliness: 0 TODO/FIXME in non-test `tools/` code.

- **Ambiguous / Architectural Decisions for Orchestrator**:
  1. `tools/garden.py` blindspot: `check_skills_content_drift()` currently only compares `SKILL.md` body (ignoring frontmatter and subdirectories like `shared/` or `reference/`), allowing the Copilot/Gemini drift above to report 0 errors. Should `garden.py` perform full recursive diffs on mirrored skill directories?
  2. Hook advice update: Update `.claude/hooks/guard.py:354` hint text from `kilo_cli_delegate.py` to `opencode_delegate.py` to align with the routing table in `AGENTS.md`.
