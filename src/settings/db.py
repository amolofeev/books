from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='DB_', env_file='.env', extra='ignore')

    CONNECTION_STRING: str
    CONNECTION_TIMEOUT: int = 20
    MIN_POOL_SIZE: int = 1
    MAX_POOL_SIZE: int = 5
