from typing import List

from pydantic import BaseModel


class SOM(BaseModel):
    bounds: List[float]
    interactive: bool
    clickable: bool
    scrollable: bool
    selected: bool
    content: str | None

    def to_llm_string(self):
        name = 'button' if self.clickable or self.selected else \
            'scroll' if self.scrollable else 'view'
        llm_string = f'{name}@{','.join(map(lambda x: f"{x:g}", self.bounds))}:{self.content}'
        return llm_string