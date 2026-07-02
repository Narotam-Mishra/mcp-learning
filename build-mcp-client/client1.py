
# build your own mcp client

import asyncio
from pathlib import Path

from langchain_mcp_adapters.client import MultiServerMCPClient

SERVER_PROJECT = Path(__file__).resolve().parent.parent / "basic-math-mcp-local-server"

SERVERS = {
    "math_local_mcp_server": {
      "transport": "stdio",
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--project",
        str(SERVER_PROJECT),
        "fastmcp",
        "run",
        str(SERVER_PROJECT / "main.py")
      ]
    }
}

async def main():
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()
    print(f"tools: {tools}")


if __name__ == '__main__':
    asyncio.run(main())
