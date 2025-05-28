from pydantic_settings import BaseSettings, SettingsConfigDict

class Environmentals(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION_NAME: str
    MODEL_SONNET: str
    MODEL_HAIKU: str
    MODEL_DEEPSEEK: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

env = Environmentals()