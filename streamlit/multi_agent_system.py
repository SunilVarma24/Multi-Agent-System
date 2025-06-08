# import libraries

import os
import yaml
from typing import Annotated, Sequence, TypedDict, Literal, Union, List, Tuple, Dict
from langchain_core.messages import BaseMessage, ToolMessage, AIMessage, HumanMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import ToolNode
from langgraph.graph import END, StateGraph
import operator


# 0. **Set up OpenAI & Tavily Search API keys**

from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
tavily_api_key = os.getenv("TAVILY_API_KEY")

# 1. **Create Tools**

tv_search = TavilySearchResults(max_results=5, search_depth='advanced', max_tokens=10000)

@tool
def kaggle_dataset_search(query: str) -> str:
    """Search for relevant datasets on Kaggle"""
    # Using Tavily to search Kaggle specifically
    return tv_search.invoke(f"site:kaggle.com datasets {query}")

@tool
def huggingface_search(query: str) -> str:
    """Search for relevant datasets on HuggingFace"""
    # Using Tavily to search HuggingFace specifically
    return tv_search.invoke(f"site:huggingface.co {query}")

@tool
def github_search(query: str) -> str:
    """Search for relevant repositories on GitHub"""
    # Using Tavily to search GitHub specifically
    return tv_search.invoke(f"site:github.com {query}")

# 2. **Graph State**

# This defines the object that is passed between each node
# in the graph. We will create different nodes for each agent and tool
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str

# 3. **Create Agents**
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Industry Research Agent
industry_research_prompt = ChatPromptTemplate.from_messages([
    ("system", f"""You are an Industry Research Specialist AI assistant.

    Your task is to provide detailed, structured insights about the company and its industry to enable downstream agents to generate actionable AI/ML use cases.

    Your responsibilities include:
    1. **Industry Overview**:
       - Identify and describe the industry/segment the company operates in.
       - Mention key trends, challenges, and opportunities in this industry.

    2. **Company-Specific Insights**:
       - Research and list the company’s main products, services, and target markets.
       - Highlight the company's key strategic focus areas (e.g., operations, supply chain, customer experience, innovation).
       - Analyze the company's current technology adoption trends, especially in Machine Learning and Generative AI.

    **Instructions**:
    - Use the {tv_search} tool to gather accurate and up-to-date information.
    - Structure your response as follows:
      - Industry Overview
      - Company Overview
    - Ensure your output is detailed enough for downstream agents to work effectively.

    When you have gathered all the required information, start your response with "RESEARCH COMPLETE".
    """),
    MessagesPlaceholder(variable_name="messages"),
])

# Use Case Generator Agent
use_case_prompt = ChatPromptTemplate.from_messages([
    ("system", f"""You are a Use Case Generator for AI/ML solutions.

    Your responsibilities include:
    1. Based on the research findings, identify specific areas where Machine Learning or Generative AI can add value. 

    2. Propose practical use cases on these areas where the company can leverage Generative AI, Large Language Models (LLMs), and Machine Learning.
    Also each use case should include:
    - Problem Statement:
    - Proposed Solution:
    - Expected Benefits:

    Instructions:
    - Format your findings clearly with proper citations
    - Make sure use cases are practical and relevant
    - Include examples from similar companies when possible

    When you have generated comprehensive use cases, start your response with "USE CASES COMPLETE".
    """),
    MessagesPlaceholder(variable_name="messages"),
])

# Resource Collector Agent
resource_prompt = ChatPromptTemplate.from_messages([
    ("system", f"""You are a Resource Collector for AI projects.

    Your responsibilities include:
    1. Only List the top use cases that can be delivered to the customer, ensuring they are relevant to the company/industry goals and operational needs.
    Also each use case should include below points along with its references:
    - Problem Statement:
    - Proposed Solution:
    - Expected Benefits:
    
    2. For each use case listed find relevant resources from:
       - Kaggle (datasets)
       - HuggingFace (datasets)
       - GitHub (repositories)

    3. For each resource you find, list:
       - The clickable link
       - What the resource contains
       - How it can be used for the use case

    Instructions:
    - Use {kaggle_dataset_search} for Kaggle resources
    - Use {huggingface_search} for HuggingFace resources
    - Use {github_search} for GitHub resources
    - Make sure all links are clickable
    - Format output in markdown for easy reading

    When you have collected all resources, start your response with "**FINAL ANSWER**".
    """),
    MessagesPlaceholder(variable_name="messages"),
])

# Bind tools to agents
research_tools = [tv_search]
industry_research_agent = industry_research_prompt | llm.bind_tools(research_tools)

usecase_generator_agent = use_case_prompt | llm

resource_tools = [kaggle_dataset_search, huggingface_search, github_search]
resource_collector_agent = resource_prompt | llm.bind_tools(resource_tools)

# 4. **Define Agent Nodes*

def industry_research_node(state):
    result = industry_research_agent.invoke(state)
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name="Industry_Researcher")
    return {
        "messages": [result],
        "sender": "Industry_Researcher"
    }

def usecase_generator_node(state):
    result = usecase_generator_agent.invoke(state)
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name="UseCase_Generator")
    return {
        "messages": [result],
        "sender": "UseCase_Generator"
    }

def resource_collector_node(state):
    result = resource_collector_agent.invoke(state)
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name="Resource_Collector")
    return {
        "messages": [result],
        "sender": "Resource_Collector"
    }


# 5. **Define Tool Nodes**

from langgraph.prebuilt import ToolNode

tools = [tv_search, kaggle_dataset_search, huggingface_search, github_search]
tool_node = ToolNode(tools)

# 6. **Define Edge Logic**

def router(state) -> Literal["call_tool", "__end__", "continue_to_usecase", "continue_to_resource"]:
    messages = state["messages"]
    last_message = messages[-1]

    if "FINAL ANSWER" in last_message.content:
        return "__end__"

    if "RESEARCH COMPLETE" in last_message.content:
        return "continue_to_usecase"

    if "USE CASES COMPLETE" in last_message.content:
        return "continue_to_resource"

    return "call_tool"

# 7. **Define Multi-Agent Graph**

# Initialize and configure the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("Industry_Researcher", industry_research_node)
workflow.add_node("UseCase_Generator", usecase_generator_node)
workflow.add_node("Resource_Collector", resource_collector_node)
workflow.add_node("call_tool", tool_node)

# Add edges
workflow.add_conditional_edges(
    "Industry_Researcher",
    router,
    {
        "continue_to_usecase": "UseCase_Generator",
        "call_tool": "call_tool",
    }
)

workflow.add_conditional_edges(
    "UseCase_Generator",
    router,
    {
        "continue_to_resource": "Resource_Collector",
    }
)

workflow.add_conditional_edges(
    "Resource_Collector",
    router,
    {
        "call_tool": "call_tool",
        "__end__": END
    }
)

workflow.add_conditional_edges(
    "call_tool",
    lambda x: x["sender"],
    {
        "Industry_Researcher": "Industry_Researcher",
        "Resource_Collector": "Resource_Collector"
    }
)

# Set entry point
workflow.set_entry_point("Industry_Researcher")


# Expose workflow and AgentState for import
__all__ = ["workflow", "AgentState"]