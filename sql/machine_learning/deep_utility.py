# coding: utf-8
import sql_manipulator
import csv
import os
from datetime import datetime as dt

class Utility():
    def __init__(self):
        self.dummy = 0

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
        return 2 
    # 馬場状態インデックスを取得
    def get_condition_index(self, cond):
        if cond[0] == "不":
            return 0
        if cond[0] == "重":
            return 1
        if cond[0] == "稍":
            return 2
        if cond[0] == "良":
            return 3
        return 0
    # 距離インデックスを取得
    def get_distance_index(self, dist):
        dist_list = [1000,1150,1200,1300,1400,1500,1600,1700,1800,1900,2000,2200,2600]
        if dist < 1000:
            return 0
        for i in range(len(dist_list)):
            if dist <= dist_list[i]:
                return i+1
        return len(dist_list)+1
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

