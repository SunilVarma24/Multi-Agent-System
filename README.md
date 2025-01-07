# Market Research & Use Case Generation Agent

## Introduction
AI and Generative AI technologies can revolutionize businesses by improving operations, customer satisfaction, and efficiency. This project focuses on creating a Multi-Agent system to generate use cases tailored to specific industries or companies by conducting research and proposing AI/ML solutions.

## System Architecture
The system consists of three main agents:
1. **Industry/Company Research Agent**:
   - Uses a web browser tool to understand the company's industry, offerings, and strategic focus areas.
   - Identifies key information like operations, supply chain, and customer experience focus.

2. **Market Standards & Use Case Generation Agent**:
   - Analyzes AI/ML and automation trends in the target industry.
   - Proposes AI, GenAI, and ML use cases tailored to the company's needs.

3. **Resource Asset Collection Agent**:
   - Searches platforms like Kaggle, HuggingFace, and GitHub for relevant datasets.
   - Collects resource links in a markdown file.
   - [Optional] Suggests GenAI solutions for internal or external purposes.


## Features
- **Industry Analysis**: Understands market trends and company needs.
- **Use Case Generation**: Suggests AI and ML applications to boost operational efficiency and customer satisfaction.
- **Dataset Collection**: Gathers relevant resource links for proposed use cases.
- **Customizable Proposals**: Provides actionable insights tailored to the company.

## Technologies Used
- **LangChain**: To build and manage agents.
- **LangGraph**: For multi-agent communication and task execution.
- **Streamlit**: To deploy and visualize the system.

## Source Code
## 1. multi_agent_system.py
This script defines the core functionality of the multi-agent system, including agents, workflows, and tools.

### 1.1 Key Components

#### Agents:
* Industry Research Agent: Gathers industry and company-specific information.
* Use Case Generator Agent: Generates relevant AI/ML use cases.
* Resource Collector Agent: Collects datasets, repositories, and tools to implement use cases.

#### Tools:
* Tavily Search (tv_search): Extracts industry/company information.
* Kaggle, HuggingFace, GitHub search tools: Used for dataset and resource collection.

#### Workflow:
* A StateGraph workflow manages the transitions between agents, tools, and decision points.

### 1.2 Code Structure

#### Imports
The script imports required libraries, including langchain and langgraph modules, for agent orchestration, workflow creation, and LLM interaction.

#### Agents
Agents are implemented using prompts and tied to LLMs:

**Industry Research Agent:**
* Purpose: To collect industry-specific information and analyze trends.
* Tools Used: Tavily search (tv_search).

**Use Case Generator Agent:**
* Purpose: Generate AI/ML use cases, including problem statements, solutions, and benefits.
* Tools Used: None by default (relies on Industry Research output).

**Resource Collector Agent:**
* Purpose: Gather resources from Kaggle, HuggingFace, and GitHub for implementing use cases.
* Tools Used: Kaggle, HuggingFace, GitHub search tools.

#### Workflow Definition
A StateGraph defines transitions between agents and tools:
* Entry point: Industry_Researcher
* Conditional routing:
  * From Industry_Researcher to UseCase_Generator or tool call.
  * From UseCase_Generator to Resource_Collector.
  * From Resource_Collector to tool call or end state.

#### Visualization
The workflow is visualized using a Mermaid diagram to understand agent interactions.

## 2. app.py
This script provides a Streamlit-based frontend for interacting with the multi-agent system.

### 2.1 Key Components

#### UI Layout:
* User input for company/industry names and configuration parameters.
* Display results from each agent's output in an organized manner.

#### Backend Integration:
* Calls the multi_agent_system.py workflow and manages its execution.
* Displays real-time outputs for transparency.

### 2.2 Code Structure

#### Imports
The script imports Streamlit for the frontend, as well as the multi_agent_system workflow.

#### User Input
```python
user_input = st.text_input("Enter your query about industry/company"
```
Fields to capture user-specific inputs for customization.

#### Agent Execution
```python
result = agent_workflow.run(user_input)
```
Runs the compiled workflow and passes user input to the agents.

#### Output Display
Results from each agent are formatted and displayed in dedicated sections:
* Generated use cases
* Collected resources

#### Error Handling
Includes error messages if:
* Inputs are missing.
* Workflow execution fails due to API errors.

### 2.3 Running the Application
To run the `app.py` Streamlit application, follow these steps:

1. **Ensure Streamlit is Installed**
   * If Streamlit is not installed, use the following command:
   ```bash
   pip install streamlit
   ```

2. **Navigate to the Script Directory**
   * Open a terminal or command prompt.
   * Navigate to the folder where `app.py` is located:
   ```bash
   cd /path/to/your/project/
   ```

3. **Run the Streamlit Application**
   * Execute the following command:
   ```bash
   streamlit run app.py
   ```

4. **Access the Application**
   * After running the above command, a local server will start.
   * Open the URL displayed in the terminal (e.g., `http://localhost:8501`) in your web browser to access the Streamlit interface.

## 3. Interactions Between Scripts

### Frontend (app.py):
* Captures user input.
* Executes the multi-agent workflow.
* Displays results interactively.

### Backend (multi_agent_system.py):
* Defines agents and their functionality.
* Manages workflows and transitions between agents.
* Executes tasks and returns results to the frontend.

## 4. Key Interactions

### Agent-to-Agent Communication:
* Industry_Researcher feeds insights to UseCase_Generator.
* UseCase_Generator provides problems/solutions to Resource_Collector.

### Tool Usage:
* Industry_Researcher calls Tavily search for information.
* Resource_Collector uses Kaggle, HuggingFace, and GitHub tools for resource collection.
