import requests
import json
from pathlib import Path
from PIL import Image
from io import BytesIO

def generate(text, apiKey):
    url = f"https://api.imgbun.com/png?key={apiKey}&text={text}&color=FFFFFF&size=16"

    response = requests.get(url).content #get the content
    to_json = response.decode('utf-8')
    json_str = json.loads(to_json)

    return json_str['direct_link']