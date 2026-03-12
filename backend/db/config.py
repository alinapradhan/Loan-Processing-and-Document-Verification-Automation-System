from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./loan.db"
    ocr_engine: str = "tesseract"
    tesseract_cmd: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
