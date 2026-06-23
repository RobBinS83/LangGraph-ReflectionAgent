from dotenv import load_dotenv
from typing import TypedDict, Annotated, List, Literal
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from chains import generate_chain, reflect_chain

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

REFLECT = "reflect"
GENERATE = "generate"

def generator_node(state: AgentState) -> dict:
    response = generate_chain.invoke({"messages": state["messages"]})
    return {"messages": [response]}

def reflector_node(state: AgentState) -> dict:
    reponse = reflect_chain.invoke({"messages": state["messages"]})
    return {"messages": [HumanMessage(content=reponse.content)]}

builder = StateGraph(state_schema=AgentState)
builder.add_node(GENERATE, generator_node)
builder.add_node(REFLECT, reflector_node)
builder.set_entry_point(GENERATE)

def should_continue(state: AgentState):
    messages = state["messages"]
    last_maessage = messages[-1]

    content = last_maessage.content
    
    # if isinstance(content, list):
    #     text_str = " ".join(
    #         block.get("text", "") for block in content if isinstance(block, dict) and "text" in block
    #     )
    # else:
    #     text_str = str(content or "")

    # if "APPROVED" in text_str.upper():
    #     return END

    if "APPROVED" in content:
        return END
    
    if len(messages) > 20:
        return END
    
    return GENERATE

builder.add_conditional_edges(REFLECT, should_continue, path_map={
    END: END,
    GENERATE: GENERATE})
builder.add_edge(GENERATE, REFLECT)

workflow = builder.compile()
workflow.get_graph().draw_mermaid_png(output_file_path="flow.png") 


def main():
    print("Hello from LangGraph!")
    inputs = HumanMessage(content=""" Make this email better: 
                          Team, 
                          I want to share an update regarding our executive leadership team. 
                          Sam Hammock, our Chief Human Resources Officer, has decided this is the 
                          right time for her to pursue a new opportunity outside of Verizon. 
                          Sam will be with us through July 1. We’ve been working on next steps 
                          for the HR Organization and I will share more about our transition before 
                          the month ends. In the meantime, all of us on the VLC will keep our focus 
                          exactly where it needs to be: on our people, our customers and the 
                          important work ahead of us.
                          
                          Sam has been an exceptional leader at Verizon, and I have truly 
                          valued working with her. She joined Verizon in 2020 at a time of real 
                          uncertainty and never once wavered in her commitment to our people, 
                          bringing clarity, creativity and care to the work that mattered most. 
                          Sam has made an enormous contribution to what makes Verizon a place 
                          where people thrive and build their careers. Sam has been a trusted 
                          advisor and friend, and I will miss her.
                          
                          Thank you, Sam, for your leadership and the impact that you have 
                          made at Verizon.
                          
                          Please join me in wishing Sam all the best in her next chapter.
                          """)
    
    response = workflow.invoke({"messages": [inputs]})


if __name__ == "__main__":
    main()
