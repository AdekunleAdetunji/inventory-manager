#!/usr/bin/python3
"""
This module contains validator for environment variables in the project .env file
"""
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from typing import Literal


class DBEnvironmentVariableValidator(BaseSettings):
    """Database Environment variable validator class"""

    model_config = SettingsConfigDict(env_file=".env")

    DB_NAME: str
    DB_USER: str
    DB_HOST: str
    DB_PORT: int
    DB_PASSWORD: str


@lru_cache
def get_db_env_vars():
    """return database environment variables validator"""
    return DBEnvironmentVariableValidator()
