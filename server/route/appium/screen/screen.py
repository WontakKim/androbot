from typing import List, Tuple
from xml.etree import ElementTree

from ..data.som import SOM
from ..screen.ui_element import UiElement, from_xml_element
from ..util.box_utils import get_occluded_indices


class Screen:
    def __init__(self, xml_string: str):
        self.xml_string = xml_string

        self.tree = ElementTree.fromstring(xml_string)

        self._rotation: float = float(self.tree.attrib['rotation'])
        self._width: float = float(self.tree.attrib['width'])
        self._height: float = float(self.tree.attrib['height'])

        self._children: List['UiElement'] = [
            from_xml_element(element)
            for element in self.tree
        ]

    def elements(self, hierarchy: bool=True):
        return self._children if hierarchy \
            else sum([child.flatten() for child in self._children], [])

def from_xml_string(xml_string: str) -> Screen:
    return Screen(xml_string)

def from_xml_path(path: str) -> Screen:
    with open(path, 'r', encoding='utf-8') as file:
        return from_xml_string(file.read())

def minify(screen: Screen) -> List[SOM]:
    def _minify(element: UiElement, depth: int=0) -> Tuple[List[UiElement], List[SOM]]:
        to_return_concats = []
        to_return_soms = []

        children = element.children

        if children:
            # remove occluded children
            (bounds, drawing_orders) = zip(*[(child.bounds, child.drawing_order) for child in element.children])
            occluded_indices = set(get_occluded_indices(bounds, drawing_orders))

            for i, child in enumerate(element.children):
                if i in occluded_indices:
                    continue

                (concats, soms) = _minify(child, depth=depth+1)
                to_return_concats.extend(concats)
                to_return_soms.extend(soms)

        if element.is_meaningful:
            # sanitize
            to_return_concats.insert(0, element)
            to_return_concats = [item for item in to_return_concats if item.text.strip()]

            if element.is_scrollable:
                soms = [SOM(
                    bounds=item.bounds,
                    interactive=item.is_interactive,
                    clickable=item.clickable,
                    scrollable=item.is_scrollable,
                    content=item.text,
                    selected=item.selected,
                ) for item in to_return_concats if item.text.strip()]
            else:
                concat_text = '|'.join(item.text.strip() for item in to_return_concats)
                soms = [SOM(
                    bounds=element.bounds,
                    interactive=element.is_interactive,
                    clickable=element.clickable,
                    scrollable=element.scrollable,
                    content=concat_text,
                    selected=element.selected
                )]

            to_return_concats.clear()
            to_return_soms = soms + to_return_soms
        elif element.text.strip():
            to_return_concats.insert(0, element)

        return to_return_concats, to_return_soms

    elements = screen.elements(hierarchy=True)
    to_return_soms = sum([_minify(element)[1] for element in elements], [])
    return to_return_soms