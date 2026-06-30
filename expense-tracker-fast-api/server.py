
from fastmcp import FastMCP
from main import app

# convert fast api to mcp server
mcp = FastMCP.from_fastapi(
    app=app,
    name="Expense Tracker server",
)

if __name__ == "__main__":
    mcp.run()