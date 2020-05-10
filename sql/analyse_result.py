# coding: utf-8
import sql_pattern
import os
import csv
import parse
from datetime import datetime as dt
import keras
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout
from keras.optimizers import Adamax 
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
        self.main_placeA_list = ["中山","阪神"]
        self.main_placeB_list = ["京都","東京"]
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
            for dct in single_race:
                if dct["today_zi"] != 0:
                    zi_list.append(dct["today_zi"])
                if dct["horsename"] != horse_name:
                    horse_count = horse_count + 1
                    horse_name = dct["horsename"]
                if dct["today_jockey_name"] in self.kami_jockey_list:
                    kamij_count = kamij_count + 1
                if dct["today_jockey_name"] in self.chuana_jockey_list:
                    chuanaj_count = chuanaj_count + 1
            for dct in single_race:
                single_learn = []
                #single_learn.append(self.get_dl_element_ex1(dct))
                #single_learn.append(self.get_dl_element1(dct,zi_list))
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
                single_learn.append(self.get_dl_element32(dct))
                single_learn.append(self.get_dl_element33(dct))
                single_learn.append(self.get_dl_element34(dct))
                single_learn.append(self.get_dl_element35(dct))
                single_learn.append(self.get_dl_element36(dct))
                single_learn.append(self.get_dl_element37(dct))
                single_learn.append(self.get_dl_element38(dct))
                single_learn.append(self.get_dl_element39(dct))
                single_learn.append(self.get_dl_element40(dct))
                single_learn.append(self.get_dl_element41(dct))
                single_learn.append(self.get_dl_element42(dct))
                single_learn.append(self.get_dl_element43(dct))
                single_learn.append(self.get_dl_element44(dct))
                single_learn.append(self.get_dl_element45(dct))
                single_learn.append(self.get_dl_element46(dct))
                single_learn.append(self.get_dl_element47(dct))
                single_learn.append(self.get_dl_element48(dct))

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
    # そのレースのZI平均より大きいか
    def get_dl_element1(self, dct, zi_list):
        if dct["today_zi"] == 0 or len(zi_list) == 0:
            return 0
        mx_mn_diff = max(max(zi_list)-min(zi_list),1)
        diff = max(dct["today_zi"]-sum(zi_list)/len(zi_list),0)
        return diff/mx_mn_diff
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
    # 過去走の馬体重
    def get_dl_element7(self, dct):
        return (min(max(dct["past_horseweight"],380),560)-380)/180
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
    # 過去走は芝かダートか
    def get_dl_element15(self, dct):
        if dct["past_turf_dirt"] == "芝":
            return 1
        return 0
    # 過去走の馬場状態インデックス2進数の2桁目
    def get_dl_element16(self, dct):
        bi = '{:02b}'.format(self.get_condition_index(dct["past_course_condition"]))
        return bi[1]
    # 過去走の馬場状態インデックス2進数の1桁目
    def get_dl_element17(self, dct):
        bi = '{:02b}'.format(self.get_condition_index(dct["past_course_condition"]))
        return bi[0]
    # 今回の距離は過去走より長いか
    def get_dl_element18(self, dct):
        return min(max(dct["today_distance"]-dct["past_distance"],0),1000)/1000
    # 今回の距離は過去走より短いか
    def get_dl_element19(self,dct):
        return min(max(dct["past_distance"]-dct["today_distance"],0),1000)/1000
    # レース間隔が１年以上空いているか
    def get_dl_element20(self, dct):
        diff = (dct["today_rdate"]-dct["past_rdate"]).days
        if diff > 350:
            return (max(diff,750)-350)/400
        return 0
    # 今回のクラスランク2進数の2桁目
    def get_dl_element21(self, dct):
        bi = '{:02b}'.format(self.get_class_rank(dct["today_class"]))
        return bi[1]
    # 今回のクラスランク2進数の1桁目
    def get_dl_element22(self, dct):
        bi = '{:02b}'.format(self.get_class_rank(dct["today_class"]))
        return bi[0]
    # 過去走のクラスランク2進数の2桁目
    def get_dl_element23(self, dct):
        bi = '{:02b}'.format(self.get_class_rank(dct["past_class"]))
        return bi[1]
    # 過去走のクラスランク2進数の1桁目
    def get_dl_element24(self, dct):
        bi = '{:02b}'.format(self.get_class_rank(dct["past_class"]))
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
    # 過去走は阪神・中山開催か
    def get_dl_element32(self, dct):
        if dct["past_place"] in self.main_placeA_list:
            return 1
        return 0
    # 過去走は京都・東京開催か
    def get_dl_element33(self, dct):
        if dct["past_place"] in self.main_placeB_list:
            return 1
        return 0
    # 今回は阪神・中山開催か
    def get_dl_element34(self, dct):
        if dct["today_place"] in self.main_placeA_list:
            return 1
        return 0
    # 今回は京都・東京開催か
    def get_dl_element35(self, dct):
        if dct["today_place"] in self.main_placeB_list:
            return 1
        return 0
    # 過去走は上がり3F地点差2s以上の差があるか
    def get_dl_element36(self, dct):
        if dct["past_diff3f"] >= 2.0:
            return 1
        return 0
    # 前走の着差
    def get_dl_element37(self, dct):
        return min(dct["past_time_diff"],2.5)/2.5
    # 今回の距離インデックス4桁目
    def get_dl_element38(self, dct):
        bi = '{:04b}'.format(self.get_distance_index(dct["today_distance"]))
        return bi[3]
    # 今回の距離インデックス3桁目
    def get_dl_element39(self, dct):
        bi = '{:04b}'.format(self.get_distance_index(dct["today_distance"]))
        return bi[2]
    # 今回の距離インデックス2桁目
    def get_dl_element40(self, dct):
        bi = '{:04b}'.format(self.get_distance_index(dct["today_distance"]))
        return bi[1]
    # 今回の距離インデックス1桁目
    def get_dl_element41(self, dct):
        bi = '{:04b}'.format(self.get_distance_index(dct["today_distance"]))
        return bi[0]
    # 過去走の距離インデックス4桁目
    def get_dl_element42(self, dct):
        bi = '{:04b}'.format(self.get_distance_index(dct["past_distance"]))
        return bi[3]
    # 過去走の距離インデックス3桁目
    def get_dl_element43(self, dct):
        bi = '{:04b}'.format(self.get_distance_index(dct["past_distance"]))
        return bi[2]
    # 過去走の距離インデックス2桁目
    def get_dl_element44(self, dct):
        bi = '{:04b}'.format(self.get_distance_index(dct["past_distance"]))
        return bi[1]
    # 過去走の距離インデックス1桁目
    def get_dl_element45(self, dct):
        bi = '{:04b}'.format(self.get_distance_index(dct["past_distance"]))
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
    # 過去走の馬体重
    def get_dl_element48(self, dct):
        return (min(max(dct["past_horseweight"],380),560)-380)/180.0

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

    # クラスランク0~3を取得
    def get_class_rank(self, cls):
        if cls in ["未勝利","新馬"]:
            return 0
        if cls in ["500万","1勝"]:
            return 1
        if cls in ["1000万","2勝","1600万","3勝"]:
            return 2
        return 3

    # 馬場状態インデックスを取得
    def get_condition_index(self, cond):
        if cond == "不":
            return 0
        if cond == "重":
            return 1
        if cond == "稍":
            return 2
        if cond == "良":
            return 3
        return 0

    # 距離インデックスを取得
    def get_distance_index(self, dist):
        if dist < 1000:
            return 0
        if dist <= 1000:
            return 1
        if dist <= 1150:
            return 2
        if dist <= 1200:
            return 3
        if dist <= 1300:
            return 4
        if dist <= 1400:
            return 5
        if dist <= 1500:
            return 6
        if dist <= 1600:
            return 7
        if dist <= 1700:
            return 8
        if dist <= 1800:
            return 9
        if dist <= 2000:
            return 10
        if dist <= 2200:
            return 11
        if dist <= 2600:
            return 12
        if dist > 2600:
            return 13
        return 0

    def convert_fullgate_goal_list(self, goal):
        goal_list = []
        goal_feature = 0
        if goal <= 2 and goal != 0:
            goal_feature = 0
        else:
            goal_feature = 1

        for i in range(2):
            if i == goal_feature:
                goal_list.append(1)
            else:
                goal_list.append(0)
        return goal_list

# deep learning "methods part"
    def deep_learning(self, x_train, y_train, dim, horsename_list, pred_x_np, todayinfo_lst):
        model = Sequential()
        model.add(Dense(dim*2, activation='relu', input_dim=dim))
        model.add(Dropout(0.3))
        model.add(BatchNormalization())
        model.add(Dense(dim*2, activation='relu'))
        model.add(Dropout(0.3))
        model.add(BatchNormalization())
        model.add(Dense(dim*2, activation='relu'))
        model.add(Dropout(0.3))
        model.add(BatchNormalization())
        model.add(Dense(2, activation='softmax'))

        adamax = Adamax()
        model.compile(loss='categorical_crossentropy', optimizer=adamax, metrics=['accuracy'])

        history = model.fit(x_train, y_train, epochs=120, batch_size=5000, validation_split=0.1)
        #loss, accuracy = model.evaluate(x_train[29000:],y_train[29000:],verbose=0)
        #print("Accuracy = {:.2f}".format(accuracy))
        
        # モデル、学習済の重みを保存
        open('deep_model.json',"w").write(model.to_json())
        model.save_weights('deep_model.h5')

    def output_deeplearning_result_to_csv(self , pred_x_np, todayinfo_lst):
        model = model_from_json(open('deep_model.json',"r").read())
        model.load_weights('deep_model.h5')

        with open("../deeplearning_result.csv","w") as f:
            writer = csv.writer(f)
            writer.writerow(["place","race","horsename","~2nd","3rd~"])
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
# ディープラーニング, 読み込むだけのときはコメントアウトする
#ar.deep_learning(x_np, y_np, dim, hn_lst, pred_x_np, todayinfo_lst)
ar.output_deeplearning_result_to_csv(pred_x_np, todayinfo_lst)
