# coding: utf-8
import os
import sys
import re
import statistics
import math
import csv
from .sql_manipulator import SQLManipulator
from .utility import Utility
from .horse_race import HorseRace

class Jockey():
    def __init__(self):
        self.sql = SQLManipulator()
        self.utility = Utility()
        self.jockey_dict_list = self.get_jockey_dict_list_from_db()
        # テーブル作成用データ
        print(os.getcwd())
        self.jockey_list = self.utility.get_list_from_json("db/jockey.json","jockey_list")
        self.database = []
        self.small_turn_list = ["札幌","函館","福島","中山","小倉"]
        self.race_position_forward_list = [False,True] # 先行か
        self.small_turn_list = [False,True] # スパイラルカーブか
        self.turf_dirt_list = ["ダート","芝"]
        # テーブル作成用データ ここまで

    def get_jockey_dict_list(self):
        return self.jockey_dict_list

    def get_jockey_dict_list_from_db(self, condition=""):
        where_cond_msg = ""
        if condition != "":
            where_cond_msg = "course_condition='"+condition+"'"
        else:
            where_cond_msg = "1=1"
        select_msg = "select * "
        from_msg = "from jockey_table "
        msg = select_msg+from_msg+"where "+where_cond_msg+";"
        tpl = self.sql.sql_manipulator(msg)
        retlist = []
        for t in tpl:
            single_dict = {"name":t[0],"belongs":t[1],"birth":t[2],"sturn_turf_front":t[3],"sturn_turf_stay":t[4],"sturn_dirt_front":t[5],"sturn_dirt_stay":t[6],"normal_turf_front":t[7],"normal_turf_stay":t[8],"normal_dirt_front":t[9],"normal_dirt_stay":t[10]}
            retlist.append(single_dict)
        return retlist

    def add_jockey_db(self):
        hr = HorseRace()
        self.database = hr.get_horse_race_dict_list_from_db(" odds<=15.0 and race_table.rdate between '2017-01-01' and '2020-10-15'")
        for jk in self.jockey_list:
            single_scores = []
            for sturn in self.small_turn_list:
                for td in self.turf_dirt_list:
                    for dist in self.race_position_forward_list:
                        app = self.get_approach_rate(jk["name"],td,dist,sturn)
                        single_scores.append(app)
            self.sql.sql_manipulator("insert into jockey_table values ('"+jk["name"]+"','"+jk["belongs"]+"','"+jk["date_of_birth"]+"',"+str(single_scores[0])+","+str(single_scores[1])+","+str(single_scores[2])+","+str(single_scores[3])+","+str(single_scores[4])+","+str(single_scores[5])+","+str(single_scores[6])+","+str(single_scores[7])+");")

    # スパイラルループ、オッズ15倍以内での差し,先行での好走率(着差0.3s以内)をテーブルに記載
    def get_approach_rate(self, jockey_name, td, position_stay_flg, small_turn):
        match_all_list = [x for x in self.database if x['jockey_name']==jockey_name and x['turf_dirt']==td]
        if small_turn:
            match_all_list = [x for x in match_all_list if "[G002]" in x['course_mark']]
        if position_stay_flg:
            match_all_list = [x for x in match_all_list if x['diff3f']>=1.0]
        else:
            match_all_list = [x for x in match_all_list if x['diff3f']<1.0]
        match_good_list = [x for x in match_all_list if x['time_diff']<=0.3]
        if len(match_all_list) > 0:
            return round(len(match_good_list)/len(match_all_list)*100,1)
        else:
            return 0
#jk = Jockey()
#jk.add_jockey_db()
