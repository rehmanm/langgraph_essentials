from typing import TypedDict, Annotated, Literal, List
from langgraph.graph import START, END, StateGraph
import operator

from langgraph.types import Command, interrupt

class State(TypedDict):
    nList: Annotated[List[str], operator.add]


def node_a(state: State):
    return


def node_b(state: State) -> State:
    print (f"Adding 'B' to {state['nList']}")
    return State(nList = ["B"])

def node_c(state: State) -> State:
    print (f"Adding 'C' to {state['nList']}")
    return State(nList = ["C"])


def conditional_edge(state: State) -> Literal["node_b", "node_c", END]:
    select =state["nList"][-1]
    if select == "b":
        return "node_b"
    elif select == "c":
        return "node_c"
    elif select == "q":
        return END
    else:
        return END
 

builder = StateGraph(State)

builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_node("node_c", node_c)

builder.add_edge(START, "node_a")
builder.add_conditional_edges("node_a", conditional_edge)
builder.add_edge("node_b", END)

builder.add_edge("node_c", END)

graph = builder.compile()
