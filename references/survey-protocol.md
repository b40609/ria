# Survey Protocol — the anti-narrow playbook

The single most common failure mode of competitive surveys: two queries, one
language, star-sorted results — which surfaces only mature incumbents and misses
the same-problem indie cluster entirely. This protocol exists because that
failure happened in a real teardown (see examples/): round one found 30k★
incumbents; a forced multi-angle re-sweep found FOUR sub-100★ projects built on
the exact same thesis within the last 18 months. Both maps were true. Only the
second one was useful.

## Step 1 — Perspectives before queries (STORM method)

Before typing any query, generate 4-6 perspectives on the topic. Each
perspective writes its OWN queries — never reuse one query set across
perspectives. Proven perspectives:

| Perspective | Asks | Typically surfaces |
|---|---|---|
| Indie hacker building the same thing | "how would I build this", stack keywords | small same-problem repos, Show HN posts |
| VC / market analyst | category names, "alternatives to X", comparison posts | incumbents, funding pages, market maps |
| Non-English ecosystem user (user's language: zh/ja/ko/…) | native keywords, 本地生态 terms | regional tools invisible in EN search |
| Power user migrating | "switching from X", "X alternative self-hosted" | migration threads, pain-point lists |
| Academic / researcher | survey papers, benchmark repos | foundational techniques, eval sets |
| Skeptic | "X is dead", "X shut down", failure post-mortems | sustainability risks, dead predecessors |

## Step 2 — Parallel platform matrix

Run perspectives against multiple sources in the same round:

- **Web search** (EN + user's language) — 2 engines if available
- **GitHub**: dual-track with concrete syntax —
  - Baseline (maturity): `gh search repos "<keywords>" --sort stars --limit 10`
  - Emerging (the vibe-coding cluster): `gh search repos "<keywords>" --sort updated --created=">YYYY-MM-DD" (≤90d) --stars=5..500 --json fullName,stargazersCount,createdAt,pushedAt,description` — recent creation + real push activity, star band excludes both toys and giants
  - Also `gh search repos` with different phrasings; search awesome-lists in the domain
- **Hacker News archive** (Algolia API) — Show HN posts reveal projects too
  young to rank, and post-mortems reveal dead ones
- **Product directories** (AlternativeTo / mcp registries / skills marketplaces,
  domain-specific)

Record for every candidate: `stars / created / last-push`. A 4k★ repo created 3
months ago is a stronger signal than a 30k★ repo pushing less often.

## Step 3 — Mandatory inclusion rules

1. Emerging projects (<1k★, created <18mo) get the same table space as
   incumbents. Same-problem indies validate the thesis and are the closest
   architectural references.
2. At least one non-English sweep per survey.
3. At least one "who died and why" check (Omnivore-style post-mortems) — a dead
   predecessor's cause of death is strategy input.

## Step 3b — Emerging-project quality screen (15-minute triage)

The vibes era produces shells: a brilliant README over 200 lines of hollow
code. Before investing a deep-read in a low-star new project, pass it through:

| Check | Pass signal | Fail signal |
|---|---|---|
| README ↔ code consistency | claimed feature locatable in source | headline feature has no code |
| Tests | has tests, any quality | zero tests AND zero CI |
| Commit texture | real history, iterations | single init commit / mass-generated |
| Dependency sanity | plausible deps for the claim | imports that don't exist or do nothing |

One fail = demote to `reference` (notes only). Two fails = drop with a note.
This screen is what makes "mandatory inclusion of emerging projects" affordable.

## Step 4 — Stop rule

Three consecutive full sweeps (new perspectives or new phrasings) returning zero
new names. Fewer than that, you are guessing the market is exhausted.
