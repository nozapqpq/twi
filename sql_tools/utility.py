from datetime import datetime as dt
import json

class Utility():
    def __init__(self):
        self.aa = 0
    def convert_datetime_to_str(self, date_t):
        return date_t.strftime('%Y-%m-%d')
    def get_list_from_json(self, json_name, list_name):
        json_open = open(json_name,'r')
        json_load = json.load(json_open)
        return json_load[list_name]
