# coding: utf-8
import sql_manipulator
import csv
import os
from datetime import datetime as dt

class DeepSingleRace():
    def __init__(self):
        self.sql = sql_manipulator.SQLManipulator()
        self.single_horse_dicts = []
        self.whole_race_dict = {}

    def set_main_dicts(self, whole_list):
        self.clean()
        if len(whole_list) > 0:
            self.set_whole_race_dict(whole_list)
            self.set_single_horse_dicts(whole_list)
            self.set_whole_race_dict_extra_with_single_dicts()

    def clean(self):
        self.single_horse_dicts = []
        self.whole_race_dict = {"place":"","race":0,"rdate":"","horse_total":"","top_zi":0,"top_odds":0,"fastest_time":0.0,"pop_tddiff":False}

    def set_whole_race_dict(self, whole_list):
        self.whole_race_dict["place"] = whole_list[-1]["today_place"]
        self.whole_race_dict["race"] = whole_list[-1]["today_race"]
        self.whole_race_dict["rdate"] = whole_list[-1]["today_rdate"]
        self.whole_race_dict["horse_total"] = whole_list[-1]["today_horse_total"]
        self.whole_race_dict["top_zi"] = max(whole_list, key=lambda x:x['today_zi'])['today_zi']
        self.whole_race_dict["top_odds"] = min(whole_list, key=lambda x:x['today_odds'])['today_odds']
        fastest = min(whole_list, key=lambda x:x['past_race_time'] if x["past_distance"]==x["today_distance"] and x["past_race_time"]>=50.0 and x["past_turf_dirt"]==x["today_turf_dirt"] and (x["past_course_condition"]=="良" or x["past_course_condition"]=="稍") else 0)
        if fastest == 0:
            self.whole_race_dict["fastest_time"] = fastest
        else:
            self.whole_race_dict["fastest_time"] = fastest["past_race_time"]

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
        single_dict = {"race_count":len(single_list),"td_diff_count":0,"diff02_count":0,"diff20_count":0,"diff20_lasttime":False,"zi_diff_from_top":0,"highodds05":False,"aheadlose10":False,"odds":999}
        diff02_count = 0
        diff20_count = 0
        td_diff_count = 0
        aheadlose10_count = 0
        if len(single_list) > 0:
            for i in range(len(single_list)):
                if i == 0:
                    single_dict["odds"] = single_list[i]["today_odds"]
                    if single_list[i]["past_time_diff"] >= 2.0:
                        single_dict["diff20_lasttime"] = True
                    single_dict["zi_diff_from_top"] = self.whole_race_dict["top_zi"] - single_list[i]["today_zi"]
                if single_list[i]["past_time_diff"] >= 2.0:
                    diff20_count = diff20_count + 1
                if single_list[i]["past_time_diff"] <= 0.3:
                    diff02_count = diff02_count + 1
                if single_list[i]["past_odds"] >= 50.0 and single_list[i]["past_time_diff"] <= 0.5:
                    single_dict["highodds05"] = True
                if single_list[i]["today_turf_dirt"] != single_list[i]["past_turf_dirt"]:
                    td_diff_count = td_diff_count + 1
                if single_list[i]["past_diff3f"] <= 0.3 and single_list[i]["past_time_diff"] >= 1.0:
                    aheadlose10_count = aheadlose10_count + 1
            single_dict["diff20_count"] = diff20_count
            single_dict["diff02_count"] = diff02_count
            single_dict["td_diff_count"] = td_diff_count
            single_dict["aheadlose10_count"] = aheadlose10_count
        return single_dict
    def set_whole_race_dict_extra_with_single_dicts(self):
        for shd in self.single_horse_dicts:
            if shd["odds"] <= 5.0 and shd["race_count"] == shd["td_diff_count"]:
                self.whole_race_dict["pop_tddiff"] = True
                break
