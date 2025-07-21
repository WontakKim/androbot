from fastmcp import FastMCP

from route.gplay.mcp import mcp as gplay_mcp
from route.appium.mcp import mcp as appium_mcp

mcp = FastMCP('androbot')

mcp.mount(gplay_mcp)
# mcp.mount(appium_mcp)

if __name__ == '__main__':
    mcp.run()