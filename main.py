from pathlib import Path
from openai import OpenAI
import json


client = OpenAI(api_key=json.load(open('openai.json'))["apikey"])
config = json.load(open('config.json'))
docs_path = Path(config["docspath"])


def traducir(texto, idioma):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Translate the following text into {idioma}: {texto}\n"
            }
        ],
        model="gpt-3.5-turbo"
    )
    return chat_completion.choices[0].message.content


for arch in docs_path.glob("*.txt"):
    with open(arch) as f:
        texto = f.readlines()
        for idioma, cod_idioma in config["idiomas"].items():
            with open(f"{docs_path}/{arch.stem}_{cod_idioma}.txt", "w", encoding="utf-8") as f2:
                f2.writelines(traducir(texto, idioma))
