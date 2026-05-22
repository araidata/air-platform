from pydantic import BaseModel, ConfigDict


class ApiModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class StrictApiModel(BaseModel):
    model_config = ConfigDict(extra="forbid")
