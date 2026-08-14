---
name: just-ask
description: One-shot answer-only turn — the user is asking a question, not assigning work. Invoked as /just-ask with the question attached (e.g. "/just-ask why does this test flake"). For that turn only, investigate read-only and reply with an analyzed answer; do not edit files, run state-changing commands, write a plan, or start a fix. The next message returns to normal. Meant for explicit invocation; also applies when the user says "just answer, don't do anything", "just explain, don't fix it".
metadata:
  short-description: One-shot answer-only question
---

# just-ask — a question, not a work order

This skill compresses a prompt the user is tired of typing: "I'm only asking — investigate and answer; don't touch anything." It exists because an agent deep in a working context tends to treat every message as the next task, and starts fixing what the user only wanted explained.

## Scope: exactly one turn

It covers the turn it is invoked with, and nothing after. Once the answer is sent, the skill is spent; read the next message normally, with no mode to announce or exit.

Invoked bare, with no question attached: reply with one line asking for the question, and treat the next message as that question — still one turn.

## What the turn is

The deliverable is an answer — analyzed, grounded in what you actually looked at. The user wants to understand something, not to have it acted on.

The question is not an instruction, however much dissatisfaction it implies. "Why is this function so slow?" wants the reason, not an optimization. If you think the fix is obvious, that belief goes into the answer as a sentence, not into the files as an edit.

If other work was in flight in this conversation, do not advance it this turn, and do not silently fold the question's implications back into that work ("so I'll change the approach"). Answer, then end the turn; the user's next message decides what happens to the task.

## What you may and may not do

Allowed: reading files, searching, read-only commands (`git log`, `git diff`, `ls`, `grep`), read-only subagents. Investigate as much as the question deserves — read-only does not mean answer from memory.

Not allowed: editing or creating files, state-changing commands, creating tasks or todo lists, entering plan mode, or staging a fix "while you're in there".

If settling the answer truly requires a mutation — running the build, applying a candidate patch to test it — do not do it. Give the best answer the read-only evidence supports, say how confident you are and why, and name the one command or change that would settle it, for the user to run or approve.

## Shape of the answer

Lead with the answer, then the evidence, then what is still uncertain. State what you looked at and what you skipped.

No "next steps" section, no plan awaiting approval. You may end with at most one short line offering to act ("say the word and I'll fix it"); never with a plan.

**Language**: mirror the user's language.
