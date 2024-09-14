import aioprometheus
from pydantic_settings import BaseSettings, SettingsConfigDict


class PodInfo(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="POD_", env_file=".env", extra="ignore")
    name: str | None
    ip: str | None
    node: str | None
    namespace: str | None
    image: str | None
    version: str | None


class APM(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="ELASTIC_APM_", env_file=".env", extra="ignore")
    ENABLED: bool


class LogConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LOG_", env_file=".env", extra="ignore")
    LEVEL: str = "INFO"
    FORMATTER: str | None = "json"
    apm: APM = APM()
    pod: PodInfo = PodInfo()

    EXTRA: dict = {
        **{f"pod.{k}": v for k, v in pod.model_dump().items()},
    }


class Metrics:
    http_requests_count = aioprometheus.Counter(
        "http_requests_count",
        "http_requests_count",
    )
    http_requests_latency = aioprometheus.Summary(
        "http_requests_latency",
        "http_requests_latency",
    )

    @staticmethod
    def render() -> tuple[bytes, dict]:
        return aioprometheus.render(
            aioprometheus.REGISTRY,
            [],
        )
