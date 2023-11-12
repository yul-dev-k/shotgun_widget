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


def saveSchemaField(schemaName):
    """shotgun의 스키마 필드를 json 형태로 저장해주는 함수입니다.

    Args: 
      스키마명을 매개변수로 받습니다.
    """
    # dict 형태로 받아오나, 가독성이 좋지 않아 JSON 형태로 추출합니다.
    sys.stdout = open(f"schema/{schemaName}.json", "w", encoding="utf-8")
    data = sg.schema_field_read(schemaName)
    json_data = json.dumps(data, indent=4)
    print(json_data)


saveSchemaField('Shot')
saveSchemaField('Task')
