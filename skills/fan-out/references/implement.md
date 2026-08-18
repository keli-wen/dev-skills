# fan-out: implementation

Read this before dispatching a fan-out that writes code. The gate in SKILL.md still applies first — implementation is usually more coupled than it looks, and a bad split here costs a rewrite, not just a wasted agent.

**Discover the full work list before splitting anything.** Never size a fan-out off an estimate. Grep, read, and enumerate every site that must change; count the list and look at it. Sized before discovery, a fan-out either leaves sites untouched or hands the same file to two agents. If discovery itself is wide, make that its own fan-out first — explorers return lists, you merge them, and implementation dispatches from the merged list, never from one explorer's slice.

**Fix the cross-cutting decisions before dispatch.** Interfaces, signatures, data structures, naming, error handling, and the overall approach are yours, decided while you still hold the whole picture, then written verbatim into every affected contract. An agent told to "add caching here" will invent a cache key format; three agents will invent three. Anything you would otherwise reconcile afterwards is cheaper as one sentence in a contract than as a refactor across five agents' output.

**Cut along coupling, not along stage.** Good cuts: one agent per call site, package, or adapter, sharing nothing but the interface you already fixed. Bad cuts: one agent writes the code, one writes the tests, one writes the docs — that splits exactly where shared context is highest, and each stage has to reconstruct what the last one meant. If two slices would need to talk mid-run to stay consistent, they are one slice; merge them.

**Isolate the workspace when agents mutate the same repo in parallel.** Agents sharing a checkout race on the index, on build outputs, and on each other's half-finished edits, and the resulting failures look like logic bugs. Give each writer its own git worktree on its own branch and merge them yourself. If worktrees are unavailable, serialize the writers and keep the parallelism for reads.

**Every implementation contract carries these, on top of the standard contract fields:**

- the fixed decisions, quoted, not paraphrased
- the exact files this agent owns, and the ones it must not touch
- acceptance criteria stated as observable behavior, in the form the verifier will later be given
- how to build and test this slice, so a failure comes back as a result instead of surfacing at integration
- a stop rule: if the slice appears to need a change to a shared interface, report instead of changing it

**Verification is on by default.** Spawn a black-box verify subagent that receives only the acceptance criteria and the artifact — not the plan, not the implementer's reasoning, not the justification attached to the diff. Context is what makes a verifier agree with the implementer, so withholding it is the whole point. Skip verification only when the user explicitly opts out; that is an advanced-user move, and when they take it you say so once. Never drop it silently to save a dispatch.

**Integrate by hunting inconsistencies.** Read every agent's output yourself and look specifically for what individually-correct slices get wrong together: two spellings of one identifier, the same helper written twice, incompatible assumptions about nullability or ordering, an interface that drifted from the one you fixed. Then build and test the merged tree, not each slice in isolation. Report which sites changed, which were deliberately skipped, and why.
