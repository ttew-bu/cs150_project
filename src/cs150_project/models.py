from pydantic import BaseModel, ConfigDict


# very simple, but at least force the type of value for a specific interaction
class SplitterResponse(BaseModel):
    value: float
    reason: str
    model_config = ConfigDict(extra="forbid")


class ResponderResponse(BaseModel):
    value: bool
    reason: str
    model_config = ConfigDict(extra="forbid")


class ChatterResponse(BaseModel):
    value: str
    reason: str
    model_config = ConfigDict(extra="forbid")
