from setuptools import setup, find_packages

setup(
    name='AI_FastAPI_MCP',
    version='0.1',
    packages=find_packages(include=['langgraph-mcp', 'langgraph-mcp.*']),  # 只找langgraph相關套件
)
