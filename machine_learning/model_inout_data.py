# coding: utf-8
import json
import math
import re
import time # sleep用
from .utility import Utility

class ModelInOutData():
    def __init__(self):
        self.utility = Utility()
        self.temperature = self.utility.get_temperature_from_json("machine_learning/deep_temperature.json")
        self.learn_input_json_fn = "machine_learning/deep_pattern.json"
        self.learn_input_list = json.load(open(self.learn_input_json_fn,'r'))
        self.stallion_type = ["その他","ロイヤルチャージャー系","ネイティヴダンサー系","ニアークティック系","ナスルーラ系","セントサイモン系","マンノウォー系","トウルビヨン系"]

    def set_stallion_table(self, st_table):
        self.stallion = st_table

    def set_trainer_table(self, tr_table):
        self.trainer = tr_table

    def make_model_in_out_list(self, source_data, use_blank=False):
        input_list = []
        output_list = []
        race_count = 0

        target_hrl = self.get_target_data_from_horse_race_list(source_data)
        # 未出走は予想対象としない
        if len(source_data["history_horse_race_list"]) == 0:
            return [], []
        for ptn in self.learn_input_list["object_list"]:
            if ptn["activate"] == "on":
                exec_cmd = self.utility.get_exec_command(ptn["func"],ptn["args"])
                input_list.append(eval(exec_cmd))
        if target_hrl != {} and (target_hrl["goal_order"] == 0 or use_blank):
            return input_list, "x"
        if target_hrl != {}:
            output_list = self.make_output_list(source_data)
        return input_list, output_list

    def get_dl_element1(self, source_data):
        if "転初" in source_data["past_list"][0]["transfer"]:
            return 1
        return 0
    def get_dl_element2(self,source_data):
        '''
        print(source_data.keys())
        print("-------")
        print(source_data["past_list"][0].keys())
        print(source_data["today_dict"].keys())
        print(source_data["horse_race_list"][0].keys())
        print(source_data["history_horse_race_list"][0].keys())
        time.sleep(100)
        '''
        if "去初" in source_data["past_list"][0]["castration"]:
            return 1
        return 0
    def get_dl_element3(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 360 and \
                self.utility.check_same_condition(source_data["today_dict"]["course_condition"],r["course_condition"]):
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element4(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                r["place"] == "札幌" and "芝" in r["turf_dirt"] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element5(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                r["place"] == "札幌" and "ダート" in r["turf_dirt"] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element6(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                r["place"] == "函館" and "芝" in r["turf_dirt"] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element7(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                r["place"] == "函館" and "ダート" in r["turf_dirt"] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element8(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                r["place"] in ["福島","小倉"] and "芝" in r["turf_dirt"] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element9(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                r["place"] in ["福島","小倉"] and "ダート" in r["turf_dirt"] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element10(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                r["place"] in ["中山","阪神"] and "芝" in r["turf_dirt"] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element11(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                r["place"] in ["中山","阪神"] and "ダート" in r["turf_dirt"] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element12(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                r["place"] in ["京都"] and "芝" in r["turf_dirt"] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element13(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                r["place"] in ["京都"] and "ダート" in r["turf_dirt"] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element14(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                r["place"] in ["東京","中京"] and "芝" in r["turf_dirt"] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element15(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                r["place"] in ["東京","中京"] and "ダート" in r["turf_dirt"] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element16(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                abs(int(r["distance"])-int(source_data["today_dict"]["distance"])) <= 200 and r["turf_dirt"][0] == source_data["today_dict"]["turf_dirt"][0] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element17(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                int(r["distance"])-int(source_data["today_dict"]["distance"]) > 200 and r["turf_dirt"][0] == source_data["today_dict"]["turf_dirt"][0] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element18(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                int(r["distance"])-int(source_data["today_dict"]["distance"]) < -200 and r["turf_dirt"][0] == source_data["today_dict"]["turf_dirt"][0] and \
                source_data["today_dict"]["class"] == r["class"]:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element19(self,source_data):
        total = 0
        double_win = 0
        for r in source_data["past_list"]:
            if self.utility.compare_class_priority(source_data["today_dict"]["class"],r["class"]) > 0:
                total = total + 1
                if int(r["time_diff"]) < 0.5:
                    double_win = double_win + 1
        if total == 0:
            return 0
        return double_win/total
    def get_dl_element20(self,source_data):
        ret_val = 0
        for r in source_data["past_list"]:
            if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(r["rdate"])).days < 500 and \
                self.utility.compare_class_priority(source_data["today_dict"]["class"],r["class"]) < 0:
                ret_val = max((2.5-min(max(r["time_diff"],2.5),0))/2.5,ret_val)
        return ret_val
    def get_dl_element21(self,source_data):
        tr = [x for x in self.trainer if x['name']==source_data["past_list"][0]["trainer"]]
        if len(tr) == 0:
            return 0
        if tr[0]['belongs'] == "栗東":
            return 1
        return 0
    def get_dl_element22(self,source_data):
        tr = [x for x in self.trainer if x['name']==source_data["past_list"][0]["trainer"]]
        if len(tr) == 0:
            return 0
        if tr[0]['belongs'] == "美浦":
            return 1
        return 0
    def get_dl_element23(self,source_data):
        if source_data["past_list"][0]["horseweight"] == "---":
            return 0
        if int(source_data["past_list"][0]["horseweight"]) > 500:
            return 1
        return 0
    def get_dl_element24(self,source_data):
        if (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(source_data["past_list"][0]["rdate"])).days > 10:
            return 1
        return 0
    def get_dl_element25(self,source_data):
        return source_data["horsenum"]%2
    def get_dl_element26(self,source_data):
        return 1-source_data["horsenum"]%2
    def get_dl_element27(self,source_data):
        if "ノーザンファーム" in source_data["history_horse_race_list"][0]["breeder"]:
            return 1
        return 0
    def get_dl_element28(self,source_data):
        if "牡" in source_data["past_list"][0]["horse_sex"] or "セ" in source_data["past_list"][0]["horse_sex"]:
            return 1
        return 0
    def get_dl_element29(self,source_data):
        if int(source_data["past_list"][0]["horse_age"]) <= 6:
            return 1
        return 0
    def get_dl_element30(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor1"] == "ロイヤルチャージャー系":
            return 1
        return 0
    def get_dl_element31(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor1"] == "ネイティヴダンサー系":
            return 1
        return 0
    def get_dl_element32(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor1"] == "ニアークティック系":
            return 1
        return 0
    def get_dl_element33(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor1"] == "ナスルーラ系":
            return 1
        return 0
    def get_dl_element34(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor1"] == "セントサイモン系":
            return 1
        return 0
    def get_dl_element35(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor1"] == "マンノウォー系":
            return 1
        return 0
    def get_dl_element36(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor1"] == "トウルビヨン系":
            return 1
        return 0
    def get_dl_element37(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor2"] == "ロイヤルチャージャー系":
            return 1
        return 0
    def get_dl_element38(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor2"] == "ネイティヴダンサー系":
            return 1
        return 0
    def get_dl_element39(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor2"] == "ニアークティック系":
            return 1
        return 0
    def get_dl_element40(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor2"] == "ナスルーラ系":
            return 1
        return 0
    def get_dl_element41(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor2"] == "セントサイモン系":
            return 1
        return 0
    def get_dl_element42(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor2"] == "マンノウォー系":
            return 1
        return 0
    def get_dl_element43(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor2"] == "トウルビヨン系":
            return 1
        return 0
    def get_dl_element44(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor3"] == "ロイヤルチャージャー系":
            return 1
        return 0
    def get_dl_element45(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor3"] == "ネイティヴダンサー系":
            return 1
        return 0
    def get_dl_element46(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor3"] == "ニアークティック系":
            return 1
        return 0
    def get_dl_element47(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor3"] == "ナスルーラ系":
            return 1
        return 0
    def get_dl_element48(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor3"] == "セントサイモン系":
            return 1
        return 0
    def get_dl_element49(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor3"] == "マンノウォー系":
            return 1
        return 0
    def get_dl_element50(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor3"] == "トウルビヨン系":
            return 1
        return 0
    def get_dl_element51(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor4"] == "ロイヤルチャージャー系":
            return 1
        return 0
    def get_dl_element52(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor4"] == "ネイティヴダンサー系":
            return 1
        return 0
    def get_dl_element53(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor4"] == "ニアークティック系":
            return 1
        return 0
    def get_dl_element54(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor4"] == "ナスルーラ系":
            return 1
        return 0
    def get_dl_element55(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor4"] == "セントサイモン系":
            return 1
        return 0
    def get_dl_element56(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor4"] == "マンノウォー系":
            return 1
        return 0
    def get_dl_element57(self,source_data):
        st = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(st) == 0:
            return 0
        if st[0]["ancestor4"] == "トウルビヨン系":
            return 1
        return 0
    def get_dl_element58(self, source_data):
        ret_3f = 0
        count = 0
        for p in source_data["past_list"]:
            if p["diff3f"] == "":
                continue
            ret_3f = ret_3f + float(p["diff3f"])
            count = count + 1
            if count == 4:
                break
        if count == 0:
            return 0
        if ret_3f/count <= 0.5:
            return 1
        return 0
    def get_dl_element59(self, source_data):
        span = (self.utility.str_to_date(source_data["rdate"])-self.utility.str_to_date(source_data["past_list"][0]["rdate"])).days
        if span >= 20 and span <= 100:
            return 1
        return 0
    def get_dl_element65(self, source_data):
        if len(source_data["history_horse_race_list"]) == 0:
            return 0
        delta_d = self.utility.calc_days_after_birth(self.utility.str_to_date(source_data["rdate"]),source_data["history_horse_race_list"][0]["birthday"])
        return -math.cos((delta_d%14)*360/14)/2+0.5
    def get_dl_element66(self, source_data):
        if len(source_data["history_horse_race_list"]) == 0:
            return 0
        delta_d = self.utility.calc_days_after_birth(self.utility.str_to_date(source_data["rdate"]),source_data["history_horse_race_list"][0]["birthday"])
        return -math.cos((delta_d%21)*360/21)/2+0.5
    def get_dl_element67(self, source_data):
        if len(source_data["history_horse_race_list"]) == 0:
            return 0
        delta_d = self.utility.calc_days_after_birth(self.utility.str_to_date(source_data["rdate"]),source_data["history_horse_race_list"][0]["birthday"])
        return -math.cos((delta_d%28)*360/28)/2+0.5
    def get_dl_element68(self, source_data):
        if len(source_data["history_horse_race_list"]) == 0:
            return 0
        delta_d = self.utility.calc_days_after_birth(self.utility.str_to_date(source_data["rdate"]),source_data["history_horse_race_list"][0]["birthday"])
        return -math.cos((delta_d%56)*360/56)/2+0.5
    def get_dl_element69(self, source_data):
        if len(source_data["history_horse_race_list"]) == 0:
            return 0
        delta_d = self.utility.calc_days_after_birth(self.utility.str_to_date(source_data["rdate"]),source_data["history_horse_race_list"][0]["birthday"])
        return -math.cos((delta_d%108)*360/108)/2+0.5
    def get_dl_element70(self, source_data):
        if len(source_data["history_horse_race_list"]) == 0:
            return 0
        delta_d = self.utility.calc_days_after_birth(self.utility.str_to_date(source_data["rdate"]),source_data["history_horse_race_list"][0]["birthday"])
        return -math.cos((delta_d%180)*360/180)/2+0.5

    def make_output_list(self, source_data):
        retlist = [0, 0]
        target_hrl = self.get_target_data_from_horse_race_list(source_data)
        if target_hrl["time_diff"] <= 0.2 and target_hrl["goal_order"] >= 1:
            retlist[0] = 1
        else:
            retlist[1] = 1
        return retlist

    def get_target_data_from_horse_race_list(self, source_data):
        ret_target = {}
        for hrl in source_data["horse_race_list"]:
            if hrl["horsenum"] == source_data["horsenum"]:
                ret_target = hrl
                break
        return ret_target
