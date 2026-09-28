from typing import TypedDict
from langgraph.graph import END, StateGraph

class State(TypedDict):
    number: int
    
def double(state: State)->dict:
    boardnum=state["number"]
    newnum=boardnum*2
    print('in double')
    print(newnum)
    return {"number":newnum}

def finish(state: State)->dict:
    boardnum=state['number']
    print('in finish')
    print(boardnum)
    return {"number":boardnum}

def decision(state: State)->str:
    if state["number"]<100:
        return "double"
    else:
        return "finish"
    
builder=StateGraph(State)
builder.add_node("double",double)
builder.add_node("finish",finish)

#entry point

builder.set_entry_point("double")

builder.add_conditional_edges(
    "double",
    decision,
    {"double":"double","finish":"finish"}
)

builder.add_edge("finish",END)

graph=builder.compile()

if __name__=="__main__":
    result=graph.invoke({"number":10})