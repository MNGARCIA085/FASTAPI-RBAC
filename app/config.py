from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Auth API"
    admin_email: str = "mail@mail.com"
    DB_USER:str
    DB_URL:str
    DB_URL_TEST:str
    SECRET_KEY: str
    

    class Config:
        env_file = ".env"


settings = Settings()



"""

gnerar la secret key

# to get a string like this run:
# openssl rand -hex 32

"""