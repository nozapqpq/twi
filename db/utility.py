from datetime import datetime as dt
import json
import re

class Utility():
    def __init__(self):
        self.aa = 0
    def convert_datetime_to_str(self, date_t):
        return date_t.strftime('%Y-%m-%d')
    def get_list_from_json(self, json_name, list_name):
        json_open = open(json_name,'r')
        json_load = json.load(json_open)
        return json_load[list_name]
    def analyse_class(self, cls):
        if cls=="500万" or cls=="1勝":
            return "500万' or class='1勝' or class='1000万"
        elif cls=="未勝利" or cls=="新馬":
            return "未勝利' or class='500万"
        elif cls=="1000万" or cls=="2勝":
            return "1000万' or class='2勝' or class='500万"
        else:
            return "500万' or class='1000万' or class='2勝' or class='1600万' or class='3勝' or class='オープン' or class='Ｇ３' or class='Ｇ１' or class='Ｇ２"
    def convert_date_format(self, dt):
        # target format 0000.0.0 -> 0000-00-00
        lst = re.findall("\d+",dt)
        ret = lst[0].zfill(4)+"-"+lst[1].zfill(2)+"-"+lst[2].zfill(2)
        return ret
    def convert_turf_dirt(self, s):
        if s=="T":
            return "芝"
        elif s=="D":
            return "ダート"
        else:
            return "その他"
    def convert_race_time(self, s):
        if (len(s) == 3 or len(s) == 4) and s != "----":
            return round((int(int(s)/1000)*600+int(s[-3:]))*0.1,1)
        else:
            return "0.0"
    def remove_pm_space(self, pm):
        return pm.replace(" ","")

