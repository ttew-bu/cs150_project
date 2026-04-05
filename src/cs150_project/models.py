from pydantic import BaseModel

class SplitterResponse(BaseModel):
    value: float

class ResponderResponse(BaseModel):
    value: bool


class ChatterResponse(BaseModel):
    value: bool