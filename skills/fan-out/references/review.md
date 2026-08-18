# fan-out: review

Read this before dispatching a fan-out that reviews code — a diff, a PR, a subsystem. Review fans out well because the axes are genuinely independent: each finder needs the same code and a different question.

**Split by dimension, one finder per axis.** The four defaults:

- **correctness** — does the code do what it claims: logic, edge cases, error and retry paths, concurrency, resource lifetimes, and tests that only appear to test something
- **standards** — does it follow *this* repo's conventions, both documented (lint and formatter config, CONTRIBUTING, CLAUDE.md / AGENTS.md, ADRs) and observed (how the neighbouring modules already do it). Tell the finder to establish the convention from the repo before judging anything, and to cite the file that establishes it — a convention it cannot cite is a preference, not a finding.
- **spec alignment** — does it do what the originating issue, ticket, or spec actually asked: requirements left unmet, cases silently dropped, and scope the author added on their own
- **security** — untrusted input reaching a sink, authz checks missing or done in the wrong layer, secrets and logging, injection, unsafe defaults

The standards and spec-alignment axes are adapted from `code-review` in [mattpocock/skills](https://github.com/mattpocock/skills) (MIT).

Add axes when the change earns them — performance, migration and backward compatibility, public API surface, operability. Drop an axis only when the diff plainly has none of that surface, and say in the report that you dropped it.

**Give every finder the same code and a different question.** Inputs by reference: base ref, changed paths, the originating issue. Each returns findings as items, never prose: location as `file:line`, what is wrong, why it is wrong here, proposed severity, and the evidence — the quoted code, the cited convention, the requirement it misses. Forbid cross-axis commentary; a finder cannot see the other finders and should not guess at them.

**Then verify adversarially, one verifier per finding.** The verifier's job is to kill the finding, not to confirm it — reviewers reliably produce claims that are plausible and wrong. It gets the finding and the code, not the finder's confidence or reasoning. It reproduces the problem, reads the surrounding code, and checks the obvious refutations: the missing check exists upstream, the case is unreachable, the convention was superseded, the requirement is met elsewhere. It returns confirmed / cannot reproduce / refuted with reasoning. Only confirmed findings reach the report; the rest are dropped, and a "cannot reproduce" on something serious is worth one line saying so.

**Integrate into one severity-ranked report.** Merge duplicates across axes into a single entry that names every axis that found it — an issue three finders hit independently is usually the most important one on the list. Rank blocking, then should-fix, then nits, and keep nits short. One entry per real problem, written by you. Never pass agent outputs through as a stack.

**State coverage.** What was reviewed (refs, paths, file count), and what was not: generated files, vendored dependencies, an axis you dropped and why, anything too large to read in full. No silent truncation — an unstated gap reads as a clean bill of health.
