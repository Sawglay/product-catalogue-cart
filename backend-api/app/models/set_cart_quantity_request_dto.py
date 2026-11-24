from pydantic import BaseModel, ConfigDict, Field


class SetCartQuantityRequestDto(BaseModel):
    model_config = ConfigDict(extra="forbid")
    quantity: int = Field(strict=True, ge=0, le=2147483647)
