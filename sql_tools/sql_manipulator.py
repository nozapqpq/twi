# coding: utf-8
import MySQLdb
import os
import csv
import sys
import re
#reload(sys)
#sys.setdefaultencoding('utf-8')
print(sys.getdefaultencoding())
class SQLManipulator():
    def __init__(self, ):
        i=0

    def sql_manipulator(self, msg):
        connection = MySQLdb.connect(
            host='localhost',
            user='noza',
            passwd='Pass_123',
            db='horse',
            use_unicode=True,
            charset='utf8')
        cursor = connection.cursor()

        cursor.execute(msg)
        retval = cursor.fetchall()
        connection.commit()
        connection.close()

        return retval

    def get_horse_race_data(self, condition_msg):
        msg_select = "select race_table.rdate,race_table.place,race_table.race,class,turf_dirt,distance,course_condition,rap3f,rap5f,race_table.last3f,race_table.horse_total,race_table.rpci,race_table    .dividend,race_table.course_mark,race_table.early_rap2,race_table.early_rap3,race_table.early_rap4,race_table.last_rap1,race_table.last_rap2,race_table.last_rap3,race_table.last_rap4,goal_order,brinker,horsenum,horsename,horse_sex,age,jockey_weight,jockey_name,race_time,time_diff,passorder1,passorder2,passorder3,passorder4,finish,horse_table.last3f,diff3f,odds_order,odds,horseweight,weightdiff,trainer,carrier,owner,breeder,stallion,broodmaresire,color,span,castration,pci "
        msg_from = "from horse_table "
        msg_join = "inner join race_table on horse_table.rdate = race_table.rdate and horse_table.place = race_table.place and horse_table.race = race_table.race "
        msg = msg_select+msg_from+msg_join+"where race_time != 0 and "+condition_msg+";"
        tpl = self.sql_manipulator(msg)
        retlist = []
        for t in tpl:
            single_dict = {"rdate":t[0],"place":t[1],"race":t[2],"class":t[3],"turf_dirt":t[4],"distance":t[5],"course_condition":t[6],"rap3f":t[7],"rap5f":t[8],"race_last3f":t[9],"horse_total":t[10],    "rpci":t[11],"dividend":t[12],"course_mark":t[13],"early_rap2":t[14],"early_rap3":t[15],"early_rap4":t[16],"last_rap1":t[17],"last_rap2":t[18],"last_rap3":t[19],"last_rap4":t[20],"goal_order":t[21],"brinker":t[22],"horsenum":t[23],"horsename":t[24],"horse_sex":t[25],"age":t[26],"jockey_weight":t[27],"jockey_name":t[28],"race_time":t[29],"time_diff":t[30],"passorder1":t[31],"passorder2":t[32],"pass    order3":t[33],"passorder4":t[34],"finish":t[35],"horse_last3f":t[36],"diff3f":t[37],"odds_order":t[38],"odds":t[39],"horseweight":t[40],"weightdiff":t[41],"trainer":t[42],"carrier":t[43],"owner":t[44],"breeder":t[45],"stallion":t[46],"broodmaresire":t[47],"color":t[48],"span":t[49],"castration":t[50],"pci":t[51]}
            retlist.append(single_dict)
        return retlist

    def get_simple_horse_data(self, condition_msg):
        msg_select = "select rdate, place, race, horsenum, horsename, horse_sex, age, jockey_weight, jockey_name, time_diff, odds, trainer, carrier, owner, breeder, stallion, broodmaresire "
        msg_from = "from horse_table "
        msg = msg_select+msg_from+"where "+condition_msg+";"
        tpl = self.sql_manipulator(msg)
        retlist = []
        for t in tpl:
            single_dict = {"rdate":t[0],"place":t[1],"race":t[2],"horsenum":t[3],"horsename":t[4],"horse_sex":t[5],"age":t[6],"jockey_weight":t[7],"jockey_name":t[8],"time_diff":t[9],"odds":t[10],"trainer":t[11],"carrier":t[12],"owner":t[13],"breeder":t[14],"stallion":t[15],"broodmaresire":t[16]}
            retlist.append(single_dict)
        return retlist
    def get_simple_race_data(self, condition_msg):
        msg_select = "select rdate, place, race, class, turf_dirt, distance, course_condition, rap3f, rap5f, last3f, horse_total, rpci, dividend, course_mark, early_rap2, early_rap3, early_rap4, last_rap1, last_rap2, last_rap3, last_rap4 "
        msg_from = "from race_table "
        msg = msg_select+msg_from+"where "+condition_msg+";"
        tpl = manipulator.sql_manipulator(msg)
        retlist = []
        for t in tpl:
            single_dict = {"rdate":t[0],"place":t[1],"race":t[2],"class":t[3],"turf_dirt":t[4],"distance":t[5],"course_condition":t[6],"rap3f":t[7],"rap5f":t[8],"last3f":t[9],"horse_total":t[10],"rpci":t[11],"dividend":t[12],"course_mark":t[13],"early_rap2":t[14],"early_rap3":t[15],"early_rap4":t[16],"last_rap1":t[17],"last_rap2":t[18],"last_rap3":t[19],"last_rap4":t[20]}
            retlist.append(single_dict)
        return retlist
