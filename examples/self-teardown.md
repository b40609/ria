# Case: the skill tore itself down (real, sanitized-by-construction)

The day after publishing v1.3, we ran this skill on **its own market** —
competitor-skill projects — as the first end-to-end dogfood run.

## What the run looked like

1. **FRAME**: product = this skill v1.3; same-problem = skills/workflows that
   tear down competitor source code into borrow decisions.
2. **SURVEY**: five independent model reviews + two live-search rounds had
   already built the landscape (the anti-narrow protocol exists because round 1
   of that earlier campaign missed the entire emerging cluster). Shortlist for
   deep-read: daymade/competitors-analysis (incumbent), boshu2/reverse-engineer
   (rigor specialist).
3. **READ**: `scripts/pin.py` cloned + SHA-pinned both
   (daymade @39d04e9, boshu2 @b7bbd41, licenses auto-classified). Deep-read went
   straight for `references/` + `scripts/` — the parts five model reviews had
   only summarized from READMEs. That's where everything valuable turned out
   to live.
4. **VERDICT + GATE**: full teardown files under `research/teardown/`; the
   borrow matrix went to `research/recommendations.md`; **implementation of
   v1.4 stopped at the approval gate**, exactly as SKILL.md rule 6 demands.

## Headline findings (all `confirmed-code`, see teardown files)

- daymade separates *observation depth* (cloned ≠ read ≠ exercised ≠ adopted)
  from claim truth — our verdict marks graded claims but not depth.
- boshu2's harder rules: "no code evidence → no steal", "prove absence on YOUR
  tree with a cited search", "steal the pattern, not the platform".
- Both treat competitor READMEs as untrusted input; we hadn't warned about
  prompt injection through competitor docs at all.

## Why dogfooding paid for itself three times

1. **Friction found**: the research/ tree, pin.py and slop_check slotted into
   their own workflow exactly as documented (or the docs got fixed).
2. **Real borrow list**: v1.4+ items came from files nobody had read before
   this run — not from README paraphrasing.
3. **The gate demo**: the most credible way to show what this skill forbids is
   to be forbidden by it — this case study ends at a stopped gate.

## Meta-lesson

Every scar rule in this skill came from a real campaign (see omnikeep-case.md);
this one added four more from the skill's own market.
