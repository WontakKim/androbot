from typing import List

from pydantic import BaseModel


class SOM(BaseModel):
    # type: str
    # enabled: bool
    bounds: List[float]
    interactive: bool
    content: str | None