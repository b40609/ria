# Report Template & Verdict Rules

Teardowns are durable artifacts, not chat messages. Produce this tree inside
the research directory (structure battle-tested in a real campaign):

```text
research/
├── landscape.md            # the market map + survey method used
├── shortlist.md            # candidates in, candidates out, why
├── teardown/<project>.md   # one file per deep-read project (schema below)
├── evidence.md             # cross-project index of key claims → citations
├── recommendations.md      # borrow priority matrix + disagreements
├── decision-log.md         # what the user decided, with reasons
└── implementation-brief.md # ONLY written after approval — the handoff spec
```

One section per deep-read project, using this schema:

```markdown
## <Project> — <stars>★ (created YYYY-MM, last push YYYY-MM-DD), <license>

**One-line positioning**: what it is, who it's for.

### Deep-dive modules (when a mechanism matters)
Analyze by business capability, not by file. Each deep-dive module covers four
essentials — core data structures / execution flow (Mermaid optional, with
`file:line`) / design decision & trade-off / inter-module dependencies — and
answers: why does this module exist (what breaks without it)? **Completeness
bar: another AI reading only your report should be able to redraw the
architecture.** (discipline from yzddmr6/repo-analyzer)

### Better than us  (every claim: `path/file.py:LINE @ short-sha` — confirmed)
| # | Claim | Evidence | Size/coupling | What would overturn it |
|---|---|---|---|---|
| 1 | e.g. 11-tier scoring engine w/ time decay | src/learning/preference_engine.py:1-180 @a1b2c3d | 1,098 lines, coupled to their store via 1 interface | engine bypassed in current flow; weights hardcoded |

Evidence is pinned to the commit analyzed (`git rev-parse --short HEAD` in the
clone) — repos move; unpinned citations rot. (discipline borrowed from
daymade/competitors-analysis, MIT)

### Borrow list
| Item | Source | License-clean? | Port cost | Recommendation |
|---|---|---|---|---|
| e.g. decay-weighted profile centroid | embeddings.py:88-140 | MIT ✓ | ~2 days re-implement | **re-implement** (vendor drags their store interface) |

`Port cost` must pick one: **vendor** (copy file(s), keep attribution) or
**re-implement** (keep architecture, write natively). Vendor only when coupling
is near-zero and license is permissive. Also flag **scale-fit**: designs that
make sense at THEIR scale (team, traffic, funding) but not at the user's.

### Ours-not-theirs
- …
- …
(moat check — if this list is empty, say so plainly)

### Didn't-ask-but-should-know
Things the user did not ask about but would change their decision if they knew
(buried config costs, an undocumented hard dependency, an upstream feud, a
dead predecessor with the same thesis). Fixed section, never optional — the
highest-value lines of the report usually live here.

### Overlap: ~N%
What fraction of this product's core the user's product already has.
Fork test: overlap <50% → borrowing modules beats forking their base.
```

## Verdict marks (every non-trivial statement carries one)

- `confirmed-code` — you read it in the cloned source at a citable `file:line @ sha`.
  When depth matters, append it: `/read` (traced on the tree) → `/exercised`
  (ran or tested it) → `/adopted` (verified in real use).
  **Cloned ≠ read ≠ exercised ≠ adopted** — grade the observation, not just the claim.
- `confirmed-docs` — the project's own docs/README claim it; plausible but NOT
  code-verified. May support gap/park/reject decisions — **never a borrow**.
- `hosted` — a service/control-plane claim you cannot inspect. Unverifiable by
  construction; never drives borrowing.
- `needs_validation` — your inference from structure/patterns
- `rejected` — claimed elsewhere but disproven in source (state the counter-evidence)

Mixing these up is the cardinal sin of AI audits: unverified inference presented
as confirmed finding.

## Hard decision rules

1. **No code evidence, no steal.** Without `confirmed-code`, any borrow decision
   is capped at gap / park / reject.
2. **Prove absence on your side.** Every "we lack X" row cites the search that
   proved it (command + scope run against the USER's tree). And per the
   mechanism-tracing discipline: an unused helper in their repo is evidence
   about that helper, not about every way either product does the job.
3. **Steal the pattern, not the platform.** Default is re-expressing in the
   user's own primitives; vendoring requires an explicit, coupling-justified
   override.

## Synthesis section (after all projects)

1. **Crowded vs empty**: which capability layers have strong incumbents, which are open
2. **The cluster map**: same-problem indies listed separately from incumbents —
   a fresh cluster of sub-100★ same-thesis projects means the thesis is timely
   and unclaimed
3. **Recommended borrow priority**: ordered by leverage-per-effort, as an option
   matrix (choices + tradeoffs + one recommended default)
4. **Disagreements with the user's assumptions**, if any — stated to their face

## Discussion gate

The report ENDS at the synthesis. Implementation order, roadmap placement, and
any code changes wait for explicit user approval. Present the fork-vs-borrow
test result BEFORE anyone gets excited about rewriting.
