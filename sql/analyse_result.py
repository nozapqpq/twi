# coding: utf-8
import sql_pattern
import utility
import machine_learning.deep_one_two_pred
import machine_learning.deep_utility
import os
import csv
from datetime import datetime as dt
import keras
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout
from keras.optimizers import Adamax 
from keras.layers.normalization import BatchNormalization
import numpy as np
import seaborn as sns
import matplotlib as mpl
import sklearn

# place_listに入っている場所に対するディープラーニングを利用できる
# ディープラーニングの性能を図りたいときはresearch_flg = True
place_list = ["東京","阪神","福島"]
research_flg = True
all_place_flg = True
all_td_flg = False

class AnalyseResult():
    def __init__(self):
        self.pat = sql_pattern.SQLPattern()
        self.dotp = machine_learning.deep_one_two_pred.DeepOneTwoPred()
        self.ml_util = machine_learning.deep_utility.Utility()
        self.util = utility.Utility()
        self.json_name = "deep_model.json"
        self.h5_name = "deep_model.h5"
        # csv出力用
        self.result_list = []
        self.research_result_list = []
        self.favorite_list = []

    def set_deep_model_name(self, place_dict):
        place_list = ["札幌","函館","福島","新潟","中山","東京","中京","京都","阪神","小倉"]
        td_list = ["芝","ダート"]
        if place_dict["place"] == "all" and place_dict["turf_dirt"] == "all":
            self.json_name = "deep_model1.json"
            self.h5_name = "deep_model1.h5"
            return
        if place_dict["place"] == "all":
            p_index = 99
        else:
            p_index = place_list.index(place_dict["place"])
        if place_dict["turf_dirt"] == "all":
            td_index = 9
        else:
            td_index = td_list.index(place_dict["turf_dirt"])
        self.json_name = "deep_model"+str(p_index).zfill(2)+str(td_index)+".json"
        self.h5_name = "deep_model"+str(p_index).zfill(2)+str(td_index)+".h5"

    # twiフォルダの名前が日付になっているフォルダを取得
    def get_csv_dir_list(self):
        all_files = os.listdir(path='..')
        # 名前が日付になっているフォルダを取得
        dir_list = [f for f in all_files if os.path.isdir(os.path.join('..',f)) and f[0].isdigit()]
        dir_list.sort()
        return dir_list

    # 与えられたフォルダリスト内のcsvファイルから馬データ取得
    def get_main_data_from_dir_list(self, dir_list, place_dict_list):
        dir_count = 0
        entry_horses_list = []
        # フォルダ毎、main.csvを取得していく
        for dl in dir_list:
            csv_list = self.ml_util.get_maincsv_list_from_dir("../"+dl)
            self.dotp.today_date = self.ml_util.get_date_from_dirname(dl)
            print(dl)
            for fl in csv_list:
                #print("../"+dl+"/"+fl)
                main_dict = self.pat.get_maindata_dict_from_csv("../"+dl+"/"+fl)
                thinned_out_main_dict = [x for x in main_dict if (place_dict_list["place"] == "all" or x["today_place"] == place_dict_list["place"]) and (place_dict_list["turf_dirt"] == "all" or x["today_turf_dirt"] == place_dict_list["turf_dirt"])]
                if len(thinned_out_main_dict) > 0:
                    entry_horses_list.append(thinned_out_main_dict)
        return entry_horses_list

    # １日分の馬データからdeeplearning_result.csvへの出力する追加情報を取得
    def get_todayinfo_list(self, dir_list, place_dict_list):
        horses_data_list = self.get_main_data_from_dir_list(dir_list, place_dict_list)
        todayinfo_list = []
        extra_list = []
        extra_exist_flg = False
        for hdl in horses_data_list:
            todayinfo_list = todayinfo_list + [[x['horsename'],x['today_race'],x['today_place']] for x in hdl]
            extra_list_add = [[x['today_goal'],x['today_time_diff'],x['today_dividend']] for x in hdl]
            extra_list = extra_list + extra_list_add
            goal_sum_list = [x[0] for x in extra_list_add]
            if sum(goal_sum_list) > 0:
                extra_exist_flg = True
        if not extra_exist_flg: # ファイル内すべてのgoal値が0のとき
            extra_list = []
        return todayinfo_list, extra_list

    # 判定機をjsonから読み出しdeeplearning_result.csv用リストに書き込み
    def get_deep_model(self):
        model = model_from_json(open(self.json_name,"r").read())
        model.load_weights(self.h5_name)
        print(self.json_name)
        return model
    def set_deeplearning_result(self , all_score, todayinfo_lst, extra_lst, place_dict, today_date=""):
        out_analyse_list = []

        for i in range(len(all_score)):
            score = list(all_score[i])
            extra = []
            if extra_lst != []:
                extra = extra_lst[i]
                out_analyse_list.append(todayinfo_lst[i]+score+extra)
            self.result_list.append(todayinfo_lst[i]+score+extra)
        if today_date != "":
            self.analyse_deeplearning_output(out_analyse_list,today_date, place_dict)

    # 性能判定を行い、出力
    def analyse_deeplearning_output(self, out_list, today_date, place_dict):
        if len(out_list) < 10:
            return
        places = list(set([x[2] for x in out_list]))
        # １着度高い順に並べ替え
        out_list = sorted(out_list, reverse=True, key=lambda x: x[3])
        self.research_result_list.append([today_date,place_dict["place"],place_dict["turf_dirt"]]+self.get_analyse_result(places,out_list,"1着度","over",3,False))
        self.research_result_list.append([today_date,place_dict["place"],place_dict["turf_dirt"]]+self.get_analyse_result(places,out_list,"1着度","over",3,True))

    # deeplearning_result.csvへの出力結果を性能評価し、結果出力
    def get_analyse_result_title(self):
        return ["date","場所","芝ダ","title","午前午後","総数","1着","2着","3着","連対率","複勝率","5位以内との連対回数","2〜5位総数","10位以内との連対回数","6〜10位総数","11位以下との連対回数","11位以下総数","total配当(馬連)","平均配当(馬連)","1〜3位ボックス馬連的中回数","1〜3位ボックスワイド的中回数","1〜3位ボックスtotal配当(馬連)","under_three_count","over_four_count","three_total","four_total","three_dividend","four_dividend"]
    def get_analyse_result(self, places, out_list, elem_name, direction, target, afternoon_flg):
        count_dict = {"total":0,"1st":0,"2nd":0,"3rd":0,"with_5th":0,"5th_count":0,"with_10th":0,"10th_count":0,"with_11th":0,"11th_count":0,"box_quinella_count":0,"box_triple_count":0,"three_qui":0,"four_qui":0,"three_total":0,"four_total":0,"three_dividend":0,"four_dividend":0}
        # goal index in deeplearning_result.csv
        goal_index = 5
        dividend_index = 7
        horsename_index = 0
        total_dividend = 0
        box_total_dividend = 0
        # 午前中のレースは4つ
        target_race_total = 4
        noon_comment = "午前"
        if afternoon_flg:
            target_race_total = 8
            noon_comment = "午後"

        for p in places:
            for count in range(target_race_total): # レース数
                i = count
                if afternoon_flg:
                    i = count + 4
                horsename_tmplist = []
                single_analyse_list = []
                # 並べ替えてある順に1レース分の馬名をhorsename_tmplistに入れていく
                for ol in out_list:
                    if ol[1] == (i+1) and ol[2] == p:
                        if not ol[0] in horsename_tmplist:
                            single_analyse_list.append(ol)
                            horsename_tmplist.append(ol[0])
                top_horse = self.get_favorite_horse_data(out_list)
                # 着順データが入っていない場合(レース当日使用の場合)、research_result.csvは作らない
                # when top horse's goal == 0, skip
                if single_analyse_list == [] or len(single_analyse_list[0]) < 8 or single_analyse_list[0][goal_index] == 0:
                    continue
                # 1位から1頭ずつ見ていく
                box_list = [0, 0, 0]
                for j in range(len(single_analyse_list)):
                    # 1位に対する処理
                    if j == 0:
                        print(single_analyse_list[j])
                        count_dict["total"] = count_dict["total"] + 1
                        if single_analyse_list[j][goal_index] == 1:
                            count_dict["1st"] = count_dict["1st"] + 1
                            total_dividend = total_dividend + single_analyse_list[j][dividend_index]
                        elif single_analyse_list[j][goal_index] == 2:
                            count_dict["2nd"] = count_dict["2nd"] + 1
                            total_dividend = total_dividend + single_analyse_list[j][dividend_index]
                        elif single_analyse_list[j][goal_index] == 3:
                            count_dict["3rd"] = count_dict["3rd"] + 1
                    elif j < 5:
                        count_dict["5th_count"] = count_dict["5th_count"] + 1
                    elif j < 10:
                        count_dict["10th_count"] = count_dict["10th_count"] + 1
                    else:
                        count_dict["11th_count"] = count_dict["11th_count"] + 1
                    # 1位が連対した場合にカウント
                    if j >= 1 and (single_analyse_list[0][goal_index] == 1 or single_analyse_list[0][goal_index] == 2) and (single_analyse_list[j][goal_index] == 1 or single_analyse_list[j][goal_index] == 2):
                        if j < 5:
                            count_dict["with_5th"] = count_dict["with_5th"] + 1
                        elif j < 10:
                            count_dict["with_10th"] = count_dict["with_10th"] + 1
                        else:
                            count_dict["with_11th"] = count_dict["with_11th"] + 1
                    # top horse quinella
                    if single_analyse_list[j][horsename_index] == top_horse[horsename_index]:
                        if top_horse[1] <= 3:
                            count_dict["three_total"] = count_dict["three_total"] + 1
                        elif top_horse[1] >= 4:
                            count_dict["four_total"] = count_dict["four_total"] + 1
                        if single_analyse_list[j][goal_index] == 1 or single_analyse_list[j][goal_index] == 2:
                            if top_horse[1] <= 3:
                                count_dict["three_qui"] = count_dict["three_qui"] + 1
                                count_dict["three_dividend"] = count_dict["three_dividend"] + single_analyse_list[j][dividend_index]
                            elif top_horse[1] >= 4:
                                count_dict["four_qui"] = count_dict["four_qui"] + 1
                                count_dict["four_dividend"] = count_dict["four_dividend"] + single_analyse_list[j][dividend_index]
                    # 上位3頭ボックス
                    if j < 3:
                        box_list[j] = single_analyse_list[j][goal_index]
                # 上位3頭ボックス処理
                box_quinella = 0
                box_triple = 0
                for bl in box_list:
                    if bl >= 1 and bl <= 3:
                        box_triple = box_triple + 1
                        if bl <= 2:
                            box_quinella = box_quinella + 1
                if box_triple >= 2:
                    count_dict["box_triple_count"] = count_dict["box_triple_count"] + 1
                if box_quinella >= 2:
                    count_dict["box_quinella_count"] = count_dict["box_quinella_count"] + 1
                    box_total_dividend = box_total_dividend + single_analyse_list[0][dividend_index]
        average_dividend = 0
        if count_dict["total"] > 0:
            average_dividend = round(total_dividend/count_dict["total"],0)
        print(average_dividend)
        return [elem_name, noon_comment, count_dict["total"], count_dict["1st"], count_dict["2nd"], count_dict["3rd"], self.util.get_quinella_rate(count_dict), self.util.get_double_win_rate(count_dict), count_dict["with_5th"], count_dict["5th_count"], count_dict["with_10th"], count_dict["10th_count"], count_dict["with_11th"], count_dict["11th_count"],total_dividend,average_dividend,count_dict["box_quinella_count"],count_dict["box_triple_count"],box_total_dividend,count_dict["three_qui"],count_dict["four_qui"],count_dict["three_total"],count_dict["four_total"],count_dict["three_dividend"],count_dict["four_dividend"]]

    # get list [horsename, count(x/5), race, place, win_rate]
    def get_favorite_horse_title(self):
        return ["horsename","fav_count","race","place","win_rate"]
    def get_favorite_horse_data(self, top_list):
        retlist = []
        top_horse_data = []
        from collections import Counter
        all_horse_list = []
        if len(top_list) == 0:
            return []
        if len(top_list) > 5:
            top_list = top_list[0:5]
        for tl in top_list:
            all_horse_list.append(tl[0])
        counter = Counter(all_horse_list)
        for tl in top_list:
            if tl[0] == counter.most_common()[0][0]: # [0][0]:tophorsename [0][1]:tophorsecount
                retlist = [counter.most_common()[0][0],counter.most_common()[0][1],tl[1],tl[2],tl[3]]
                break
        return retlist
    def set_favorite_list(self):
        place_list = list(set([x[2] for x in self.result_list]))
        race_list = list(set([x[1] for x in self.result_list]))
        winrate_index = 3
        fav_horsename_index = 0
        fav_count_index = 1
        fav_winrate_index = 3
        for place in place_list:
            for race in race_list:
                single_list = []
                for arrl in self.result_list:
                    if arrl[1] == race and arrl[2] == place:
                        single_list.append(arrl)
                sorted_list = sorted(single_list, reverse=True, key=lambda x: x[winrate_index])
                favorite = ar.get_favorite_horse_data(sorted_list)
                if len(favorite) > 0 and favorite[fav_count_index] >= 4:
                    # 取捨選択用に全頭の名前とwinrateを与える
                    for single in sorted_list:
                        if single[fav_horsename_index] not in favorite:
                            favorite.append(single[fav_horsename_index])
                            favorite.append(single[fav_winrate_index])
                    self.favorite_list.append(favorite)

    # ディープラーニング本体
    def deep_learning(self, x_train, y_train, dim):
        model = Sequential()
        y_sm = y_train.sum(axis=0)
        pos = y_sm[0]
        neg = y_sm[1]
        output_bias = keras.initializers.Constant(np.log([pos/neg]))
        class_weight = {1: (1/neg)*(pos+neg)/2.0, 0: (1/pos)*(pos+neg)/2.0}
        print(class_weight)

        model.add(Dense(dim, activation='relu', input_dim=dim))
        model.add(Dropout(0.3))
        model.add(BatchNormalization())
        model.add(Dense(dim*80, activation='relu'))
        model.add(Dropout(0.3))
        model.add(BatchNormalization())
        model.add(Dense(dim*80, activation='relu'))
        model.add(Dropout(0.3))
        model.add(BatchNormalization())

        model.add(Dense(self.dotp.get_number_of_output_kind(), activation='softmax', bias_initializer=output_bias))
        # うまく行かないとき用
        # model.add(Dense(self.dotp.get_number_of_output_kind(), activation='softmax'))

        adamax = Adamax()
        model.summary()
        model.compile(loss='categorical_crossentropy', optimizer=adamax, metrics=['accuracy'])

        history = model.fit(x_train, y_train, epochs=15, batch_size=2000, validation_split=0.1, class_weight=class_weight)
        #self.util.compare_TV(history)

        # モデル、学習済の重みを保存
        open(self.json_name,"w").write(model.to_json())
        model.save_weights(self.h5_name)

# ======class AnalyseResult terminated======

def process_as_product(ar, place_dict_list):
    for pdl in place_dict_list:
        ar.set_deep_model_name(pdl)
        dir_list = ar.get_csv_dir_list()

        race_data = ar.get_main_data_from_dir_list(dir_list,pdl)
        dl_input, dl_output_dict = ar.dotp.make_deeplearning_data(race_data,"machine_learning/deep_pattern.json")
        # 着順分類リスト作成
        goal_list = []
        for i in range(len(dl_input)):
            goal_list.append(ar.dotp.convert_fullgate_goal_list(dl_output_dict[i]["goalorder"],dl_output_dict[i]["timediff"],dl_output_dict[i]["dividend"]))

        dim = len(dl_input[0])
        x_np = np.array(dl_input)
        y_np = np.array(goal_list)
        ar.deep_learning(x_np, y_np, dim)

        # 精度確認用にconfusion_matrixをプロット
        model = ar.get_deep_model()
        ar.util.plot_confusion_matrix(y_np, model.predict(x_np), 0.8)

def process_as_research(ar, place_dict_list):
    for pdl in place_dict_list:
        ar.set_deep_model_name(pdl)
        model = ar.get_deep_model()
        #for tl in ["201107"]:
        for tl in ["140615","141109","150315","150412","150620","160410","161112","171111","180414","181110","190407","191116","200419"]:
            goal_list = []
            todayinfo_lst, extra_lst = ar.get_todayinfo_list([tl],pdl)
            # 当日データのときuse_blank_flg = Trueとしたい
            use_blank_flg = False if extra_lst != [] else True
            target, dummy1 = ar.dotp.make_deeplearning_data(ar.get_main_data_from_dir_list([tl],pdl),"machine_learning/deep_pattern.json", use_blank_flg)
            pred_x_np = np.array(target)
            if len(target) == 0:
                continue
            ar.set_deeplearning_result(model.predict(pred_x_np), todayinfo_lst, extra_lst, pdl, tl)
    with open("../deeplearning_research_result.csv","w") as f:
        writer = csv.writer(f)
        writer.writerow(ar.get_analyse_result_title())
        writer.writerows(ar.research_result_list)
    with open("../deeplearning_result.csv","w") as f:
        writer = csv.writer(f)
        writer.writerow(ar.dotp.get_output_list_title())
        writer.writerows(ar.result_list)
    with open("../deeplearning_favorite_horses.csv","w") as f:
        writer = csv.writer(f)
        writer.writerow(ar.get_favorite_horse_title())
        ar.set_favorite_list()
        writer.writerows(ar.favorite_list)

ar = AnalyseResult()
place_dict_list = ar.util.make_usedlset_dictlist(place_list, all_place_flg, all_td_flg)
if research_flg:
    # performance evaluation
    process_as_research(ar,place_dict_list)
else:
    # honban
    process_as_product(ar,place_dict_list)
