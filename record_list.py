import os
import json


def get_record_list():
    record_list = []
    if os.path.exists("record_list.json"):
        with open('record_list.json', 'r') as f:
            config_len = len(f.readlines())
        with open('record_list.json', 'r') as f:
            if config_len != 0:
                record_list = json.load(f)
    record_list_result = []
    for record in record_list:
        record_list_result.append(record)
    return record_list_result


def set_record_list(add_record):
    record_list = get_record_list()
    if os.path.exists("record_list.json"):
        tag = True
        for record in record_list:
            if record['date'] == add_record['date']:
                record['count'] = add_record['count']
                tag = False
                break
        if tag:
            record_list.append(add_record)
    else:
        record_list = [add_record]
    with open('record_list.json', 'w') as f:
        json.dump(record_list, f)
    return record_list
