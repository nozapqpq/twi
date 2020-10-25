# coding: utf-8
import os
import sys
import re
import sql_manipulator
import utility
import statistics
import math

class Jockey():
    def __init__(self):
        self.sql = sql_manipulator.SQLManipulator()
        self.utl = utility.Utility()
        self.small_turn_list = ["札幌","函館","福島","中山","小倉"]
        self.jockey_list = self.utl.get_list_from_json("jockey.json","jockey_list")
        self.race_position_forward_list = [False,True] # 先行か
        self.small_turn_list = [False,True] # スパイラルカーブか
        self.turf_dirt_list = ["ダート","芝"]
        self.database = self.sql.get_horse_race_data(" odds<=15.0 and race_table.rdate between '2017-01-01' and '2020-10-15'")

    def add_jockey_table(self):
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

jk = Jockey()
jk.add_jockey_table()
