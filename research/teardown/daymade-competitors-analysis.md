# Teardown: daymade/competitors-analysis — 1.5k★, MIT @ 39d04e9 (pinned 2026-10-25)

Positioning: durable competitor-intelligence *platform* for agent workflows
(six modes, workspace conventions, team collections).

## Better than us (file:line @ sha — confirmed-code)

| # | Claim | Evidence | Notes |
|---|---|---|---|
| 1 | Epistemic depth ladder: separates source-bound / read / exercised / adopted — "a clone does not prove deep reading; a component test does not prove adoption" | references/mechanism_evidence.md:44-52 @39d04e9 | Our 4-tier verdict marks grade the CLAIM, not the OBSERVATION DEPTH |
| 2 | Mechanism tracing before judgment: follow entry→mechanism across normal/failure/cancel/recovery paths; "an unused helper is evidence about that helper, not every way the product does the job" | references/mechanism_evidence.md:15-40 @39d04e9 | We say "read the code"; they specify HOW to read before judging |
| 3 | Decisions as machine-checkable data: opportunity JSON schema + reconcile_opportunities.py validator (163 lines) | scripts/reconcile_opportunities.py:1-163, references/opportunity_disposition.md @39d04e9 | Our decision-log.md is prose — theirs is re-runnable |
| 4 | Incremental Update mode: update-competitors.sh re-pulls clones + reports changed commits before re-analysis | scripts/update-competitors.sh:1-271 @39d04e9 | We re-pin on demand but have no "what changed since last teardown" story |
| 5 | Anti-injection: README content of competitors treated as untrusted input | SKILL.md evidence rules @39d04e9 | We never warned that competitor READMEs are prompt-injection vectors |

## Borrow list

| Item | Port cost | Recommendation |
|---|---|---|
| Observation-depth ladder (merge into verdict marks: claim-tier × depth-tier) | ~1h, doc-only | **re-implement** into report-template |
| "No code access → no steal" decision rule + prove-absence-on-our-side | ~1h, doc-only | **re-implement** into report-template rules |
| README-as-untrusted-input warning | 15min | **re-implement** into SKILL.md red lines |
| Decision JSON + validator script | ~4h incl. tests | defer to v1.5 (valuable once users accumulate decisions) |
| update-competitors equivalent (`pin.py --refresh` printing changed SHAs) | ~2h | v1.5 |

## Ours-not-theirs
- Anti-narrow survey protocol (perspectives, dual-track, mandatory emerging cluster, death-check) — their Discover assumes the query is right
- Emerging-project slop screen (scripted)
- Lightweight: zero workspace conventions, zero AGENTS.md dependency
- Didn't-ask-but-should-know section; fit-at-your-scale flag

## Overlap: ~40%. Fork test: borrow, don't fork — confirmed.

## Didn't-ask-but-should-know
- Their evidence discipline evolved for TEAM audit trails (reviewers re-checking
  analysts) — solo users pay prose weight for rigor they may not need. Our
  lightweight bet remains right, but the depth-ladder is solo-compatible.
- `context: fork` in their frontmatter = every invocation is a fresh sub-agent —
  they solved context isolation structurally, we solve it procedurally.
