import os
import subprocess
import tempfile
from typing import List
from uuid import uuid4


def execute_adb_command(command: str) -> str:
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr)
    return result.stdout.strip()


def get_installed_package_names(device_id: str) -> List[str]:
    cmd = f'adb -s {device_id} shell pm list packages -3'
    result = execute_adb_command(cmd)

    package_names = []

    for line in result.split('\n'):
        if line.startswith('package:'):
            package_name = line.split(':', 1)[1].strip()
            package_names.append(package_name)

    return package_names

def get_app_name(device_id: str, package_name: str):
    try:
        cmd = f'adb -s {device_id} shell pm dump {package_name}'
        result = execute_adb_command(cmd)

        lines = result.split('\n')
        for i, line in enumerate(lines):
            if 'applicationLabel' in line and i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if '=' in next_line:
                    return next_line.split('=', 1)[1].strip()
    except:
        pass

    return 'unknown'

def open_app(device_id: str, package_name: str):
    cmd = f'adb -s {device_id} shell monkey -p {package_name} -c android.intent.category.LAUNCHER 1'
    execute_adb_command(cmd)

def tap_x_y(device_id: str, x: int, y: int):
    cmd = f'adb -s {device_id} shell input tap {x} {y}'
    execute_adb_command(cmd)

def take_screenshot(device_id: str) -> str:
    temp_dir = tempfile.gettempdir()
    temp_dir = os.path.join(temp_dir, "androbot")

    filename = f"screenshot_{uuid4().hex}.png"
    filepath = os.path.join(temp_dir, filename)

    os.makedirs(temp_dir, exist_ok=True)

    cmd = f'adb -s {device_id} shell screencap -p > {filepath}'
    execute_adb_command(cmd)
    return filepath

def get_screen_size(device_id: str):
    cmd = f'adb -s {device_id} shell wm size'
    result = execute_adb_command(cmd)
    return result

if __name__ == '__main__':
    print(take_screenshot("R3CY406N0PL"))