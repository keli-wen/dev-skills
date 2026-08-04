---
name: ctx-grill
description: Stress-test a plan, decision, or idea with a context-aware interview. Use for /ctx-grill, "grill this plan", "stress-test this plan", or when the user wants their thinking stress-tested before committing. Reads durable contexts first (never asks what they answer), asks direction-changing questions one at a time with a recommended answer, stops at diminishing returns, and files resolved decisions back. Interactive only — never invoke under CI, loops, or other non-interactive runs.
metadata:
  short-description: Context-aware plan grilling
---

# ctx-grill

An interview that sharpens a plan until we reach shared understanding. It differs from generic grilling in three ways: existing contexts are read before any question is asked, questions are ranked by whether the answer would change the plan's direction, and resolved decisions are written back so they are never asked again. The interview engine is adapted from `grilling` in [mattpocock/skills](https://github.com/mattpocock/skills) (MIT).

**Language**: mirror the user's language.

## Steps

1. **Ground**: read the context entries relevant to this plan. Sort what they settle into: already decided (never ask — cite the file), assumed but unverified (confirm cheaply), genuinely open (the question pool).
2. **Interview**: walk down each branch of the decision tree, resolving dependencies between decisions one by one. Ask the questions one at a time, waiting for feedback on each before continuing — asking multiple questions at once is bewildering. For each question, provide your recommended answer and a rough confidence. If a *fact* can be found by exploring the environment (filesystem, tools, docs), look it up rather than asking. The *decisions* are the user's — put each one to them and wait.
3. **Rank as you go**: take branches in order of "would the answer change the plan's direction"; within a branch, follow dependency order. Re-rank after each answer — an answer can reshape the tree.
4. **Stop at diminishing returns**: when no remaining question would change the plan's direction, stop. Name what was left unasked and why it is safe to defer — do not grind every branch to the bottom.
5. **Write back**: file one-way or durable decisions with `/to-ctx` the moment they resolve; batch the small ones at the end. Close with the sharpened plan, the decisions filed, and the open items deferred.

## Rules

- Do not act on the plan until the user confirms we have reached a shared understanding.
- Never ask what contexts already answer; cite the context file instead.
- Interactive only: if the session cannot receive answers (CI, loops, background runs), refuse and say why.
- Dependency direction: may use `/to-ctx`; never invokes user-facing skills.
