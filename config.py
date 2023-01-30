import os
import json


def get_drink_config():
    drink_config = {}
    if os.path.exists("config.json"):
        with open('config.json', 'r') as f:
            config_len = len(f.readlines())
        with open('config.json', 'r') as f:
            if config_len != 0:
                drink_config = json.load(f)
    if len(drink_config) == 0:
        drink_config = {
            "active_time_list": [
                {
                    "active": False,
                    "start_time": "00:00",
                    "end_time": "00:00"
                },
                {
                    "active": False,
                    "start_time": "00:00",
                    "end_time": "00:00"
                },
                {
                    "active": False,
                    "start_time": "00:00",
                    "end_time": "00:00"
                },
            ],
            "remind_interval": 0,           # 间隔时间(分钟)
            "drinking_count": 8,            # 喝水数量
            "view_message": "positive",     # 窗口信息 正着计数(positive)/倒着计数(negative)
            "view_top": "normal"            # 窗口 置顶(top)/正常(normal)/置底(under)
        }
        with open('config.json', 'w') as f:
            json.dump(drink_config, f)
    return drink_config


def set_drink_config(new_drink_config):
    drink_config = new_drink_config
    with open('config.json', 'w') as f:
        json.dump(drink_config, f)
    return drink_config
