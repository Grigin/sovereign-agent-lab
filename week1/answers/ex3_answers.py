"""
Exercise 3 — Answers
====================
Fill this in after completing the three Rasa conversations.

CALM vs Old Rasa — what changed
---------------------------------
The old open-source Rasa approach used:
  - nlu.yml: intent training examples
  - rules.yml: explicit dialogue rules
  - FormValidationAction: Python class to parse slot values

Rasa Pro CALM uses:
  - flows.yml: natural language descriptions of what each flow does
  - from_llm slots: the LLM extracts values from conversation
  - ONE custom action: ActionValidateBooking for the business rules

The conversation is the same from the manager's perspective.
The machinery underneath is completely different.

CONVERSATION SCRIPTS
---------------------
Conversation 1 (happy path):
  You:    calling to confirm a booking
  Agent:  [asks guest count]
  You:    160 guests
  Agent:  [asks vegan count]
  You:    about 50 need vegan
  Agent:  [asks deposit]
  You:    £200 deposit
  Agent:  [confirms or escalates?]

Conversation 2 (deposit too high):
  Same as above but use a deposit above £300 (e.g. "£500 deposit").

Conversation 3 (out of scope):
  Start normally, then when asked for vegan count say something like
  "can you arrange parking for the speakers?" and observe what happens.
  Does CALM handle this differently than the old rules approach?
"""

# ── Conversation 1: Happy path ─────────────────────────────────────────────

CONVERSATION_1_TRACE = """
Bot loaded. Type a message and press enter (use '/stop' to exit):
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £200 deposit
Thank you — booking confirmed. 160 guests, 50 requiring vegan meals, £200 deposit accepted. I'll send written confirmation to the organiser shortly.
Is there anything else I can help you with?
Your input ->  /stop
"""

CONVERSATION_1_OUTCOME = "confirmed"

# ── Conversation 2: Deposit too high ───────────────────────────────────────

CONVERSATION_2_TRACE = """
Bot loaded. Type a message and press enter (use '/stop' to exit):
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  about 50 need vegan
What deposit amount in GBP are you proposing to secure the booking?
Your input ->  £500 deposit
I need to check one thing with the organiser before I can confirm. The issue is: a deposit of £500 exceeds the organiser's authorised limit of £300. Can I call you back within 15 minutes?
Is there anything else I can help you with?
Your input ->  /stop
"""

CONVERSATION_2_OUTCOME = "escalated"
CONVERSATION_2_REASON  = "a deposit of £500 exceeds the organiser's authorised limit of £300"

# ── Conversation 3: Out of scope ───────────────────────────────────────────

CONVERSATION_3_TRACE = """
Bot loaded. Type a message and press enter (use '/stop' to exit):
Your input ->  calling to confirm a booking
How many guests are you confirming for tonight's event?
Your input ->  160 guests
And how many of those guests will need vegan meals?
Your input ->  can you arrange parking for the speakers?
I'm sorry, I'm not trained to help with that.
I can only help with confirming tonight's venue booking. For anything else, please contact the event organiser directly.
Would you like to continue with confirm booking?
Your input ->  /stop

(Note: an earlier attempt typed the parking message before the previous bot
 reply had finished printing, which the Rasa shell logged as an empty input;
 the cleaned trace above shows the same exchange after the shell caught up.)
"""

# Describe what CALM did after the out-of-scope message. Min 20 words.
CONVERSATION_3_WHAT_HAPPENED = """
CALM did not attempt to extract a number from the parking message or interpret it as a vegan count. 
It detected the off-topic -> routed to the handle_out_of_scope flow. Then the LLM matched semantically
against that flow description in flows.yml (which actualy lists "parking" as an example). 
The active confirm_booking flow was paused (but not lost!), the bot responded with deflection message: "I can only help
  with confirming tonight's venue booking" and then offered to resume the original flow with "Would you like to continue with confirm booking?". 
State was preserved throughout (guest_count=160 was saved).
"""

# Compare Rasa CALM's handling of the out-of-scope request to what
# LangGraph did in Exercise 2 Scenario 3. Min 40 words.
OUT_OF_SCOPE_COMPARISON = """
Both agents refused to hallucinate and didn't go rogue, neither made a wrong tool call/invented an answer.  
They reached that outcome in opposite ways however. LangGraph improvised: model reasoned through the tools,
 found no match and then drew on training-time parametric knowledge to recommend apps and operators before pivoting forward. 
CALM did none of that run-around reasonign. It directly matched the parking question against a pre-declared handle_out_of_scope flow description in flows.yml,
then paused the active confirm_booking flow without losing the slot values it already collected, provided a hardcoded response from domain.yml 
+ offered to resume the original task. 

Again, CALM's reply is auditable and predictable; LangGraph's is helpful yet unpredictable. 
Each is correct for its usecase. LangGraph's improvisation is what you'd want from a research assistant,
and CALM's rigidity is what we want from a confirmation agent that must not recommend anything that stakeholder
(in our case Prof. Rod) hasn't authorised.
"""

# ── Task B: Cutoff guard ───────────────────────────────────────────────────

TASK_B_DONE = True

# List every file you changed.
TASK_B_FILES_CHANGED = ["exercise3_rasa/actions/actions.py"]

# How did you test that it works? Min 20 words.
TASK_B_HOW_YOU_TESTED = """
I ran the same conversation as Conversation 1 (a happy-path book with 160 guests, 50 vegan, £200 deposit), 
which previously confirmed under all three original guards.  With cutoff guard now active and the system clock at 23:40,
the same inputs triggered an escalation as expected.
"""

# ── CALM vs Old Rasa ───────────────────────────────────────────────────────

# In the old open-source Rasa (3.6.x), you needed:
#   ValidateBookingConfirmationForm with regex to parse "about 160" → 160.0
#   nlu.yml intent examples to classify "I'm calling to confirm"
#   rules.yml to define every dialogue path
#
# In Rasa Pro CALM, you need:
#   flow descriptions so the LLM knows when to trigger confirm_booking
#   from_llm slot mappings so the LLM extracts values from natural speech
#   ONE action class (ActionValidateBooking) for the business rules
#
# What does this simplification cost? What does it gain?
# Min 30 words.

CALM_VS_OLD_RASA = """
LLM took over three things that Python used to handle: slot parsing (from_llm replaces regex validate_* methods) / intent triggering (flow descriptions replace nlu.yml examples and a classifier) /
 and dialogue routing (linear steps: replace rules.yml). 
 
 What stayed in Python are the business rules: ActionValidateBooking is identical to the old version. 
 
 That separation looks deliberate: language is handled by the LLM because it's flexible, but anything binding (deposit ≤ £300, capacity ≤ 170) stays in deterministic Python route. 
 The gain is much less boilerplate -> natural-language slot extraction + easier-to-read flows. 
 The costs: an LLM call on every turn (that is money + latency + a 3rd party dependency), a Rasa license 
 + Possibly we are losing the bit-for-bit determinism of regex slot parsing as the LLM might mis-extract a number under unusual phrasing in a way regex wouldn't.
"""

# ── The setup cost ─────────────────────────────────────────────────────────

# CALM still required: config.yml, domain.yml, flows.yml, endpoints.yml,
# rasa train, two terminals, and a Rasa Pro licence.
# The old Rasa ALSO needed nlu.yml, rules.yml, and a FormValidationAction.
#
# CALM is simpler. But it's still significantly more setup than LangGraph.
# That setup bought you something specific.
# Min 40 words.

SETUP_COST_VALUE = """
The setup is heavier than LangGraph's three lines but it buys us transparency:
I can read flows.yml and domain.yml and understand exactly what the agent can do without even running it. 
CALM can't improvise like the LangGraph agent did in Ex2 with the LNER recommendation,
 that improvisation is great for research but bad for a confirmation call where the model could accidentally promise something Rod didn't authorise. 
The setup with license, the training and two terminals, doesn't  make CALM smarter but it bounds what it can do. 
And this is the whole point for this use case.
"""
