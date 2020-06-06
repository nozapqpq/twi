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
    def convert_nondigit_to_strzero(self, target):
        if not target.isdecimal():
            try:
                float(target)
                return target
            except ValueError:
                return "0"
        else:
            return target

