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
        self.jockey = self.util.get_jockey_all_data()
        self.stallion = self.util.get_stallion_all_data()
        self.trainer = self.util.get_trainer_all_data()
        self.european_grass_list = ["札幌","函館"]
        self.spiral_list = ["札幌","函館","小倉","福島"]
        self.main_place_list = ["中山","東京","京都","阪神"]
        self.stallion_type = ["その他","ロイヤルチャージャー系","ネイティヴダンサー系","ニアークティック系","ナスルーラ系","セントサイモン系","マンノウォー系","トウルビヨン系"]

    # input_lst[1レース分][1頭分]
    def make_deeplearning_data(self, input_lst, json_fn=""):
        learn = [] # 学習用
        target = [] # 予想対象
        ans = [] # 学習用正当データ
        horsename_lst = [] # 馬名データ
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
                elif dct["today_goal"] != 0:
                    learn.append(single_learn)
                    ans.append([dct["today_goal"],dct["today_time_diff"],dct["today_dividend"]])
                    horsename_lst.append(dct["horsename"])
        return learn, ans, horsename_lst, target
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
        if dct["today_turf_dirt"] == "芝" and dct["today_distance"] >= 1300:
            return 1
        return 0
    def get_dl_element89(self, dct):
        if dct["today_turf_dirt"] == "芝" and dct["today_distance"] >= 1600:
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
        if dct["today_turf_dirt"] != "芝" and dct["today_distance"] >= 1300:
            return 1
        return 0
    def get_dl_element93(self, dct):
        if dct["today_turf_dirt"] != "芝" and dct["today_distance"] >= 1600:
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
        if dct["past_turf_dirt"] == "芝" and dct["past_distance"] >= 1300:
            return 1
        return 0
    def get_dl_element97(self, dct):
        if dct["past_turf_dirt"] == "芝" and dct["past_distance"] >= 1600:
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
        if dct["past_turf_dirt"] != "芝" and dct["past_distance"] >= 1300:
            return 1
        return 0
    def get_dl_element101(self, dct):
        if dct["past_turf_dirt"] != "芝" and dct["past_distance"] >= 1600:
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
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_front"] >= 15:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_front"] >= 15:
            return 1
        return 0
    def get_dl_element192(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_front"] >= 30:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_front"] >= 30:
            return 1
        return 0
    def get_dl_element193(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_front"] >= 45:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_front"] >= 45:
            return 1
        return 0
    def get_dl_element194(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_front"] >= 60:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_front"] >= 60:
            return 1
        return 0
    def get_dl_element195(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_stay"] >= 15:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_stay"] >= 15:
            return 1
        return 0
    def get_dl_element196(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_stay"] >= 30:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_stay"] >= 30:
            return 1
        return 0
    def get_dl_element197(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_stay"] >= 45:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_stay"] >= 45:
            return 1
        return 0
    def get_dl_element198(self, dct):
        jk = [x for x in self.jockey if x["name"]==dct["today_jockey_name"]]
        if len(jk) == 0:
            return 0
        if dct["today_turf_dirt"] == "芝" and jk[0]["turf_stay"] >= 60:
            return 1
        if dct["today_turf_dirt"] == "ダート" and jk[0]["dirt_stay"] >= 60:
            return 1
        return 0



    # [0, 0, 0, 0]の形式、 ３着内率を配当で細分化したものに変換
    def convert_fullgate_goal_list(self, goal, today_time_diff, dividend):
        goal_list = []
        goal_feature = 0
        if today_time_diff <= 0.2:
            goal_feature = 0
        elif goal <= 3:
            goal_feature = 1
        else:
            goal_feature = 2
        for i in range(3):
            if i == goal_feature:
                goal_list.append(1)
            else:
                goal_list.append(0)
        return goal_list
    def get_output_list_title(self):
        return ["place","race","horsename","~0.2s","~3rd","other","goal","timediff","dividend"]
    def get_number_of_output_kind(self):
        return len(self.get_output_list_title())-6
