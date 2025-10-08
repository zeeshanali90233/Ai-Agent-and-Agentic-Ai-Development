# pip install fastmcp , this to be done 
from fastmcp import FastMCP

mcp = FastMCP("My MATH MCP Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Return sum."""
    return a + b

@mcp.tool()
def greet(name: str) -> str:
    """Return a greeting."""
    return f"Hello, {name}!"

@mcp.tool()
def compound_interest_calculator(principal: float, rate: float, time: float) -> float:
    """Calculate compound interest."""
    return principal * (1 + rate) ** time

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """Send a greeting email."""
    return f"Sent email to {to} with subject '{subject}' and body '{body}'!"

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)


