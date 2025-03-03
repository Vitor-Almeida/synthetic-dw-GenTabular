from gentabular import dimensoes
from dotenv import load_dotenv
import os
import json

def main():

    with open("data/vemma/schema.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    load_dotenv(".env.local")
    api_key = os.getenv("API_KEY")

    x = dimensoes.vendedores(50)


if __name__ == "__main__":
    main()