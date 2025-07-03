import json
import subprocess

import requests
from mcp.server import FastMCP

from adb_utils import get_installed_package_names, open_app, tap_x_y, take_screenshot, get_screen_size


# class AppiumService:
#     def __init__(self, url: str):
#         self.url = url
#         self.webdriver = None
#
#     def connect_device(self, device_id: str) -> str:
#         """ Connect to emulator """
#         try:
#             options = UiAutomator2Options()
#             options.platform_name = "Android"
#             options.device_name = device_id
#             options.udid = device_id
#             options.automation_name = "UiAutomator2"
#
#             self.webdriver = webdriver.Remote(self.url, options=options)
#             return f"Successfully connected to {device_id}"
#         except Exception as e:
#             print(str(e))
#             return f"Failed to connect: {str(e)}"
#
#     def is_connected(self) -> bool:
#         return self.webdriver is not None
#
#     def disconnect(self) -> str:
#         if self.webdriver is not None:
#             try:
#                 self.webdriver.quit()
#                 self.webdriver = None
#             except Exception as e:
#                 return f"Error during disconnection: {str(e)}"
#         return f"Webdriver successfully disconnected"
#
#     def __enter__(self):
#         if not self.is_connected():
#             self.connect_device()
#         return self.webdriver
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         self.disconnect()
#         if exc_type:
#             print(f"Exception occurred: {exc_type.__name__}: {exc_val}")

def omniparser(url: str, image_path: str) -> str:
    with open(image_path, "rb") as file:
        headers = {}
        form = {'file': file}
        response = requests.post(
            url='put omniparserurl',
            headers=headers,
            files=form
        )
        return response.text


# appium_service = AppiumService('http://127.0.0.1:4723')
mcp = FastMCP("androbot")


@mcp.tool()
async def get_current_android_devices() -> str:
    """ Get current connected android device list """
    try:
        result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[1:]

        devices = []
        for line in lines:
            if line.strip() and 'device' in line:
                device_id = line.split()[0]
                devices.append(device_id)

        return ','.join(devices)
    except Exception as e:
        return f"Failed to get current android device list: {str(e)}"

@mcp.tool()
def get_installed_apps(device_id: str) -> str:
    """ Get installed apps list """
    try:
        package_names = get_installed_package_names(device_id)
        return json.dumps(package_names)
    except Exception as e:
        return f"Failed to get installed apps list: {str(e)}"

@mcp.tool()
def open_android_app(device_id: str, package_name: str) -> str:
    """ Open app """
    try:
        open_app(device_id, package_name)
        return f"Successfully opened app: {package_name}"
    except Exception as e:
        return f"Failed to open app: {str(e)}"

@mcp.tool()
def get_android_phsical_screen_size(device_id: str) -> str:
    """ Get android physical screen size """
    try:
        return get_screen_size(device_id)
    except Exception as e:
        return f"Failed to get screensize: {str(e)}"

@mcp.tool()
def tap_android_x_y(device_id: str, x: int, y: int) -> str:
    """ Tap x y """
    try:
        tap_x_y(device_id, x, y)
        return f"Successfully tapped {x} {y}"
    except Exception as e:
        return f"Failed to tapped {x} {y}"

@mcp.tool()
def get_current_android_screen_info(device_id: str) -> str:
    """ Get current android screen

    """
    try:
        image_path = take_screenshot(device_id)
        return omniparser(image_path)
    except Exception as e:
        return f"Failed to get current android screen: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport='stdio')
    # get_installed_apps('R3CY406N0PL')