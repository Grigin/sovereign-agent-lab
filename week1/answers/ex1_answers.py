"""
Exercise 1 — Answers
====================
Fill this in after running exercise1_context.py.
Run `python grade.py ex1` to check for obvious issues before submitting.
"""

# ── Part A ─────────────────────────────────────────────────────────────────

# The exact answer the model gave for each condition.
# Copy-paste from your terminal output (the → "..." part).

PART_A_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_A_XML_ANSWER      = "The Albanach"
PART_A_SANDWICH_ANSWER = "The Albanach"

# Was each answer correct? True or False.
# Correct = contains "Haymarket" or "Albanach" (both satisfy all constraints).

PART_A_PLAIN_CORRECT    = True
PART_A_XML_CORRECT      = True
PART_A_SANDWICH_CORRECT = True

# Explain what you observed. Minimum 30 words.

PART_A_EXPLANATION = """From the results produced, I observe that all three calls to the model returned correct answers. 
Plain prompt variant picked Haymarket and the rest picked Albanach, both of which are acceptable answers for this task. 
The format of the prompt didn't affect correctness, but it seems to demonstrate primacy bias at work, as the XML/SANDWICH produced a shift in answer (probably because of explicitly encoded ids in xml tags).
The takeaway from this is that the format alteration changed which valid answer was surfaced, but accuracy stayed the same and the Liu et al. effect wasn't observed.
"""

# ── Part B ─────────────────────────────────────────────────────────────────

PART_B_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_B_XML_ANSWER      = "The Albanach"
PART_B_SANDWICH_ANSWER = "The Albanach"

PART_B_PLAIN_CORRECT    = True
PART_B_XML_CORRECT      = True
PART_B_SANDWICH_CORRECT = True

# Did adding near-miss distractors change any results? True or False.
PART_B_CHANGED_RESULTS = False

# Which distractor was more likely to cause a wrong answer, and why?
# Minimum 20 words.
PART_B_HARDEST_DISTRACTOR = """
I believe the hardest distractor is the Holyrood Arms and for two reasons: it satisfies 2 out of 3 conditions required,
and its failure mode (status=full) is a third check the model has to remember to make, after it already feels like it's found a winner,
which is more challenging compared to New Town Vault which "fails" the check on earlier constraint (vegan options)
Additionally Holyrood Arms is directly above the Haymarket option in the input list, which can cause attention 'blur'.
"""

# ── Part C ─────────────────────────────────────────────────────────────────

# Did the exercise run Part C (small model)?
# Check outputs/ex1_results.json → "part_c_was_run"
PART_C_WAS_RUN = True

PART_C_PLAIN_ANSWER    = "The Haymarket Vaults"
PART_C_XML_ANSWER      = "The Haymarket Vaults"
PART_C_SANDWICH_ANSWER = "The Haymarket Vaults"

# Explain what Part C showed, or why it wasn't needed. Minimum 30 words.
PART_C_EXPLANATION = """
Part C was triggered because A and B were both all-correct on 70B model calls, so it was natural to drop down to the smaller 8B.
The results produced are still all correct, but this time more consistent, The Haymarket Vaults was returned on all three counts,
meaning that the prompt changes didn't affect the model decisions this time. The Liu et al. effect didn't appear because the dataset is small and clean
(9 venues, 3 simple constraints) and even an 8B parameter model from 2024 is stronger than the GPT-3.5 used in the original paper.
The SNR is too high and the model has too much headroom for format to be the deciding factor. Honest caveat case.
"""

# ── Core lesson ────────────────────────────────────────────────────────────

# Complete this sentence. Minimum 40 words.
# "Context formatting matters most when..."

CORE_LESSON = """Context formatting matters most when the task is genuinely hard for the model: long contexts with the answer buried mid-prompt, multi-constraint reasoning where shortcut-matching would fail, 
or smaller models lacking headroom. On easy tasks the structure is overhead -> extra tokens for no accuracy gain, and a possible source of position bias.
"""
