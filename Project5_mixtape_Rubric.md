# Project 5: Mixtape Bug Hunt

## Total Points
**25 pts + 3 pts Bonus**

---

# Required Features

## 3 pts — Codebase Map

### 1 pt
Map identifies at least the main files and their roles — not just file names, but what each one does.

### 1 pt
Map describes the data flow for at least one feature (e.g., how sharing a song triggers a notification, or how the feed is populated).

### 1 pt
Map reads as if it was written before bug work — it describes the app's architecture, not the bugs.

---

## 4 pts — Bug Fix Completeness

### 2 pts
3 or more root cause analysis entries are present, each covering all 5 required fields:

- Reproduction steps
- Navigation strategy
- Root cause explanation
- Fix description
- Side-effect check

### 1 pt
Each entry is substantive — a grader who hasn't seen the codebase could understand what went wrong and why from reading the entry alone.

### 1 pt
The submission document is organized so entries are clearly associated with specific issue numbers.

---

## 5 pts — Root Cause Quality

### 2 pts
At least 3 root cause explanations identify a specific condition, comparison, function, or logic error — not just "the code was wrong here" or a restatement of the bug report.

### 2 pts
At least 2 explanations name a specific function or variable and explain the mechanism: why that specific thing caused the reported behavior under the specific conditions it manifested (e.g., "only on Sundays," "only for songs with multiple tags").

### 1 pt
At least one explanation demonstrates causal reasoning — it explains not just what was wrong but why the correct behavior requires something different.

---

## 4 pts — Navigation Strategy

### 2 pts
At least 3 entries describe a real navigation path: which files were looked at, what was followed (a function call, a query, a data flow), and what moment made the student confident they'd found the root cause.

### 2 pts
The strategies described reflect deliberate exploration, not a lucky first guess. The entries show the student tracing a path, not just arriving at an answer.

---

## 3 pts — Side-Effect Check

### 2 pts
At least 3 entries describe a specific, deliberate check — what related functionality was looked at after the fix to confirm it wasn't affected, and why that check was sufficient.

### 1 pt
At least one entry describes a check that goes beyond "the app still ran" — it identifies a specific behavior or code path that could plausibly have been affected by the fix and confirms it wasn't.

---

## 3 pts — Commit History

### 1 pt
Screenshot or commit history shows commits on the `bugfix/mixtape` branch (not just the original forked state).

### 1 pt
At least 3 separate commits are visible, each corresponding to one bug fix — not all fixes bundled into a single commit.

### 1 pt
Commit messages use conventional commit format (`fix:` prefix) and are specific enough to identify which bug was fixed without reading the code.

---

## 3 pts — AI Usage

### 1 pt
Section describes at least 2 specific uses of AI tools during codebase navigation or debugging — what was asked and what the tool helped explain or trace.

### 1 pt
Section is honest about the collaboration — describes at least one instance where the student verified something the AI explained, or where the AI's output was incomplete and the student had to course-correct.

### 1 pt
Descriptions are specific enough to distinguish real AI collaboration from generic statements like "I used AI to help with code."

---

# Stretch Features

## +1 pt — Fix a 4th Bug

A complete root cause analysis entry is present for a 4th bug, covering all 5 required fields with the same quality expected of the 3 required entries.

A separate commit for this fix is visible in the git log screenshot.

---

## +1 pt — Fix All 5 Bugs

All 5 bugs have complete root cause analysis entries.

5 separate commits are visible in the git log screenshot.

(Requires the stretch feature above.)

---

## +1 pt — Regression Test

A test is present in the repository that would have caught at least one of the fixed bugs before it was introduced.

The submission document references the test and briefly explains:

- What behavior it verifies
- Why that test would have failed against the buggy code
