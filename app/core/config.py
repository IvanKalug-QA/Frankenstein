from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = 'Default'
    database_url: str
    secret: str = 'SECRET'
    algorithm: str

    class Config:
        env_file = '.env'


settings = Settings()
