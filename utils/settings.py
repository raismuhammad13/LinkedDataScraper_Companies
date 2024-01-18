import os
from dotenv import dotenv_values, load_dotenv

load_dotenv()

def get_setting():
    config = {"email":os.getenv("Email"),
              "password": os.getenv("Password")}
    return config

