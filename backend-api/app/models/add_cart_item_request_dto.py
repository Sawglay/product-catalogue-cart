from pydantic import BaseModel, ConfigDict, Field


class AddCartItemRequestDto(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    productCode: str = Field(min_length=1, max_length=25, pattern=r"^\S+$")
    quantity: int = Field(strict=True, ge=1, le=2147483647)
