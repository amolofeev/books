from typing import Optional

from prometheus_client import Counter, Summary
from pydantic_settings import BaseSettings, SettingsConfigDict


class PodInfo(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='POD_', env_file='.env', extra='ignore')
    name: Optional[str]
    ip: Optional[str]
    node: Optional[str]
    namespace: Optional[str]
    image: Optional[str]
    version: Optional[str]


class APM(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='ELASTIC_APM_', env_file='.env', extra='ignore')
    ENABLED: bool


class LogConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='LOG_', env_file='.env', extra='ignore')
    LEVEL: str = 'INFO'
    FORMATTER: Optional[str] = 'json'
    apm: APM = APM()
    pod: PodInfo = PodInfo()

    EXTRA: dict = {
        **{f'pod.{k}': v for k, v in pod.model_dump().items()}
    }


class Metrics:
    requests_count = Counter(
        'requests_count', 'rps',
        ['url', 'method', 'status_code']
    )
    requests_latency = Summary(
        'requests_latency', 'request latency',
        ['url', 'method', 'status_code']
    )
