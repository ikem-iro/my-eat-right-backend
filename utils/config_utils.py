from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_ignore_empty=True, extra="ignore"
    )
    # 
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Eat  Right"
    FRONTEND_URL: str = "http://localhost:3000/api/v1/"
    # 
    ACCESS_TOKEN_EXPIRES: int = 60 * 24 * 7
    ACCESS_TOKEN_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    PASSWORD_RESET_TOKEN_EXPIRES: int = 60 * 24
    PASSWORD_RESET_TOKEN_SECRET_KEY: str
    VERIFY_EMAIL_TOKEN_EXPIRES: int = 60 * 24 *3
    VERIFY_EMAIL_TOKEN_SECRET_KEY: str
    # 
    EMAILS_FROM_NAME: str = "Eat Right"
    EMAILS_FROM_MAIL: str 


    # 
    # SMTP_TLS: bool = True
    # SMTP_SSL: bool = False
    # SMTP_PORT: int = 2525
    # SMTP_HOST: str = "sandbox.smtp.mailtrap.io"
    # SMTP_USER: str = "6f67eefc2d4b2a"
    # SMTP_PASSWORD: str = "ff7aed1c675a39"

    # 
    SMTP_PORT: int = 465
    SMTP_ALT_PORT: int = 587
    SMTP_SERVER: str = "smtp.zeptomail.com"
    SMTP_USER: str = "emailapikey"
    SMTP_PASS:str








settings = Settings()