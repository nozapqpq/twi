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
        if not (use_blank == False and (target_hrl == {} or target_hrl["goal_order"] == 0)):
            output_list = self.make_output_list(source_data)
        return input_list, output_list

    def get_dl_element1(self, source_data):
        return self.utility.get_condition_index(source_data["today_dict"]["course_condition"])
    def get_dl_element2(self, source_data):
        # チェック用
        '''
        print(source_data.keys())
        print("-------")
        print(source_data["past_list"][0].keys())
        print(source_data["today_dict"].keys())
        print(source_data["horse_race_list"][0].keys())
        print(source_data["history_horse_race_list"][0].keys())
        time.sleep(100)
        '''
        return self.utility.get_condition_index(source_data["history_horse_race_list"][0]["course_condition"])
    def get_dl_element3(self, source_data):
        if "転初" in source_data["past_list"][0]["transfer"]:
            return 1
        return 0
    def get_dl_element4(self,source_data):
        if "去初" in source_data["past_list"][0]["castration"]:
            return 1
        return 0
    def get_dl_element5(self, source_data):
        bi = '{:02b}'.format(self.utility.get_class_rank(source_data["today_dict"]["class"]))
        return int(bi[0])
    def get_dl_element6(self, source_data):
        bi = '{:02b}'.format(self.utility.get_class_rank(source_data["today_dict"]["class"]))
        return int(bi[1])
    def get_dl_element7(self, source_data):
        bi = '{:02b}'.format(self.utility.get_class_rank(source_data["past_list"][0]["class"]))
        return int(bi[0])
    def get_dl_element8(self, source_data):
        bi = '{:02b}'.format(self.utility.get_class_rank(source_data["past_list"][0]["class"]))
        return int(bi[1])
    def get_dl_element9(self, source_data):
        odds = (min(self.sr.whole_race_dict["top_odds"],5.0)-1.0)/4.0
        return odds
    def get_dl_element10(self, source_data):
        zi_diff = min(self.sr.single_horse_dicts[source_data["today_horsenum"]-1]["zi_diff_from_top"],30)/30
        return zi_diff
    def get_dl_element11(self, source_data):
        return min(max(source_data["past_list"][0]["time_diff"],-2.5),2.5)/2.5
    def get_dl_element12(self, source_data):
        if self.sr.whole_race_dict["pop_tddiff"]:
            return 1
        return 0
    def get_dl_element13(self, source_data):
        return self.sr.whole_race_dict["west_count"]/self.sr.whole_race_dict["horse_total"]
    def get_dl_element14(self, source_data):
        return self.sr.whole_race_dict["youngjockey_count"]/self.sr.whole_race_dict["horse_total"]
    def get_dl_element15(self, source_data):
        if source_data["today_span"] == 1:
            return 1
        return 0
    def get_dl_element16(self, source_data):
        if source_data["past_distance"] == source_data["today_distance"] and source_data["past_turf_dirt"] == source_data["today_turf_dirt"] and (source_data["past_course_condition"] == "良" or source_data["past_course_condition"] == "稍"):
            if self.sr.whole_race_dict["fastest_time"] != 0 and source_data["past_race_time"] <= self.sr.whole_race_dict["fastest_time"]+0.5:
                return 1
        return 0
    def get_dl_element17(self, source_data):
        if self.utility.get_class_priority(source_data["today_class"]) >= 2:
            return 1
        return 0
    def get_dl_element18(self, source_data):
        if source_data["today_horsenum"]%2 == 1:
            return 1
        return 0
    def get_dl_element19(self, source_data):
        if source_data["breeder"] == "ノーザンファーム":
            return 1
        return 0
    def get_dl_element20(self, source_data):
        if source_data["horse_sex"] == "牝":
            return 1
        return 0
    def get_dl_element21(self, source_data):
        bi = '{:03b}'.format(min(source_data["history_horse_race_list"][0]["age"]-2,7))
        return int(bi[0])
    def get_dl_element22(self, source_data):
        bi = '{:03b}'.format(min(source_data["history_horse_race_list"][0]["age"]-2,7))
        return int(bi[1])
    def get_dl_element23(self, source_data):
        bi = '{:03b}'.format(min(source_data["history_horse_race_list"][0]["age"]-2,7))
        return int(bi[2])
    def get_dl_element24(self, source_data):
        single = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor1"]))
            return int(bi[0])
    def get_dl_element25(self, source_data):
        single = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor1"]))
            return int(bi[1])
    def get_dl_element26(self, source_data):
        single = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor1"]))
            return int(bi[2])
    def get_dl_element27(self, source_data):
        single = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor2"]))
            return int(bi[0])
    def get_dl_element28(self, source_data):
        single = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor2"]))
            return int(bi[1])
    def get_dl_element29(self, source_data):
        single = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor2"]))
            return int(bi[2])
    def get_dl_element30(self, source_data):
        single = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor3"]))
            return int(bi[0])
    def get_dl_element31(self, source_data):
        single = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor3"]))
            return int(bi[1])
    def get_dl_element32(self, source_data):
        single = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor3"]))
            return int(bi[2])
    def get_dl_element33(self, source_data):
        single = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor4"]))
            return int(bi[0])
    def get_dl_element34(self, source_data):
        single = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor4"]))
            return int(bi[1])
    def get_dl_element35(self, source_data):
        single = [x for x in self.stallion if x['name']==source_data["history_horse_race_list"][0]['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor4"]))
            return int(bi[2])
    def get_dl_element36(self, source_data):
        single = [x for x in self.trainer if x['name']==source_data['trainer']]
        if len(single) == 0:
            return 0
        else:
            if single[0]['belongs'] == "栗東":
                return 1
            return 0
    def get_dl_element37(self, source_data):
        if "[G001]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element38(self, source_data):
        if "[G002]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element39(self, source_data):
        if "[G003]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element40(self, source_data):
        if "[G004]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element41(self, source_data):
        if "[G005]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element42(self, source_data):
        if "[G006]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element43(self, source_data):
        if "[G007]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element44(self, source_data):
        if "[G008]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element45(self, source_data):
        if "[G009]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element46(self, source_data):
        if "[G010]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element47(self, source_data):
        if "[G011]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element48(self, source_data):
        if "[G012]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element49(self, source_data):
        if "[G013]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element50(self, source_data):
        if "[G014]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element51(self, source_data):
        if "[G015]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element52(self, source_data):
        if "[G016]" in source_data["today_dict"]["course_mark"]:
            return 1
        return 0
    def get_dl_element53(self, source_data):
        if "[G001]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element54(self, source_data):
        if "[G002]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element55(self, source_data):
        if "[G003]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element56(self, source_data):
        if "[G004]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element57(self, source_data):
        if "[G005]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element58(self, source_data):
        if "[G006]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element59(self, source_data):
        if "[G007]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element60(self, source_data):
        if "[G008]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element61(self, source_data):
        if "[G009]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element62(self, source_data):
        if "[G010]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element63(self, source_data):
        if "[G011]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element64(self, source_data):
        if "[G012]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element65(self, source_data):
        if "[G013]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element66(self, source_data):
        if "[G014]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element67(self, source_data):
        if "[G015]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element68(self, source_data):
        if "[G016]" in source_data["past_course_mark"]:
            return 1
        return 0
    def get_dl_element69(self, source_data):
        if source_data["today_turf_dirt"] == "芝" and source_data["today_distance"] >= 1000:
            return 1
        return 0
    def get_dl_element70(self, source_data):
        if source_data["today_turf_dirt"] == "芝" and source_data["today_distance"] >= 1400:
            return 1
        return 0
    def get_dl_element71(self, source_data):
        if source_data["today_turf_dirt"] == "芝" and source_data["today_distance"] >= 1800:
            return 1
        return 0
    def get_dl_element72(self, source_data):
        if source_data["today_turf_dirt"] == "芝" and source_data["today_distance"] >= 2400:
            return 1
        return 0
    def get_dl_element73(self, source_data):
        if source_data["today_turf_dirt"] != "芝" and source_data["today_distance"] >= 1000:
            return 1
        return 0
    def get_dl_element74(self, source_data):
        if source_data["today_turf_dirt"] != "芝" and source_data["today_distance"] >= 1400:
            return 1
        return 0
    def get_dl_element75(self, source_data):
        if source_data["today_turf_dirt"] != "芝" and source_data["today_distance"] >= 1800:
            return 1
        return 0
    def get_dl_element76(self, source_data):
        if source_data["today_turf_dirt"] != "芝" and source_data["today_distance"] >= 2400:
            return 1
        return 0
    def get_dl_element77(self, source_data):
        if source_data["past_turf_dirt"] == "芝" and source_data["past_distance"] >= 1000:
            return 1
        return 0
    def get_dl_element78(self, source_data):
        if source_data["past_turf_dirt"] == "芝" and source_data["past_distance"] >= 1400:
            return 1
        return 0
    def get_dl_element79(self, source_data):
        if source_data["past_turf_dirt"] == "芝" and source_data["past_distance"] >= 1800:
            return 1
        return 0
    def get_dl_element80(self, source_data):
        if source_data["past_turf_dirt"] == "芝" and source_data["past_distance"] >= 2400:
            return 1
        return 0
    def get_dl_element81(self, source_data):
        if source_data["past_turf_dirt"] != "芝" and source_data["past_distance"] >= 1000:
            return 1
        return 0
    def get_dl_element82(self, source_data):
        if source_data["past_turf_dirt"] != "芝" and source_data["past_distance"] >= 1400:
            return 1
        return 0
    def get_dl_element83(self, source_data):
        if source_data["past_turf_dirt"] != "芝" and source_data["past_distance"] >= 1800:
            return 1
        return 0
    def get_dl_element84(self, source_data):
        if source_data["past_turf_dirt"] != "芝" and source_data["past_distance"] >= 2400:
            return 1
        return 0
    def get_dl_element85(self, source_data):
        # 10.0sを0, 13.0sを1とする
        return (min(max(source_data["past_early_rap2"],10.0),13.0)-10.0)/3.0
    def get_dl_element86(self, source_data):
        return (min(max(source_data["past_early_rap3"],10.0),13.0)-10.0)/3.0
    def get_dl_element87(self, source_data):
        return (min(max(source_data["past_early_rap4"],10.0),13.0)-10.0)/3.0
    def get_dl_element88(self, source_data):
        return (min(max(source_data["past_last_rap1"],10.0),13.0)-10.0)/3.0
    def get_dl_element89(self, source_data):
        return (min(max(source_data["past_last_rap2"],10.0),13.0)-10.0)/3.0
    def get_dl_element90(self, source_data):
        return (min(max(source_data["past_last_rap3"],10.0),13.0)-10.0)/3.0
    def get_dl_element91(self, source_data):
        return (min(max(source_data["past_last_rap4"],10.0),13.0)-10.0)/3.0
    def get_dl_element92(self, source_data):
        if source_data["past_list"][0]["diff3f"] == "":
            return 0
        return min(source_data["past_list"][0]["diff3f"],2.5)/2.5
    def get_dl_element93(self, source_data):
        return (min(source_data["today_horsenum"],18)-1)/17
    def get_dl_element94(self, source_data):
        return min(math.log(source_data["past_odds"],3),5)/5
    def get_dl_element95(self, source_data):
        if int(source_data["past_list"][0]["span"]) <= 0:
            return 0
        else:
            return min(math.log(int(source_data["past_list"][0]["span"]),2),8)/6
    def get_dl_element96(self, source_data):
        return min(math.log((source_data["today_rdate"]-source_data["past_rdate"]).days,4),4)/4
    def get_dl_element97(self, source_data):
        if source_data["past_rap5f"] <= 57.0:
            return 1
        return 0
    def get_dl_element98(self, source_data):
        return self.sr.whole_race_dict["younghorse_count"]/self.sr.whole_race_dict["horse_total"]
    def get_dl_element99(self, source_data):
        return self.sr.whole_race_dict["stag_count"]/self.sr.whole_race_dict["horse_total"]
    def get_dl_element100(self, source_data):
        jk = [x for x in self.jockey if x["name"]==source_data["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if source_data["today_turf_dirt"] == "芝":
            return jk[0]["turf_front"]/100
        if source_data["today_turf_dirt"] == "ダート":
            return jk[0]["dirt_front"]/100
        return 0
    def get_dl_element101(self, source_data):
        jk = [x for x in self.jockey if x["name"]==source_data["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if source_data["today_turf_dirt"] == "芝":
            return jk[0]["turf_stay"]/100
        if source_data["today_turf_dirt"] == "ダート":
            return jk[0]["dirt_stay"]/100
        return 0
    def get_dl_element102(self, source_data):
        temperature = self.utility.get_temperature(self.temperature, source_data)
        return (min(max(temperature,10),30)-10)/20
    def get_dl_element103(self, source_data):
        return min(max(self.sr.whole_race_dict["delta_rap5f"],-2.5),2.5)/2.5
    def get_dl_element104(self, source_data):
        return min(max(self.sr.whole_race_dict["delta_last3f"],-2.5),2.5)/2.5
    def get_dl_element105(self, source_data):
        # TODO:このhorsenumが過去走のhorsenumでないか、last_rap4が後ろから４番目のラップタイムでないか要確認
        rap4 = [x["last_rap4"] for x in source_data["horse_race_list"] if x["horsenum"] == source_data["horsenum"]]
        if len(rap4) == 0:
            return 1
        return (min(max(rap4[0],10),13)-10)/3
    def get_dl_element106(self, source_data):
        rap3 = [x["last_rap3"] for x in source_data["horse_race_list"] if x["horsenum"] == source_data["horsenum"]]
        if len(rap3) == 0:
            return 1
        return (min(max(rap3[0],10),13)-10)/3
    def get_dl_element107(self, source_data):
        # 取り消し馬がいてhorse_race_listのデータ数が出走頭数分と合わない場合にも対応可
        rap_base = [x["last_rap3"] for x in source_data["horse_race_list"] if x["horsenum"] == source_data["horsenum"]]
        rap_no3 = [x["last_rap2"] for x in source_data["horse_race_list"] if x["horsenum"] == source_data["horsenum"]]
        if len(rap_base) == 0 or len(rap_no3) == 0:
            return 0
        return rap_no3[0] <= rap_base[0]+0.5
    def get_dl_element108(self, source_data):
        rap_base = [x["last_rap3"] for x in source_data["horse_race_list"] if x["horsenum"] == source_data["horsenum"]]
        rap_no4 = [x["last_rap1"] for x in source_data["horse_race_list"] if x["horsenum"] == source_data["horsenum"]]
        if len(rap_base) == 0 or len(rap_no4) == 0:
            return 0
        return rap_no4[0] <= rap_base[0]+0.5
    def get_dl_element109(self, source_data):
        if len(source_data["all_horse_past"]) == 0:
            return 0
        odds_under10 = [x[0]["odds"] for x in source_data["all_horse_past"] if len(x) > 0 and x[0]["odds"] != "" and x[0]["odds"] <= 10 and x[0]["odds"] > 0]
        return max(len(odds_under10),5)/5
    def get_dl_element110(self, source_data):
        odds = source_data["past_list"][0]["odds"]
        return odds != "" and odds <= 10 and odds > 0
    def get_dl_element111(self, source_data):
        time_diff = [x["time_diff"] for x in source_data["horse_race_list"] if x["horsenum"] == source_data["horsenum"]]
        if len(time_diff) == 0:
            return 1
        return min(max(time_diff[0],-3.5),3.5)/3.5

    def make_output_list(self, source_data):
        retlist = [0, 0]
        target_hrl = self.get_target_data_from_horse_race_list(source_data)
        if target_hrl["time_diff"] <= 0.1 and target_hrl["goal_order"] >= 1:
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

    # [0, 0, 0, 0]の形式、 ３着内率を配当で細分化したものに変換
    def convert_fullgate_goal_list(self, goal, today_time_diff, dividend):
        goal_list = []
        goal_feature = 0
        if today_time_diff <= 0.1:
            goal_feature = 0
        else:
            goal_feature = 1
        for i in range(2):
            if i == goal_feature:
                goal_list.append(1)
            else:
                goal_list.append(0)
        return goal_list
    def get_output_list_title(self):
        return ["place","race","horsename","horsenum","date","~0.1s","other","goal","timediff","dividend"]
    def get_number_of_output_kind(self):
        return len(self.get_output_list_title())-8
