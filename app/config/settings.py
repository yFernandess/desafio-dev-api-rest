from __future__ import annotations

from pydantic import BaseSettings, Field

_settings = None


class Settings(BaseSettings):
    fast_api_port: int = Field(
        env="FAST_API_PORT",
        default=8000,
        description="Set this locally if you want to start the server on a port other than the default.",
    )

    @classmethod
    def get_settings(cls) -> Settings:
        global _settings
        if _settings is None:
            _settings = Settings()

        return _settings
