from dotenv import load_dotenv

import os


class Settings():

    def __init__(self) -> None:
        load_dotenv(".env")

        self.APP_TOKEN = os.getenv("APP_TOKEN")
        self.API_PORT = int(os.getenv("API_PORT"))


settings = Settings()
