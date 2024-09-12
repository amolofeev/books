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
    requests_count = aioprometheus.Counter(
        "requests_count", "rps",
        # ["url", "method", "status_code"]  # noqa: ERA001
    )
    requests_latency = aioprometheus.Summary(
        "requests_latency", "request latency",
        # ["url", "method", "status_code"]   # noqa: ERA001
    )

    @staticmethod
    def render() -> tuple[bytes, dict]:  # noqa: PLR6301
        return aioprometheus.render(
            aioprometheus.REGISTRY, [],
        )
