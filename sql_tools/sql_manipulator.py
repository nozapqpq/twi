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
        msg_select = "select race_table.rdate,race_table.place,race_table.race,class,turf_dirt,distance,course_condition,rap3f,rap5f,race_table.last3f,race_table.horse_total,race_table.rpci,race_table.triple_dividend,race_table.course_mark,race_table.level,race_table.last3f_correct,goal_order,brinker,horsenum,horsename,horse_sex,age,jockey_weight,jockey_name,race_time,time_diff,passorder1,passorder2,passorder3,passorder4,finish,horse_table.last3f,diff3f,odds_order,odds,horseweight,weightdiff,trainer,carrier,owner,breeder,stallion,broodmaresire,color,span,castration,pci "
        msg_from = "from horse_table "
        msg_join = "inner join race_table on horse_table.rdate = race_table.rdate and horse_table.place = race_table.place and horse_table.race = race_table.race "
        msg = msg_select+msg_from+msg_join+"where race_time != 0 and "+condition_msg+";"
        tpl = self.sql_manipulator(msg)
        retlist = []
        for t in tpl:
            single_dict = {"rdate":t[0],"place":t[1],"race":t[2],"class":t[3],"turf_dirt":t[4],"distance":t[5],"course_condition":t[6],"rap3f":t[7],"rap5f":t[8],"race_last3f":t[9],"horse_total":t[10],"rpci":t[11],"triple_dividend":t[12],"course_mark":t[13],"level":t[14],"last3f_correct":t[15],"goal_order":t[16],"brinker":t[17],"horsenum":t[18],"horsename":t[19],"horse_sex":t[20],"age":t[21],"jockey_weight":t[22],"jockey_name":t[23],"race_time":t[24],"time_diff":t[25],"passorder1":t[26],"passorder2":t[27],"passorder3":t[28],"passorder4":t[29],"finish":t[30],"horse_last3f":t[31],"diff3f":t[32],"odds_order":t[33],"odds":t[34],"horseweight":t[35],"weightdiff":t[36],"trainer":t[37],"carrier":t[38],"owner":t[39],"breeder":t[40],"stallion":t[41],"broodmaresire":t[42],"color":t[43],"span":t[44],"castration":t[45],"pci":t[46]}
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
