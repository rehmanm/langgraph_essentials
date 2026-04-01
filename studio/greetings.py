from typing import TypedDict, Annotated, Literal, List
from langgraph.graph import START, END, StateGraph
from datetime import datetime, timezone

from langgraph.types import Command, interrupt

# Public input to the graph (what the caller provides)
class InputState(TypedDict):
    name: str


# Public output from the graph (what the caller sees)
class OutputState(TypedDict):
    message: str


# Internal state for the graph; can contain extra fields like `happened`
class OverallState(TypedDict):
    name: str
    message: str
    happened: int

def get_time(
    state: OverallState,
) -> Command[Literal["good_morning", "good_afternoon", "good_evening", "out_of_office_time"]]:

    current_hour = datetime.now(timezone.utc).hour
    print(current_hour)
    happened = state.get("happened", 0)
    if current_hour < 12:
        next_node = "good_morning"
    elif current_hour < 18:
        next_node = "good_afternoon"
    elif current_hour < 20:
        next_node = "good_evening"
    else:
        happened += 1
        next_node = "out_of_office_time"
    
    return Command(
        update={"name": state["name"], "happened": happened},
        goto=next_node,
    )


def good_morning(state: OverallState) -> OutputState:
    print("Good morning!")
    return OutputState(message=f"Good morning, {state['name']}!")
	
def good_afternoon(state: OverallState) -> OutputState:
    print("Good afternoon!")
    return OutputState(message=f"Good afternoon, {state['name']}!")

def good_evening(state: OverallState) -> OutputState:
    print("Good evening!")
    return OutputState(message=f"Good evening, {state['name']}!")

def out_of_office_time(state: OverallState) -> Command[Literal["get_time", "fall_back_message"]]:
    happened = state.get("happened", 0)
    print("Out of office time!")
    return Command(
        update={"name": state["name"], "happened": happened},
        goto="get_time" if happened < 2 else "fall_back_message",
    )

def fall_back_message(state: OverallState) -> OutputState:
    print("Fallback!")
    return OutputState(message=f"Your shift start at 9:00, {state['name']}!")

builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)

builder.add_node("get_time", get_time)
builder.add_node("good_morning", good_morning)
builder.add_node("good_afternoon", good_afternoon)
builder.add_node("good_evening", good_evening)
builder.add_node("out_of_office_time", out_of_office_time)
builder.add_node("fall_back_message", fall_back_message)
builder.add_edge(START, "get_time")
builder.add_edge("good_morning", END)
builder.add_edge("good_afternoon", END)
builder.add_edge("good_evening", END)
builder.add_edge("fall_back_message", END)

graph = builder.compile()
