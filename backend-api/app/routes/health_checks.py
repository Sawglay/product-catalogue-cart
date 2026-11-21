from fastapi import APIRouter

from app.models.health_check_dto import HealthCheckDto
from app.services.health_check_service import HealthCheckService


class HealthChecksRoutes:
    def __init__(self, service: HealthCheckService):
        self.service = service
        self.router = APIRouter(prefix="/health", tags=["health"])
        self.router.add_api_route("/live", self.live, methods=["GET"], response_model=HealthCheckDto)
        self.router.add_api_route("/ready", self.ready, methods=["GET"], response_model=HealthCheckDto)

    def live(self) -> HealthCheckDto:
        return self.service.live()

    def ready(self) -> HealthCheckDto:
        return self.service.ready()
