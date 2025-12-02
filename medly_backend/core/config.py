from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://medly:medly@localhost:5432/medlydb"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
