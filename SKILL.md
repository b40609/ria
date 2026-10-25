---
name: competitor-code-teardown
description: Engineering teardown of competing open-source projects — multi-perspective landscape survey (anti-narrow), clone and deep-read source code, deliver an evidence-backed borrow list (file:line, license, port cost) plus a "what we have that they don't" moat check, and STOP for discussion before touching the user's codebase. Use when the user wants 競品分析/競品拆解 of source code (NOT pricing-page business teardown), wants to study similar projects before building a feature, asks "who else built this and did it better?", or wants patterns/modules borrowed from other repos into their own product.
---

# Competitor Code Teardown (Conductor)

You are the conductor of an engineering teardown. You do NOT reinvent reading or
searching — you orchestrate the giants and own the verdict. Business teardown
skills read pricing pages and app-store reviews; **this skill reads source code.**

Non-negotiable rules:
1. Evidence means `file:line @ short-sha` from actual cloned source. README paraphrasing is not evidence.
2. Clones go to a research directory OUTSIDE the user's product repo. Never `git clean` anything inside the product.
3. No LICENSE file found = ideas only, never code.
4. The user's secrets/keys must never appear in any output.
5. Every conclusion is marked `confirmed` (code-verified) or `needs_validation` (inferred). Never present inference as fact.
6. The user's product is read-only until the DISCUSS step ends with explicit approval.
7. Output abstract design + citations from competitors, never large copy-pasteable code blocks — even permissive licenses don't make wholesale dumping good practice, and it invites contamination.
8. Default to public repos only. Read the license before the deep-read, not after.

## Workflow

### 1. FRAME
Write down: the user's product in one sentence, the problem it solves, and what
counts as "same problem". Ask the user only if the framing would change which
competitors qualify. A wrong frame poisons everything downstream.

### 2. SURVEY (anti-narrow protocol — see references/survey-protocol.md)
Generate diverse perspectives BEFORE searching (STORM-style: indie hacker
building the same thing / VC mapping the market / non-English ecosystem user /
power user migrating from incumbents / academic). Each perspective writes its
own queries. Sweep in parallel: web (EN + user's language), GitHub (multi-keyword,
sorted by stars AND by recently-created), HN archive, awesome lists.

Hard rules:
- **Emerging small projects are mandatory** (<1k★, created <18mo). Big incumbents
  and same-problem indies are DIFFERENT clusters; narrow sweeps find only the first.
- Stop only after 3 consecutive sweeps return zero new names.
- Record stars/last-push/created dates for every candidate (a 3-month-old 4k★
  repo is a bigger signal than a stale 30k★ one).

### 3. TRIAGE
- **same-problem** → deep read (every file that matters)
- **adjacent** (one module overlaps) → targeted read of that module only
- **reference** (architecture worth studying) → notes only

Check LICENSE now, not later. Tag each: `MIT/BSD/Apache = borrowable`,
`AGPL/LGPL = contamination risk — flag before any code moves`, `none = ideas only`.

### 4. READ
Shallow-clone into the research dir. **Context discipline is mandatory**: never
load multiple competitor repos into the main context — one repo per sub-agent
(or one packed artifact per pass); the main agent only ever receives the
structured verdicts. Reading N repos inline is the #1 way teardowns die of
context bloat and the model starts forgetting your product mid-analysis.

Scale the reading:
- Large repo (>50k lines): pack with `npx repopack` or a DeepWiki-style index if available; the sub-agent reads the packed artifact.
- Small repo: sub-agent reads files directly.
- For each "they do X better" claim: cite `file:line @ short-sha`, measure the
  surface (lines, coupling points to their store/ORM/framework), note whether
  the design fits THEIR scale but not the user's, and what it would take to
  transplant into the user's stack.

### 5. VERDICT (per project — see references/report-template.md)
For every deep-read project produce:
1. **Better than us** — with file:line evidence
2. **Borrow list** — each item: source `file:line-range`, size, coupling, license, port cost (`vendor` vs `re-implement`, with a recommendation)
3. **Ours-not-theirs** — what the user's product has that this project lacks
   (prevents teardown myopia: after reading you only remember where you lose)

Close with the synthesis: where the market is crowded, where it is empty,
and the overlap percentage between the user's product and the best competitor.
**Fork-vs-borrow test**: if overlap < ~50%, forking their base means rewriting
most of the user's product on someone else's foundation — borrow modules instead.

### 6. DISCUSS
Present: the synthesis, your disagreements with the user's assumptions (if any),
a recommended borrow priority ordered by leverage-per-effort. Present options as
a matrix (multiple choices + tradeoffs + one recommended default), never a single pick.

### 7. DECIDE → HANDOFF
Only after explicit approval: turn the agreed borrow list into implementation
order and hand off. New scoring/ranking logic adopted this way ships only after
a benchmark against the incumbent's behavior (adopt the "current system is the
ground truth" acceptance rule — don't ship worse than what you had).

## Conductor wiring (use what's installed, degrade gracefully)
| Segment | Own scripts (in scripts/) | External fallback |
|---|---|---|
| Survey shortlist | `python scripts/discover.py "<query>"` (dual-track gh search) | manual multi-query web search |
| Emerging quality screen | `python scripts/slop_check.py <cloned-repo>` (PASS/DEMOTE/DROP) | apply survey-protocol Step 3b by hand |
| Clone + evidence pin | `python scripts/pin.py <url> ./research` (sha + license → manifest.json) | manual clone + record sha/license |
| Repo packing | `npx repopack` | `code2prompt` or direct sub-agent reads |
| Repo wiki | DeepWiki-Open if installed | read entrypoints manually |

Scripts are stdlib-only Python; they accelerate the protocol but never replace
it — a `DEMOTE` from slop_check is triage advice, and the report still needs a
human-visible reason recorded in shortlist.md.
