# coding: utf-8
from . import deep_single_race
from . import deep_utility
import json
import re

class DeepOneTwoPred():
    def __init__(self):
        self.util = deep_utility.Utility()
        self.sr = deep_single_race.DeepSingleRace()
        self.today_date = ""
        self.slow_pace = self.util.get_slow_pace_all_data()
        self.jockey = self.util.get_jockey_all_data()
        self.stallion = self.util.get_stallion_all_data()
        self.trainer = self.util.get_trainer_all_data()
        self.temperature = self.util.get_temperature_from_json("machine_learning/deep_temperature.json")
        self.european_grass_list = ["札幌","函館"]
        self.spiral_list = ["札幌","函館","小倉","福島"]
        self.main_place_list = ["中山","東京","京都","阪神"]
        self.stallion_type = ["その他","ロイヤルチャージャー系","ネイティヴダンサー系","ニアークティック系","ナスルーラ系","セントサイモン系","マンノウォー系","トウルビヨン系"]

    # input_lst[1レース分][1頭分]
    def make_deeplearning_data(self, input_lst, json_fn="", use_blank=False):
        dl_input_list = [] # 学習用
        dl_output_dict_list = [] # 学習用正当データ
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
                if not (use_blank == False and dct["today_goal"] == 0):
                    dl_input_list.append(single_learn)
                    dl_output_dict_list.append({"goalorder":dct["today_goal"],"timediff":dct["today_time_diff"],"dividend":dct["today_dividend"]})
        return dl_input_list, dl_output_dict_list

    def get_dl_element1(self, dct):
        return self.util.get_condition_index(dct["today_course_condition"])
    def get_dl_element2(self, dct):
        return self.util.get_condition_index(dct["past_course_condition"])
    def get_dl_element3(self, dct):
        if "転初" in dct["transfer"]:
            return 1
        return 0
    def get_dl_element4(self,dct):
        if "去初" in dct["castration"]:
            return 1
        return 0
    def get_dl_element5(self, dct):
        bi = '{:02b}'.format(self.util.get_class_rank(dct["today_class"]))
        return int(bi[0])
    def get_dl_element6(self, dct):
        bi = '{:02b}'.format(self.util.get_class_rank(dct["today_class"]))
        return int(bi[1])
    def get_dl_element7(self, dct):
        bi = '{:02b}'.format(self.util.get_class_rank(dct["past_class"]))
        return int(bi[0])
    def get_dl_element8(self, dct):
        bi = '{:02b}'.format(self.util.get_class_rank(dct["past_class"]))
        return int(bi[1])
    def get_dl_element9(self, dct):
        if self.sr.whole_race_dict["top_odds"] <= 1.5:
            return 1
        return 0
    def get_dl_element10(self, dct):
        if self.sr.whole_race_dict["top_odds"] <= 2.0:
            return 1
        return 0
    def get_dl_element11(self, dct):
        if self.sr.whole_race_dict["top_odds"] <= 3.0:
            return 1
        return 0
    def get_dl_element12(self, dct):
        if self.sr.single_horse_dicts[dct["today_horsenum"]-1]["zi_diff_from_top"] <= 5:
            return 1
        return 0
    def get_dl_element13(self, dct):
        if self.sr.single_horse_dicts[dct["today_horsenum"]-1]["zi_diff_from_top"] <= 10:
            return 1
        return 0
    def get_dl_element14(self, dct):
        if self.sr.single_horse_dicts[dct["today_horsenum"]-1]["zi_diff_from_top"] <= 15:
            return 1
        return 0
    def get_dl_element15(self, dct):
        if self.sr.single_horse_dicts[dct["today_horsenum"]-1]["zi_diff_from_top"] <= 20:
            return 1
        return 0
    def get_dl_element16(self, dct):
        if self.sr.single_horse_dicts[dct["today_horsenum"]-1]["zi_diff_from_top"] <= 30:
            return 1
        return 0
    def get_dl_element17(self, dct):
        if dct["past_time_diff"] <= -1.0:
            return 1
        return 0
    def get_dl_element18(self, dct):
        if dct["past_time_diff"] <= -0.5:
            return 1
        return 0
    def get_dl_element19(self, dct):
        if dct["past_time_diff"] <= 0.0:
            return 1
        return 0
    def get_dl_element20(self, dct):
        if dct["past_time_diff"] <= 0.2:
            return 1
        return 0
    def get_dl_element21(self, dct):
        if dct["past_time_diff"] <= 0.5:
            return 1
        return 0
    def get_dl_element22(self, dct):
        if dct["past_time_diff"] <= 1.0:
            return 1
        return 0
    def get_dl_element23(self, dct):
        if dct["past_time_diff"] <= 1.5:
            return 1
        return 0
    def get_dl_element24(self, dct):
        if dct["past_time_diff"] <= 2.0:
            return 1
        return 0
    def get_dl_element25(self, dct):
        if self.sr.whole_race_dict["pop_tddiff"]:
            return 1
        return 0
    def get_dl_element26(self, dct):
        if self.sr.whole_race_dict["west_count"]/self.sr.whole_race_dict["horse_total"] >= 0.01:
            return 1
        return 0
    def get_dl_element27(self, dct):
        if self.sr.whole_race_dict["west_count"]/self.sr.whole_race_dict["horse_total"] >= 0.30:
            return 1
        return 0
    def get_dl_element28(self, dct):
        if self.sr.whole_race_dict["west_count"]/self.sr.whole_race_dict["horse_total"] >= 0.60:
            return 1
        return 0
    def get_dl_element29(self, dct):
        if self.sr.whole_race_dict["west_count"]/self.sr.whole_race_dict["horse_total"] == 1:
            return 1
        return 0
    def get_dl_element30(self, dct):
        if self.sr.whole_race_dict["youngjockey_count"]/self.sr.whole_race_dict["horse_total"] >= 0.01:
            return 1
        return 0
    def get_dl_element31(self, dct):
        if self.sr.whole_race_dict["youngjockey_count"]/self.sr.whole_race_dict["horse_total"] >= 0.30:
            return 1
        return 0
    def get_dl_element32(self, dct):
        if self.sr.whole_race_dict["youngjockey_count"]/self.sr.whole_race_dict["horse_total"] >= 0.60:
            return 1
        return 0
    def get_dl_element33(self, dct):
        if self.sr.whole_race_dict["youngjockey_count"]/self.sr.whole_race_dict["horse_total"] == 1:
            return 1
        return 0
    def get_dl_element34(self, dct):
        if dct["today_span"] == 1:
            return 1
        return 0
    def get_dl_element35(self, dct):
        if dct["past_distance"] == dct["today_distance"] and dct["past_turf_dirt"] == dct["today_turf_dirt"] and (dct["past_course_condition"] == "良" or dct["past_course_condition"] == "稍"):
            if self.sr.whole_race_dict["fastest_time"] != 0 and dct["past_race_time"] <= self.sr.whole_race_dict["fastest_time"]+0.5:
                return 1
        return 0
    def get_dl_element36(self, dct):
        if self.util.get_class_priority(dct["today_class"]) >= 2:
            return 1
        return 0
    def get_dl_element37(self, dct):
        if dct["today_horsenum"]%2 == 1:
            return 1
        return 0
    def get_dl_element38(self, dct):
        if dct["breeder"] == "ノーザンファーム":
            return 1
        return 0
    def get_dl_element39(self, dct):
        if dct["horse_sex"] == "牝":
            return 1
        return 0
    def get_dl_element40(self, dct):
        bi = '{:03b}'.format(min(dct["horse_age"]-2,7))
        return int(bi[0])
    def get_dl_element41(self, dct):
        bi = '{:03b}'.format(min(dct["horse_age"]-2,7))
        return int(bi[1])
    def get_dl_element42(self, dct):
        bi = '{:03b}'.format(min(dct["horse_age"]-2,7))
        return int(bi[2])
    def get_dl_element43(self, dct):
        single = [x for x in self.stallion if x['name']==dct['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor1"]))
            return int(bi[0])
    def get_dl_element44(self, dct):
        single = [x for x in self.stallion if x['name']==dct['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor1"]))
            return int(bi[1])
    def get_dl_element45(self, dct):
        single = [x for x in self.stallion if x['name']==dct['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor1"]))
            return int(bi[2])
    def get_dl_element46(self, dct):
        single = [x for x in self.stallion if x['name']==dct['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor2"]))
            return int(bi[0])
    def get_dl_element47(self, dct):
        single = [x for x in self.stallion if x['name']==dct['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor2"]))
            return int(bi[1])
    def get_dl_element48(self, dct):
        single = [x for x in self.stallion if x['name']==dct['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor2"]))
            return int(bi[2])
    def get_dl_element49(self, dct):
        single = [x for x in self.stallion if x['name']==dct['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor3"]))
            return int(bi[0])
    def get_dl_element50(self, dct):
        single = [x for x in self.stallion if x['name']==dct['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor3"]))
            return int(bi[1])
    def get_dl_element51(self, dct):
        single = [x for x in self.stallion if x['name']==dct['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor3"]))
            return int(bi[2])
    def get_dl_element52(self, dct):
        single = [x for x in self.stallion if x['name']==dct['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor4"]))
            return int(bi[0])
    def get_dl_element53(self, dct):
        single = [x for x in self.stallion if x['name']==dct['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor4"]))
            return int(bi[1])
    def get_dl_element54(self, dct):
        single = [x for x in self.stallion if x['name']==dct['stallion']]
        if len(single) == 0:
            return 0
        else:
            bi = '{:03b}'.format(self.stallion_type.index(single[0]["ancestor4"]))
            return int(bi[2])
    def get_dl_element55(self, dct):
        single = [x for x in self.trainer if x['name']==dct['trainer']]
        if len(single) == 0:
            return 0
        else:
            if single[0]['belongs'] == "栗東":
                return 1
            return 0
    def get_dl_element56(self, dct):
        if "[G001]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element57(self, dct):
        if "[G002]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element58(self, dct):
        if "[G003]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element59(self, dct):
        if "[G004]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element60(self, dct):
        if "[G005]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element61(self, dct):
        if "[G006]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element62(self, dct):
        if "[G007]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element63(self, dct):
        if "[G008]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element64(self, dct):
        if "[G009]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element65(self, dct):
        if "[G010]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element66(self, dct):
        if "[G011]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element67(self, dct):
        if "[G012]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element68(self, dct):
        if "[G013]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element69(self, dct):
        if "[G014]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element70(self, dct):
        if "[G015]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element71(self, dct):
        if "[G016]" in dct["today_course_mark"]:
            return 1
        return 0
    def get_dl_element72(self, dct):
        if "[G001]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element73(self, dct):
        if "[G002]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element74(self, dct):
        if "[G003]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element75(self, dct):
        if "[G004]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element76(self, dct):
        if "[G005]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element77(self, dct):
        if "[G006]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element78(self, dct):
        if "[G007]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element79(self, dct):
        if "[G008]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element80(self, dct):
        if "[G009]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element81(self, dct):
        if "[G010]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element82(self, dct):
        if "[G011]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element83(self, dct):
        if "[G012]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element84(self, dct):
        if "[G013]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element85(self, dct):
        if "[G014]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element86(self, dct):
        if "[G015]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element87(self, dct):
        if "[G016]" in dct["past_course_mark"]:
            return 1
        return 0
    def get_dl_element88(self, dct):
        if dct["today_turf_dirt"] == "芝" and dct["today_distance"] >= 1000:
            return 1
        return 0
    def get_dl_element89(self, dct):
        if dct["today_turf_dirt"] == "芝" and dct["today_distance"] >= 1400:
            return 1
        return 0
    def get_dl_element90(self, dct):
        if dct["today_turf_dirt"] == "芝" and dct["today_distance"] >= 1800:
            return 1
        return 0
    def get_dl_element91(self, dct):
        if dct["today_turf_dirt"] == "芝" and dct["today_distance"] >= 2400:
            return 1
        return 0
    def get_dl_element92(self, dct):
        if dct["today_turf_dirt"] != "芝" and dct["today_distance"] >= 1000:
            return 1
        return 0
    def get_dl_element93(self, dct):
        if dct["today_turf_dirt"] != "芝" and dct["today_distance"] >= 1400:
            return 1
        return 0
    def get_dl_element94(self, dct):
        if dct["today_turf_dirt"] != "芝" and dct["today_distance"] >= 1800:
            return 1
        return 0
    def get_dl_element95(self, dct):
        if dct["today_turf_dirt"] != "芝" and dct["today_distance"] >= 2400:
            return 1
        return 0
    def get_dl_element96(self, dct):
        if dct["past_turf_dirt"] == "芝" and dct["past_distance"] >= 1000:
            return 1
        return 0
    def get_dl_element97(self, dct):
        if dct["past_turf_dirt"] == "芝" and dct["past_distance"] >= 1400:
            return 1
        return 0
    def get_dl_element98(self, dct):
        if dct["past_turf_dirt"] == "芝" and dct["past_distance"] >= 1800:
            return 1
        return 0
    def get_dl_element99(self, dct):
        if dct["past_turf_dirt"] == "芝" and dct["past_distance"] >= 2400:
            return 1
        return 0
    def get_dl_element100(self, dct):
        if dct["past_turf_dirt"] != "芝" and dct["past_distance"] >= 1000:
            return 1
        return 0
    def get_dl_element101(self, dct):
        if dct["past_turf_dirt"] != "芝" and dct["past_distance"] >= 1400:
            return 1
        return 0
    def get_dl_element102(self, dct):
        if dct["past_turf_dirt"] != "芝" and dct["past_distance"] >= 1800:
            return 1
        return 0
    def get_dl_element103(self, dct):
        if dct["past_turf_dirt"] != "芝" and dct["past_distance"] >= 2400:
            return 1
        return 0
    def get_dl_element104(self, dct):
        if dct["past_early_rap2"] >= 11.0:
            return 1
        return 0
    def get_dl_element105(self, dct):
        if dct["past_early_rap2"] >= 11.5:
            return 1
        return 0
    def get_dl_element106(self, dct):
        if dct["past_early_rap2"] >= 12.0:
            return 1
        return 0
    def get_dl_element107(self, dct):
        if dct["past_early_rap2"] >= 12.5:
            return 1
        return 0
    def get_dl_element108(self, dct):
        if dct["past_early_rap2"] >= 13.0:
            return 1
        return 0
    def get_dl_element109(self, dct):
        if dct["past_early_rap3"] >= 11.0:
            return 1
        return 0
    def get_dl_element110(self, dct):
        if dct["past_early_rap3"] >= 11.5:
            return 1
        return 0
    def get_dl_element111(self, dct):
        if dct["past_early_rap3"] >= 12.0:
            return 1
        return 0
    def get_dl_element112(self, dct):
        if dct["past_early_rap3"] >= 12.5:
            return 1
        return 0
    def get_dl_element113(self, dct):
        if dct["past_early_rap3"] >= 13.0:
            return 1
        return 0
    def get_dl_element114(self, dct):
        if dct["past_early_rap4"] >= 11.0:
            return 1
        return 0
    def get_dl_element115(self, dct):
        if dct["past_early_rap4"] >= 11.5:
            return 1
        return 0
    def get_dl_element116(self, dct):
        if dct["past_early_rap4"] >= 12.0:
            return 1
        return 0
    def get_dl_element117(self, dct):
        if dct["past_early_rap4"] >= 12.5:
            return 1
        return 0
    def get_dl_element118(self, dct):
        if dct["past_early_rap4"] >= 13.0:
            return 1
        return 0
    def get_dl_element119(self, dct):
        if dct["past_last_rap1"] >= 11.0:
            return 1
        return 0
    def get_dl_element120(self, dct):
        if dct["past_last_rap1"] >= 11.5:
            return 1
        return 0
    def get_dl_element121(self, dct):
        if dct["past_last_rap1"] >= 12.0:
            return 1
        return 0
    def get_dl_element122(self, dct):
        if dct["past_last_rap1"] >= 12.5:
            return 1
        return 0
    def get_dl_element123(self, dct):
        if dct["past_last_rap1"] >= 13.0:
            return 1
        return 0
    def get_dl_element124(self, dct):
        if dct["past_last_rap2"] >= 11.0:
            return 1
        return 0
    def get_dl_element125(self, dct):
        if dct["past_last_rap2"] >= 11.5:
            return 1
        return 0
    def get_dl_element126(self, dct):
        if dct["past_last_rap2"] >= 12.0:
            return 1
        return 0
    def get_dl_element127(self, dct):
        if dct["past_last_rap2"] >= 12.5:
            return 1
        return 0
    def get_dl_element128(self, dct):
        if dct["past_last_rap2"] >= 13.0:
            return 1
        return 0
    def get_dl_element129(self, dct):
        if dct["past_last_rap3"] >= 11.0:
            return 1
        return 0
    def get_dl_element130(self, dct):
        if dct["past_last_rap3"] >= 11.5:
            return 1
        return 0
    def get_dl_element131(self, dct):
        if dct["past_last_rap3"] >= 12.0:
            return 1
        return 0
    def get_dl_element132(self, dct):
        if dct["past_last_rap3"] >= 12.5:
            return 1
        return 0
    def get_dl_element133(self, dct):
        if dct["past_last_rap3"] >= 13.0:
            return 1
        return 0
    def get_dl_element134(self, dct):
        if dct["past_last_rap4"] >= 11.0:
            return 1
        return 0
    def get_dl_element135(self, dct):
        if dct["past_last_rap4"] >= 11.5:
            return 1
        return 0
    def get_dl_element136(self, dct):
        if dct["past_last_rap4"] >= 12.0:
            return 1
        return 0
    def get_dl_element137(self, dct):
        if dct["past_last_rap4"] >= 12.5:
            return 1
        return 0
    def get_dl_element138(self, dct):
        if dct["past_last_rap4"] >= 13.0:
            return 1
        return 0
    def get_dl_element139(self, dct):
        if dct["past_diff3f"] <= 0.1:
            return 1
        return 0
    def get_dl_element140(self, dct):
        if dct["past_diff3f"] <= 0.3:
            return 1
        return 0
    def get_dl_element141(self, dct):
        if dct["past_diff3f"] <= 0.5:
            return 1
        return 0
    def get_dl_element142(self, dct):
        if dct["past_diff3f"] <= 1.0:
            return 1
        return 0
    def get_dl_element143(self, dct):
        if dct["past_diff3f"] <= 1.5:
            return 1
        return 0
    def get_dl_element144(self, dct):
        if dct["today_horsenum"] <= 3:
            return 1
        return 0
    def get_dl_element145(self, dct):
        if dct["today_horsenum"] <= 6:
            return 1
        return 0
    def get_dl_element146(self, dct):
        if dct["today_horsenum"] <= 9:
            return 1
        return 0
    def get_dl_element147(self, dct):
        if dct["today_horsenum"] <= 12:
            return 1
        return 0
    def get_dl_element148(self, dct):
        if dct["today_horsenum"] <= 15:
            return 1
        return 0
    def get_dl_element149(self, dct):
        if dct["past_odds"] <= 2.0:
            return 1
        return 0
    def get_dl_element150(self, dct):
        if dct["past_odds"] <= 5.0:
            return 1
        return 0
    def get_dl_element151(self, dct):
        if dct["past_odds"] <= 10.0:
            return 1
        return 0
    def get_dl_element152(self, dct):
        if dct["past_odds"] <= 20.0:
            return 1
        return 0
    def get_dl_element153(self, dct):
        if dct["past_odds"] <= 30.0:
            return 1
        return 0
    def get_dl_element154(self, dct):
        if dct["past_odds"] <= 50.0:
            return 1
        return 0
    def get_dl_element155(self, dct):
        if dct["past_odds"] <= 100.0:
            return 1
        return 0
    def get_dl_element156(self, dct):
        if dct["today_span"] <= 2:
            return 1
        return 0
    def get_dl_element157(self, dct):
        if dct["today_span"] <= 4:
            return 1
        return 0
    def get_dl_element158(self, dct):
        if dct["today_span"] <= 8:
            return 1
        return 0
    def get_dl_element159(self, dct):
        if dct["today_span"] <= 16:
            return 1
        return 0
    def get_dl_element160(self, dct):
        if dct["today_span"] <= 32:
            return 1
        return 0
    def get_dl_element161(self, dct):
        if dct["today_span"] <= 48:
            return 1
        return 0
    def get_dl_element162(self, dct):
        if (dct["today_rdate"]-dct["past_rdate"]).days <= 15:
            return 1
        return 0
    def get_dl_element163(self, dct):
        if (dct["today_rdate"]-dct["past_rdate"]).days <= 30:
            return 1
        return 0
    def get_dl_element164(self, dct):
        if (dct["today_rdate"]-dct["past_rdate"]).days <= 60:
            return 1
        return 0
    def get_dl_element165(self, dct):
        if (dct["today_rdate"]-dct["past_rdate"]).days <= 120:
            return 1
        return 0
    def get_dl_element166(self, dct):
        if (dct["today_rdate"]-dct["past_rdate"]).days <= 240:
            return 1
        return 0
    def get_dl_element167(self, dct):
        if (dct["today_rdate"]-dct["past_rdate"]).days <= 360:
            return 1
        return 0
    def get_dl_element168(self, dct):
        if dct["past_rap5f"] <= 57.0:
            return 1
        return 0
    def get_dl_element169(self, dct):
        if dct["past_rap5f"] <= 57.5:
            return 1
        return 0
    def get_dl_element170(self, dct):
        if dct["past_rap5f"] <= 58.0:
            return 1
        return 0
    def get_dl_element171(self, dct):
        if dct["past_rap5f"] <= 58.5:
            return 1
        return 0
    def get_dl_element172(self, dct):
        if dct["past_rap5f"] <= 59.0:
            return 1
        return 0
    def get_dl_element173(self, dct):
        if dct["past_rap5f"] <= 59.5:
            return 1
        return 0
    def get_dl_element174(self, dct):
        if dct["past_rap5f"] <= 60.0:
            return 1
        return 0
    def get_dl_element175(self, dct):
        if dct["past_rap5f"] <= 60.5:
            return 1
        return 0
    def get_dl_element176(self, dct):
        if dct["past_rap5f"] <= 61.0:
            return 1
        return 0
    def get_dl_element177(self, dct):
        if dct["past_rap5f"] <= 61.5:
            return 1
        return 0
    def get_dl_element178(self, dct):
        if dct["past_rap5f"] <= 62.0:
            return 1
        return 0
    def get_dl_element179(self, dct):
        if dct["past_rap5f"] <= 62.5:
            return 1
        return 0
    def get_dl_element180(self, dct):
        if dct["past_rap5f"] <= 63.0:
            return 1
        return 0
    def get_dl_element181(self, dct):
        if dct["past_rap5f"] <= 63.5:
            return 1
        return 0
    def get_dl_element182(self, dct):
        if dct["past_rap5f"] <= 64.0:
            return 1
        return 0
    def get_dl_element183(self, dct):
        if self.sr.whole_race_dict["younghorse_count"]/self.sr.whole_race_dict["horse_total"] >= 0.01:
            return 1
        return 0
    def get_dl_element184(self, dct):
        if self.sr.whole_race_dict["younghorse_count"]/self.sr.whole_race_dict["horse_total"] >= 0.3:
            return 1
        return 0
    def get_dl_element185(self, dct):
        if self.sr.whole_race_dict["younghorse_count"]/self.sr.whole_race_dict["horse_total"] >= 0.6:
            return 1
        return 0
    def get_dl_element186(self, dct):
        if self.sr.whole_race_dict["younghorse_count"]/self.sr.whole_race_dict["horse_total"] == 1:
            return 1
        return 0
    def get_dl_element187(self, dct):
        if self.sr.whole_race_dict["stag_count"]/self.sr.whole_race_dict["horse_total"] >= 0.01:
            return 1
        return 0
    def get_dl_element188(self, dct):
        if self.sr.whole_race_dict["stag_count"]/self.sr.whole_race_dict["horse_total"] >= 0.30:
            return 1
        return 0
    def get_dl_element189(self, dct):
        if self.sr.whole_race_dict["stag_count"]/self.sr.whole_race_dict["horse_total"] >= 0.60:
            return 1
        return 0
    def get_dl_element190(self, dct):
        if self.sr.whole_race_dict["stag_count"]/self.sr.whole_race_dict["horse_total"] == 1:
            return 1
        return 0
    def get_dl_element191(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_front"] >= 10:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_front"] >= 10:
            return 1
        return 0
    def get_dl_element192(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_front"] >= 20:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_front"] >= 20:
            return 1
        return 0
    def get_dl_element193(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_front"] >= 30:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_front"] >= 30:
            return 1
        return 0
    def get_dl_element194(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_front"] >= 40:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_front"] >= 40:
            return 1
        return 0
    def get_dl_element195(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_stay"] >= 10:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_stay"] >= 10:
            return 1
        return 0
    def get_dl_element196(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_stay"] >= 20:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_stay"] >= 20:
            return 1
        return 0
    def get_dl_element197(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_stay"] >= 30:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_stay"] >= 30:
            return 1
        return 0
    def get_dl_element198(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_stay"] >= 40:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_stay"] >= 40:
            return 1
        return 0
    def get_dl_element199(self, dct):
        temperature = self.util.get_temperature(self.temperature, dct)
        if temperature <= 15:
            return 1
        return 0
    def get_dl_element200(self, dct):
        temperature = self.util.get_temperature(self.temperature, dct)
        if temperature <= 25:
            return 1
        return 0
    def get_dl_element201(self, dct):
        if "武豊" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element202(self, dct):
        if "松山弘平" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element203(self, dct):
        if "和田竜二" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element204(self, dct):
        if "幸英明" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element205(self, dct):
        if "大野拓弥" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element206(self, dct):
        if "三浦皇成" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element207(self, dct):
        if "横山武史" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element208(self, dct):
        if "松若風馬" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element209(self, dct):
        if "内田博幸" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element210(self, dct):
        if "ルメール" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element211(self, dct):
        if "丹内祐次" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element212(self, dct):
        if "藤岡康太" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element213(self, dct):
        if "田辺裕信" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element214(self, dct):
        if "福永祐一" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element215(self, dct):
        if "岩田康誠" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element216(self, dct):
        if "吉田隼人" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element217(self, dct):
        if "西村淳也" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element218(self, dct):
        if "岩田望来" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element219(self, dct):
        if "野中悠太" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element220(self, dct):
        if "丸山元気" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element221(self, dct):
        if "藤田菜七" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element222(self, dct):
        if "斎藤新" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element223(self, dct):
        if "北村友一" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element224(self, dct):
        if "木幡巧也" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element225(self, dct):
        if "団野大成" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element226(self, dct):
        if "武藤雅" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element227(self, dct):
        if "柴田大知" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element228(self, dct):
        if "川田将雅" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element229(self, dct):
        if "津村明秀" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element230(self, dct):
        if "坂井瑠星" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element231(self, dct):
        if "Ｍ．デム" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element232(self, dct):
        if "戸崎圭太" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element233(self, dct):
        if "鮫島克駿" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element234(self, dct):
        if "藤岡佑介" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element235(self, dct):
        if "池添謙一" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element236(self, dct):
        if "菅原明良" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element237(self, dct):
        if "石橋脩" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element238(self, dct):
        if "江田照男" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element239(self, dct):
        if "亀田温心" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element240(self, dct):
        if "菱田裕二" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element241(self, dct):
        if "酒井学" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element242(self, dct):
        if "北村宏司" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element243(self, dct):
        if "木幡育也" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element244(self, dct):
        if "山田敬士" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element245(self, dct):
        if "菊沢一樹" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element246(self, dct):
        if "石川裕紀" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element247(self, dct):
        if "浜中俊" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element248(self, dct):
        if "古川吉洋" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element249(self, dct):
        if "国分恭介" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element250(self, dct):
        if "川又賢治" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element251(self, dct):
        if "国分優作" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element252(self, dct):
        if "横山和生" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element253(self, dct):
        if "荻野極" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element254(self, dct):
        if "吉田豊" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element255(self, dct):
        if "勝浦正樹" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element256(self, dct):
        if "横山典弘" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element257(self, dct):
        if "藤井勘一" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element258(self, dct):
        if "川須栄彦" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element259(self, dct):
        if "秋山真一" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element260(self, dct):
        if "柴山雄一" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element261(self, dct):
        if "太宰啓介" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element262(self, dct):
        if "丸田恭介" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element263(self, dct):
        if "武士沢友" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element264(self, dct):
        if "柴田善臣" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element265(self, dct):
        if "黛弘人" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element266(self, dct):
        if "松岡正海" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element267(self, dct):
        if "田中勝春" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element268(self, dct):
        if "小牧太" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element269(self, dct):
        if "小林凌大" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element270(self, dct):
        if "富田暁" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element271(self, dct):
        if "松田大作" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element272(self, dct):
        if "小崎綾也" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element273(self, dct):
        if "藤懸貴志" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element274(self, dct):
        if "高倉稜" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element275(self, dct):
        if "中井裕二" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element276(self, dct):
        if "杉原誠人" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element277(self, dct):
        if "泉谷楓真" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element278(self, dct):
        if "宮崎北斗" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element279(self, dct):
        if "加藤祥太" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element280(self, dct):
        if "中谷雄太" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element281(self, dct):
        if "嘉藤貴行" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element282(self, dct):
        if "森裕太朗" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element283(self, dct):
        if "鮫島良太" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element284(self, dct):
        if "川島信二" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element285(self, dct):
        if "ミナリク" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element286(self, dct):
        if "木幡初也" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element287(self, dct):
        if "西田雄一" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element288(self, dct):
        if "嶋田純次" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element289(self, dct):
        if "水口優也" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element290(self, dct):
        if "田中健" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element291(self, dct):
        if "レーン" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element292(self, dct):
        if "和田翼" in self.sr.whole_race_dict["jockey_list"] or "岩崎翼" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element293(self, dct):
        if "岩部純二" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element294(self, dct):
        if "マーフィ" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element295(self, dct):
        if "城戸義政" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element296(self, dct):
        if "蛯名正義" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element297(self, dct):
        if "秋山稔樹" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element298(self, dct):
        if "原優介" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element299(self, dct):
        if "岡田祥嗣" in self.sr.whole_race_dict["jockey_list"]:
            return 1
        return 0
    def get_dl_element300(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 56.0:
            return 1
        return 0
    def get_dl_element301(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 56.5:
            return 1
        return 0
    def get_dl_element302(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 57.0:
            return 1
        return 0
    def get_dl_element303(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 57.5:
            return 1
        return 0
    def get_dl_element304(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 58.0:
            return 1
        return 0
    def get_dl_element305(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 58.5:
            return 1
        return 0
    def get_dl_element306(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 59.0:
            return 1
        return 0
    def get_dl_element307(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 59.5:
            return 1
        return 0
    def get_dl_element308(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 60.0:
            return 1
        return 0
    def get_dl_element309(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 60.5:
            return 1
        return 0
    def get_dl_element310(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 61.0:
            return 1
        return 0
    def get_dl_element311(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 61.5:
            return 1
        return 0
    def get_dl_element312(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 62.0:
            return 1
        return 0
    def get_dl_element313(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 62.5:
            return 1
        return 0
    def get_dl_element314(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 63.0:
            return 1
        return 0
    def get_dl_element315(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 63.5:
            return 1
        return 0
    def get_dl_element316(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 64.0:
            return 1
        return 0
    def get_dl_element317(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 64.5:
            return 1
        return 0
    def get_dl_element318(self, dct):
        if self.sr.whole_race_dict["rap5f"] >= 65.0:
            return 1
        return 0
    def get_dl_element319(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 32.0:
            return 1
        return 0
    def get_dl_element320(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 32.5:
            return 1
        return 0
    def get_dl_element321(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 33.0:
            return 1
        return 0
    def get_dl_element322(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 33.5:
            return 1
        return 0
    def get_dl_element323(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 34.0:
            return 1
        return 0
    def get_dl_element324(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 34.5:
            return 1
        return 0
    def get_dl_element325(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 35.0:
            return 1
        return 0
    def get_dl_element326(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 35.5:
            return 1
        return 0
    def get_dl_element327(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 36.0:
            return 1
        return 0
    def get_dl_element328(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 36.5:
            return 1
        return 0
    def get_dl_element329(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 37.0:
            return 1
        return 0
    def get_dl_element330(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 37.5:
            return 1
        return 0
    def get_dl_element331(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 38.0:
            return 1
        return 0
    def get_dl_element332(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 38.5:
            return 1
        return 0
    def get_dl_element333(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 39.0:
            return 1
        return 0
    def get_dl_element334(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 39.5:
            return 1
        return 0
    def get_dl_element335(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 40.0:
            return 1
        return 0
    def get_dl_element336(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 40.5:
            return 1
        return 0
    def get_dl_element337(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 41.0:
            return 1
        return 0
    def get_dl_element338(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 41.5:
            return 1
        return 0
    def get_dl_element339(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 42.0:
            return 1
        return 0
    def get_dl_element340(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 42.5:
            return 1
        return 0
    def get_dl_element341(self, dct):
        if self.sr.whole_race_dict["last3f"] >= 43.0:
            return 1
        return 0


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
        return ["place","race","horsename","horsenum","date","~0.2s or ~2nd","other","goal","timediff","dividend"]
    def get_number_of_output_kind(self):
        return len(self.get_output_list_title())-8
