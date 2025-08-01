import json
from io import BytesIO
from typing import List

import numpy as np
from PIL import Image
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.webdriver import WebDriver

from .data.som import SOM
from .screen.screen import from_xml_string, minify
from .util.utils import create_annotated_image


class AppiumClient:
    def __init__(self):
        self.driver: WebDriver | None = None

    def connect(self, device_id: str):
        self.close()

        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.device_name = device_id
        options.set_capability('ignoreUnimportantViews', True)
        options.set_capability('autoGrantPermissions', True)
        options.set_capability('skipDeviceInitialization', False)
        self.driver = webdriver.Remote(
            'http://localhost:4723',
            options=options
        )

    def close(self):
        if self.driver is not None:
            self.driver.close()
            self.driver = None

    def is_connected(self) -> bool:
        return self.driver is not None

    def validate_device_connection(self):
        if not self.is_connected():
            raise 'device is not connected'

    def is_app_installed(self, package_name: str) -> bool:
        self.validate_device_connection()
        return self.driver.is_app_installed(package_name)

    def activate_app(self, package_name: str):
        self.validate_device_connection()
        self.driver.activate_app(package_name)

    def tap_x_y(self, x: int, y: int):
        self.validate_device_connection()
        self.driver.tap([(x, y)])

    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, duration_ms: int=1000):
        self.validate_device_connection()
        self.driver.swipe(start_x, start_y, end_x, end_y, duration_ms)

    def get_current_screen(self) -> List[SOM]:
        self.validate_device_connection()

        # image_bytes = self.driver.get_screenshot_as_png()
        # pil_image = Image.open(BytesIO(image_bytes))
        # xml_string = self.driver.page_source
        # print(xml_string)
        #
        # screen = from_xml_string(xml_string)
        # # screen = from_xml_path('/Users/wontak/desktop/test2.xml')
        # elements = screen.elements(False)
        # bboxes = [element.bounds for element in elements]
        #
        # # print(xml_string)
        #
        # bboxes = np.array(bboxes)
        # annotated_image = create_annotated_image(pil_image, bboxes)
        # annotated_image.show()
        #
        # soms = minify(screen)
        # bboxes = [som.bounds for som in soms]
        # bboxes = np.array(bboxes)
        # annotated_image = create_annotated_image(pil_image, bboxes)
        # annotated_image.show()
        #
        # json_list = [som.model_dump() for som in soms]
        # print(json.dumps(json_list, ensure_ascii=False, indent=2))

        xml_string = self.driver.page_source
        screen = from_xml_string(xml_string)
        return minify(screen)

    def get_current_screen_llm_string(self) -> str:
        return ';'.join([som.to_llm_string() for som in self.get_current_screen()])
