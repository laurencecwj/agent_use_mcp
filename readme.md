# Tutorial - MCP样例 By Python

### 注意：

生产环境，请参考目录：qwen_agent

以下开始，更偏向于技术原理角度

### 环境准备

#### 1. 需要从github上找到这几个代码库

```bash
# mcp-agent： 这个是主app用的框架，用它来实现query llm及bridge to mcp，也就是找excel读excel的操作都在它这里完成
git clone https://github.com/lastmile-ai/mcp-agent
pip install -e .
# 或者也可以直接pip install mcp-agent

# pandas mcp：这个用来提供读取及分析excel的pandas服务
git clone https://github.com/marlonluo2018/pandas-mcp-server.git
# 别忘了pip install pandas，并且按装读取excel的三方库：pip install openpyxl

# file system mcp：这个用来对local directory做文件查找
git clone https://github.com/ad/mcp-filesystem.git
go build -o mcp-fs main.go
```

其中mcp-filesystem要改一下server.py，找到如下的方法修改mcp.run这行

```python
def main():
    try:
        if not init_logging():
            raise RuntimeError("Failed to initialize logging")

        logger.debug("Starting stdio MCP server...")
        mcp.run(transport="sse") ## 修改这行
    except Exception as e:
        logger.error(f"Server failed to start: {str(e)}")
        logger.debug(traceback.format_exc())
        raise
```

#### 2. 接下来实现我们自己的python app程序

```python
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
                # 这里的Prompt按你自己的改
                message="list all excel names in '/data2/working/pandas-mcp-server/data'." 
            )
            logger.info(f"found: {result}")


            result = await llm.generate_str(
                # 这里的Prompt按你自己的改
                message="""then rename all columns' name to lower case. then find the mean length of the column smiles if any.
                output as
                filename: smiles_mean_length"""
            )
            logger.info(f"calculate mean length: {result}")

if __name__ == "__main__":
    asyncio.run(example_usage())
```



### 运行准备

#### 1. 启动filesystem mcp server

```bash
# 最后那个是允许读写的目录
cd mcp-filesystem
./mcp-fs -transport http -port 8989 /data2/working/pandas-mcp-server/data

2025/07/22 03:23:52 Starting MCP server with streamable HTTP transport on port 8989...
2025/07/22 03:23:52 HTTP server listening on :8989/mcp
```



#### 2. 启动pandas mcp server

```bash
cd pandas-mcp-server
python server.py

[07/22/25 03:25:06] INFO     Logging configured with single log file: /data2/working/pandas-mcp-server/logs/mcp_server.log                           server.py:60
                    INFO     Log file created with permissions: 644                                                                                  server.py:65
INFO:     Started server process [183973]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```



## 运行APP

它将请求LLM及MCP，得到结果

```bash
cd app
python demo.py

# ...... 
# 以上省略屏幕输出

cat results.log

The directory '/data2/working/pandas-mcp-server/data' contains the following Excel files:

* chembl.xlsx
* test_96cpds.xlsx

/data2/working/pandas-mcp-server/data/test_96cpds.xlsx: 20.541666666666668
/data2/working/pandas-mcp-server/data/chembl.xlsx: 63.76939203354298 # 注意这里有时结果不对的，要核对
```






