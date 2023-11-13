import shotgun_api3
from dotenv import load_dotenv
import os
import numpy as np

load_dotenv()

URL = os.environ.get("BASE_URL")
LOGIN = os.environ.get("LOGIN")
PW = os.environ.get("PASSWORD")

sg = shotgun_api3.Shotgun(URL, login=LOGIN, password=PW)

episodes_id_name = [
    {'id': 4819, 'name': 'ep600'},
    {'id': 4820, 'name': 'ep601'},
    {'id': 4821, 'name': 'ep602'},
    {'id': 4822, 'name': 'ep603'},
    {'id': 4823, 'name': 'ep604'},
    {'id': 4824, 'name': 'ep605'},
    {'id': 4825, 'name': 'ep606'},
    {'id': 4826, 'name': 'ep607'},
    {'id': 4827, 'name': 'ep608'},
    {'id': 4828, 'name': 'ep609'},
    {'id': 4829, 'name': 'ep610'},
    {'id': 4830, 'name': 'ep611'},
    {'id': 4831, 'name': 'ep612'},
    {'id': 4832, 'name': 'ep613'},
    {'id': 4833, 'name': 'ep614'},
    {'id': 4834, 'name': 'ep615'},
    {'id': 4835, 'name': 'ep616'},
    {'id': 4836, 'name': 'ep617'},
    {'id': 4837, 'name': 'ep618'},
    {'id': 4838, 'name': 'ep619'},
    {'id': 4839, 'name': 'ep620'},
    {'id': 4840, 'name': 'ep621'},
    {'id': 4841, 'name': 'ep622'},
    {'id': 4842, 'name': 'ep623'},
    {'id': 4843, 'name': 'ep624'},
    {'id': 4844, 'name': 'ep625'},
    {'id': 4845, 'name': 'ep626'},
    {'id': 4846, 'name': 'ep627'},
    {'id': 4847, 'name': 'ep628'},
    {'id': 4848, 'name': 'ep629'},
]


def get_shot_id_data():
    """shot id와 code를 shotgun api3를 통해 받아옵니다.

    Returns: none
    """
    return (sg.find('Shot', [], ["code"]))


def save_shot_id_data(current_season="6"):
    """현재 에피소드의 샷들을 txt파일로 저장합니다.

    Args:
        current_season (string, optional): 현재 시즌의 string값을 받아옵니다. Defaults to "6".
    """
    codes = get_shot_id_data()

    for episode in episodes_id_name:
        for key, val in episode.items():
            if (key == "name"):
                ep = []
                for code in codes:
                    if (code["code"].find(f"{val[2:]}", 4) != -1) and (code["code"][2] == current_season):
                        data = ({"id": code["id"], "code": code["code"]})
                        ep.append(data)

                if ep:
                    # Save data to a .npy file
                    np.save(f"shot/{val}.npy", ep)


save_shot_id_data("6")
