import asyncio
import os
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient, load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

load_dotenv()  # 載入 .env

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

llm = ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model="gpt-4o")


def print_optimized_result(agent_response):
    messages = agent_response.get("messages", [])
    steps = []
    final_answer = None

    for message in messages:
        if hasattr(message, "additional_kwargs") and "tool_calls" in message.additional_kwargs:
            for tool_call in message.additional_kwargs["tool_calls"]:
                tool_name = tool_call['function']['name']
                tool_args = tool_call['function']['arguments']
                steps.append(f"調用工具: {tool_name} with arguments {tool_args}")
        elif message.type == "tool":
            steps.append(f"{message.name} 的結果是 {message.content}")
        elif message.type == "ai":
            final_answer = message.content

    print("\n計算過程:")
    for step in steps:
        print(f"- {step}")
    if final_answer:
        print(f"\n最終答案: {final_answer}")


async def main():
    client = MultiServerMCPClient({
        "mcp_server": {
            "url": "http://localhost:8000/mcp",  # 改成你的實際 port
            "transport": "sse",
        },
        # 其他 server 也可在此加入
    })

    tools = await client.get_tools()
    agent = create_react_agent(llm, tools)

    while True:
        try:
            user_input = input("請輸入您的問題 (或輸入 'exit' 退出): ")
            if user_input.lower() == 'exit':
                print("感謝您的使用，再見！")
                break

            agent_response = await agent.ainvoke({'messages': user_input})
            print_optimized_result(agent_response)
        except Exception as e:
            print(f"發生錯誤: {e}")

if __name__ == "__main__":
    asyncio.run(main())
