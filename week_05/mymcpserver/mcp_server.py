from mcp.server.mcpserver import MCPServer

mcp=MCPServer("saif_mcp_server")

@mcp.tool()
def saif(a:int , b:int):
    return a+b+100

if __name__=="__main__":
    mcp.run()