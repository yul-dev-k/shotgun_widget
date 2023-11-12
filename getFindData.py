import shotgun_api3
import sys
import json
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.environ.get("BASE_URL")
LOGIN = os.environ.get("LOGIN")
PW = os.environ.get("PASSWORD")

sg = shotgun_api3.Shotgun(URL, login=LOGIN, password=PW)


def getSchemaFieldData(schema, filter):
    """각 스키마 별 필터를 기반으로 필드를 모두 추출해내는 함수입니다.

    Args: 
      schema: 스키마 명을 매개변수로 받습니다.
      filter: 필터링할 값을 배열로 받습니다.
    """
    with open(f'schema/{schema}.json') as file:
        data = json.load(file)

    fields = list(data.keys())
    with open(f'schema/{schema}Field.txt', 'w', encoding="utf-8") as file:
        print(f'{schema} 데이터 추출 중 #########')
        for field in fields:
            shot = sg.find(schema, filter, [field])
            file.write(str(schema)+'\n')
            print(f'현재 {schema}의 {field} 작성 중입니다.')
        print(f'{schema} 데이터 추출 완 #########')


getShotFieldData('Shot', [["code", "is", "mf6_604_001_0001"]])
getShotFieldData('Task', [['entity', 'is', {"type": "Shot", 'id': 180784}]])
