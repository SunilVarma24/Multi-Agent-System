# app.py (Streamlit frontend for FastAPI backend)

import streamlit as st
import requests

# Define the FastAPI endpoint
FASTAPI_URL = "http://127.0.0.1:8000/generate_insights"

def main():
    st.title("Market Research & Use Case Generation Multi-Agent System")
    st.markdown("This app demonstrates a multi-agent system to research companies/industries, proposes AI/ML use cases, and collect relevant resources of them.")

    # Input box
    user_input = st.text_area("Enter your query about industry trends, AI/ML applications, or use cases:",
        placeholder="e.g., Conduct market research on the healthcare industry,propose AI/ML use cases, and find relevant datasets for these use cases.?"
    )
    # Generate button
    if st.button("Generate Insights"):
        if not user_input.strip():
            st.warning("Please enter a prompt.")
            return

        st.info("Sending prompt to FastAPI backend...")

        # Send POST request to FastAPI
        try:
            response = requests.post(FASTAPI_URL, json={"prompt": user_input})

            if response.status_code == 200:
                result = response.json()["response"]
                st.success("✅ Response received:")
                st.markdown(result)
            else:
                st.error(f"🚨 Error {response.status_code}: {response.json().get('error', 'Unknown error')}")
        except Exception as e:
            st.error(f"❌ Exception occurred: {str(e)}")

if __name__ == "__main__":
    main()
