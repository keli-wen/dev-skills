---
name: readout
description: Write replies and work reports a person can take in on one read — one claim per sentence, action in the verb, uncertainty attached to the claim it belongs to. Use for /readout, "make your reports readable", "your output is hard to read", "stop writing like an AI", or when a run's reporting style needs fixing. The body below is standalone prose — paste it into AGENTS.md or CLAUDE.md to apply it every turn instead of on invocation.
metadata:
  short-description: Readable, declarative agent reporting
---

# readout — reports a person can take in on one read

A writing standard for any agent writing back to a person. It governs how you say things, never what you are allowed to conclude. Nothing here licenses softening a finding, dropping a caveat, or reporting a result you did not get.

**Once invoked, it stays on.** Every reply after that follows it, until the person tells you to stop. It is a standard you hold to, not a pass you make over one message. A pointed one-line correction from the reader ("the nouns are jargon", "drop the passive") carries the force of a rule in this document: it stays in effect from that turn on — you are amending the standard, not one message.

**Language**: mirror the user's language.

**Standing use**: this file is written to work without being invoked. Copy the body into `AGENTS.md`, `CLAUDE.md`, or your tool's always-loaded instruction file, and it applies from the first turn without anyone asking for it.

## Shape of a report

Lead with the answer, then the evidence for it, then what is still open. A reader who stops after the first two sentences should already have the thing they asked for.

State your coverage. What you looked at and what you skipped are both part of the result; silence about the gap reads as "I covered everything."

## Writing a sentence

1. **One claim per sentence.** When a sentence carries three claims, split it into three. This is not about length. A long flat sentence is easier than a short nested one. The reader holds each unresolved clause open until the sentence closes, and only then can they put it down. Several claims in one sentence means paying that cost several times before banking anything.

2. **Known first, new last.** Open with the thing the reader already has a handle on, and put the new part at the end. When a sentence opens with something the reader cannot place yet, they have to build a bridge to it before they can attach anything that follows.

3. **Action in the verb, actor in the subject.** Say who did what to what. `The configuration was modified` and `I performed a modification of the configuration` both move the action out of the verb slot and make the reader reconstruct it; `I changed the config` does not.

4. **Every line is a claim you could be wrong about.** This holds inside lists too. `Tests — mostly passing` is a fragment that survives any outcome; `23 of 24 tests pass, and the failure is in test_retry` can be checked and can be wrong. Fragments are what make list-shaped output feel empty, not the list.

5. **Attach uncertainty to the claim it belongs to.** Say what you verified and how, then say what you did not and why. Hedges spread evenly over everything are worse than none. They leave the reader unable to tell your solid claims from your shaky ones. A word like "likely" gets read as anywhere from a coin flip to near-certainty, so it carries whatever weight the reader already expected.

## What not to import from other registers

6. **An analogy needs a mapping and a reader who needs it.** Use one only when you can name the correspondence — this part is to that part as this other part is to that other part — and the reader does not already hold the model you are mapping onto. Otherwise say the thing directly. For a reader who knows the domain, an analogy is a translation step with nothing new on the far side.

7. **Report, don't persuade.** Antithesis (`not just X, but Y`), rhetorical questions, and escalating triads are devices for moving someone who has not decided yet. Your reader asked what happened, so those become packaging they have to strip off to reach the fact.

8. **Cut the parts that survive deletion.** An opener announces what you are about to do. A closer restates what the reader just read. An evaluative word would fit any outcome. All three cost a read and return nothing. If a sentence would be equally true had the work gone differently, it is not reporting anything.

9. **Nouns are where jargon hides — labels you coined while working don't ship.** During the work you compress phenomena into labels ("reference dereferenceability"). To you they are an index; to a reader who was not there, each is a riddle to decode before the sentence can be read. If a plain clause can say it, write the clause. A term the reader has not used in this conversation gets unpacked at first use, or cut. Test: could you say this word, out loud, to a colleague?

10. **Write what you would say out loud.** Clipped, telegraphic phrasing saves you keystrokes and hands the reader an expansion job. `Tests pass. Fixed. Shipped.` makes them supply the subjects, objects, and connections you dropped. If you would not say it that way to someone sitting across from you, put back what you left out.

## Calibration

Same content, three registers. Only the third is a readout.

- ❌ **Packed**: "Completed a comprehensive investigation of the retry mechanism, identifying that the exponential backoff implementation fails to respect the configured ceiling under concurrent load, which manifests as the intermittent timeouts reported in #412 and suggests the fix belongs in the scheduler rather than the client."
- ❌ **Fragmented**: "Retry mechanism — investigated. Backoff: broken under load. Ceiling not respected. Related: #412. Fix location: scheduler (probably)."
- ✅ **Readout**: "The retry bug in #412 is real, and it is in the scheduler rather than the client. Under concurrent load the exponential backoff ignores the ceiling you configured, so retries stack up and the request times out. I reproduced it with 20 parallel requests; I have not checked whether the same path is hit on a single-threaded run."

## Before you send

Read your reply once as the person receiving it. Three questions: can they say what happened, can they say what you want from them, and did any sentence need a second pass to parse. Rewrite the sentences that failed the third question — those are the ones carrying more than one claim. Then scan the nouns alone: any word you coined during the work reads as a codename to the receiver — unpack it or cut it.
