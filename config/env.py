import os


def env(name: str, default: str) -> str:
    return os.getenv(name, default)
