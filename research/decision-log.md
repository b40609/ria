# Decision Log

## 2026-10-26 — RIA naming decision
- User selected RIA — Research & Improve Anything and requested the name change everywhere, including GitHub.
- Renamed the repository and installed skill to `ria`; updated branding and installation URLs.
- Product direction covers starting a product, improving an existing product, and adding features. Full support for all three scenarios remains future work.
- Kept the evidence requirements and discussion gate unchanged.

## 2026-10-25 — Standing authorization for the self-improvement loop
User granted: survey same-problem works → clone/deep-read → self-assess →
execute, WITHOUT stopping at the gate each time. Constraints agreed:
scope = this repo only; red lines additive-only; tests+CI stay green; every
autonomous decision logged here; major versions still go to multi-model review.

## 2026-10-25 — Iteration 3 (first fully autonomous loop)
- Fresh sweep via own `discover.py`: new emerging cluster found — vertical
  "evidence-based" business-teardown skills (Etsy/ecommerce/brand, all 2026,
  0-60★). Engineering lane still empty. No action.
- Deep-read 2 new targets (pinned via pin.py): yzddmr6/repo-analyzer,
  EveryInc/compound-engineering-plugin.
- DECIDED + EXECUTED (both doc-level, attributed):
  1. Module-analysis essentials + the "reproduction test" completeness bar
     (another AI reading only the report must be able to redraw the
     architecture) → report-template.md. Source: yzddmr6 module-analysis-guide.
  2. Proportionality gate at FRAME (Quick scan vs Full teardown, escalate on
     doubt) → SKILL.md step 1. Source: EveryInc CONCEPTS.md sizing/shape rules.
- Rejected (no borrow): compound-engineering's heavy frontmatter vocabulary
  (ecosystem-specific); repo-analyzer's Mermaid-for-everything (verbosity risk).
