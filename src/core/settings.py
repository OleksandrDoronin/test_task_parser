import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


env_file = os.getenv('ENV_FILE', '.env')
load_dotenv(dotenv_path=env_file)


class Settings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    model_config = SettingsConfigDict(
        env_file=env_file,
    )

    @property
    def database_url(self) -> str:
        return (
            f'postgresql://'
            f'{self.postgres_user}:'
            f'{self.postgres_password}@'
            f'{self.postgres_host}:{self.postgres_port}/'
            f'{self.postgres_db}'
        )


settings = Settings()  # noqa