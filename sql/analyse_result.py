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

# place_listに入っている場所に対するディープラーニングを利用できる
# ディープラーニングの性能を図りたいときはresearch_flg = True
place_list = ["東京","京都","新潟"]
research_flg = True
all_place_flg = True
all_td_flg = True

class AnalyseResult():
    def __init__(self):
        self.pat = sql_pattern.SQLPattern()
        self.dotp = machine_learning.deep_one_two_pred.DeepOneTwoPred()
        self.ml_util = machine_learning.deep_utility.Utility()
        self.util = utility.Utility()
        self.json_name = "deep_model.json"
        self.h5_name = "deep_model.h5"

    def set_deep_model_name(self, place_dict):
        place_list = ["札幌","函館","福島","新潟","中山","東京","中京","京都","阪神","小倉"]
        td_list = ["芝","ダート"]
        if place_dict["place"] == "all" and place_dict["turf_dirt"] == "all":
            self.json_name = "deep_model14.json"
            self.h5_name = "deep_model14.h5"
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

    # 判定機をjsonから読み出しdeeplearning_result.csvを出力、性能判定も行う
    def get_deep_model(self):
        model = model_from_json(open(self.json_name,"r").read())
        model.load_weights(self.h5_name)
        print(self.json_name)
        return model
    def output_deeplearning_result_to_csv(self , model, pred_x_np, todayinfo_lst, dim, extra_lst, place_dict, today_date=""):
        out_analyse_list = []

        with open("../deeplearning_result.csv","a") as f:
            writer = csv.writer(f)
            all_score = model.predict(pred_x_np)
            for i in range(len(pred_x_np)):
                score = list(all_score[i])
                #score = list(model.predict(pred_x_np[i].reshape(1,dim))[0])
                extra = []
                if extra_lst != []:
                    extra = extra_lst[i]
                    out_analyse_list.append(todayinfo_lst[i]+score+extra)
                writer.writerow(todayinfo_lst[i]+score+extra)
        if today_date != "":
            self.analyse_deeplearning_output(out_analyse_list,today_date, place_dict)

    # 性能判定を行い、出力
    def analyse_deeplearning_output(self, out_list, today_date, place_dict):
        if len(out_list) < 10:
            return
        places = list(set([x[2] for x in out_list]))
        with open("../deeplearning_research_result.csv","a") as f:
            # １着度高い順に並べ替え
            out_list = sorted(out_list, reverse=True, key=lambda x: x[3])
            writer = csv.writer(f)
            writer.writerow([today_date,place_dict["place"],place_dict["turf_dirt"]]+self.get_analyse_result(places,out_list,"1着度","over",3,False))
            writer.writerow([today_date,place_dict["place"],place_dict["turf_dirt"]]+self.get_analyse_result(places,out_list,"1着度","over",3,True))

    # deeplearning_result.csvへの出力結果を性能評価し、結果出力
    def get_analyse_result_title(self):
        return ["date","場所","芝ダ","title","午前午後","総数","1着","2着","3着","連対率","複勝率","5位以内との連対回数","2〜5位総数","10位以内との連対回数","6〜10位総数","11位以下との連対回数","11位以下総数","total配当(馬連)","平均配当(馬連)"]
    def get_analyse_result(self, places, out_list, elem_name, direction, target, afternoon_flg):
        count_dict = {"total":0,"1st":0,"2nd":0,"3rd":0,"with_5th":0,"5th_count":0,"with_10th":0,"10th_count":0,"with_11th":0,"11th_count":0}
        total_dividend = 0
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
                    if ol[1] == (i+1) and ol[2] == p and not ol[0] in horsename_tmplist:
                        single_analyse_list.append(ol)
                        horsename_tmplist.append(ol[0])
                # 着順データが入っていない場合(レース当日使用の場合)、research_result.csvは作らない
                # when top horse's goal == 0, skip
                if single_analyse_list == [] or len(single_analyse_list[0]) < 9 or single_analyse_list[0][6] == 0:
                    continue
                # 1位から1頭ずつ見ていく
                single_one_two_count = 0
                for j in range(len(single_analyse_list)):
                    # 1位に対する処理
                    if j == 0:
                        print(single_analyse_list[j])
                        count_dict["total"] = count_dict["total"] + 1
                        if single_analyse_list[j][6] == 1:
                            count_dict["1st"] = count_dict["1st"] + 1
                            total_dividend = total_dividend + single_analyse_list[j][8]
                        elif single_analyse_list[j][6] == 2:
                            count_dict["2nd"] = count_dict["2nd"] + 1
                            total_dividend = total_dividend + single_analyse_list[j][8]
                        elif single_analyse_list[j][6] == 3:
                            count_dict["3rd"] = count_dict["3rd"] + 1
                    elif j < 5:
                        count_dict["5th_count"] = count_dict["5th_count"] + 1
                    elif j < 10:
                        count_dict["10th_count"] = count_dict["10th_count"] + 1
                    else:
                        count_dict["11th_count"] = count_dict["11th_count"] + 1
                    # 1位が連対した場合にカウント
                    if j >= 1 and (single_analyse_list[0][6] == 1 or single_analyse_list[0][6] == 2) and (single_analyse_list[j][6] == 1 or single_analyse_list[j][6] == 2):
                        if j < 5:
                            count_dict["with_5th"] = count_dict["with_5th"] + 1
                        elif j < 10:
                            count_dict["with_10th"] = count_dict["with_10th"] + 1
                        else:
                            count_dict["with_11th"] = count_dict["with_11th"] + 1
        average_dividend = 0
        if count_dict["total"] > 0:
            average_dividend = round(total_dividend/count_dict["total"],0)
        print(average_dividend)
        print(count_dict)
        return [elem_name, noon_comment, count_dict["total"], count_dict["1st"], count_dict["2nd"], count_dict["3rd"], self.util.get_quinella_rate(count_dict), self.util.get_double_win_rate(count_dict), count_dict["with_5th"], count_dict["5th_count"], count_dict["with_10th"], count_dict["10th_count"], count_dict["with_11th"], count_dict["11th_count"],total_dividend,average_dividend]

    # matplotでaccuracyとlossをプロットして出力
    def compare_TV(self, history):
        import matplotlib.pyplot as plt

        # Setting Parameters
        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']
        loss = history.history['loss']
        val_loss = history.history['val_loss']

        epochs = range(len(acc))

        # 1) Accracy Plt
        plt.plot(epochs, acc, 'bo' ,label = 'training acc')
        plt.plot(epochs, val_acc, 'b' , label= 'validation acc')
        plt.title('Training and Validation acc')
        plt.legend()

        plt.figure()

        # 2) Loss Plt
        plt.plot(epochs, loss, 'bo' ,label = 'training loss')
        plt.plot(epochs, val_loss, 'b' , label= 'validation loss')
        plt.title('Training and Validation loss')
        plt.legend()

        plt.show()

    # ディープラーニング本体
    def deep_learning(self, x_train, y_train, dim, horsename_list, pred_x_np, todayinfo_lst):
        model = Sequential()
        model.add(Dense(dim, activation='relu', input_dim=dim))
        model.add(Dropout(0.3))
        model.add(BatchNormalization())
        model.add(Dense(dim*40, activation='relu'))
        model.add(Dropout(0.3))
        model.add(BatchNormalization())
        model.add(Dense(dim*40, activation='relu'))
        model.add(Dropout(0.3))
        model.add(BatchNormalization())

        model.add(Dense(self.dotp.get_number_of_output_kind(), activation='softmax'))

        adamax = Adamax()
        model.summary()
        model.compile(loss='categorical_crossentropy', optimizer=adamax, metrics=['accuracy'])

        history = model.fit(x_train, y_train, epochs=15, batch_size=2000, validation_split=0.1)
        #self.compare_TV(history)
        #loss, accuracy = model.evaluate(x_train[29000:],y_train[29000:],verbose=0)
        #print("Accuracy = {:.2f}".format(accuracy))

        # モデル、学習済の重みを保存
        open(self.json_name,"w").write(model.to_json())
        model.save_weights(self.h5_name)

# ======class AnalyseResult terminated======

def process_as_product(ar, place_dict_list):
    with open("../deeplearning_result.csv","w") as f:
        writer = csv.writer(f)
        writer.writerow(ar.dotp.get_output_list_title())
    for pdl in place_dict_list:
        ar.set_deep_model_name(pdl)
        goal_list = []
        dir_list = ar.get_csv_dir_list()
        todayinfo_lst, extra_lst = ar.get_todayinfo_list([str(dir_list[-1])],pdl)
        dummy1, dummy2, dummy3, target = ar.dotp.make_deeplearning_data(ar.get_main_data_from_dir_list([str(dir_list[-1])],pdl),"machine_learning/deep_pattern.json")
        pred_x_np = np.array(target)
        dim = len(pred_x_np[0])

        lst = ar.get_main_data_from_dir_list(dir_list,pdl)
        learn_lst, ans_lst, hn_lst, dummy_target = ar.dotp.make_deeplearning_data(lst,"machine_learning/deep_pattern.json")
        # 着順分類リスト作成
        for i in range(len(learn_lst)):
            gl = ar.dotp.convert_fullgate_goal_list(ans_lst[i][0],ans_lst[i][1],ans_lst[i][2])
            goal_list.append(gl)
        # 各リストのnumpy化
        x_np = np.array(learn_lst)
        y_np = np.array(goal_list)
        # ディープラーニング
        ar.deep_learning(x_np, y_np, dim, hn_lst, pred_x_np, todayinfo_lst)

        # 結果出力
        model = ar.get_deep_model()
        ar.output_deeplearning_result_to_csv(model, pred_x_np, todayinfo_lst, dim, extra_lst, pdl)

def process_as_research(ar, place_dict_list):
    with open("../deeplearning_research_result.csv","w") as f:
        writer = csv.writer(f)
        writer.writerow(ar.get_analyse_result_title())
    with open("../deeplearning_result.csv","w") as f:
        writer = csv.writer(f)
        writer.writerow(ar.dotp.get_output_list_title())
    for pdl in place_dict_list:
        ar.set_deep_model_name(pdl)
        model = ar.get_deep_model()
        for tl in ["171014","171029","181014","181020","181027","191026","201010","201011","201017","201018"]:
            goal_list = []
            todayinfo_lst, extra_lst = ar.get_todayinfo_list([tl],pdl)
            dummy1, dummy2, dummy3, target = ar.dotp.make_deeplearning_data(ar.get_main_data_from_dir_list([tl],pdl),"machine_learning/deep_pattern.json")
            pred_x_np = np.array(target)
            if len(target) == 0:
                continue
            dim = len(pred_x_np[0])
            ar.output_deeplearning_result_to_csv(model, pred_x_np, todayinfo_lst, dim, extra_lst, pdl, tl)

def make_usedlset_dictlist(place_list, all_place_flg, all_td_flg):
    dict_list = []
    if all_place_flg:
        place_list = ["all"]
    for pl in place_list:
        if all_td_flg:
            dict_list.append({"place":pl,"turf_dirt":"all"})
        else:
            dict_list.append({"place":pl,"turf_dirt":"芝"})
            dict_list.append({"place":pl,"turf_dirt":"ダート"})
    return dict_list

ar = AnalyseResult()
place_dict_list = make_usedlset_dictlist(place_list, all_place_flg, all_td_flg)
if research_flg:
    # performance evaluation
    process_as_research(ar,place_dict_list)
else:
    # honban
    process_as_product(ar,place_dict_list)
