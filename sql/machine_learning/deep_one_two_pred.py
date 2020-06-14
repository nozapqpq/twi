# coding: utf-8
from . import deep_utility
import json

class DeepOneTwoPred():
    def __init__(self):
        self.util = deep_utility.Utility()
        self.today_date = ""
        self.european_grass_list = ["札幌","函館"]
        self.spiral_list = ["札幌","函館","小倉","福島"]
        self.west_list = ["小倉","阪神","京都","中京"]
        self.kami_jockey_list = ["モレイラ","ルメール","レーン","川田将雅","ムーア","マーフィ","Ｍ．デム","Ｃ．デム","北村友一","福永祐一","戸崎圭太","武豊"]

    # input_lst[1レース分][1頭分]
    def make_deeplearning_data(self, input_lst, json_fn=""):
        count = 0
        learn = [] # 学習用
        target = [] # 予想対象
        ans = []
        horsename_lst = []
        todayinfo_lst = []
        if json_fn != "":
            json_open = open(json_fn,'r')
            json_load = json.load(json_open)
        for single_race in input_lst:
            zi_list = []
            horse_name = ""
            horse_count = 0
            kamij_count = 0
            for dct in single_race:
                if dct["today_zi"] != 0:
                    zi_list.append(dct["today_zi"])
                if dct["horsename"] != horse_name:
                    horse_count = horse_count + 1
                    horse_name = dct["horsename"]
                if dct["today_jockey_name"] in self.kami_jockey_list:
                    kamij_count = kamij_count + 1
            for dct in single_race:
                single_learn = []
                for ptn in json_load["object_list"]:
                    if ptn["activate"] == "on":
                        exec_cmd = self.util.get_exec_command(ptn["func"],ptn["args"])
                        single_learn.append(eval(exec_cmd))
                # 本日と過去走のデータリストを作成、障害や出走取り消し等で着順が入っていないデータは双方から除外
                if (dct["today_rdate"] == self.today_date and not "障害" in dct["today_turf_dirt"]):
                    target.append(single_learn)
                    todayinfo_lst.append([dct["today_place"],dct["today_race"],dct["horsename"]])
                elif dct["today_goal"] != 0:
                    learn.append(single_learn)
                    ans.append([dct["today_goal"],dct["today_triple_dividend"]])
                    horsename_lst.append(dct["horsename"])
        return learn, ans, horsename_lst, target, todayinfo_lst

    # 国分恭介くんが乗っているか
    def get_dl_element_ex1(self, dct):
        if dct["today_jockey_name"] == "国分恭介":
            return 1
        return 0
    # 過去走は芝かダートか 
    def get_dl_element1(self, dct):
        if dct["past_turf_dirt"] == "芝":
            return 1
        return 0
    # 今回は芝かダートか
    def get_dl_element2(self, dct):
        if dct["today_turf_dirt"] == "芝":
            return 1
        return 0
    # 上がり3F地点差
    def get_dl_element3(self, dct):
        if dct["past_diviation"] == 0:
            return 0
        return (3-max(dct["past_diff3f"],3))/3
    # 過去走の偏差値 
    def get_dl_element4(self, dct):
        return (min(max(dct["past_diviation"],20),70)-20)/50
    # 偏差値データなしか
    def get_dl_element5(self, dct):
        if (dct["past_diviation"] == 0):
            return 1
        return 0
    # 10頭未満のレースか
    def get_dl_element6(self, horse_count):
        if horse_count < 10:
            return 1
        return 0
    # 今回と過去走の馬体重差
    def get_dl_element7(self, dct):
        return min(max(dct["today_horseweight"]-dct["past_horseweight"],-20),20)/40+0.5
    # 今回の馬体重 
    def get_dl_element8(self, dct):
        return (min(max(dct["today_horseweight"],380),560)-380)/180
    # 今回の斤量
    def get_dl_element9(self, dct):
        return (min(max(dct["today_jockey_weight"],48),60)-48)/12
    # 今回と過去走の斤量差
    def get_dl_element10(self, dct):
        return min(max(dct["today_jockey_weight"]-dct["past_jockey_weight"],-12),12)/24+0.5
    # 過去走馬番
    def get_dl_element11(self, dct):
        return (dct["past_horsenum"]-1)/17
    # 今回馬番
    def get_dl_element12(self, dct):
        return (dct["today_horsenum"]-1)/17 
    # 今回コースグループ1
    def get_dl_element13(self, dct):
        if "[G001]" in dct["today_course_mark"]:
            return 1
        return 0
    # 今回コースグループ2
    def get_dl_element14(self, dct):
        if "[G002]" in dct["today_course_mark"]:
            return 1
        return 0
    # 今回コースグループ3 
    def get_dl_element15(self, dct):
        if "[G003]" in dct["today_course_mark"]:
            return 1
        return 0
    # 過去走の馬場状態インデックス2進数の2桁目
    def get_dl_element16(self, dct):
        bi = '{:02b}'.format(self.util.get_condition_index(dct["past_course_condition"]))
        return bi[1]
    # 過去走の馬場状態インデックス2進数の1桁目
    def get_dl_element17(self, dct):
        bi = '{:02b}'.format(self.util.get_condition_index(dct["past_course_condition"]))
        return bi[0]
    # 転厩初戦か
    def get_dl_element18(self, dct):
        if "転初" in dct["transfer"]:
            return 1
        return 0
    # 去勢空けか
    def get_dl_element19(self,dct):
        if "去初" in dct["castration"]:
            return 1
        return 0
    # ブランク
    def get_dl_element20(self, dct):
        return min(dct["today_span"]-1,20)/20
    # 今回のクラスランク2進数の2桁目
    def get_dl_element21(self, dct):
        bi = '{:02b}'.format(self.util.get_class_rank(dct["today_class"]))
        return bi[1]
    # 今回のクラスランク2進数の1桁目
    def get_dl_element22(self, dct):
        bi = '{:02b}'.format(self.util.get_class_rank(dct["today_class"]))
        return bi[0]
    # 過去走のクラスランク2進数の2桁目
    def get_dl_element23(self, dct):
        bi = '{:02b}'.format(self.util.get_class_rank(dct["past_class"]))
        return bi[1]
    # 過去走のクラスランク2進数の1桁目
    def get_dl_element24(self, dct):
        bi = '{:02b}'.format(self.util.get_class_rank(dct["past_class"]))
        return bi[0] 
    # 神ジョッキーが今回のレースに何人乗るか
    def get_dl_element25(self, dct, j_count):
        count = max([j_count,8])
        if count == 0:
            return 0
        return (count+8)/16
    # 前半ラップ57s+二進数000の3桁目
    def get_dl_element26(self, dct):
        bi = '{:03b}'.format(min(max(int(dct["past_rap5f"]),57),64)-57)
        return bi[2]
    # 前半ラップ57s+二進数000の2桁目
    def get_dl_element27(self, dct):
        bi = '{:03b}'.format(min(max(int(dct["past_rap5f"]),57),64)-57)
        return bi[1] 
    # 前半ラップ57s+二進数000の1桁目
    def get_dl_element28(self, dct):
        bi = '{:03b}'.format(min(max(int(dct["past_rap5f"]),57),64)-57)
        return bi[0]
    # 神ジョッキーが乗るか
    def get_dl_element29(self, dct):
        if dct["today_jockey_name"] in self.kami_jockey_list:
            return 1
        return 0
    # 過去走の偏差値のσ値 
    def get_dl_element30(self, dct):
        return min(dct["past_sigma"],5.0)/5.0
    # 過去走の平均着順
    def get_dl_element31(self, dct):
        return min(dct["past_mean_goal"],12.0)/12.0
    # 今回コースグループ4
    def get_dl_element32(self, dct):
        if "[G004]" in dct["today_course_mark"]:
            return 1
        return 0
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
    def convert_fullgate_goal_list(self, goal, triple):
        goal_list = []
        goal_feature = 0
        if goal <= 3 and goal != 0 and triple <= 10000:
            goal_feature = 0
        elif goal <= 3 and goal != 0 and triple <= 50000:
            goal_feature = 1
        elif goal <= 3 and goal != 0 and triple > 50000:
            goal_feature = 2
        else:
            goal_feature = 3
        for i in range(4):
            if i == goal_feature:
                goal_list.append(1)
            else:
                goal_list.append(0)
        return goal_list
