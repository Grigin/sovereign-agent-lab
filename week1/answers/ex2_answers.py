"""
Exercise 2 — Answers
====================
Fill this in after running exercise2_langgraph.py.
Run `python grade.py ex2` to check for obvious issues.
"""

# ── Task A ─────────────────────────────────────────────────────────────────

# List of tool names called during Task A, in order of first appearance.
# Look at [TOOL_CALL] lines in your terminal output.
# Example: ["check_pub_availability", "get_edinburgh_weather"]

TASK_A_TOOLS_CALLED = [
    "check_pub_availability",
    "calculate_catering_cost",
    "get_edinburgh_weather",
    "generate_event_flyer",
]

# Which venue did the agent confirm? Must be one of:
# "The Albanach", "The Haymarket Vaults", or "none"
TASK_A_CONFIRMED_VENUE = "The Albanach"

# Total catering cost the agent calculated. Float, e.g. 5600.0
# Write 0.0 if the agent didn't calculate it.
TASK_A_CATERING_COST_GBP = 5600.0

# Did the weather tool return outdoor_ok = True or False?
TASK_A_OUTDOOR_OK = False

TASK_A_NOTES = r"""The agent only checked The Albanach, not The Haymarket Vaults.
The prompt says "Check The Albanach and The Haymarket Vaults. If one works, calculate catering...",
and Qwen3-32B interpreted "if one works" as a stopping condition: it checked Albanach first, saw it satisfied all constraints,
and moved straight on to catering without ever calling check_pub_availability for Haymarket.
Also, the model's internal reasoning is visible as <think>...</think> blocks in every AI message.
Qwen3-32B is a thinking-style model, so the trace exposes its chain-of-thought rather than just final decisions."""

# ── Task B ─────────────────────────────────────────────────────────────────
#
# The scaffold ships with a working generate_event_flyer that has two paths:
#
#   - Live mode: if FLYER_IMAGE_MODEL is set in .env, the tool calls that
#     model and returns a real image URL.
#   - Placeholder mode: otherwise (the default) the tool returns a
#     deterministic placehold.co URL with mode="placeholder".
#
# Both paths return success=True. Both count as "implemented" for grading.
# This is not the original Task B — the original asked you to write a direct
# FLUX image call, but Nebius removed FLUX on 2026-04-13. See CHANGELOG.md
# §Changed for why we pivoted the task.

# NOTE: Week 1 was submitted before the upstream v1.1.0 patch reframed
# Task B around the FLUX deprecation (2026-04-13). The fields below
# (TASK_B_MODE, TASK_B_IMAGE_URL, TASK_B_WHY_AGENT_SURVIVED) didn't exist
# in the version graded. The values below reconstruct the original live
# run; they're not re-filled because the submission is locked.

# Did your run of the flyer tool produce a success=True result?
# (This will be True for both live and placeholder mode — both are valid.)
TASK_B_IMPLEMENTED = True

# Which path did your run take? "live" or "placeholder"
# Our original run hit the live Nebius FLUX endpoint before the
# 2026-04-13 deprecation, so this was "live" at submission time.
TASK_B_MODE = "live"

# The image URL returned by the tool — the real Nebius CDN URL from
# the original live run (pre-deprecation).
TASK_B_IMAGE_URL = "https://pictures-storage.storage.eu-north1.nebius.cloud/text2img-1485eb73-fdd0-49be-bda2-2b86300fd9ed_00001_.webp"

# The prompt sent to the image model. Copy from terminal output.
TASK_B_PROMPT_USED = "Professional event flyer for Edinburgh AI Meetup, tech professionals, modern venue at The Haymarket Vaults, Edinburgh. 160 guests tonight. Warm lighting, Scottish architecture background, clean modern typography."

# Why did the agent's behaviour NOT change when Nebius removed FLUX?
# One sentence. This is the point of the lesson.
# (Retrofitted answer — this field didn't exist when Week 1 was submitted.)
TASK_B_WHY_AGENT_SURVIVED = """
The tool's contract (a success=True dict with prompt_used and image_url) stayed identical across the deprecation, so the ReAct loop never noticed that the underlying provider had been swapped out for a deterministic placeholder.
"""

# ── Task C ─────────────────────────────────────────────────────────────────

# Scenario 1: first choice unavailable
# Quote the specific message where the agent changed course. Min 20 words.
SCENARIO_1_PIVOT_MOMENT = """
The pivot occurred after check_pub_availability returned meets_all_constraints: false for The Bow Bar (capacity 80 < 160 and full).
In the next AI message the agent reasoned "the user's instruction was to check The Bow Bar first, and if it doesn't meet the requirements, check any other available venue"
and then immediately called check_pub_availability again for The Albanach. Nothing in the prompt named Albanach as a fallback, the agent picked it from its own memory of known venues.
"""

SCENARIO_1_FALLBACK_VENUE = "The Albanach"

# Scenario 2: impossible constraint (300 guests)
# Did the agent recommend a pub name not in the known venues list?
SCENARIO_2_HALLUCINATED = False

# Paste the final [AI] message.
SCENARIO_2_FINAL_ANSWER = """
None of the four known Edinburgh venues (The Albanach, The Haymarket Vaults, The Guilford Arms, The Bow Bar) can accommodate 300 people while meeting all requirements. The maximum capacity among them is 200 at The Guilford Arms, but it lacks vegan options. All venues either have insufficient capacity (max 200) or don't meet the dietary requirements. You would need to consider alternative venues outside this predefined list.
"""

# Scenario 3: out of scope (train times)
# Did the agent try to call a tool?
SCENARIO_3_TRIED_A_TOOL = False

SCENARIO_3_RESPONSE = """I don't have access to real-time train schedules or transportation data. For the most accurate information about the last train from Edinburgh Waverley to London, I recommend checking:
1. The National Rail website (www.nationalrail.co.uk)
2. Train service apps like Citymapper or Trainline
3. The specific train operator's website (e.g., LNER)

Would you like help with anything related to Edinburgh pubs, weather, or event planning instead?"""

# Would this behaviour be acceptable in a real booking assistant? Min 30 words.
SCENARIO_3_ACCEPTABLE = """
 Yes, this is acceptable and arguably a very nice response for a real booking assistant.
 Agent didn't hallucinate a train schedule, didn't waste time / api call on an irrelevant tool.
 Recognised the request was outside its scope -> told the user honestly -> redirected them to three concrete external sources,
 and pivoted back to offering help with what it actually can do. The only mild concern is recommending specific third-party services
 (in case some are stale/hallucinated or require partnership) but on this occasion the recommendations are spot on.
"""

# ── Task D ─────────────────────────────────────────────────────────────────

# Paste the Mermaid output from `python exercise2_langgraph.py task_d` here.
TASK_D_MERMAID_OUTPUT = """
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	agent(agent)
	tools(tools)
	__end__([<p>__end__</p>]):::last
	__start__ --> agent;
	agent -.-> __end__;
	agent -.-> tools;
	tools --> agent;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
"""

# Compare the LangGraph graph to exercise3_rasa/data/flows.yml. Min 30 words.
TASK_D_COMPARISON = """
The LangGraph Mermaid output is trivial and small. Four nodes (start, agent, tools, end) + a self-loop between agent and tools.
It tells us about nothing about which tools exist or in what order they'll be called; everything is decided by the model at runtime.
Rasa's flows.yml is the exact opposite: every flow is declared explicitly + every step is named + fixed slot collection order
+ the validation logic runs in Python as a deterministic action.

These two describe the same kind of system but in completely opposite ways. LangGraph is flexible but opaque,
the only way to know what the agent did is to read a trace after it ran. Rasa CALM is rigid but auditable.
You can read the flow file in code review and know every possible path the conversation can take.
The trade-off matches our assignment's "Headless Automator vs Digital Employee":
 LangGraph is right when the path can't be predetermined; Rasa's CALM is right when we must guarantee every step.
"""

# ── Reflection ─────────────────────────────────────────────────────────────

# The most unexpected thing the agent did. Min 40 words.
# Must reference a specific behaviour from your run.

MOST_SURPRISING = """
The most unexpected behaviour came from Task C Scenario 3, where we asked about train times.
 Instead of a plain "I can't help with that," the agent went considerably further: it explicitly named
  National Rail (with a website url), Trainline, Citymapper, and LNER as concrete places to look.
 The LNER mention specifically is commendable! that's the actual operator on the Edinburgh-Waverley to London route,
 which means the model isn't just listing generic transport apps; it's drawing on training-time domain knowledge about the specific journey to
  make the recommendation useful. There's no tool that exposes operator information nor did we prompt it to say that,
  so this came entirely from the model's parametric knowledge.
"""
