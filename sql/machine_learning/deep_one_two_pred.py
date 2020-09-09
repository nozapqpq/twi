# coding: utf-8
from . import deep_utility
import json

class DeepOneTwoPred():
    def __init__(self):
        self.util = deep_utility.Utility()
        self.today_date = ""
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
        if json_fn != "":
            json_open = open(json_fn,'r')
            json_load = json.load(json_open)
        for single_race in input_lst:
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
    # 前半ラップ57s+二進数000の2桁目
    def get_dl_element(self, dct):
        bi = '{:03b}'.format(min(max(int(dct["past_rap5f"]),57),64)-57)
        return bi[1] 
    # 前半ラップ57s+二進数000の1桁目
    def get_dl_element(self, dct):
        bi = '{:03b}'.format(min(max(int(dct["past_rap5f"]),57),64)-57)
        return bi[0]
    # 過去走の偏差値のσ値 
    def get_dl_element(self, dct):
        return min(dct["past_sigma"],5.0)/5.0
    # 過去走の平均着順
    def get_dl_element(self, dct):
        return min(dct["past_mean_goal"],12.0)/12.0
    # 今回コースグループ5
    def get_dl_element33(self, dct):
        if "[G005]" in dct["today_course_mark"]:
            return 1
        return 0
    # 今回コースグループ6
    def get_dl_element34(self, dct):
        if "[G006]" in dct["today_course_mark"]:
            return 1
        return 0
    # 今回の馬場状態インデックス2進数の2桁目
    def get_dl_element35(self, dct):
        bi = '{:02b}'.format(self.util.get_condition_index(dct["today_course_condition"]))
        return bi[1]
    # 今回の馬場状態インデックス2進数の1桁目
    def get_dl_element36(self, dct):
        bi = '{:02b}'.format(self.util.get_condition_index(dct["today_course_condition"]))
        return bi[0]
    # 過去走の着差
    def get_dl_element37(self, dct):
        return min(dct["past_time_diff"],2.5)/2.5
    # 今回の距離インデックス4桁目
    def get_dl_element38(self, dct):
        bi = '{:04b}'.format(self.util.get_distance_index(dct["today_distance"]))
        return bi[3]
    # 今回の距離インデックス3桁目
    def get_dl_element39(self, dct):
        bi = '{:04b}'.format(self.util.get_distance_index(dct["today_distance"]))
        return bi[2]
    # 今回の距離インデックス2桁目
    def get_dl_element40(self, dct):
        bi = '{:04b}'.format(self.util.get_distance_index(dct["today_distance"]))
        return bi[1]
    # 今回の距離インデックス1桁目
    def get_dl_element41(self, dct):
        bi = '{:04b}'.format(self.util.get_distance_index(dct["today_distance"]))
        return bi[0]
    # 過去走の距離インデックス4桁目
    def get_dl_element42(self, dct):
        bi = '{:04b}'.format(self.util.get_distance_index(dct["past_distance"]))
        return bi[3]
    # 過去走の距離インデックス3桁目
    def get_dl_element43(self, dct):
        bi = '{:04b}'.format(self.util.get_distance_index(dct["past_distance"]))
        return bi[2]
    # 過去走の距離インデックス2桁目
    def get_dl_element44(self, dct):
        bi = '{:04b}'.format(self.util.get_distance_index(dct["past_distance"]))
        return bi[1]
    # 過去走の距離インデックス1桁目
    def get_dl_element45(self, dct):
        bi = '{:04b}'.format(self.util.get_distance_index(dct["past_distance"]))
        return bi[0]
    # 過去走の上がり3Fはレース上がりより速いか
    def get_dl_element46(self, dct):
        diff = min(dct["past_race_last3f"]-dct["past_horse_last3f"],2.0)
        if diff >= 0.2:
            return (diff-0.2)/1.8
        return 0
    # 過去走の上がり3Fはレース上がりより遅いか
    def get_dl_element47(self, dct):
        diff = min(dct["past_horse_last3f"]-dct["past_race_last3f"],2.0)
        if diff >= 0.2:
            return (diff-0.2)/1.8
        return 0
    # 過去走は上がり3F地点差2s以上の差があるか
    def get_dl_element48(self, dct):
        if dct["past_diff3f"] >= 2.0:
            return 1
        return 0
    # 最高と最低を除いたZI値の範囲
    def get_dl_element49(self, dct, zi_list):
        if len(zi_list) < 3:
            return 0
        return min(sorted(zi_list)[-2]-sorted(zi_list)[1],40)/40
    # 最高と2番目のZI値の差
    def get_dl_element50(self, dct, zi_list):
        if len(zi_list) < 3:
            return 0
        return min(sorted(zi_list)[-1]-sorted(zi_list)[-2],40)/40
    # ZI最高値の馬か
    def get_dl_element51(self, dct, zi_list):
        if dct["today_zi"] == sorted(zi_list)[-1]:
            return 1
        return 0
    # 連闘か
    def get_dl_element52(self, dct):
        if dct["today_span"] == 1:
            return 1
        return 0
    # 過去走コースグループ1
    def get_dl_element53(self, dct):
        if "[G001]" in dct["past_course_mark"]:
            return 1
        return 0
    # 過去走コースグループ2
    def get_dl_element54(self, dct):
        if "[G002]" in dct["past_course_mark"]:
            return 1
        return 0
    # 過去走コースグループ3
    def get_dl_element55(self, dct):
        if "[G003]" in dct["past_course_mark"]:
            return 1
        return 0
    # 過去走コースグループ4
    def get_dl_element56(self, dct):
        if "[G004]" in dct["past_course_mark"]:
            return 1
        return 0
    # 過去走コースグループ5
    def get_dl_element57(self, dct):
        if "[G005]" in dct["past_course_mark"]:
            return 1
        return 0
    # 過去走コースグループ6
    def get_dl_element58(self, dct):
        if "[G006]" in dct["past_course_mark"]:
            return 1
        return 0
    # 過去走洋芝コースか
    def get_dl_element59(self, dct):
        if dct["past_place"] in self.european_grass_list and dct["past_turf_dirt"] == "芝":
            return 1
        return 0
    # 今回洋芝コースか
    def get_dl_element60(self, dct):
        if dct["today_place"] in self.european_grass_list and dct["today_turf_dirt"] == "芝":
            return 1
        return 0
    # 過去走スパイラルカーブか
    def get_dl_element61(self, dct):
        if dct["past_place"] in self.spiral_list:
            return 1
        return 0
    # 今回スパイラルカーブか
    def get_dl_element62(self, dct):
        if dct["today_place"] in self.spiral_list:
            return 1
        return 0
    # 過去走西のコースか
    def get_dl_element63(self, dct):
        if dct["past_place"] in self.west_list:
            return 1
        return 0
    # 今回西のコースか
    def get_dl_element64(self, dct):
        if dct["today_place"] in self.west_list:
            return 1
        return 0
    # 過去走PCIとレースPCIの差
    def get_dl_element65(self, dct):
        if dct["past_pci"] == 0 or dct["past_rpci"] == 0:
            return 0.5
        diff = max(min(dct["past_pci"]-dct["past_rpci"],10),-10)/20+0.5
        return diff

    # [0, 0, 0, 0]の形式、 ３着内率を配当で細分化したものに変換
    def convert_fullgate_goal_list(self, goal, today_time_diff, triple):
        goal_list = []
        goal_feature = 0
        if today_time_diff <= 0.1: 
            goal_feature = 0
        elif today_time_diff <= 0.3:
            goal_feature = 1
        elif today_time_diff <= 0.7:
            goal_feature = 2
        elif today_time_diff <= 1.5:
            goal_feature = 3
        else:
            goal_feature = 4
        for i in range(5):
            if i == goal_feature:
                goal_list.append(1)
            else:
                goal_list.append(0)
        return goal_list
    def get_output_list_title(self):
        return ["place","race","horsename","~0.1s","~0.3s","~0.7s","~1.5s","1.6s~"]
    def get_number_of_output_kind(self):
        return len(self.get_output_list_title())-3
