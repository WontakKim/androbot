from fastmcp import FastMCP

from .client import AppiumClient
from .util.utils import execute_command

mcp = FastMCP('appium')

client: AppiumClient = AppiumClient()

@mcp.tool()
def get_available_device_ids() -> str:
    """
    Get a list of available device ids that can be connected to.

    Returns:
        Comma(,) separated string of device ids that are online
    """
    cmd = 'adb devices'
    result = execute_command(cmd)

    device_ids = []

    for line in result.splitlines()[1:]:
        device_id = line.strip().split()[0]
        device_ids.append(device_id)

    return ','.join(device_ids)

@mcp.tool()
def connect_device(device_id: str) -> str:
    """
    Connect to a device by device id

    Args:
        device_id (str): device id

    Returns:
        Execution result message
    """
    client.connect(device_id)
    return 'ok'

@mcp.tool()
def is_app_installed(package_name: str) -> str:
    """
    Checks whether the application specified by `package_name` is installed on the device.

    Args:
        package_name (str): package name

    Returns:
        execution result
    """
    result = client.is_app_installed(package_name)
    return 'installed' if result else 'not installed'

@mcp.tool()
def activate_app(package_name: str) -> str:
    """
    Activates the application if it is not running or is running in the background.

    Args:
        package_name: the application id to be activated

    Returns:
        execution result
    """
    client.activate_app(package_name)
    return 'ok'

@mcp.tool()
def get_current_screen_info() -> str:
    """
    Get current screen layout information

    Returns:
        screen layout in format `type@x1,y1,x2,y2:content` where:
            - type: element type - `button`(clickable), `scroll`(scrollable), `view`(display only)
            - x1,y1,x2,y2: bounding box coordinates
            - content: text content(empty if no content)

            elements are separated by semicolons(;)
    """
    return client.get_current_screen_llm_string()

@mcp.tool()
def tap_x_y(x: int, y: int) -> str:
    """
    Tap `x` and `y`

    Args:
        x (int): x coordinate
        y (int): y coordinate

    Returns:
        execution result
    """
    client.tap_x_y(x, y)
    return 'ok'

@mcp.tool()
def swipe(start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int) -> str:
    """
    Swipe `start_x` and `start_y` to `end_x` and `end_y`

    Args:
        start_x (int): start x coordinate
        start_y (int): start y coordinate
        end_x (int): end x coordinate
        end_y (int): end y coordinate
        duration_ms (int): duration in milliseconds

    Returns:
        execution result
    """
    client.swipe(start_x, start_y, end_x, end_y, duration_ms)
    return 'ok'
