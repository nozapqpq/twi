# coding: utf-8
import sql_pattern
import os
import csv
import parse
from datetime import datetime as dt
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
import numpy as np
class AnalyseResult():
    def __init__(self):
        self.pat = sql_pattern.SQLPattern()
        self.today_pred_target = []
        self.today_date = ""
        self.output_target_list = []
        self.output_target_date = ""
        self.left_turning_list = ["新潟","中京","東京"]
        self.small_turning_list = ["札幌","函館","小倉","福島"]
        self.west_list = ["小倉","阪神","京都","中京"]
        self.zako_list = ["未勝利","1勝","500万","新馬"]
        self.kami_jockey_list = ["モレイラ","ルメール","レーン","川田将雅","ムーア","マーフィ","Ｍ．デム","Ｃ．デム","北村友一","福永祐一","戸崎圭太","武豊"]
        self.chuana_jockey_list = ["ルメール","川田将雅","フォーリ","Ｍ．デム","田辺裕信","北村友一","松田大作","松山弘平","福永祐一","シュタル","戸崎圭太","岩田康誠","石橋脩","勝浦正樹","武豊","三浦皇成","浜中俊","国分恭介","丸山元気","秋山真一","池添謙一"]

    def get_main_data_from_csv(self):
        entry_horses_list = []
        all_files = os.listdir(path='..')
        # 名前が日付になっているフォルダを取得
        dir_list = [f for f in all_files if os.path.isdir(os.path.join('..',f)) and f[0].isdigit()]

        dir_count = 0
        # フォルダ毎、main.csvを取得していく
        for dl in dir_list:
            csv_list = self.get_maincsv_list_from_dir(dl)
            self.today_date = self.get_date_from_dirname(dl)
            for fl in csv_list:
                print("../"+dl+"."+fl)
                main_dict = self.pat.get_maindata_dict_from_csv("../"+dl+"/"+fl)
                entry_horses_list.append(main_dict)
        return entry_horses_list

    # input_lst[1レース分][1頭分]
    def make_deeplearning_data(self, input_lst):
        count = 0
        learn = [] # 学習用
        target = [] # 予想対象
        ans = []
        horsename_lst = []
        todayinfo_lst = []
        for single_race in input_lst:
            zi_list = []
            horse_name = ""
            horse_count = 0
            kamij_count = 0
            chuanaj_count = 0
            max_zi = 0
            for dct in single_race:
                zi_list.append(dct["today_zi"])
                if dct["horsename"] != horse_name:
                    horse_count = horse_count + 1
                    horse_name = dct["horsename"]
                if dct["today_jockey_name"] in self.kami_jockey_list:
                    kamij_count = kamij_count + 1
                if dct["today_jockey_name"] in self.chuana_jockey_list:
                    chuanaj_count = chuanaj_count + 1
            try:
                max_zi = max(zi_list)
            except:
                max_zi = 0
            for dct in single_race:
                single_learn = []
                single_learn.append(self.get_dl_element_ex1(dct))
                single_learn.append(self.get_dl_element1(dct,max_zi))
                single_learn.append(self.get_dl_element2(dct))
                single_learn.append(self.get_dl_element3(dct))
                single_learn.append(self.get_dl_element4(dct))
                single_learn.append(self.get_dl_element5(dct))
                single_learn.append(self.get_dl_element6(horse_count))
                single_learn.append(self.get_dl_element7(dct))
                single_learn.append(self.get_dl_element8(dct))
                single_learn.append(self.get_dl_element9(dct))
                single_learn.append(self.get_dl_element10(dct))
                single_learn.append(self.get_dl_element11(dct))
                single_learn.append(self.get_dl_element12(dct))
                single_learn.append(self.get_dl_element13(dct))
                single_learn.append(self.get_dl_element14(dct))
                single_learn.append(self.get_dl_element15(dct))
                single_learn.append(self.get_dl_element16(dct))
                single_learn.append(self.get_dl_element17(dct))
                single_learn.append(self.get_dl_element18(dct))
                single_learn.append(self.get_dl_element19(dct))
                single_learn.append(self.get_dl_element20(dct))
                single_learn.append(self.get_dl_element21(dct))
                single_learn.append(self.get_dl_element22(dct))
                single_learn.append(self.get_dl_element23(dct))
                single_learn.append(self.get_dl_element24(dct))
                single_learn.append(self.get_dl_element25(dct, kamij_count))
                single_learn.append(self.get_dl_element26(dct))
                single_learn.append(self.get_dl_element27(dct))
                single_learn.append(self.get_dl_element28(dct))
                single_learn.append(self.get_dl_element29(dct))
                single_learn.append(self.get_dl_element30(dct))
                single_learn.append(self.get_dl_element31(dct))

                # 本日と過去走のデータリストを作成、障害や出走取り消し等で着順が入っていないデータは双方から除外
                if (dct["today_rdate"] == self.today_date and not "障害" in dct["today_turf_dirt"]):
                    target.append(single_learn)
                    todayinfo_lst.append([dct["today_place"],dct["today_race"],dct["horsename"]])
                elif dct["today_goal"] != 0:
                    learn.append(single_learn)
                    ans.append(dct["today_goal"])
                    horsename_lst.append(dct["horsename"])
        return learn, ans, horsename_lst, target, todayinfo_lst

    # 国分恭介くんが乗っているか
    def get_dl_element_ex1(self, dct):
        if dct["today_jockey_name"] == "国分恭介":
            return 1
        return 0
    # そのレースの最大ZIの馬との差
    def get_dl_element1(self, dct, max_zi):
        diff = max_zi-dct["today_zi"]
        if max_zi == 0:
            return 0
        return diff/max_zi
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
    # 偏差値60以上か
    def get_dl_element4(self, dct):
        if (dct["past_diviation"] >= 60):
            return 1
        return 0
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
    # 偏差値40以下か
    def get_dl_element7(self, dct):
        if dct["past_diviation"] <= 40:
            return 1
        return 0
    # 過去走は小回りか
    def get_dl_element8(self, dct):
        if dct["past_place"] in self.small_turning_list:
            return 1
        return 0
    # 今回は小回りか
    def get_dl_element9(self, dct):
        if dct["today_place"] in self.small_turning_list:
            return 1
        return 0
    # 過去走は左回りか
    def get_dl_element10(self, dct):
        if dct["past_place"] in self.left_turning_list:
            return 1
        return 0
    # 今回は左回りか
    def get_dl_element11(self, dct):
        if dct["today_place"] in self.left_turning_list:
            return 1
        return 0
    # 過去走は西のレースか
    def get_dl_element12(self, dct):
        if dct["past_place"] in self.west_list:
            return 1
        return 0
    # 今回は西のレースか
    def get_dl_element13(self, dct):
        if dct["today_place"] in self.west_list:
            return 1
        return 0
    # 斤量
    def get_dl_element14(self, dct):
        return (min(dct["today_jockey_weight"],60)-48)/12
    # 今回は500万以下のレースか
    def get_dl_element15(self, dct):
        if dct["today_class"] in self.zako_list:
            return 1
        return 0
    # 過去走の距離は1600m以下か
    def get_dl_element16(self, dct):
        return (1600-min(dct["past_distance"],1600))/1600
    # 今回の距離は1600m以下か
    def get_dl_element17(self, dct):
        return (1600-min(dct["past_distance"],1600))/1600
    # 今回の距離は過去走より長いか
    def get_dl_element18(self, dct):
        return min(max(dct["today_distance"]-dct["past_distance"],0),1000)/1000
    # 今回の距離は過去走より短いか
    def get_dl_element19(self,dct):
        return min(max(dct["past_distance"]-dct["today_distance"],0),1000)/1000
    # 偏差値70以上か
    def get_dl_element20(self, dct):
        if (dct["past_diviation"] >= 70):
            return 1
        return 0
    # 今回と過去走でクラスが別か
    def get_dl_element21(self, dct):
        if (dct["past_class"] != dct["today_class"]):
            return 1
        return 0
    # 今回と過去走で芝/ダートが異なるか
    def get_dl_element22(self, dct):
        if (dct["past_turf_dirt"] != dct["today_turf_dirt"]):
            return 1
        return 0
    # 今回が1000万以上で過去走が未勝利・新馬か
    def get_dl_element23(self, dct):
        if (not dct["today_class"] in self.zako_list and dct["past_class"] in ["未勝利","新馬"]):
            return 1
        return 0
    # 神ジョッキーが乗るか
    def get_dl_element24(self, dct):
        if dct["today_jockey_name"] in self.kami_jockey_list:
            return 1
        return 0
    # 神ジョッキーが今回のレースに何人乗るか
    def get_dl_element25(self, dct, j_count):
        count = max([j_count,8])
        if count == 0:
            return 0
        return (count+8)/16
    # 前半ラップは58s以内か
    def get_dl_element26(self, dct):
        if dct["past_rap5f"] <= 58:
            return 1
        return 0
    # 前半ラップは60s以内か
    def get_dl_element27(self, dct):
        if dct["past_rap5f"] <= 60:
            return 1
        return 0
    # 前半ラップは62s以内か
    def get_dl_element28(self, dct):
        if dct["past_rap5f"] <= 62:
            return 1
        return 0
    # 前半ラップは64s以内か
    def get_dl_element29(self, dct):
        if dct["past_rap5f"] <= 64:
            return 1
        return 0
    # 過去走で上がり3Fはレース上がりより速かったか
    def get_dl_element30(self, dct):
        diff = dct["past_horse_last3f"]-dct["past_race_last3f"]
        diff = min([diff,-3.0])
        if diff > 0:
            return 0
        return (diff-3.0)/(-6.0)
    # 過去走で上がり3Fはレース上がりより遅かったか
    def get_dl_element31(self, dct):
        diff = dct["past_horse_last3f"]-dct["past_race_last3f"]
        diff = max([diff,3.0])
        if diff < 0:
            return 0
        return (diff+3.0)/6.0

    # ディレクトリ名"yymmdd"から日付を取得
    def get_date_from_dirname(self, dirname):
        yyyymmdd = "20"+dirname[0:2]+"-"+dirname[2:4]+"-"+dirname[4:6]
        return dt.strptime(yyyymmdd,'%Y-%m-%d')

    def get_maincsv_list_from_dir(self, dirname):
        pathname = "../"+dirname
        all_files = os.listdir(path=pathname)
        file_list = [f for f in all_files if "main_" in f]
        return file_list

    def get_mainlist_from_csv(self, filename):
        with open(filename,'r') as f:
            retlist = []
            reader = csv.reader(f)
            count = 0
            for row in reader:
                if count != 0:
                    retlist.append(row)
                count = count + 1
        return retlist

    def convert_nondigit_to_strzero(self, target):
        if not target.isdecimal():
            try:
                float(target)
                return target
            except ValueError:
                return "0"
        else:
            return target

    def convert_fullgate_goal_list(self, goal):
        goal_list = []
        goal_feature = 0
        if goal == 1:
            goal_feature = 0
        elif goal <= 3 and goal != 0:
            goal_feature = 1
        elif goal <= 5 and goal != 0:
            goal_feature = 2
        elif goal <= 10 and goal != 0:
            goal_feature = 3
        else:
            goal_feature = 4

        for i in range(5):
            if i == goal_feature:
                goal_list.append(1)
            else:
                goal_list.append(0)
        return goal_list

# deep learning "methods part"
    def deep_learning(self, x_train, y_train, dim, horsename_list, pred_x_np, todayinfo_lst):
        model = Sequential()
        model.add(Dense(dim*3, activation='relu', input_dim=dim))
        model.add(Dropout(0))
        model.add(BatchNormalization())
        model.add(Dense(dim*5, activation='relu'))
        model.add(Dropout(0))
        model.add(BatchNormalization())
        model.add(Dense(dim*5, activation='relu'))
        model.add(Dropout(0.5))
        model.add(BatchNormalization())
        model.add(Dense(5, activation='softmax'))

        adam = Adam()
        model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

        history = model.fit(x_train, y_train, epochs=30, batch_size=100, validation_split=0.1)
        #loss, accuracy = model.evaluate(x_train[29000:],y_train[29000:],verbose=0)
        #print("Accuracy = {:.2f}".format(accuracy))
        output_list = []
        with open("../deeplearning_result.csv","w") as f:
            writer = csv.writer(f)
            writer.writerow(["place","race","horsename","1st","~3rd","~5th","~10th","11th~"])
            for i in range(len(pred_x_np)):
                score = list(model.predict(pred_x_np[i].reshape(1,dim))[0])
                writer.writerow(todayinfo_lst[i]+score)

goal_list = []
ar = AnalyseResult()
lst = ar.get_main_data_from_csv()
learn_lst, ans_lst, hn_lst, target, todayinfo_lst = ar.make_deeplearning_data(lst)
dim = len(learn_lst[0])
# 着順分類リスト作成
for i in range(len(learn_lst)):
    gl = ar.convert_fullgate_goal_list(ans_lst[i])
    goal_list.append(gl)
# 各リストのnumpy化
x_np = np.array(learn_lst)
y_np = np.array(goal_list)
pred_x_np = np.array(target)
# ディープラーニング
ar.deep_learning(x_np, y_np, dim, hn_lst, pred_x_np, todayinfo_lst)
