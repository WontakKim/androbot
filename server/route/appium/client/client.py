from io import BytesIO

import numpy as np
from PIL import Image
from appium.options.android import UiAutomator2Options
from appium import webdriver
from appium.webdriver import appium_service
from appium.webdriver.appium_service import AppiumService
from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from server.route.appium.screen.screen import Screen, from_xml_string, minify, from_xml_path
from server.route.appium.util.utils import create_annotated_image


class AppiumClient:
    def __init__(self):
        self.driver: WebDriver | None = None

    def connect(self, device_id: str):
        self.close()

        options = UiAutomator2Options()
        options.platform_name = 'Android'
        options.device_name = device_id
        options.set_capability('ignoreUnimportantViews', True)
        self.driver = webdriver.Remote(
            'http://localhost:4723',
            options=options
        )

    def close(self):
        if self.driver is not None:
            self.driver.close()
            self.driver = None

    def is_app_installed(self, package_name: str) -> bool:
        if self.driver is None:
            raise 'device is not connected'
        return self.driver.is_app_installed(package_name)

    def activate_app(self, package_name: str):
        if self.driver is None:
            raise 'device is not connected'
        self.driver.activate_app(package_name)

    def get_current_screen(self):
        if self.driver is None:
            raise 'device is not connected'

        image_bytes = self.driver.get_screenshot_as_png()
        pil_image = Image.open(BytesIO(image_bytes))

        self.driver.switch_to.context('NATIVE_APP')
        wait = WebDriverWait(self.driver, 10)
        xml_string = self.driver.page_source
        screen = from_xml_string(xml_string)
        # screen = from_xml_path('/Users/wontak/desktop/test2.xml')
        elements = screen.elements(False)
        bboxes = [element.bounds for element in elements]

        # print(xml_string)

        bboxes = np.array(bboxes)
        annotated_image = create_annotated_image(pil_image, bboxes)
        annotated_image.show()

        soms = minify(screen)
        bboxes = [som.bounds for som in soms]
        bboxes = np.array(bboxes)
        annotated_image = create_annotated_image(pil_image, bboxes)
        annotated_image.show()

if __name__ == '__main__':
    client = AppiumClient()
    client.connect('R3CY406N0PL')
    client.get_current_screen()
