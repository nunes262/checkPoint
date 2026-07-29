from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configurações centrais da aplicação.
    Os valores são lidos automaticamente do arquivo .env na raiz do projeto.
    """

    # Banco de dados
    database_url: str = "postgresql://usuario:senha@localhost:5432/game_diary"

    # JWT / autenticação
    secret_key: str = "changeme"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # RAWG — deixar vazio até você ter a credencial
    rawg_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
