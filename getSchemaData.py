import shotgun_api3
import sys
import json
from dotenv import load_dotenv
import os

# shotgun의 schema 데이터를 JSON 형태로 받아오는 스크립트입니다.

load_dotenv()

URL = os.environ.get("BASE_URL")
LOGIN = os.environ.get("LOGIN")
PW = os.environ.get("PASSWORD")

sg = shotgun_api3.Shotgun(URL, login=LOGIN, password=PW)

# dict 형태로 받아오나, 가독성이 좋지 않습니다.
sys.stdout = open("schema.json", "w", encoding="utf-8")
data = sg.schema_field_read("Shot")


json_object = json.dumps(data, indent=4)

print(json_object)
