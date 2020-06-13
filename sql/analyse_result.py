# coding: utf-8
import sql_pattern
import machine_learning.deep_one_two_pred
import machine_learning.deep_utility
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
        self.dotp = machine_learning.deep_one_two_pred.DeepOneTwoPred()
        self.ml_util = machine_learning.deep_utility.Utility()

    def get_main_data_from_csv(self):
        entry_horses_list = []
        all_files = os.listdir(path='..')
        # 名前が日付になっているフォルダを取得
        dir_list = [f for f in all_files if os.path.isdir(os.path.join('..',f)) and f[0].isdigit()]

        dir_count = 0
        # フォルダ毎、main.csvを取得していく
        for dl in dir_list:
            csv_list = self.ml_util.get_maincsv_list_from_dir("../"+dl)
            self.dotp.today_date = self.ml_util.get_date_from_dirname(dl)
            for fl in csv_list:
                print("../"+dl+"."+fl)
                main_dict = self.pat.get_maindata_dict_from_csv("../"+dl+"/"+fl)
                entry_horses_list.append(main_dict)
        return entry_horses_list

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
        model.add(Dense(4, activation='softmax'))

        adamax = Adamax()
        model.compile(loss='categorical_crossentropy', optimizer=adamax, metrics=['accuracy'])

        history = model.fit(x_train, y_train, epochs=30, batch_size=5000, validation_split=0.1)
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
            writer.writerow(["place","race","horsename","~3rd(~10k)","~3rd(~50k)","~3rd(50k~)","4th~"])
            for i in range(len(pred_x_np)):
                score = list(model.predict(pred_x_np[i].reshape(1,dim))[0])
                writer.writerow(todayinfo_lst[i]+score)

goal_list = []
ar = AnalyseResult()
lst = ar.get_main_data_from_csv()
learn_lst, ans_lst, hn_lst, target, todayinfo_lst = ar.dotp.make_deeplearning_data(lst,"machine_learning/deep_pattern.json")
dim = len(learn_lst[0])
# 着順分類リスト作成
for i in range(len(learn_lst)):
    gl = ar.dotp.convert_fullgate_goal_list(ans_lst[i][0],ans_lst[i][1])
    goal_list.append(gl)
# 各リストのnumpy化
x_np = np.array(learn_lst)
y_np = np.array(goal_list)
pred_x_np = np.array(target)
# ディープラーニング, 読み込むだけのときはコメントアウトする
ar.deep_learning(x_np, y_np, dim, hn_lst, pred_x_np, todayinfo_lst)
ar.output_deeplearning_result_to_csv(pred_x_np, todayinfo_lst)
