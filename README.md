# competitor-code-teardown

**An agent skill that conducts engineering teardowns of competing open-source
projects — then helps you decide what to borrow before anyone writes code.**

Business teardown skills read pricing pages, app-store reviews and SWOT.
This one clones repos and reads source.

```
your agent + this skill  =  the conductor
├── SURVEY   STORM-style multi-perspective queries (anti-narrow) ──→ your research stack / deep-research agent
├── READ     clone + repopack / DeepWiki-style packing ────────────→ github.com/yamadashy/repopack (8k★) etc.
└── VERDICT  file:line evidence · license check · borrow list · moat check · confirmed/needs_validation
```

It orchestrates giants instead of competing with them, and contributes the thin
layer none of them ship: **the teardown verdict format and the stop-and-discuss
gate**.

## What it does

1. **Frames** your product and what counts as "same problem"
2. **Surveys** from 4-6 generated perspectives (indie hacker / market analyst /
   non-English ecosystem / migrating power user / skeptic), across web, GitHub
   (stars AND recency sorts), HN archive — with mandatory inclusion of emerging
   sub-1k★ same-problem projects and a "who died and why" check
3. **Triages**: same-problem (deep read) / adjacent (targeted) / reference, with
   license classification at this stage (`AGPL = contamination risk`,
   `no-license = ideas only`)
4. **Reads**: shallow clones outside your repo; large repos packed via repopack;
   every claim cited as `file:line`
5. **Verdicts**: per project — better-than-you (with evidence), borrow list
   (vendor vs re-implement + port cost), and **ours-not-theirs** (the moat check
   that keeps you from teardown myopia), plus the fork test (overlap <50% →
   borrow, don't fork)
6. **Stops** for discussion. Your codebase is read-only until you approve.

## Install

Drop this folder into your agent's skills directory:

```bash
git clone https://github.com/b40609/competitor-code-teardown ~/.agents/skills/competitor-code-teardown
# or for Claude Code-style layouts:
git clone https://github.com/b40609/competitor-code-teardown ~/.claude/skills/competitor-code-teardown
```

Then just say: *"競品工程拆解：我在做 X，針對 Y 出一份帶證據的可搬清單"* —
or in English: *"engineering teardown of projects solving X for my product Y"*.

## Why these rules exist (all from a real teardown)

See `examples/omnikeep-case.md` — a full case where the narrow first sweep
missed four same-thesis indie projects, a no-license repo nearly got its code
borrowed, and an AGPL incumbent nearly got forked. Every rule in this skill
is a scar from that campaign.

## Scripts (the executable half)

```bash
# 1. Dual-track discovery: mature incumbents + the emerging vibe-coding cluster
python scripts/discover.py "self-hosted second brain"

# 2. Clone a candidate + pin evidence (sha + license → research/manifest.json)
python scripts/pin.py https://github.com/owner/repo ./research

# 3. Quality-screen an emerging project (PASS / DEMOTE / DROP)
python scripts/slop_check.py ./research/clones/owner--repo
```

Stdlib-only, zero dependencies. Smoke-tested against live repos — the smoke run
itself caught and fixed three bugs in the heuristics (depth-1 clones falsifying
commit counts, a file-count bar punishing deliberate-minimal architectures, a
ratio formula typo). Tests: `python -m pytest tests/ -q`.

## Credits & neighbors

Standing on: Stanford STORM (multi-perspective questioning), the deep-research
agent lineage (Alibaba DeepResearch 20k★, dzhng/deep-research 19.8k★),
DeepWiki-Open (18.1k★), repopack. Evidence discipline (commit-pinned citations,
falsification criteria) borrowed from
[daymade/competitors-analysis](https://github.com/daymade/claude-code-skills) (MIT).

**vs daymade/competitors-analysis** — that is a durable competitor-intelligence
*platform* (workspace conventions, AGENTS.md product contracts, team
collections, six modes). This skill is the opposite bet: **one folder, zero
conventions, survey-first** — the anti-narrow protocol and the evidence→decision
gate are the product. They coexist fine; some teams run daymade as the engine
and this as the front door.

## License

MIT
