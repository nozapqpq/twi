# coding: utf-8
import sql_manipulator
import csv

class SQLJockey():
    def __init__(self):
        count = 0

    def get_jockey_info(self, jockey, place, td, distance, condition="良"):
        base = self.get_jockey_sql_data(jockey,place,td,distance,condition)
        time_list = [0,58.0,60.0,62.0,100]
        finish_list = ["逃げ","先行","中団","差し","追込","後方","マクリ"]
        about_fin = ["前","中","後","マクリ他"]
        result = [[[0 for i in range(31)] for j in range(4)] for k in range(4)]
        for b in base:
            for tl in range(len(time_list)-1):
                if b[0] > time_list[tl] and b[0] <= time_list[tl+1]:
                    fin = 0
                    if b[1] == finish_list[0] or b[1] == finish_list[1]:
                        fin = 0
                    elif b[1] == finish_list[2] or b[1] == finish_list[3]:
                        fin = 1
                    elif b[1] == finish_list[4] or b[1] == finish_list[5]:
                        fin = 2
                    else:
                        fin = 3
                    diff = b[2]
                    if b[2] >= 3.0:
                        diff = 3.0
                    result[tl][fin][int(diff*10)] = result[tl][fin][int(diff*10)] + 1
        ret = []
        for i in range(4):
            for j in range(4):
                for k in range(30):
                    result[i][j][k+1] = result[i][j][k] + result[i][j][k+1]
        for i in range(4):
            for j in range(4):
                if result[i][j][30] >= 10:
                    for k in range(31):
                        result[i][j][k] = result[i][j][k]/result[i][j][30]*10
                ret.append([jockey,condition,time_list[i],about_fin[j]]+result[i][j])
        return ret

    def get_jockey_sql_data(self, jockey, place, td, distance, condition=""):
        where_cond_msg = ""
        if condition != "":
            where_cond_msg = "and course_condition='"+condition+"'"
        manipulator = sql_manipulator.SQLManipulator()
        select_msg = "select race_table.rap5f,horse_table.finish,horse_table.time_diff,goal_order,horsename,horse_sex,age,race_table.rdate,race_table.race,race_table.place,odds_order,odds,race_table.turf_dirt,race_table.distance,jockey_name "
        from_msg = "from horse_table "
        join_msg = "inner join race_table on horse_table.rdate = race_table.rdate and horse_table.place = race_table.place and horse_table.race = race_table.race "
        where_msg = "where race_time != 0 and jockey_name='"+jockey+"' and race_table.place='"+place+"' and turf_dirt='"+td+"' and distance="+distance+" "+where_cond_msg+";"
        ret = manipulator.sql_manipulator(select_msg+from_msg+join_msg+where_msg)
        return ret

    def get_dictionary(self, jockey, place, td, distance, condition=""):
        data = self.get_jockey_sql_data(jockey,place,td,distance,condition)
        ret_list = []
        for d in data:
            single_dict = {"rap5f":d[0],"finish":d[1],"time_diff":d[2],"goal_order":d[3],"horsename":d[4],"horse_sex":d[5],"age":d[6],"rdate":d[7],"race":d[8],"place":d[9],"odds_order":d[10],"odds":d[11],"turf_dirt":d[12],"distance":d[13],"jockey_name":d[14]}
            ret_list.append(single_dict)
        return ret_list



