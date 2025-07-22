import asyncio
import os

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
#from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM
from mcp_agent.workflows.llm.augmented_llm_google import GoogleAugmentedLLM

app = MCPApp(name="hello_world_agent")

async def example_usage():
    async with app.run() as mcp_agent_app:
        logger = mcp_agent_app.logger
        # This agent can read the filesystem or fetch URLs
        finder_agent = Agent(
            name="finder",
            instruction="""You can read local files or fetch URLs.
                Return the requested information when asked.""",
            server_names=["filesystem", "pandas"], # MCP servers this Agent can use
        )

        async with finder_agent:
            # Automatically initializes the MCP servers and adds their tools for LLM use
            tools = await finder_agent.list_tools()
            logger.info(f"Tools available:", data=tools)

            # Attach an OpenAI LLM to the agent (defaults to GPT-4o)
            llm = await finder_agent.attach_llm(GoogleAugmentedLLM)

            # This will perform a file lookup and read using the filesystem server
            result = await llm.generate_str(
                message="list all excel names in '/data2/working/pandas-mcp-server/data'."
            )
            logger.info(f"found: {result}")
            with open("./results.log", 'a') as wfl:
                wfl.write(f"{result}\n\n")

            result = await llm.generate_str(
                message="""then rename all columns' name to lower case. then find the mean length of the column smiles if any.
                output as     
                filename: smiles_mean_length"""
            )
            logger.info(f"calculate mean length: {result}")
            with open("./results.log", 'a') as wfl:
                wfl.write(f"{result}\n\n")


if __name__ == "__main__":
    asyncio.run(example_usage())

