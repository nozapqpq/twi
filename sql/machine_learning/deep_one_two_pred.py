# coding: utf-8
from . import deep_single_race
from . import deep_utility
import json

class DeepOneTwoPred():
    def __init__(self):
        self.util = deep_utility.Utility()
        self.sr = deep_single_race.DeepSingleRace()
        self.today_date = ""
        self.slow_pace = self.util.get_slow_pace_all_data()
        self.european_grass_list = ["札幌","函館"]
        self.spiral_list = ["札幌","函館","小倉","福島"]
        self.main_place_list = ["中山","東京","京都","阪神"]

    # input_lst[1レース分][1頭分]
    def make_deeplearning_data(self, input_lst, json_fn=""):
        learn = [] # 学習用
        target = [] # 予想対象
        ans = [] # 学習用正当データ
        horsename_lst = [] # 馬名データ
        todayinfo_lst = [] # 場所、レース番号、馬名データ
        race_count = 0
        if json_fn != "":
            json_open = open(json_fn,'r')
            json_load = json.load(json_open)
        for single_race in input_lst:
            race_count = race_count + 1
            if race_count % 200 == 0:
                print("making deep learning input data:"+str(race_count)+" / "+str(len(input_lst)))
            self.sr.set_main_dicts(single_race)
            for dct in single_race:
                single_learn = []
                for ptn in json_load["object_list"]:
                    if ptn["activate"] == "on":
                        exec_cmd = self.util.get_exec_command(ptn["func"],ptn["args"])
                        single_learn.append(eval(exec_cmd))
                # 本日と過去走のデータリストを作成
                # 障害や出走取り消し等で着順が入っていないデータは双方から除外
                if (dct["today_rdate"] == self.today_date and not "障害" in dct["today_turf_dirt"]):
                    target.append(single_learn)
                    todayinfo_lst.append([dct["today_place"],dct["today_race"],dct["horsename"]])
                elif dct["today_goal"] != 0:
                    learn.append(single_learn)
                    ans.append([dct["today_goal"],dct["today_time_diff"],dct["today_triple_dividend"]])
                    horsename_lst.append(dct["horsename"])
        return learn, ans, horsename_lst, target, todayinfo_lst

    def get_dl_element1(self, dct):
        if dct["today_turf_dirt"] == "芝":
            return 1
        return 0
    def get_dl_element2(self, dct):
        if dct["past_turf_dirt"] == "芝":
            return 1
        return 0
    def get_dl_element3(self, dct):
        return self.util.get_distance_index(dct["today_distance"])
    def get_dl_element4(self, dct):
        return self.util.get_distance_index(dct["past_distance"])
    def get_dl_element5(self, dct):
        if "[G001]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element6(self, dct):
        if "[G002]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element7(self, dct):
        if "[G003]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element8(self, dct):
        if "[G004]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element9(self, dct):
        if "[G005]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element10(self, dct):
        if "[G006]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element11(self, dct):
        if "[G001]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element12(self, dct):
        if "[G002]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element13(self, dct):
        if "[G003]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element14(self, dct):
        if "[G004]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element15(self, dct):
        if "[G005]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element16(self, dct):
        if "[G006]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element17(self, dct):
        return self.util.get_condition_index(dct["today_course_condition"])
    def get_dl_element18(self, dct):
        return self.util.get_condition_index(dct["past_course_condition"])
    def get_dl_element19(self, dct):
        return self.util.is_european_grass(dct["today_place"])
    def get_dl_element20(self, dct):
        return self.util.is_european_grass(dct["past_place"])
    def get_dl_element21(self, dct):
        return self.util.is_spiral_curve(dct["today_place"])
    def get_dl_element22(self, dct):
        return self.util.is_spiral_curve(dct["past_place"])
    def get_dl_element23(self, dct):
        return self.util.is_main_place(dct["today_place"])
    def get_dl_element24(self, dct):
        return self.util.is_main_place(dct["past_place"])
    def get_dl_element25(self, dct):
        if "転初" in dct["transfer"]:
            return 1
        return 0
    def get_dl_element26(self,dct):
        if "去初" in dct["castration"]:
            return 1
        return 0
    def get_dl_element27(self, dct):
        bi = '{:02b}'.format(self.util.get_class_rank(dct["today_class"]))
        return int(bi[0])
    def get_dl_element28(self, dct):
        bi = '{:02b}'.format(self.util.get_class_rank(dct["today_class"]))
        return int(bi[1])
    def get_dl_element29(self, dct):
        return self.util.is_upper_class(dct["past_class"],dct["today_class"])
    def get_dl_element30(self, dct):
        if dct["past_diff3f"] <= 0.3:
            return 1
        return 0
    def get_dl_element31(self, dct):
        if dct["past_diff3f"] >= 1.5:
            return 1
        return 0
    def get_dl_element32(self, dct):
        virtual_cls = self.util.get_slow_pace_virtual_class(dct["past_class"])
        rap = [x for x in self.slow_pace if x['place']==dct['past_place'] and x['distance']==dct['past_distance'] and x['course_condition']==dct['past_course_condition'] and x['turf_dirt']==dct['past_turf_dirt'] and x['class']==virtual_cls]
        if len(rap) == 0:
            rap = [{"rap3f":37.0,"rap5f":65.0}]
        if dct["past_distance"] <= 1400 and dct["past_rap3f"] >= rap[0]["rap3f"]:
            return 1
        elif dct["past_distance"] > 1400 and dct["past_rap5f"] >= rap[0]["rap5f"]:
            return 1
        return 0
    def get_dl_element33(self, dct):
        if dct["today_span"] >= 15:
            return 1
        return 0
    def get_dl_element34(self, dct):
        if self.sr.whole_race_dict["top_odds"] <= 2.0:
            return 1
        return 0
    def get_dl_element35(self, dct):
        if self.sr.single_horse_dicts[dct["today_horsenum"]-1]["zi_diff_from_top"] <= 20:
            return 1
        return 0
    def get_dl_element36(self, dct):
        if self.sr.single_horse_dicts[dct["today_horsenum"]-1]["diff02_count"] >= 2:
            return 1
        return 0
    def get_dl_element37(self, dct):
        if self.sr.single_horse_dicts[dct["today_horsenum"]-1]["diff20_count"] >= 2:
            return 1
        return 0
    def get_dl_element38(self, dct):
        if self.sr.whole_race_dict["pop_tddiff"]:
            return 1
        return 0
    def get_dl_element39(self, dct):
        if self.sr.single_horse_dicts[dct["today_horsenum"]-1]["highodds05"]:
            return 1
        return 0
    def get_dl_element40(self, dct):
        if self.util.get_class_priority(dct["today_class"]) <= self.util.get_class_priority(dct["past_class"]) and dct["past_horse_last3f"] <= dct["past_race_last3f"]-0.5:
            return 1
        return 0
    def get_dl_element41(self, dct):
        count = 0
        for shd in self.sr.single_horse_dicts:
            if shd["odds"] >= 100.0:
                count = count + 1
        if count >= 3:
            return 1
        return 0
    def get_dl_element42(self, dct):
        count = 0
        for shd in self.sr.single_horse_dicts:
            if shd["odds"] <= 20.0:
                count = count + 1
        if count >= 7:
            return 1
        return 0
    def get_dl_element43(self, dct):
        if self.sr.single_horse_dicts[dct["today_horsenum"]-1]["aheadlose10"] >= 2:
            return 1
        return 0
    def get_dl_element44(self, dct):
        if dct["today_span"] == 1:
            return 1
        return 0
    def get_dl_element45(self, dct):
        if dct["past_distance"] == dct["today_distance"] and dct["past_turf_dirt"] == dct["today_turf_dirt"] and (dct["past_course_condition"] == "良" or dct["past_course_condition"] == "稍"):
            if self.sr.whole_race_dict["fastest_time"] != 0 and dct["past_race_time"] <= self.sr.whole_race_dict["fastest_time"]+0.5:
                return 1
        return 0
    def get_dl_element46(self, dct):
        if self.util.get_class_priority(dct["today_class"]) >= 2:
            return 1
        return 0

    # [0, 0, 0, 0]の形式、 ３着内率を配当で細分化したものに変換
    def convert_fullgate_goal_list(self, goal, today_time_diff, triple):
        goal_list = []
        goal_feature = 0
        if today_time_diff <= 0.3: 
            goal_feature = 0
        elif today_time_diff <= 0.7:
            goal_feature = 1
        elif today_time_diff <= 1.5:
            goal_feature = 2
        else:
            goal_feature = 3
        for i in range(4):
            if i == goal_feature:
                goal_list.append(1)
            else:
                goal_list.append(0)
        return goal_list
    def get_output_list_title(self):
        return ["place","race","horsename","~0.3s","~0.7s","~1.5s","1.6s~"]
    def get_number_of_output_kind(self):
        return len(self.get_output_list_title())-3
