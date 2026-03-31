from typing import TypedDict, List
from langgraph.graph import START, END, StateGraph

class State(TypedDict):
    nList: List[str]


def node_a(state: State) -> State:
    print (f"node a is receiving {state['nList']}")
    note = "Hello World from Node A"
    return State(nList = [note])

builder = StateGraph(State)

builder.add_node("node_a", node_a)

builder.add_edge(START, "node_a")
builder.add_edge("node_a", END)

graph = builder.compile()
