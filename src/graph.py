# src/graph.py

from langgraph.prebuilt import ToolNode
from langgraph.graph import END, StateGraph
from typing import Literal

from src.agents import AgentState, industry_research_node, usecase_generator_node, resource_collector_node
from src.tools import tv_search, kaggle_dataset_search, huggingface_search, github_search

# Define Tool Nodes
tools = [tv_search, kaggle_dataset_search, huggingface_search, github_search]
tool_node = ToolNode(tools)

# Define Router/Edge Logic
def router(state: AgentState) -> Literal["call_tool", "__end__", "continue_to_usecase", "continue_to_resource"]:
    messages = state["messages"]
    last_message = messages[-1]

    if "FINAL ANSWER" in last_message.content:
        return "__end__"

    if "RESEARCH COMPLETE" in last_message.content:
        return "continue_to_usecase"

    if "USE CASES COMPLETE" in last_message.content:
        return "continue_to_resource"

    return "call_tool"

# Build the multi-agent graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("Industry_Researcher", industry_research_node)
workflow.add_node("UseCase_Generator", usecase_generator_node)
workflow.add_node("Resource_Collector", resource_collector_node)
workflow.add_node("call_tool", tool_node)

# Add conditional edges from Industry Researcher
workflow.add_conditional_edges(
    "Industry_Researcher",
    router,
    {
        "continue_to_usecase": "UseCase_Generator",
        "call_tool": "call_tool",
    }
)

# Add conditional edges from Use Case Generator
workflow.add_conditional_edges(
    "UseCase_Generator",
    router,
    {
        "continue_to_resource": "Resource_Collector",
    }
)

# Add conditional edges from Resource Collector
workflow.add_conditional_edges(
    "Resource_Collector",
    router,
    {
        "call_tool": "call_tool",
        "__end__": END
    }
)

# Add conditional edges from the tool node back to agents based on sender
workflow.add_conditional_edges(
    "call_tool",
    lambda state: state["sender"],
    {
        "Industry_Researcher": "Industry_Researcher",
        "Resource_Collector": "Resource_Collector"
    }
)

# Set entry point and compile the graph
workflow.set_entry_point("Industry_Researcher")
agent_workflow = workflow.compile()

# Expose the compiled workflow for use in main.py
def get_agent_workflow():
    return agent_workflow
