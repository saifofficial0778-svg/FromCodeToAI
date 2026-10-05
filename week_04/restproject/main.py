r"""
Restaurant order-management agent built with LangGraph.

Flow
----
START -> get_input -> parse_input --(unrelated)--> handle_unrelated
                          |
                          v
                    order_confirm --(CONFIRMED)--> cook --(READY)--> serve --(COMPLETE)--> end_success
                          |                          ^  \                  |
                (PARTIAL / UNAVAILABLE)              |   (fail, retries)    (fail, retries left) -> cook
                          v                          |
                    handle_shortfall -> ask_decision / get_input
Any exhausted retry counter -> end_failure (LLM apology) -> END

Run interactively:   python restaurant_agent.py
Requires:            pip install langgraph langchain-groq python-dotenv
Env (.env):          GROQ_API_KEY=...   (model: openai/gpt-oss-120b)
"""
from __future__ import annotations

import json
import os
import random
from typing import Annotated, Literal, Optional, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

# --------------------------------------------------------------------------- #
# Config / menu
# --------------------------------------------------------------------------- #
MENU: dict[str, int] = {  # dish -> quantity currently available
    "pizza": 5,
    "pasta": 3,
    "burger": 2,
    "salad": 0,  # on the menu but out of stock
}

COOK_SUCCESS_PROB = 0.6   # 60% success / 40% fail
SERVE_SUCCESS_PROB = 0.6  # not specified in the brief -> assumed same as cook

MAX_ORDER_RETRIES = 3
MAX_COOK_RETRIES = 2
MAX_SERVE_RETRIES = 2


# --------------------------------------------------------------------------- #
# State
# --------------------------------------------------------------------------- #
class OrderState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]  # user + LLM conversation
    dish_name: str
    required_quantity: int
    available_quantity: int          # written by order_confirm from MENU
    status: str                      # see STATUS values below
    order_retries: int               # starts at 3
    cook_retries: int                # starts at 2
    serve_retries: int               # starts at 2
    final_result: str                # "" | "COMPLETED" | "FAILED"


# status values:
#   PENDING, UNRELATED, CONFIRMED, PARTIAL, UNAVAILABLE   (order stage)
#   READY, COOK_FAILED                                    (cook stage)
#   SERVE_FAILED, COMPLETE                                (serve stage)
#   FAILED                                                (gave up)


def initial_state() -> OrderState:
    return OrderState(
        messages=[],
        dish_name="",
        required_quantity=0,
        available_quantity=0,
        status="PENDING",
        order_retries=MAX_ORDER_RETRIES,
        cook_retries=MAX_COOK_RETRIES,
        serve_retries=MAX_SERVE_RETRIES,
        final_result="",
    )


# --------------------------------------------------------------------------- #
# LLM layer (pluggable so tests can run offline)
# --------------------------------------------------------------------------- #
class ParsedOrder(BaseModel):
    intent: Literal["order", "unrelated"] = Field(
        description="'order' if the user is trying to order food, else 'unrelated'")
    dish: str = Field(default="", description="Dish name, lowercase. Empty if unrelated.")
    quantity: int = Field(default=0, description="Requested quantity. 0 if unrelated.")


class ParsedDecision(BaseModel):
    decision: Literal["accept", "reorder", "reject"] = Field(
        description="accept = user wants to go ahead with the partial order; "
                    "reorder = user names a new dish/quantity; "
                    "reject = user declines but gives no new order")
    dish: str = Field(default="")
    quantity: int = Field(default=0)


SPEAK_SYSTEM = (
    "You are an AI agent for restaurant food ordering - NOT a general-purpose assistant. "
    "Write 1-2 short, friendly sentences to the customer for the given EVENT. "
    "Base every fact on the STATE provided (status, quantities, retry counters, menu). "
    "Retry counters are attempts remaining; 0 means that step has run out of attempts. "
    "Never invent dishes or quantities."
)


class LangChainLLM:
    """Groq-hosted model. Reads GROQ_API_KEY from .env."""

    def __init__(self, model: Optional[str] = None):
        from dotenv import load_dotenv
        from langchain_groq import ChatGroq

        load_dotenv()  # loads GROQ_API_KEY from .env
        if not os.getenv("GROQ_API_KEY"):
            raise RuntimeError("GROQ_API_KEY not found - add it to your .env file")
        self.chat = ChatGroq(model=model or "openai/gpt-oss-120b", temperature=0)

    def parse_order(self, text: str) -> ParsedOrder:
        sys = ("Extract a restaurant order from the message: one dish and its quantity. "
               "If the message is not about ordering food, intent='unrelated'.")
        return self.chat.with_structured_output(ParsedOrder).invoke(
            [("system", sys), ("human", text)])

    def parse_decision(self, text: str) -> ParsedDecision:
        sys = ("The customer was offered a PARTIAL order (less than they asked). Decide whether they "
               "accept it, place a new order (extract dish/quantity), or just reject it.")
        return self.chat.with_structured_output(ParsedDecision).invoke(
            [("system", sys), ("human", text)])

    def speak(self, event: str, facts: dict) -> str:
        msg = f"EVENT: {event}\nSTATE: {json.dumps(facts)}"
        return self.chat.invoke([("system", SPEAK_SYSTEM), ("human", msg)]).content


# --------------------------------------------------------------------------- #
# Dependencies (swap in tests)
# --------------------------------------------------------------------------- #
class Deps:
    llm = None                                     # set lazily in main()
    input_fn = staticmethod(input)
    output_fn = staticmethod(print)
    cook_fn = staticmethod(lambda: random.random() < COOK_SUCCESS_PROB)
    serve_fn = staticmethod(lambda: random.random() < SERVE_SUCCESS_PROB)


def _facts(state: OrderState) -> dict:
    return {
        "dish_name": state["dish_name"], "required_quantity": state["required_quantity"],
        "available_quantity": state["available_quantity"], "status": state["status"],
        "order_retries": state["order_retries"], "cook_retries": state["cook_retries"],
        "serve_retries": state["serve_retries"], "menu": MENU,
    }


def say(event: str, state: OrderState) -> AIMessage:
    text = Deps.llm.speak(event, _facts(state))
    Deps.output_fn(f"Bot: {text}")
    return AIMessage(content=text)


def _last_human(state: OrderState) -> str:
    for m in reversed(state["messages"]):
        if isinstance(m, HumanMessage):
            return m.content
    return ""


# --------------------------------------------------------------------------- #
# Nodes
# --------------------------------------------------------------------------- #
def get_input(state: OrderState) -> dict:
    text = Deps.input_fn("You: ")
    return {"messages": [HumanMessage(content=text)]}


def parse_input(state: OrderState) -> dict:
    parsed = Deps.llm.parse_order(_last_human(state))
    if parsed.intent == "unrelated" or not parsed.dish or parsed.quantity <= 0:
        return {"status": "UNRELATED"}
    return {"dish_name": parsed.dish.lower().strip(), "required_quantity": parsed.quantity,
            "status": "PENDING"}


def handle_unrelated(state: OrderState) -> dict:
    # An unrelated message uses up one order attempt (see open question #1).
    new = {"order_retries": state["order_retries"] - 1}
    return {**new, "messages": [say("unrelated_request", {**state, **new})]}


def order_confirm(state: OrderState) -> dict:
    available = MENU.get(state["dish_name"], 0)   # not on menu -> 0
    required = state["required_quantity"]
    if available >= required and available > 0:
        status = "CONFIRMED"
    elif available > 0:
        status = "PARTIAL"
    else:
        status = "UNAVAILABLE"
    return {"available_quantity": available, "status": status}


def handle_shortfall(state: OrderState) -> dict:
    """Order was PARTIAL or UNAVAILABLE: burn one order attempt and tell the user."""
    new = {"order_retries": state["order_retries"] - 1}
    s = {**state, **new}
    if s["status"] == "PARTIAL":
        event = "partial_available_ask_accept_or_new_order" if s["order_retries"] > 0 \
            else "partial_available_last_chance_accept_or_end"
    else:
        event = "not_available_ask_new_order" if s["order_retries"] > 0 else "not_available_no_attempts_left"
    return {**new, "messages": [say(event, s)]}


def ask_decision(state: OrderState) -> dict:
    text = Deps.input_fn("You: ")
    human = HumanMessage(content=text)
    d = Deps.llm.parse_decision(text)
    if d.decision == "accept":
        return {"messages": [human], "required_quantity": state["available_quantity"],
                "status": "CONFIRMED"}
    if d.decision == "reorder" and d.dish and d.quantity > 0:
        return {"messages": [human]}            # parse_input will re-read this message
    # plain rejection
    update = {"messages": [human], "status": "REJECTED"}
    if state["order_retries"] > 0:
        update["messages"].append(say("partial_rejected_ask_new_order", state))
    return update


def cook(state: OrderState) -> dict:
    if Deps.cook_fn():
        return {"status": "READY", "messages": [say("cooking_done", {**state, "status": "READY"})]}
    new = {"cook_retries": max(0, state["cook_retries"] - 1)}
    if new["cook_retries"] > 0:
        return {**new, "status": "COOK_FAILED",
                "messages": [say("cook_failed_retrying", {**state, **new, "status": "COOK_FAILED"})]}
    return {**new, "status": "FAILED"}


def serve(state: OrderState) -> dict:
    if Deps.serve_fn():
        return {"status": "COMPLETE"}
    new = {"serve_retries": state["serve_retries"] - 1}
    # A serve failure sends the dish back to the kitchen; that consumes a cook retry.
    if new["serve_retries"] > 0 and state["cook_retries"] > 0:
        new["cook_retries"] = state["cook_retries"] - 1
        return {**new, "status": "SERVE_FAILED",
                "messages": [say("serve_failed_recooking", {**state, **new, "status": "SERVE_FAILED"})]}
    return {**new, "status": "FAILED"}


def end_success(state: OrderState) -> dict:
    s = {**state, "status": "COMPLETE"}
    return {"status": "COMPLETE", "final_result": "COMPLETED",
            "messages": [say("order_complete", s)]}


def end_failure(state: OrderState) -> dict:
    s = {**state, "status": "FAILED"}
    return {"status": "FAILED", "final_result": "FAILED",
            "messages": [say("apologise_order_failed", s)]}


# --------------------------------------------------------------------------- #
# Routers
# --------------------------------------------------------------------------- #
def after_parse(state: OrderState) -> str:
    return "handle_unrelated" if state["status"] == "UNRELATED" else "order_confirm"


def after_unrelated(state: OrderState) -> str:
    return "end_failure" if state["order_retries"] <= 0 else "get_input"


def after_confirm(state: OrderState) -> str:
    return "cook" if state["status"] == "CONFIRMED" else "handle_shortfall"


def after_shortfall(state: OrderState) -> str:
    if state["status"] == "PARTIAL":
        return "ask_decision"                      # user may still accept partial on last attempt
    return "end_failure" if state["order_retries"] <= 0 else "get_input"


def after_decision(state: OrderState) -> str:
    if state["status"] == "CONFIRMED":             # accepted partial
        return "cook"
    if state["order_retries"] <= 0:
        return "end_failure"
    return "get_input" if state["status"] == "REJECTED" else "parse_input"


def after_cook(state: OrderState) -> str:
    return {"READY": "serve", "COOK_FAILED": "cook"}.get(state["status"], "end_failure")


def after_serve(state: OrderState) -> str:
    return {"COMPLETE": "end_success", "SERVE_FAILED": "cook"}.get(state["status"], "end_failure")


# --------------------------------------------------------------------------- #
# Graph
# --------------------------------------------------------------------------- #
def build_graph():
    g = StateGraph(OrderState)
    for name, fn in [
        ("get_input", get_input), ("parse_input", parse_input),
        ("handle_unrelated", handle_unrelated), ("order_confirm", order_confirm),
        ("handle_shortfall", handle_shortfall), ("ask_decision", ask_decision),
        ("cook", cook), ("serve", serve),
        ("end_success", end_success), ("end_failure", end_failure),
    ]:
        g.add_node(name, fn)

    g.add_edge(START, "get_input")
    g.add_edge("get_input", "parse_input")
    g.add_conditional_edges("parse_input", after_parse, ["handle_unrelated", "order_confirm"])
    g.add_conditional_edges("handle_unrelated", after_unrelated, ["get_input", "end_failure"])
    g.add_conditional_edges("order_confirm", after_confirm, ["cook", "handle_shortfall"])
    g.add_conditional_edges("handle_shortfall", after_shortfall,
                            ["ask_decision", "get_input", "end_failure"])
    g.add_conditional_edges("ask_decision", after_decision,
                            ["cook", "parse_input", "get_input", "end_failure"])
    g.add_conditional_edges("cook", after_cook, ["serve", "cook", "end_failure"])
    g.add_conditional_edges("serve", after_serve, ["end_success", "cook", "end_failure"])
    g.add_edge("end_success", END)
    g.add_edge("end_failure", END)
    return g.compile()


def run(graph=None) -> OrderState:
    graph = graph or build_graph()
    return graph.invoke(initial_state(), {"recursion_limit": 100})


if __name__ == "__main__":
    Deps.llm = LangChainLLM()
    print("Bot: Welcome! Tell me what you'd like to order (dish and quantity).")
    final = run()
    print(f"\n=== FINAL RESULT: {final['final_result']} ===")