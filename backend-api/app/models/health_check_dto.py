from pydantic import BaseModel


class HealthCheckDto(BaseModel):
    status: str
