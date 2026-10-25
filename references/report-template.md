# Report Template & Verdict Rules

One section per deep-read project. Copy this schema verbatim.

```markdown
## <Project> — <stars>★ (created YYYY-MM, last push YYYY-MM-DD), <license>

**One-line positioning**: what it is, who it's for.

### Better than us  (every claim: `path/file.py:LINE` — confirmed)
| # | Claim | Evidence | Size/coupling |
|---|---|---|---|
| 1 | e.g. 11-tier scoring engine w/ time decay | src/learning/preference_engine.py:1-180 | 1,098 lines, coupled to their store via 1 interface |

### Borrow list
| Item | Source | License-clean? | Port cost | Recommendation |
|---|---|---|---|---|
| e.g. decay-weighted profile centroid | embeddings.py:88-140 | MIT ✓ | ~2 days re-implement | **re-implement** (vendor drags their store interface) |

`Port cost` must pick one: **vendor** (copy file(s), keep attribution) or
**re-implement** (keep architecture, write natively). Vendor only when coupling
is near-zero and license is permissive.

### Ours-not-theirs
- …
- …
(moat check — if this list is empty, say so plainly)

### Overlap: ~N%
What fraction of this product's core the user's product already has.
Fork test: overlap <50% → borrowing modules beats forking their base.
```

## Verdict marks (every non-trivial statement carries one)

- `confirmed` — you read it in the cloned source at a citable location
- `needs_validation` — inferred from README/docs/structure, not yet code-verified
- `rejected` — claimed elsewhere but disproven in source (state the counter-evidence)

Mixing these up is the cardinal sin of AI audits: unverified inference presented
as confirmed finding.

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
