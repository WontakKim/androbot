import re
from typing import Tuple, List
from xml.etree import ElementTree

from pydantic import BaseModel


class UiElement(BaseModel):
    index: int
    package_name: str
    class_name: str
    text: str
    checkable: bool
    checked: bool
    clickable: bool
    enabled: bool
    focusable: bool
    focused: bool
    password: bool
    scrollable: bool
    selected: bool
    bounds: List[float]
    displayed: bool
    drawing_order: int
    content_desc: str
    children: List['UiElement']

    @property
    def is_meaningful(self):
        return self.displayed and (
            self.is_clickable or
            self.is_scrollable
        )

    @property
    def is_clickable(self):
        return self.clickable or self.selected

    @property
    def is_scrollable(self):
        return (
            self.scrollable or
            # React native bottom sheet
            'SeekBar' in self.class_name
        )

    @property
    def is_interactive(self) -> bool:
        return self.clickable or self.is_scrollable

    def is_visible(self) -> bool:
        return self.displayed

    def to_llm_string(self) -> str:
        return self._to_llm_string()

    def _to_llm_string(self, depth: int=0) -> str:
        llm_string = f'§{depth}{self.class_name}@{','.join(map(str, self.bounds))}:{self.text}'
        sub_llm_strings = [child._to_llm_string(depth + 1) for child in self.children]
        return ';'.join([llm_string, *sub_llm_strings])

    #
    def to_simple_tag(self) -> str:
        if self.children:
            return 'L'

        pass

    def flatten(self) -> List['UiElement']:
        return [self] + sum([child.flatten() for child in self.children], [])

def from_xml_element(element: ElementTree.Element) -> UiElement:
    def opt_int(attrs: dict[str, str], key: str) -> int:
        value = opt_str(attrs, key)
        return int(value)

    def opt_bool(attrs: dict[str, str], key: str) -> bool:
        value = opt_str(attrs, key)
        return value.lower() in ('yes', 'true', '1')

    def opt_str(attrs: dict[str, str], key: str) -> str:
        return attrs[key] if key in attrs else ''

    def opt_bounds(attrs: dict[str, str], key: str) -> List[float]:
        value = opt_str(attrs, key)
        coords = re.findall(r'\d+', value)
        return list(map(float, coords))


    children = [from_xml_element(child) for child in element]

    return UiElement(
        index=opt_int(element.attrib, 'index'),
        package_name=opt_str(element.attrib, 'package'),
        class_name=element.attrib['class'],
        text=element.attrib['text'],
        checkable=opt_bool(element.attrib, 'checkable'),
        checked=opt_bool(element.attrib, 'checked'),
        clickable=opt_bool(element.attrib, 'clickable'),
        enabled=opt_bool(element.attrib, 'enabled'),
        focusable=opt_bool(element.attrib, 'focusable'),
        focused=opt_bool(element.attrib, 'focused'),
        password=opt_bool(element.attrib, 'password'),
        scrollable=opt_bool(element.attrib, 'scrollable'),
        selected=opt_bool(element.attrib, 'selected'),
        bounds=opt_bounds(element.attrib, 'bounds'),
        displayed=opt_bool(element.attrib, 'displayed'),
        drawing_order=opt_int(element.attrib, 'drawing-order'),
        content_desc=opt_str(element.attrib, 'content-desc'),
        children=children,
    )
