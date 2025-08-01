import os
import sys

from fastmcp import FastMCP

from route.gplay.mcp import mcp as gplay_mcp
from route.appium.mcp import mcp as appium_mcp

# root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, root_dir)

mcp = FastMCP('androbot')

mcp.mount(gplay_mcp)
mcp.mount(appium_mcp)

if __name__ == '__main__':
    mcp.run()


# if __name__ == '__main__':
#     from server.route.appium.client import AppiumClient
#     client = AppiumClient()
#     client.connect('R3CY406N0PL')
#     print(client.get_current_screen_llm_string())