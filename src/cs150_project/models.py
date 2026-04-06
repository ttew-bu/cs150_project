from pydantic import BaseModel


# very simple, but at least force the type of value for a specific interaction
class SplitterResponse(BaseModel):
    value: float
    reason: str


class ResponderResponse(BaseModel):
    value: bool
    reason: str


class ChatterResponse(BaseModel):
    value: str
    reason: str
