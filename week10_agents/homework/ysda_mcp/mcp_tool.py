from mcp.server.fastmcp import FastMCP
from parser import parse_lectures, parse_tasks
mcp = FastMCP("DataSchoolParser")



@mcp.tool()
def parse_tasks_tool() -> list[dict]:
    return parse_tasks()

@mcp.tool()
def parse_lectures_tool() -> list[dict]:
    return parse_lectures()


if __name__ == "__main__":
    mcp.run()