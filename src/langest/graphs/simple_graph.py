"""Simple graph example using LangGraph with Groq."""

from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GraphState(TypedDict):
    """State of the graph."""
    messages: Annotated[list, operator.add]
    input: str
    output: str


def chatbot_node(state: GraphState) -> GraphState:
    """Simple chatbot node that processes the input message."""
    # Initialize the Groq LLM
    llm = ChatGroq(
        model="mixtral-8x7b-32768",  # You can also use "llama2-70b-4096", "gemma-7b-it", etc.
        temperature=0.7,
        api_key=os.getenv("GROQ_API_KEY")
    )
    
    # Create messages
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=state["input"])
    ]
    
    # Get response from LLM
    response = llm.invoke(messages)
    
    return {
        "messages": [response],
        "input": state["input"],
        "output": response.content
    }


def create_simple_graph() -> StateGraph:
    """Create a simple LangGraph workflow."""
    # Initialize the state graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("chatbot", chatbot_node)
    
    # Set entry point
    workflow.set_entry_point("chatbot")
    
    # Add edges
    workflow.add_edge("chatbot", END)
    
    # Compile the graph
    return workflow.compile()


if __name__ == "__main__":
    # Example usage
    graph = create_simple_graph()
    result = graph.invoke({
        "input": "Tell me a joke about programming",
        "messages": [],
        "output": ""
    })
    print("Output:", result["output"])
