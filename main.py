import shotgun_api3
from dotenv import load_dotenv
import os

load_dotenv()

URL = os.environ.get("BASE_URL")
LOGIN = os.environ.get("LOGIN")
PW = os.environ.get("PASSWORD")

sg = shotgun_api3.Shotgun(URL, login=LOGIN, password=PW)


def get_retake(shot_id, task_id):
    """Retake의 필드 데이터를 받아오는 함수입니다.

    Args:
        shot_id (number): Shot의 Id값을 받아옵니다.
        task_id (number): 해당 Shot의 Task Id를 받아옵니다.

    Returns:
        (list): retake02(감독님 피드백), retake03(편집 피드백)을 리스트 형태로 내보냅니다.
    """

    fields = ["sg_note", "sg_f_status", "image"]
    retake_02 = (sg.find("Task", [["entity", "is", {"type": "Shot", "id": shot_id}], [
        "id", "is", task_id]], fields))  # retake02 note 추출
    retake_03 = (sg.find("Task", [["entity", "is", {
        "type": "Shot", "id": shot_id}], ["id", "is", task_id + 1]], fields))  # retake02 note 추출

    return [retake_02, retake_03]


retake_arr = get_retake(180784, 1587815)
