# Case: OmniKeep (real teardown, sanitized)

A self-hosted multimodal intelligence radar + second brain
(FastAPI + SQLite/FTS5 + Vue3 PWA). Question: "many people must have built
this same thing, better — who?"

## Round 1 — the narrow sweep (what went wrong)

Two queries, English, star-sorted. Found the mature layer only:

| Project | Stars | Layer |
|---|---|---|
| Mem0 | 67.7k | agent memory |
| Folo | 39.1k | AI RSS reader |
| Khoj | 37.8k | self-hosted AI second brain |
| Karakeep (ex-Hoarder) | 30.0k | self-hosted bookmark-everything |
| wallabag / Linkwarden | 13k / 20.2k | read-later incumbents |

Conclusion drawn (WRONG in scope): "collection and news layers are lost causes;
only our closed loop is unique."

## Round 2 — forced multi-angle re-sweep

A second reviewer challenged with four project names round 1 never found.
Applying the perspective protocol surfaced the same-problem indie cluster:

| Project | Stars | Created | Same thesis |
|---|---|---|---|
| CondenseIt | 91 | 2026-05 | self-hosted digest, 8 source types, star+engagement dual learning |
| Cruxwire | 12 | 2026-06 | pure-stdlib single container, interest description woven into scoring prompt |
| Prismis | 13 | 2025-09 | Go TUI research daemon |
| Brain | 0 | 2026-07 | closest full-loop analog: batch-gate scoring, ideas tied to user's projects |

**Both maps were true. Only the second was useful.** Four indie teams starting
the same thesis within 18 months = thesis validated, market unclaimed.

## Deep-read verdicts (cloned to a research dir)

- **CondenseIt** — crown jewel `learning/` (1,757 lines): 11-tier preference
  engine, exponential time decay, implicit signals ×0.5, single-call LLM
  rerank. Coupled to their store by one interface. `confirmed` by file read.
- **trend-radar** — great zero-server pattern, **no LICENSE file** → ideas
  only, never code. `confirmed` (license absence is checkable)
- **Karakeep** — AGPL-3.0 → forking it contaminates the user's future open-source
  release. Borrow ideas, never base. `confirmed`

## Decisions that came out of it

1. **No fork** — overlap with the best same-problem competitor was ~30%:
  forking its base meant rewriting 70% of the user's product on someone else's
  foundation. Borrow the 1,757-line module architecture, re-implement natively.
2. **Borrow list** (leverage-ordered): sqlite-vec semantic search · monolith
  full-page snapshots · interest-profile-in-scoring-prompt · gate-tiered
  scoring (8+/6-7/drop) · profile self-reflection pass.
3. **Ours-not-theirs** (moat survived the teardown): local-project watch with
  two-axis permissions (read scope × cloud-consent) + secret redaction +
  proposal approval loop + MCP write-back. No competitor had any of it.
4. **Bonus finding from cross-checking** the second reviewer's report against
  source: a P0 auth gap in the user's own product (verify function defined,
  never wired to routes). Teardowns of others routinely surface your own bugs.

## Lessons encoded into this skill

- The anti-narrow protocol exists because round 1 happened
- `needs_validation` exists because README claims (e.g. "Karakeep semantic
  search") turned out version-dependent (current version: Meilisearch backend)
- The license check at TRIAGE exists because of trend-radar
- The moat section exists because after reading five better-funded codebases,
  the user's takeaway had become "we lose everywhere" — the ours-not-theirs
  list reversed that to "we lose the layers everyone has; we own the loop
  nobody has"
