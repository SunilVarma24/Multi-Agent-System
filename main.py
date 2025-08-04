# main.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from src.graph import get_agent_workflow

# Initialize FastAPI app
app = FastAPI(
    title="Market Research & Use Case Generation Multi-Agent System",
    description="An API for conducting industry research and generating AI/ML use cases",
    version="1.0.0"
)

# Get the compiled agent workflow
agent_workflow = get_agent_workflow()

# Request model for POST endpoints
class PromptRequest(BaseModel):
    prompt: str

# Endpoint
@app.post("/generate_insights")
async def generate_insights(request: PromptRequest):
    try:
        result = await agent_workflow.ainvoke({
            "messages": [HumanMessage(content=request.prompt)],
            "sender": "human"
        })
        return JSONResponse(content={"response": result["messages"][-1].content})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Run using: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)