# fan-out: research

Read this before dispatching a research fan-out. Research is the pattern fan-out was made for — the information space is wider than one context, and the angles genuinely do not need to talk to each other.

**Make the angles genuinely distinct.** The default axis is source type, because different sources fail in different ways:

- official material — docs, specs, changelogs, the source of the thing itself
- community and prior art — issues, discussions, posts, competing implementations, the reasons people abandoned approaches
- papers and formal treatments, where the topic has them
- code in the wild — how real repositories actually use it, which often contradicts the docs

When source type does not split the question, split by subsystem, by time window (what was true two versions ago versus now — essential for anything with churn), or by perspective (proponent, skeptic, operator). Test any split by asking whether two agents would come back with the same links. If they would, it is one agent.

**Each explorer starts wide, then narrows.** Put it in the contract: survey the space first and report what the landscape looks like, then go deep on the two or three most load-bearing items. An agent aimed straight at a narrow query returns the first plausible answer it finds and stops, which is how a fan-out produces four confident agents and no coverage.

**Demand raw citable findings, not summaries.** Each finding carries the claim, the source name, the URL or file path, the date or version when the topic moves, and a verbatim quote for anything precise — numbers, API signatures, guarantees. Two prohibitions worth stating explicitly in the contract: no cross-source synthesis (an explorer cannot see the other explorers, so "the sources agree" is a guess), and no inference dressed as a finding — inference is allowed, but labelled as the agent's own.

**Verify what will drive a decision.** Any claim a decision will rest on gets a separate pass whose job is to refute it or show it is stale — reopen the source, check the version, look for the retraction or the newer answer. Mark each key claim confirmed, plausible, or refuted, and note what would change the verdict. Claims that are merely interesting do not earn this.

**Synthesize with the line visible.** One report: answer first, then evidence, then open questions. Every sentence a reader might act on either carries a citation or is visibly your own judgment — the two must never blur into one voice. State coverage: angles covered, angles dropped, and where the sources were thin or disagreed. Contradiction between sources is a finding; report it as one rather than averaging it away.

One note on scope: for deep research grounded in a project's durable context system — read the existing contexts first, sharpen the question down to the real gap, file the verified result back — the user-facing entry point is `/ctx-research`, which wraps this pattern with grounding and file-back. This playbook stays generic and does not duplicate that workflow.
