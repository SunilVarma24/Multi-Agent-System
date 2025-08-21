# Market Research & Use Case Generation System

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
   - Searches platforms like Kaggle, HuggingFace, and GitHub for relevant resources of use cases proposed.
   - Provides a structured output of datasets, repositories, and tools for implementation.

## Features
- **Industry Analysis**: Understands market trends and company needs.
- **Use Case Generation**: Suggests AI and ML applications to boost operational efficiency and customer satisfaction.
- **Dataset Collection**: Gathers relevant resource links for proposed use cases.
- **Customizable Proposals**: Provides actionable insights tailored to the company.

## Technologies Used
- **OpenAI API**: For natural language processing and understanding.
- **LangChain**: To build and manage agents.
- **LangGraph**: For multi-agent communication and task execution.
- **FastAPI**: To provide a robust backend API for executing agent workflows.
- **Streamlit**: To deploy and visualize the system via a user-friendly frontend.
- **Docker**: For containerization of the application.
- **Azure**: For cloud deployment and scalability.

## Source Code
## 1. src/agents.py
This script defines the core functionality of the multi-agent system, including agent definitions, prompts, and tool integrations.

### 1.1 Key Components

#### Agents:
* Industry Research Agent: Gathers industry and company-specific information.
* Use Case Generator Agent: Generates relevant AI/ML use cases.
* Resource Collector Agent: Collects datasets, repositories, and tools to implement use cases.

#### Prompts:
* Each agent has a specific prompt template that guides its operation.
* Prompts are designed to extract relevant information and generate actionable insights.

#### Tools:
* Tavily search for industry research.
* Kaggle, HuggingFace, GitHub search tools for dataset and resource collection.

## 2. src/tools.py
This script defines the tools used by agents to perform specific tasks, such as searching for datasets or repositories.

### 2.1 Key Components

#### Tools:
* Tavily search for industry research.
* Kaggle dataset search for relevant datasets.
* HuggingFace search for machine learning models and datasets.
* GitHub search for repositories and code examples.

### 3. src/graph.py
This script defines the multi-agent workflow using LangGraph, integrating agents and tools into a cohesive system.

## 3.1 Key Components

### StateGraph:
* Defines the flow of information between agents and tools.
* Manages transitions based on agent outputs and tool results.

## 4. main.py
This script provides a FastAPI-based backend for executing the multi-agent workflow.

### 4.1 Key Components

#### FastAPI Integration:
* Initializes a FastAPI application to handle requests.
* Defines endpoints for executing agent workflows and returning results.

#### Request Handling:
* Accepts user input as a POST request.
* Validates input and executes the agent workflow.
* Returns results in a structured JSON format.

## 5. app.py
This script provides a Streamlit-based frontend for interacting with the FastAPI backend.

### 5.1 Key Components

#### UI Layout:
* User input for company/industry names and configuration parameters.
* Display results from each agent's output in an organized manner.

#### Backend Integration:
* Calls the FastAPI backend endpoints and manages their execution.
* Displays results in real-time, allowing users to interactively explore generated use cases and collected resources.

## How to Run the Application
### 0. Prerequisites
Ensure you have Python 3.8 or higher installed along with the required libraries. You can install the necessary dependencies using pip:
```bash
pip install -r requirements.txt
```
### Environment Variables
Set the following environment variables in a `.env` file or your system's environment:
```plaintext
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

### 1. FastAPI Backend
To run the FastAPI backend, follow these steps:
1. **Ensure FastAPI and Uvicorn are Installed**
   * If not installed, use the following command:
   ```bash
   pip install fastapi uvicorn
   ```
2. **Navigate to the Script Directory**
   * Open a terminal or command prompt.
   * Navigate to the folder where `main.py` is located:
   ```bash
   cd /path/to/your/project/
   ```
3. **Run the FastAPI Application**
   * Execute the following command:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
4. **Access the API Documentation**
   * Open your web browser and go to `http://localhost:8000/docs` to view the API documentation and test endpoints.

### 2. Streamlit Frontend
To run the Streamlit frontend, follow these steps:
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
   streamlit run streamlit/app.py
   ```
4. **Access the Streamlit Application**
   * After running the above command, a local server will start.
   * Open the URL displayed in the terminal (e.g., `http://localhost:8501`) in your web browser to access the Streamlit interface.

## Interactions Between Scripts

### Frontend (app.py):
* Captures user input.
* Calls the FastAPI backend to execute agent workflows.
* Displays results interactively.

### Backend (main.py):
* Receives user input from the frontend.
* Validates and processes the input.
* Executes the agent workflow defined.
* Returns results to the frontend in a structured format.

## Results
The application generates AI/ML use cases based on the provided company or industry name. It collects relevant datasets and resources, which are displayed in the Streamlit frontend. The results include:
- Proposed AI/ML use cases tailored to the company's needs.
- Collected resources such as datasets, repositories, and tools for implementation.

You can also view a sample response pdf file in the results folder, which includes:
- Use cases generated by the agents.
- Collected resources in a structured format.

## Cloud Deployment
To deploy the application on Azure, we build a Docker image and push the image to Azure Container Registry (ACR) and then run the image in a Azure Container Instance (ACI).
### 0. start.sh
- This script is used to start the FastAPI and Streamlit applications concurrently. It ensures that both services are running and accessible.
- Create a Dockerfile in the project root directory.
- Create a docker-compose.yml file to manage the services.

### 1. Build the Docker Image
```bash
docker build -t myacrmultiagent.azurecr.io/myapp:latest .
```
### 2. Create a Resource Group
```bash
az group create --name myResourceGroup --location eastus
```
### 3. Create an Azure Container Registry
```bash
az acr create --resource-group myResourceGroup --name myacrmultiagent --sku Basic --admin-enabled true
```
### 4. Login to Azure Container Registry
```bash
az acr login --name myacrmultiagent
```
### 5. Push the Docker Image to Azure Container Registry
```bash
docker push myacrmultiagent.azurecr.io/myapp:latest
```
### 6. Create Azure Container Instance
```bash
az container create --resource-group myResourceGroup --name myContainer --image myacrmultiagent.azurecr.io/myapp:latest --registry-login-server myacrmultiagent.azurecr.io --registry-username <your-username> --registry-password <your-password> --os-type Linux --ports 8000 8501 --cpu 2 --memory 4 --environment-variables OPENAI_API_KEY=your_openai_api_key TAVILY_API_KEY=your_tavily_api_key --dns-name-label multiagentsystem --ip-address public
```
### 7. Get the IP and DNS
```bash
az container show --resource-group myResourceGroup --name myContainer --query "{IP: ipAddress.ip, DNS:ipAddress.fqdn}" -o table
```
### 8. Access the Application
* FastAPI API: `http://<your-public-ip>:8000/docs`
* Streamlit UI: `http://<your-public-ip>:8501`
### 9. Stop the Application
```bash
az container stop --resource-group myResourceGroup --name myContainer
```
### 10. Delete the Container
```bash
az container delete --resource-group myResourceGroup --name myContainer --yes
```
### 11. Delete the Resource Group
```bash
az group delete --name myResourceGroup --yes --no-wait
```

## Testing
To test the application, you can use the provided FastAPI endpoints to submit requests and verify the responses. The Streamlit frontend allows for interactive testing by entering company or industry names and viewing the generated use cases and collected resources.

## Future Enhancements
- **Enhanced Agent Capabilities**: Add more agents for deeper analysis and broader use case generation.
- **Integration with More Data Sources**: Expand the toolset to include additional data sources for resource collection.
- **User Authentication**: Implement user authentication for secure access to the application.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Conclusion
This project provides a comprehensive multi-agent system for conducting market research and generating AI/ML use cases. By leveraging LangChain and LangGraph, it enables efficient collaboration between agents to gather insights, propose solutions, and collect resources. The FastAPI backend and Streamlit frontend facilitate easy interaction and visualization of results, making it a powerful tool for businesses looking to leverage AI technologies.
