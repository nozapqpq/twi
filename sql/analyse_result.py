# coding: utf-8
import sql_pattern
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
        self.json_name = "deep_model.json"
        self.h5_name = "deep_model.h5"

    def get_csv_dir_list(self):
        all_files = os.listdir(path='..')
        # 名前が日付になっているフォルダを取得
        dir_list = [f for f in all_files if os.path.isdir(os.path.join('..',f)) and f[0].isdigit()]
        dir_list.sort()
        return dir_list

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

    def get_todayinfo_list(self, dir_list):
        horses_data_list = self.get_main_data_from_dir_list(dir_list)
        todayinfo_list = []
        for hdl in horses_data_list:
            todayinfo_list = todayinfo_list + [[x['horsename'],x['today_race'],x['today_place']] for x in hdl]
        return todayinfo_list

# deep learning "methods part"
    def deep_learning(self, x_train, y_train, dim, horsename_list, pred_x_np, todayinfo_lst):
        model = Sequential()
        model.add(Dense(dim, activation='relu', input_dim=dim))
        model.add(Dropout(0.4))
        model.add(BatchNormalization())
        model.add(Dense(dim*10, activation='relu'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(dim*10, activation='relu'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(dim*10, activation='relu'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(dim*10, activation='relu'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(dim*10, activation='relu'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(dim*10, activation='relu'))
        model.add(Dropout(0.1))
        model.add(BatchNormalization())
        model.add(Dense(dim*10, activation='relu'))
        model.add(Dropout(0.1))
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

    def output_deeplearning_result_to_csv(self , pred_x_np, todayinfo_lst, dim):
        model = model_from_json(open(self.json_name,"r").read())
        model.load_weights(self.h5_name)

        with open("../deeplearning_result.csv","w") as f:
            writer = csv.writer(f)
            writer.writerow(self.dotp.get_output_list_title())
            for i in range(len(pred_x_np)):
                score = list(model.predict(pred_x_np[i].reshape(1,dim))[0])
                writer.writerow(todayinfo_lst[i]+score)

    def compare_TV(self, history):
        import matplotlib.pyplot as plt

        # Setting Parameters
        print(history.history)
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
goal_list = []
ar = AnalyseResult()
dir_list = ar.get_csv_dir_list()
todayinfo_lst = ar.get_todayinfo_list([str(dir_list[-1])])
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
ar.output_deeplearning_result_to_csv(pred_x_np, todayinfo_lst, dim)
