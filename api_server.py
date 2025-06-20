from fastapi import FastAPI, Request
from pydantic import BaseModel
import asyncio
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


# 初始化
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_INPUT_LENGTH = os.getenv("MAX_INPUT_LENGTH", 8000)
llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model="gpt-4o-mini")

app = FastAPI()
agent = None

class Query(BaseModel):
    question: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或改成 ["http://localhost:3000"] 更安全
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    global agent
    client = MultiServerMCPClient({
        "tool_server": {
            "url": "http://localhost:8000/mcp",
            "transport": "sse",
        }
    })
    tools = await client.get_tools()
    print(f"已加載 {len(tools)} 個工具")
    print(tools)
    agent = create_react_agent(llm, tools)

def print_optimized_result(agent_response):
    messages = agent_response.get("messages", [])
    steps = []
    final_answer = None

    for message in messages:
        if hasattr(message, "additional_kwargs") and "tool_calls" in message.additional_kwargs:
            for tool_call in message.additional_kwargs["tool_calls"]:
                tool_name = tool_call['function']['name']
                print(f"調用工具: {tool_name}")
                
                tool_args = tool_call['function']['arguments']
                steps.append(f"調用工具: {tool_name} with arguments {tool_args}")
        elif message.type == "tool":
            steps.append(f"{message.name} 的結果是 {message.content}")
        elif message.type == "ai":
            final_answer = message.content

    print("\n思考過程:")
    for step in steps:
        print(f"- {step}")
    if final_answer:
        return f"\n最終結果: {final_answer}"


@app.post("/ask")
async def ask(query: Query):
    try:
        max_input_length = MAX_INPUT_LENGTH
        response = await agent.ainvoke({
            "messages": query.question[:max_input_length]
        })
        import pprint
        pprint.pprint(response["messages"])
        final_answer = print_optimized_result(response)
        return {"response": final_answer}
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('api_server:app', host="0.0.0.0", port=8001)