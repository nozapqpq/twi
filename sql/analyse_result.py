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
class AnalyseResult():
    def __init__(self):
        self.pat = sql_pattern.SQLPattern()
        self.dotp = machine_learning.deep_one_two_pred.DeepOneTwoPred()
        self.ml_util = machine_learning.deep_utility.Utility()
        self.util = utility.Utility()
        self.json_name = "deep_model.json"
        self.h5_name = "deep_model.h5"

    # twiフォルダの名前が日付になっているフォルダを取得
    def get_csv_dir_list(self):
        all_files = os.listdir(path='..')
        # 名前が日付になっているフォルダを取得
        dir_list = [f for f in all_files if os.path.isdir(os.path.join('..',f)) and f[0].isdigit()]
        dir_list.sort()
        return dir_list

    # 与えられたフォルダリスト内のcsvファイルから馬データ取得
    def get_main_data_from_dir_list(self, dir_list):
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
                entry_horses_list.append(main_dict)
        return entry_horses_list

    # １日分の馬データからdeeplearning_result.csvへの出力する追加情報を取得
    def get_todayinfo_list(self, dir_list):
        horses_data_list = self.get_main_data_from_dir_list(dir_list)
        todayinfo_list = []
        extra_list = []
        extra_exist_flg = False
        for hdl in horses_data_list:
            todayinfo_list = todayinfo_list + [[x['horsename'],x['today_race'],x['today_place']] for x in hdl]
            extra_list_add = [[x['today_goal'],x['today_time_diff'],x['today_triple_dividend']] for x in hdl]
            extra_list = extra_list + extra_list_add
            goal_sum_list = [x[0] for x in extra_list_add]
            if sum(goal_sum_list) > 0:
                extra_exist_flg = True
        if not extra_exist_flg: # ファイル内すべてのgoal値が0のとき
            extra_list = []
        return todayinfo_list, extra_list

    # 判定機をjsonから読み出しdeeplearning_result.csvを出力、性能判定も行う
    def output_deeplearning_result_to_csv(self , pred_x_np, todayinfo_lst, dim, extra_lst):
        model = model_from_json(open(self.json_name,"r").read())
        model.load_weights(self.h5_name)
        out_analyse_list = []

        with open("../deeplearning_result.csv","w") as f:
            writer = csv.writer(f)
            writer.writerow(self.dotp.get_output_list_title())
            for i in range(len(pred_x_np)):
                score = list(model.predict(pred_x_np[i].reshape(1,dim))[0])
                extra = []
                if extra_lst != []:
                    extra = extra_lst[i]
                    out_analyse_list.append(todayinfo_lst[i]+score+extra)
                writer.writerow(todayinfo_lst[i]+score+extra)
        self.analyse_deeplearning_output(out_analyse_list)

    # 性能判定を行い、出力
    def analyse_deeplearning_output(self, out_list):
        if len(out_list) < 10:
            return
        places = list(set([x[2] for x in out_list]))
        # １着度高い順に並べ替え
        out_list = sorted(out_list, reverse=True, key=lambda x: x[4])
        self.output_analyse_result(places,out_list,"1着度","over",4)
        # 着外度低い順に並べ替え
        out_list = sorted(out_list, reverse=False, key=lambda x: x[6])
        self.output_analyse_result(places,out_list,"着内度","under",6)

    # deeplearning_result.csvへの出力結果を性能評価し、結果出力
    def output_analyse_result(self, places, out_list, elem_name, direction, target):
        order_analyse_strongest = [0,0,0,0,0,0]
        order_analyse_till_3rd = [0,0,0,0,0,0]
        order_analyse_till_5th = [0,0,0,0,0,0]
        order_analyse_bottom = [0,0,0,0,0,0]
        order_analyse_20per = [0,0,0,0,0,0]
        order_analyse_30per = [0,0,0,0,0,0]
        order_analyse_40per = [0,0,0,0,0,0]
        for p in places:
            for i in range(12):
                horsename_tmplist = []
                single_analyse_list = []
                for ol in out_list:
                    if ol[1] == (i+1) and ol[2] == p and not ol[0] in horsename_tmplist:
                        single_analyse_list.append(ol)
                        horsename_tmplist.append(ol[0])
                for j in range(len(single_analyse_list)):
                    if single_analyse_list[j][7] >= 1 and single_analyse_list[j][7] <= 5: # 5着以内のデータのリストへの追加
                        if j == 0:
                            order_analyse_strongest[single_analyse_list[j][7]-1] = order_analyse_strongest[single_analyse_list[j][7]-1] + 1
                        if j < 3:
                            order_analyse_till_3rd[single_analyse_list[j][7]-1] = order_analyse_till_3rd[single_analyse_list[j][7]-1] + 1
                        if j < 5:
                            order_analyse_till_5th[single_analyse_list[j][7]-1] = order_analyse_till_5th[single_analyse_list[j][7]-1] + 1
                        if j == len(single_analyse_list)-1:
                            order_analyse_bottom[single_analyse_list[j][7]-1] = order_analyse_bottom[single_analyse_list[j][7]-1] + 1
                        if single_analyse_list[j][target] <= 0.2 and direction == "under" or single_analyse_list[j][target] >= 0.2 and direction == "over":
                            order_analyse_20per[single_analyse_list[j][7]-1] = order_analyse_20per[single_analyse_list[j][7]-1] + 1
                        if single_analyse_list[j][target] <= 0.3 and direction == "under" or single_analyse_list[j][target] >= 0.3 and direction == "over":
                            order_analyse_30per[single_analyse_list[j][7]-1] = order_analyse_30per[single_analyse_list[j][7]-1] + 1
                        if single_analyse_list[j][target] <= 0.4 and direction == "under" or single_analyse_list[j][target] >= 0.4 and direction == "over":
                            order_analyse_40per[single_analyse_list[j][7]-1] = order_analyse_40per[single_analyse_list[j][7]-1] + 1

                    elif single_analyse_list[j][7] >= 6: # 6着以内のデータのリストへの追加
                        if j == 0:
                            order_analyse_strongest[5] = order_analyse_strongest[5] + 1
                        if j < 3:
                            order_analyse_till_3rd[5] = order_analyse_till_3rd[5] + 1
                        if j < 5:
                            order_analyse_till_5th[5] = order_analyse_till_5th[5] + 1
                        if j == len(single_analyse_list)-1:
                            order_analyse_bottom[5] = order_analyse_bottom[5] + 1
                        if single_analyse_list[j][target] <= 0.2 and direction == "under" or single_analyse_list[j][target] >= 0.2 and direction == "over":
                            order_analyse_20per[5] = order_analyse_20per[5] + 1
                        if single_analyse_list[j][target] <= 0.3 and direction == "under" or single_analyse_list[j][target] >= 0.3 and direction == "over":
                            order_analyse_30per[5] = order_analyse_30per[5] + 1
                        if single_analyse_list[j][target] <= 0.4 and direction == "under" or single_analyse_list[j][target] >= 0.4 and direction == "over":
                            order_analyse_40per[5] = order_analyse_40per[5] + 1
        print(elem_name+"が1位の馬：    "+str(order_analyse_strongest).ljust(30,' ')+self.util.show_win_rate(order_analyse_strongest))
        print(elem_name+"が3位以内の馬："+str(order_analyse_till_3rd).ljust(30,' ')+self.util.show_win_rate(order_analyse_till_3rd))
        print(elem_name+"が5位以内の馬："+str(order_analyse_till_5th).ljust(30,' ')+self.util.show_win_rate(order_analyse_till_5th))
        print(elem_name+"が最下位の馬： "+str(order_analyse_bottom).ljust(30,' ')+self.util.show_win_rate(order_analyse_bottom))
        print(elem_name+"が20%"+direction+"の馬："+str(order_analyse_20per))
        print(elem_name+"が30%"+direction+"の馬："+str(order_analyse_30per))
        print(elem_name+"が40%"+direction+"の馬："+str(order_analyse_40per))

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
        model.add(Dropout(0.8))
        model.add(BatchNormalization())
        model.add(Dense(dim*80, activation='relu'))
        model.add(Dropout(0.5))
        model.add(BatchNormalization())

        model.add(Dense(self.dotp.get_number_of_output_kind(), activation='softmax'))

        adamax = Adamax()
        model.summary()
        model.compile(loss='categorical_crossentropy', optimizer=adamax, metrics=['accuracy'])

        history = model.fit(x_train, y_train, epochs=30, batch_size=2000, validation_split=0.1)
        self.compare_TV(history)
        #loss, accuracy = model.evaluate(x_train[29000:],y_train[29000:],verbose=0)
        #print("Accuracy = {:.2f}".format(accuracy))

        # モデル、学習済の重みを保存
        open(self.json_name,"w").write(model.to_json())
        model.save_weights(self.h5_name)
goal_list = []
ar = AnalyseResult()
dir_list = ar.get_csv_dir_list()
todayinfo_lst, extra_lst = ar.get_todayinfo_list([str(dir_list[-1])])
dummy1, dummy2, dummy3, target = ar.dotp.make_deeplearning_data(ar.get_main_data_from_dir_list([str(dir_list[-1])]),"machine_learning/deep_pattern.json")
pred_x_np = np.array(target)
dim = len(pred_x_np[0])

#'''
# 学習済で結果出力だけのときはこの塊をコメントアウト
lst = ar.get_main_data_from_dir_list(dir_list)
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
#'''

# 結果出力
ar.output_deeplearning_result_to_csv(pred_x_np, todayinfo_lst, dim, extra_lst)
