# src/agents.py

from typing import Annotated, Sequence, TypedDict
import operator

from langchain_core.messages import BaseMessage, ToolMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.tools import tv_search, kaggle_dataset_search, huggingface_search, github_search

# Load environment variables from .env file
# Step 1: Get absolute path to the project root
from dotenv import load_dotenv
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

# Step 2: Construct .env path explicitly
env_path = project_root / ".env"

# Step 3: Load it explicitly
load_dotenv(dotenv_path=env_path)

# Graph state: the object passed between nodes
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str

# Initialize the LLM
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
Also each use case should include below points along with its citations:
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
- The output should be structured as follows for each use case:
  - Use Case 1:
    - Problem Statement: [Insert Problem Statement]
    - Proposed Solution: [Insert Proposed Solution]
    - Expected Benefits: [Insert Expected Benefits]
    - Relevant Resources:
      1. Kaggle: [Link]
        - Content: [Description]
        - Usage: [How it can be used]
      2. HuggingFace: [Link]
        - Content: [Description]
        - Usage: [How it can be used]
      3. GitHub: [Link]
        - Content: [Description]
        - Usage: [How it can be used]
  - Repeat for each use case


When you have collected all resources, start your response with "FINAL ANSWER".
"""),
    MessagesPlaceholder(variable_name="messages"),
])

# Bind tools to agents
research_tools = [tv_search]
industry_research_agent = industry_research_prompt | llm.bind_tools(research_tools)

usecase_generator_agent = use_case_prompt | llm

resource_tools = [kaggle_dataset_search, huggingface_search, github_search]
resource_collector_agent = resource_prompt | llm.bind_tools(resource_tools)

# Define Agent Nodes
async def industry_research_node(state: AgentState) -> AgentState:
    result = await industry_research_agent.ainvoke(state)
    if isinstance(result, ToolMessage):
        return state  # unchanged if tool message
    result = AIMessage(**result.dict(exclude={"type", "name"}), name="Industry_Researcher")
    return {
        "messages": [result],
        "sender": "Industry_Researcher"
    }

async def usecase_generator_node(state: AgentState) -> AgentState:
    result = await usecase_generator_agent.ainvoke(state)
    if isinstance(result, ToolMessage):
        return state
    result = AIMessage(**result.dict(exclude={"type", "name"}), name="UseCase_Generator")
    return {
        "messages": [result],
        "sender": "UseCase_Generator"
    }

async def resource_collector_node(state: AgentState) -> AgentState:
    result = await resource_collector_agent.ainvoke(state)
    if isinstance(result, ToolMessage):
        return state
    result = AIMessage(**result.dict(exclude={"type", "name"}), name="Resource_Collector")
    return {
        "messages": [result],
        "sender": "Resource_Collector"
    }