from pydantic import BaseModel


class AppDetails(BaseModel):
    app_id: str
    title: str
    summary: str
    installs: int
    score: float
    ratings: int
    reviews: int
    version: str
    updated: str

    def to_json(self) -> str:
        return self.model_dump_json(indent=2)

    def to_dict(self) -> dict:
        return self.model_dump()
