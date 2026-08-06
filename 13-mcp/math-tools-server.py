from fastmcp import FastMCP

mcp = FastMCP("MATH and Email MCP Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Return sum."""
    return a + b

@mcp.tool()
def search(query:str) -> str:
    """Searches on Internet."""
    
    return "Nothing Found"

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email."""
    
    return f"Sent email to {to} with subject '{subject}' and body '{body}'!"

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)


