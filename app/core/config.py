import os

SECRET_KEY: str = os.getenv("BULBE_SECRET_KEY", "troque-esta-chave-em-producao-bulbe-2026")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("BULBE_TOKEN_MINUTOS", "30"))

DATABASE_URL: str = os.getenv("BULBE_DATABASE_URL", "sqlite:///./bulbe.db")
