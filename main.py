# main.py

from IPython.display import Image, display, Markdown
from src.graph import get_agent_workflow

def main():
    # Visualize the agent workflow graph
    agent_workflow = get_agent_workflow()
    display(Image(agent_workflow.get_graph().draw_mermaid_png()))
    
    # Test the Multi Agent System with a sample prompt
    prompt = ("Conduct research on the medical industry, propose AI/ML use cases, "
              "and find relevant datasets for these use cases.")
    
    response = agent_workflow.invoke(
        {
            "messages": [("human", prompt)]
        }
    )
    
    # Display the final output using Markdown
    display(Markdown(response['messages'][-1].content))

if __name__ == "__main__":
    main()
