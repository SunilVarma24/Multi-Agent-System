import streamlit as st
from langchain_core.messages import HumanMessage


# Import your predefined workflow
from multi_agent_system import workflow, AgentState

# Initialize the workflow
agent_workflow = workflow.compile()

# Streamlit app definition
def main():
    st.title("Market Research & Use Case Generation Agent")
    st.markdown("""
    This app demonstrates a multi-agent system to research companies/industries, proposes AI/ML use cases, and collect relevant resources of them.
    """)
    
    # User input for query
    user_input = st.text_input(
        "Enter your query about industry trends, AI/ML applications, or use cases:",
        placeholder="e.g., Conduct market research on the healthcare industry,propose AI/ML use cases, and find relevant datasets for these use cases.?"
    )
    
    if st.button("Generate"):
        if not user_input.strip():
            st.error("Please enter a valid query.")
            return
        
        st.info("Processing your query. This may take a few moments...")
        
        # Initialize agent state
        agent_state = AgentState(
            messages=[HumanMessage(content=user_input)],
            sender="User"
        )
        
        # Run the workflow
        try:
            response = agent_workflow.invoke(agent_state)
            
            # Display final result
            final_message = response["messages"][-1].content
            st.markdown(final_message)
			
        except Exception as e:
            st.error(f"An error occurred: {e}")
    
    st.markdown("---")

if __name__ == "__main__":
    main()
