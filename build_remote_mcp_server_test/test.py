
# build remote MCP server

from fastmcp import FastMCP
import random
import json

# create the fast mcp server instance
mcp = FastMCP("Simple Calculator Server")

# tool: add two numbers
@mcp.tool
def add(a: int, b: int) -> int:
    """add two numbers together

    Args:
        a: first number
        b: second number

    Returns:
        the sum of `a` and `b`
    """
    return a + b

# tool: Generate a random number
@mcp.tool
def random_number(min_val: int = 1, max_val: int = 100) -> int:
    """ generate a random number within a range

    Args:
        min_val: minimum value (deafult: 1)
        max_val: maximum value (default: 100)

    Returns:
        A random integer between min_val and max_val 
    """

    return random.randint(min_val, max_val)

@mcp.resource("info://server")
def server_info() -> str:
    """get information about this server"""
    info = {
        "name": "Simple Calculator Server",
        "version": "1.0.0",
        "description": "A basic MCP server with main tools",
        "tools": ["add", "random_number"],
        "author": "Your Name"
    }
    return json.dumps(info, indent=2)


# start the server
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)



