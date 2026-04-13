"""
Exercise 4 — Answers
====================
Fill this in after running exercise4_mcp_client.py.
"""

# ── Basic results ──────────────────────────────────────────────────────────

# Tool names as shown in "Discovered N tools" output.
TOOLS_DISCOVERED = ["search_venues", "get_venue_details"]

QUERY_1_VENUE_NAME    = "The Haymarket Vaults"
QUERY_1_VENUE_ADDRESS = "1 Dalry Road, Edinburgh"
QUERY_2_FINAL_ANSWER  = "There are currently no Edinburgh venues available that can accommodate 300 people, even without requiring vegan options."

# ── The experiment ─────────────────────────────────────────────────────────
# Required: modify venue_server.py, rerun, revert.

EX4_EXPERIMENT_DONE = True

# What changed, and which files did or didn't need updating? Min 30 words.
EX4_EXPERIMENT_RESULT = """
Had to change one line in mcp_venue_server.py (Albanach status: available -> full) and then re-ran the script. 
Query 1's search_venues went from returning 2 matches (Albanach + Haymarket) to 1 (Haymarket).
Server filtered Albanach out correctly because it was no longer available. 
Query 2 was unchanged (no venue fits 300 guests). 
The client code and agent code stayed as is, data change propagated to the agent's behaviour purely through the MCP tool layer.
"""

# ── MCP vs hardcoded ───────────────────────────────────────────────────────

LINES_OF_TOOL_CODE_EX2 = 6   # count in exercise2_langgraph.py
LINES_OF_TOOL_CODE_EX4 = 37  # count in exercise4_mcp_client.py

# What does MCP buy you beyond "the tools are in a separate file"? Min 30 words.
MCP_VALUE_PROPOSITION = """
The most important gain is the dynamic tool discovery, instead of pre-setting tools list when creating context on startup,
with MCP we call list_tools() at runtime and because it wraps whatever server exposes this means we can add new tools
to mcp and they instanlty become available in the agent.

In general MCP decouples the runtime: our server can serve at same time all of: LangGraph agent / Rasa action / and a CLI script over the same protocol, without them sharing a Python env or package path.
"""

# ── Week 5 architecture ────────────────────────────────────────────────────
# Describe your full sovereign agent at Week 5 scale.
# At least 5 bullet points. Each bullet must be a complete sentence
# naming a component and explaining why that component does that job.

WEEK_5_ARCHITECTURE = """
 - The MCP server acts as the shared tool layer because both agents discover and call the same tools via standardised anthropic's mcp protocol,
  meaning venue data changes propagate to all clients without us having to redeploy any agent code.
 - Planner-executor model uses a strong reasoning model (DeepSeek R1) for task decomposition and a faster model (Llama 70B) for tool execution,
so we optimise both for efficiency/response speed and quality of decisions of our agent.
 - Vector store + session memory let the research agent recall past bookings, failed venues, and user preferences across sessions
  so it doesn't waste tool calls to rediscover info it already has.
 - Observability and cost tracking for every LLM query, tool call, and token count -> 
 operators can monitor spend, debug failures, and audit the agent's traces chain.
 - Safety guardrails filter agent outputs before they reach users, 
 preventing the system from making commitments or recommendations that weren't authorised by us.
"""

# ── The guiding question ───────────────────────────────────────────────────
# Which agent for the research? Which for the call? Why does swapping feel wrong?
# Must reference specific things you observed in your runs. Min 60 words.

GUIDING_QUESTION_ANSWER = """
 The LangGraph research agent (the headless automator) handles open-ended venue search, planning, and cost estimation 
 because it can reason through unknowns and call tools in whatever order it decides at runtime, 
 as we saw in Ex2 when it autonomously skipped Haymarket after confirming Albanach. 
 Rasa CALM agent handles structured high-stakes calls with pub managers 
 because every dialogue step is declared in flows.yml and business constraints (deposit limits, capacity ceilings) are
 enforced in deterministic Python that the LLM cannot override, as we saw in Ex3.
 Swapping them is obviously dangerous, because then we have an agent that we've observed improvises quite well
 in novel situations, so letting it get creative with payments and budgets is a dangerous idea. Vice a versa, CALM is
 too constrained, so it's not going to be of any benefit in research, when it only follows rails. 
  
"""
