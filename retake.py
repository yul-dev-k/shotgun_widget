import shotgun_api3
from dotenv import load_dotenv
import os
import time
load_dotenv()
start = time.time()


class Retake:
    URL = os.environ.get("BASE_URL")
    LOGIN = os.environ.get("LOGIN")
    PW = os.environ.get("PASSWORD")

    sg = shotgun_api3.Shotgun(URL, login=LOGIN, password=PW)

    episodes_id_name = [
        # {'id': 4819, 'name': 'EP600'},
        # {'id': 4820, 'name': 'EP601'},
        # {'id': 4821, 'name': 'EP602'},
        # {'id': 4822, 'name': 'EP603'},
        # {'id': 4823, 'name': 'EP604'},
        {'id': 4824, 'name': 'EP605'},
        # {'id': 4825, 'name': 'EP606'},
        {'id': 4826, 'name': 'EP607'},
        # {'id': 4827, 'name': 'EP608'},
        # {'id': 4828, 'name': 'EP609'},
        {'id': 4829, 'name': 'EP610'},
        {'id': 4830, 'name': 'EP611'},
        # {'id': 4831, 'name': 'EP612'},
        # {'id': 4832, 'name': 'EP613'},
        # {'id': 4833, 'name': 'EP614'},
        # {'id': 4834, 'name': 'EP615'},
        # {'id': 4835, 'name': 'EP616'},
        # {'id': 4836, 'name': 'EP617'},
        # {'id': 4837, 'name': 'EP618'},
        # {'id': 4838, 'name': 'EP619'},
        # {'id': 4839, 'name': 'EP620'},
        # {'id': 4840, 'name': 'EP621'},
        # {'id': 4841, 'name': 'EP622'},
        # {'id': 4842, 'name': 'EP623'},
        # {'id': 4843, 'name': 'EP624'},
        # {'id': 4844, 'name': 'EP625'},
        # {'id': 4845, 'name': 'EP626'},
        # {'id': 4846, 'name': 'EP627'},
        # {'id': 4847, 'name': 'EP628'},
        # {'id': 4848, 'name': 'EP629'},
    ]

    def __init__(self):
        self.user_id = self.get_user_id()['id']
        self.selected_data = [
            {"task_id": item['tasks'][4]['id'], "code": item['code'], "assigned": item['sg_assigned']} for sublist in self.all_shot_data() for item in sublist
        ]
        self.all_retake = self.all_retake_data()

    def get_user_id(self):
        return (self.sg.find_one('HumanUser', [["login", "is", self.LOGIN]], fields=["id"]))

    def all_shot_data(self):
        all_shot = []
        for episode_id in self.episodes_id_name:
            all_shot.append(self.sg.find("Shot", [["sg_episode", "is", {
                "type": 'Episode', "id": episode_id['id']}]], ["code",  "sg_assigned", "tasks"]))

        return all_shot

    def all_retake_data(self):
        """test

        Returns:
            _type_: _description_
        """
        return self.sg.find('Task', [['sg_f_status', 'is', 'rtks']],
                            ["sg_note", "sg_f_status", "image"])

    def get_all_retake(self):
        retake_list = []
        selected_data = self.selected_data
        all_retake = self.all_retake
        for data in selected_data:
            for retake in all_retake:
                if data['task_id'] == retake['id']:
                    retake_list.append({"code": data['code'], "assigned": data['assigned'],
                                       "note": retake['sg_note'], "img": retake['image'], "retake_v": '감독님', "task_id": data['task_id']})
                elif data['task_id']+1 == retake['id']:
                    retake_list.append({"code": data['code'], "assigned": data['assigned'],
                                       "note": retake['sg_note'], "img": retake['image'], "retake_v": '편집팀', "task_id": data['task_id']+1})
        # print("time :", time.time() - start)
        return retake_list

    def get_my_retake(self):
        retake_list = []
        for data in self.selected_data:
            for retake in self.all_retake:

                if data['task_id'] == retake['id'] and data['assigned'][0]['id'] == self.user_id:

                    retake_list.append({"code": data['code'], "assigned": data['assigned'],
                                       "note": retake['sg_note'], "img": retake['image'], "retake_v": '감독님', "task_id": data['task_id']})
                elif data['task_id']+1 == retake['id'] and data['assigned'][0]['id'] == self.user_id:

                    retake_list.append({"code": data['code'], "assigned": data['assigned'],
                                       "note": retake['sg_note'], "img": retake['image'], "retake_v": '편집팀', "task_id": data['task_id']+1})
        # print("time :", time.time() - start)
        return retake_list
