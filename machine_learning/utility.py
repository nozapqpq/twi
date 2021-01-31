# coding: utf-8
import csv
import json
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime as dt
from datetime import date
from dateutil.relativedelta import relativedelta
from sklearn.metrics import confusion_matrix

class Utility():
    def __init__(self):
        self.dummy = 0

    # クラスランク0~3を取得
    def get_class_rank(self, cls):
        if cls in ["未勝利","新馬"]:
            return 0
        if cls in ["500万","1勝"]:
            return 1
        if cls in ["1000万","1600万","2勝","3勝"]:
            return 2
        return 3
    # クラスの序列
    def compare_class_priority(self, cls1, cls2):
        priority1 = self.get_class_priority(cls1)
        priority2 = self.get_class_priority(cls2)
        return priority1-priority2
    def get_class_priority(self, cls):
        if cls in ["未勝利","新馬"]:
            return 0
        elif cls in ["500万","1勝"]:
            return 1
        elif cls in ["1000万","2勝"]:
            return 2
        elif cls in ["1600万","3勝"]:
            return 3
        elif cls in ["オープン","OP(L)"]:
            return 4
        elif cls in ["重賞"]:
            return 5
        elif cls in ["Ｇ３"]:
            return 6
        elif cls in ["Ｇ２"]:
            return 7
        elif cls in ["Ｇ１"]:
            return 8
        else:
            return 0
    # 馬場状態インデックスを取得
    def get_condition_index(self, cond):
        if cond[0] == "良" or cond[0] == "稍":
            return 0
        return 1
    # 2レースの馬場状態が同じであればtrueを返す
    def check_same_condition(self, cond1, cond2):
        return cond1[0] == cond2[0]
    # 距離インデックスを取得
    def get_distance_index(self, dist):
        dist_list = [1000,1150,1200,1300,1400,1500,1600,1700,1800,1900,2000,2200,2600]
        if dist <= 1400:
            return 1
        else:
            return 0
        #if dist < 1000:
        #    return 0
        #for i in range(len(dist_list)):
        #    if dist <= dist_list[i]:
        #        return i+1
        #return len(dist_list)+1
    # slow_pace_table固有の仮想クラス表現を取得
    def get_slow_pace_virtual_class(self, actual_cls):
        cls_list1 = ["新馬","未勝利"]
        cls_list2 = ["1勝","500万"]
        virtual_cls = ""
        if actual_cls in cls_list1:
            virtual_cls = actual_cls
        elif actual_cls in cls_list2:
            virtual_cls = "1勝"
        else:
            virtual_cls = "2勝"
        return virtual_cls
    # 特定条件でのスローペースのボーダータイムを取得
    def get_slow_pace_rap(self, place, distance, cls, cond, td):
        virtual_cls = self.get_slow_pace_virtual_class(cls)
        sp = self.sql.sql_manipulator("select * from slow_pace_table where place='"+place+"' and class='"+virtual_cls+"' and turf_dirt='"+td+"' and distance="+str(distance)+" and course_condition='"+cond+"';")
        if len(sp) == 0:
            return {"rap3f":37.0,"rap5f":65.0}
        return {"rap3f":float(sp[0][5]),"rap5f":float(sp[0][6])}
    # スローペーステーブルの全データを取得
    def get_slow_pace_all_data(self):
        ret_list = []
        sp = self.sql.sql_manipulator("select * from slow_pace_table;")
        for s in sp:
            ret_list.append({"place":s[0],"class":s[1],"turf_dirt":s[2],"distance":s[3],"course_condition":s[4],"rap3f":s[5],"rap5f":s[6]})
        return ret_list
    # 騎手テーブルの全データを取得
    def get_jockey_all_data(self):
        ret_list = []
        jk = self.sql.sql_manipulator("select * from jockey_table;")
        for j in jk:
            turf_front = (self.convert_few_data_to_20(j[3])+self.convert_few_data_to_20(j[7]))/2
            turf_stay = (self.convert_few_data_to_20(j[4])+self.convert_few_data_to_20(j[8]))/2
            dirt_front = (self.convert_few_data_to_20(j[5])+self.convert_few_data_to_20(j[9]))/2
            dirt_stay = (self.convert_few_data_to_20(j[6])+self.convert_few_data_to_20(j[10]))/2
            ret_list.append({"name":j[0],"belongs":j[1],"age":self.get_age_from_dateofbirth(dt.strptime(j[2],'%Y-%m-%d')),"turf_front":turf_front,"turf_stay":turf_stay,"dirt_front":dirt_front,"dirt_stay":dirt_stay})
        return ret_list
    # 種牡馬テーブルの全データを取得
    def get_stallion_all_data(self):
        ret_list = []
        st = self.sql.sql_manipulator("select * from stallion_table;")
        for s in st:
            ret_list.append({"name":s[0],"ancestor1":s[1],"ancestor2":s[2],"ancestor3":s[3],"ancestor4":s[4]})
        return ret_list
    # 調教師テーブルの全データを取得
    def get_trainer_all_data(self):
        ret_list = []
        tr = self.sql.sql_manipulator("select * from trainer_table;")
        for t in tr:
            ret_list.append({"name":t[0],"belongs":t[1]})
        return ret_list
    # 気温データをJSONファイルから取得
    def get_temperature_from_json(self, json_fn):
        json_open = open(json_fn,'r')
        temperature_dict = json.load(json_open)["temperature_dict"]
        return temperature_dict
    # 気温データを取得
    def get_temperature(self, temperature_dict, dct):
        month = int(re.findall('\d+-(\d+)-\d+ \d+:\d+:\d',str(dct["today_rdate"]))[0])
        place = dct["today_place"]
        temperature = temperature_dict[place][month-1]
        if dct["today_course_condition"] == "稍":
            temperature = temperature-2
        elif dct["today_course_condition"] == "重" or dct["today_course_condition"] == "不":
            temperature = temperature-5
        return temperature
    # 日付から年齢を取得
    def get_age_from_dateofbirth(self, date):
        delta = relativedelta(dt.now(),date)
        age = delta.years
        return age
    # 洋芝
    def is_european_grass(self, place):
        if place in ["札幌","函館"]:
            return 1
        return 0
    # スパイラルカーブ
    def is_spiral_curve(self, place):
        if place in ["札幌","函館","小倉","福島"]:
            return 1
        return 0
    # メイン開催場
    def is_main_place(self, place):
        if place in ["中山","東京","京都","阪神"]:
            return 1
        return 0
    def is_upper_class(self, cls1, cls2):
        if self.get_class_priority(cls2) > self.get_class_priority(cls1):
            return 1
        else:
            return 0
    # 騎手インデックスを取得
    def get_jockey_index(self, jockey):
        jockey_idx_list = [[""], \
                [""], \
                ["ルメール","モレイラ","川田将雅","Ｍ．デム","戸崎圭太","福永祐一","アヴドゥ","Ｃ．デム","ホワイト","武豊","北村友一","岩田康成","池添謙一","浜中俊","田辺裕信","","",""], \
                [""], \
                [""], \
                [""]]
        for i in range(len(jockey_idx_list)):
            if jockey in jockey_idx_list[i]:
                return i+1
        return 0
    def get_exec_command(self,funcname,arg_list):
        args = ""
        for i in range(len(arg_list)):
            if i != 0:
                args = args + ","
            args = args + arg_list[i]
        return "self."+funcname+"("+args+")"
    def calc_days_after_birth(self,today,birth):
        return (today-birth).days
    def convert_nondigit_to_strzero(self, target):
        if not target.isdecimal():
            try:
                float(target)
                return target
            except ValueError:
                return "0"
        else:
            return target
    # 100%が最大値のデータでdata==100%のとき、データ不足と判断して20%とみなす
    def convert_few_data_to_20(self, data):
        if data == 100:
            data = 20
        if data == 1:
            data = 0.2
        return data
    # str -> datetime -> dateへ変換
    def str_to_date(self, s):
        tmp_dt = dt.strptime(s, '%Y-%m-%d')
        return date(tmp_dt.year, tmp_dt.month, tmp_dt.day)
    # matplotでaccuracyとlossをプロットして出力
    def compare_TV(self, history):
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
    # 正答と予測のconfusion_matrixをプロットして出力
    def plot_confusion_matrix(self, labels, predictions, p):
        matrix_y = np.array([x[0] for x in labels])
        matrix_pred = np.array([x[0] for x in predictions])
        cm = confusion_matrix(matrix_y, matrix_pred > p)
        plt.figure(figsize=(5,5))
        sns.heatmap(cm, annot=True, fmt="d")
        plt.title('Confusion matrix @{:.2f}'.format(p))
        plt.ylabel('Actual label')
        plt.xlabel('Predicted label')
        plt.show()
    # [0,1,0]を[[0,1],[1,0],[0,1]]というように2次元リストに変換
    def divide_to_2dim_list(self, lst):
        retlist = []
        for l in lst:
            single = [0,0]
            if l == 1:
                single[0] = 1
            else:
                single[1] = 1
            retlist.append(single)
        return retlist
