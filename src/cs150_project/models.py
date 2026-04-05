from pydantic import BaseModel


# very simple, but at least force the type of value for a specific interaction
class SplitterResponse(BaseModel):
    value: float

class ResponderResponse(BaseModel):
    value: bool

class ChatterResponse(BaseModel):
    value: bool