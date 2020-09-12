# coding: utf-8
import sql_manipulator
import csv
import os
from datetime import datetime as dt

class Utility():
    def __init__(self):
        self.dummy = 0
        self.sql = sql_manipulator.SQLManipulator()

    # ディレクトリ名"yymmdd"から日付を取得
    def get_date_from_dirname(self, dirname):
        yyyymmdd = "20"+dirname[0:2]+"-"+dirname[2:4]+"-"+dirname[4:6]
        return dt.strptime(yyyymmdd,'%Y-%m-%d')
    def get_maincsv_list_from_dir(self, dirname):
        pathname = dirname
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
        if cond[0] == "重" or cond[0] == "不":
            return 1
        #if cond[0] == "稍":
        #    return 2
        #if cond[0] == "良":
        #    return 3
        #return 0
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
    def get_slow_pace_all_data(self):
        ret_list = []
        sp = self.sql.sql_manipulator("select * from slow_pace_table;")
        for s in sp:
            ret_list.append({"place":s[0],"class":s[1],"turf_dirt":s[2],"distance":s[3],"course_condition":s[4],"rap3f":s[5],"rap5f":s[6]})
        return ret_list
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
    def convert_nondigit_to_strzero(self, target):
        if not target.isdecimal():
            try:
                float(target)
                return target
            except ValueError:
                return "0"
        else:
            return target

