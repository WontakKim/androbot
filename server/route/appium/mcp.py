from fastmcp import FastMCP

from .client.client import AppiumClient
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
