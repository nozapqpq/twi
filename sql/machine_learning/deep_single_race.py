# coding: utf-8
import sql_manipulator
import utility
import csv
import os
from datetime import datetime as dt
from . import deep_utility

class DeepSingleRace():
    def __init__(self):
        self.sm = sql_manipulator.SQLManipulator()
        self.util = deep_utility.Utility()
        self.parent_util = utility.Utility()
        self.single_horse_dicts = []
        self.whole_race_dict = {}
        self.trainer = self.util.get_trainer_all_data()
        self.jockey = self.util.get_jockey_all_data()

    def set_main_dicts(self, whole_list):
        self.clean()
        if len(whole_list) > 0:
            self.set_whole_race_dict(whole_list)
            self.set_single_horse_dicts(whole_list)
            self.set_whole_race_dict_extra_with_single_dicts()

    def clean(self):
        self.single_horse_dicts = []
        self.whole_race_dict = {"place":"","race":0,"rdate":"","horse_total":"","top_zi":0,"top_odds":0,"fastest_time":0.0,"pop_tddiff":False,"stag_count":0,"west_count":0,"younghorse_count":0,"youngjockey_count":0,"jockey_list":[],"delta_rap5f":0.0,"delta_last3f":0.0}

    # 1レース分のデータを扱う(栗東率、牡馬率、若手騎手率、2,3歳限定寄りかなど)
    def set_whole_race_dict(self, whole_list):
        self.whole_race_dict["place"] = whole_list[-1]["today_place"]
        self.whole_race_dict["race"] = whole_list[-1]["today_race"]
        self.whole_race_dict["rdate"] = whole_list[-1]["today_rdate"]
        self.whole_race_dict["horse_total"] = whole_list[-1]["today_horse_total"]
        self.whole_race_dict["top_zi"] = max(whole_list, key=lambda x:x['today_zi'])['today_zi']
        self.whole_race_dict["top_odds"] = min(whole_list, key=lambda x:x['today_odds'])['today_odds']
        # delta_rap5f, delta_last3fは500万、1000万クラスの平均との差を保持するものとする
        race_dict = self.parent_util.get_single_race_table_dict(self.whole_race_dict["rdate"].strftime('%Y-%m-%d'), self.whole_race_dict["place"], self.whole_race_dict["race"])
        same_races = self.parent_util.get_race_table("place='"+race_dict["place"]+"' and turf_dirt='"+race_dict["turf_dirt"] +"' and distance="+str(race_dict["distance"])+" and course_condition='"+race_dict["course_condition"]+"' and class in ('500万','1000万','1勝','2勝') and rap5f>0 and last3f>0")
        if race_dict != {} and len(same_races) > 0:
            self.whole_race_dict["delta_rap5f"] = race_dict['rap5f']-sum(d['rap5f'] for d in same_races)/len(same_races)
            self.whole_race_dict["delta_last3f"] = race_dict['last3f']-sum(d['last3f'] for d in same_races)/len(same_races)
        else:
            self.whole_race_dict["delta_rap5f"] = 0.0
            self.whole_race_dict["delta_last3f"] = 0.0

        name_list = []
        west_count = 0
        stag_count = 0
        younghorse_count = 0
        youngjockey_count = 0
        for wl in whole_list:
            trainer = [x for x in self.trainer if x['name'] == wl['trainer']]
            jockey = [x for x in self.jockey if x['name'] == wl['today_jockey_name']]
            if not wl['horsename'] in name_list:
            #if len(single) > 0 and not wl['horsename'] in name_list and wl["today_place"] == self.whole_race_dict["place"] and wl["today_race"] == self.whole_race_dict["race"]:
                if len(trainer) > 0 and trainer[0]['belongs'] == "栗東":
                    west_count = west_count + 1
                if wl["horse_sex"] != "牝":
                    stag_count = stag_count + 1
                if wl["horse_age"] <= 3:
                    younghorse_count = younghorse_count + 1
                if len(jockey) > 0:
                    self.whole_race_dict["jockey_list"].append(jockey[0]['name'])
                    if jockey[0]['age'] <= 25:
                        youngjockey_count = youngjockey_count + 1
                name_list.append(wl['horsename'])
        self.whole_race_dict["west_count"] = west_count
        self.whole_race_dict["stag_count"] = stag_count
        self.whole_race_dict["younghorse_count"] = younghorse_count
        self.whole_race_dict["youngjockey_count"] = youngjockey_count

        matched = [x for x in whole_list if x["past_distance"]==x["today_distance"] and x["past_turf_dirt"]==x["today_turf_dirt"] and (x["past_course_condition"]=="良" or x["past_course_condition"]=="稍")]
        if len(matched) > 0:
            self.whole_race_dict["fastest_time"] =  sorted(matched, key=lambda x:x["past_race_time"])[0]["past_race_time"]

    def set_single_horse_dicts(self, whole_list):
        min_index = 0
        max_index = 0
        self.single_horse_dicts = []
        horsenum = whole_list[0]["today_horsenum"]
        if horsenum != 1:
            for i in range(horsenum-1):
                self.single_horse_dicts.append(self.get_single_horse_data([]))
        for i in range(len(whole_list)):
            if whole_list[i]["today_horsenum"] != horsenum:
                self.single_horse_dicts.append(self.get_single_horse_data(whole_list[min_index:max_index]))
                min_index = max_index
                if whole_list[i]["today_horsenum"] - horsenum > 1:
                    for j in range(whole_list[i]["today_horsenum"] - horsenum - 1):
                        self.single_horse_dicts.append(self.get_single_horse_data([]))
                horsenum = whole_list[i]["today_horsenum"]
            max_index = max_index + 1
        self.single_horse_dicts.append(self.get_single_horse_data(whole_list[min_index:max_index]))
        for i in range(whole_list[0]["today_horse_total"]-horsenum):
            self.single_horse_dicts.append(self.get_single_horse_data([]))

    def get_single_horse_data(self, single_list):
        single_dict = {"race_count":len(single_list),"zi_diff_from_top":0,"td_diff_count":0,"odds":999}
        td_diff_count = 0
        if len(single_list) > 0:
            for i in range(len(single_list)):
                if i == 0:
                    single_dict["odds"] = single_list[i]["today_odds"]
                    single_dict["zi_diff_from_top"] = self.whole_race_dict["top_zi"] - single_list[i]["today_zi"]
                if single_list[i]["today_turf_dirt"] != single_list[i]["past_turf_dirt"]:
                    td_diff_count = td_diff_count + 1
            single_dict["td_diff_count"] = td_diff_count
        return single_dict

    def set_whole_race_dict_extra_with_single_dicts(self):
        for shd in self.single_horse_dicts:
            if shd["odds"] <= 5.0 and shd["race_count"] == shd["td_diff_count"]:
                self.whole_race_dict["pop_tddiff"] = True
                break
