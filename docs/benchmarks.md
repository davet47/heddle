# Benchmarks — the scorecard

Every token-reduction number heddle has produced, in one place: what was
measured, on what project, when, under which heddle, and who was driving.

All ratios are deterministic token counts — both sides of every comparison are
counted with the same tiktoken encoder (`cl100k`), so **the ratio does not
depend on the AI model driving the session**. The driving model is recorded as
provenance of each run, not as a variable in the result; the twin's ratio
moving only 9.2× → 9.1× across a month, a heddle upgrade, and a change of
driving model is itself evidence the metric is stable.

## Headline numbers

| scenario | scope | raw tokens | heddle tokens | ratio | median/unit | date | heddle | run driven by |
|---|---|--:|--:|--:|--:|---|---|---|
| sales example (DoD gate) | 3 tasks over 20 contracts | 6,004 | 1,117 | **5.4×** | — | 2026-07-04 | 0.3.0 | CI (mechanical, every push) |
| enora twin, full sweep | all 43 contracts, each regenerated once | 170,789 | 18,722 | **9.1×** | 7.9× | 2026-07-04 | 0.3.0 | Claude Fable 5 session |
| enora twin, prior run | all 43 contracts | — | — | ~9.2× | — | 2026-06-14 | 0.1.x | Claude Opus session |

Raw-side counts reproduce exactly; heddle-side totals jitter by ~1 token per
unit between runs (verify statuses flip `pass` → `cached-pass`), so per-unit
last decimals move while every ratio above is stable. An independent re-run
the same day confirmed all ratios, the median (7.93×), and the below-5×
count.

The two projects answer different challenges. The sales example is heddle's own
20-contract demo — small, and the repo README concedes its baseline is
constructed. The enora twin is a real customer-side digital-twin PoC (43
contracts, 24 source modules, energy-domain logic) that was **not built to
flatter the tool** — and it scores *higher*, because real projects have deeper
dependency structure than a demo: the more closure a unit has, the more a
~300-token packet saves.

## What one number hides: the distribution

From the twin's full sweep (2026-07-04):

- **Deep units** (large transitive closures) are where heddle earns its keep:
  `create_app` ~40× (17,404 → ~430 tokens), `replay_counterfactual` ~26×,
  `run_scenario` ~22×, `apply_scenario` ~16×, `simulate` ~15×.
- **Leaf types** barely benefit: `EnergySeries` ~1.9× — no dependency closure
  means the raw files were already cheap. 13 of 43 units individually fall
  below 5×.
- The overall 9.1× is raw-token-weighted, so deep units dominate it — but the
  per-unit **median is 7.9×**, close enough that the headline is not a
  weighting artifact.

## Cache economics (from real stores, not benchmarks)

Verification caching is the other half of the payoff, and both dogfood stores
carry live, **cumulative** counters — they advance with every use, including
benchmark sweeps, so these are dated snapshots, not constants:

| store | snapshot (2026-07-04) | verify requests | served from cache | test runs avoided | hit rate |
|---|---|--:|--:|--:|--:|
| enora twin | before the day's benchmark sweeps | 135 | 92 | 92 | 68% |
| enora twin | after three full 43-unit sweeps | 357 | 271 | 271 | 76% |
| heddle-on-heddle | day one of dogfooding | 43 | 31 | 31 | 72% |

The twin's two rows illustrate the mechanism working as designed: benchmark
sweeps themselves hit the cache, so repeated verification drives the
cumulative hit rate up, not down.

One accounting caveat: `status`'s cumulative **token counters populate only via
the MCP server** (`_respond` in `server.py` counts every tool response); both
projects have so far been driven through the CLI, so their `tokens` blocks read
zero. They will accumulate the first time an agent session drives
`heddle serve` for real.

## What the numbers claim — and what they don't

The methodology (identical in both projects' `bench/benchmark.py`): **raw
mode** counts what a file-based agent reads to regenerate one unit — the spec
and full source file of the unit *and* of every transitive dependency, the
unit's own tests, and one pytest run's output. **Heddle mode** counts the JSON of three
tool responses: `get_contract`, `get_dependents(transitive=true)`, `verify`.

Read the numbers with these concessions attached:

- **The baseline is granted free, perfect knowledge of the dependency
  closure** — no grep, no wrong-file reads, no discovery cost. That is
  deliberately generous to the baseline, since computing the closure is
  precisely what heddle does; a real file-based agent pays discovery on top.
- **The heddle side assumes first-try-green regeneration** from the packet
  alone — no failure/iteration loop, no re-reading tests — and MCP session
  overhead (tool schemas, call inputs) is uncounted.
- **It is a per-change maintenance estimate, not a session total.** Repeated
  edits in one session amortize raw file reads; conversely, every fresh
  session pays them again.
- **The initial build is not measured and costs *more* with heddle** —
  contracts are authored on top of the code and tests. The payoff is at
  maintenance and regeneration time.
- The twin's pytest output is quiet (`addopts="-q"`, 143 tokens on a green
  run); a failing raw run would dump tracebacks where heddle serves a
  ≤40-token summary, so the failure-path advantage is invisible in these
  numbers.

## Reproduce

```bash
# sales example (also the CI DoD gate — exits nonzero below 5x)
cd heddle && uv run python bench/benchmark.py

# enora twin (private repo)
cd enora.enora-twin && make bench
```

New scenario runs belong in the table above — record date, heddle version, and
what drove the run.
