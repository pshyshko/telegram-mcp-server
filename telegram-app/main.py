from smolagents import LiteLLMModel, CodeAgent, ToolCollection
import asyncio

model = LiteLLMModel(
  model_id='ollama_chat/qwen3:14b'
)
async def main():

    with ToolCollection.from_mcp({"url": "http://127.0.0.1:8050/mcp", "transport": "streamable-http"}, trust_remote_code=True) as tool_collection:
      agent = CodeAgent(tools=[*tool_collection.tools], add_base_tools=True, model=model, additional_authorized_imports=["json"])
      agent.run("Create a new reservation today on 11.00 and return id")

if __name__ == "__main__":
    asyncio.run(main())