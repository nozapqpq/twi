# coding: utf-8
import os
import sys
import re
import statistics
import math
from .sql_manipulator import SQLManipulator

class SlowPace():
    def __init__(self):
        self.sql = SQLManipulator()
        self.slow_pace_list = self.get_slow_pace_dict_list_from_db()
        self.place_list = ["札幌","函館","福島","新潟","中山","東京","中京","阪神","京都","小倉"]
        self.distance_list = [1000,1150,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,3000,3200,3400,3600]
        self.cls_list = ["新馬","未勝利","1勝","2勝"]
        self.cls_name = ["新馬","未勝利","1勝","2勝以上"]
        self.condition_list = ["良","稍","重","不"]
        self.turf_dirt_list = ["ダート","芝"]

    def get_slow_pace_dict_list(self):
        return self.slow_pace_dict_list

    def get_slow_pace_dict_list_from_db(self):
        select_msg = "select * "
        from_msg = "from slow_pace_table"
        msg = select_msg+from_msg+";"
        tpl = self.sql.sql_manipulator(msg)
        retlist = []
        for t in tpl:
            single_dict = {"place":t[0],"class":t[1],"turf_dirt":t[2],"distance":t[3],"course_condition":t[4],"border_3f":t[5],"border_5f":t[6]}
            retlist.append(single_dict)
        return retlist

    def add_slow_pace_table(self):
        border = 0
        for p in self.place_list:
            for d in self.distance_list:
                for cl in self.cls_list:
                    for con in self.condition_list:
                        for td in self.turf_dirt_list:
                            border_3f, border_5f = self.get_slow_pace_border(p,self.class_converter(cl),cl,td,d,con)
                            if border_3f != 0:
                                self.sql.sql_manipulator("insert into slow_pace_table values ('"+p+"','"+cl+"','"+td+"',"+str(d)+",'"+con+"',"+str(border_3f)+","+str(border_5f)+");")

    def get_slow_pace_border(self, place, cls, actual_cls, td, distance, cond):
        dict_list = []
        exist_check = self.sql.sql_manipulator("select * from slow_pace_table where place='"+place+"' and class='"+actual_cls+"' and turf_dirt='"+td+"' and distance='"+str(distance)+"' and course_condition='"+cond+"';")
        if len(exist_check) > 0:
            print("data already exists.")
            return 0, 0
        date_rnum = self.sql.sql_manipulator("select rdate,race from race_table where place='"+place+"' and (class='"+cls+"') and turf_dirt='"+td+"' and distance='"+str(distance)+"' and course_condition='"+cond+"';")
        if len(date_rnum) == 0:
            return 0, 0
        database = self.sql.get_horse_race_data("race_table.place='"+place+"' and (class='"+cls+"') and turf_dirt='"+td+"' and distance='"+str(distance)+"' and course_condition='"+cond+"'")
        print(place+str(distance)+td+cond+cls)
        for dr in date_rnum:
            # dr[0]:rdate, dr[1]:race
            dt = self.utl.convert_datetime_to_str(dr[0])
            div = 0
            total = 0
            single_dict = {}
            for db in database:
                if db['rdate'] == dr[0] and db['race'] == dr[1]:
                    if total == 0:
                        single_dict['rap3f'] = db['rap3f']
                        single_dict['rap5f'] = db['rap5f']
                    div = div + (db["goal_order"]-db["passorder3"])**2
                    total = total + 1
            if total > 0:
                single_dict['indicator'] = div/(total**3)
                dict_list.append(single_dict)
        rap3f_list = []
        rap5f_list = []
        indicator_list = []
        for dl in dict_list:
            rap3f_list.append(dl['rap3f'])
            rap5f_list.append(dl['rap5f'])
            indicator_list.append(dl['indicator'])
        print(statistics.mean(rap3f_list))
        print(statistics.mean(rap5f_list))
        print(statistics.mean(indicator_list))
        print(statistics.pstdev(rap5f_list))
        print(statistics.pstdev(indicator_list))
        border_indicator = statistics.mean(indicator_list)-statistics.pstdev(indicator_list)
        low_indicator_list_3f = []
        low_indicator_list_5f = []
        for dl in dict_list:
            if dl['indicator'] <= border_indicator:
                low_indicator_list_3f.append(dl['rap3f'])
                low_indicator_list_5f.append(dl['rap5f'])
        if len(low_indicator_list_3f) == 0:
            return 37.0, 65.0
        ret_3f = statistics.mean(low_indicator_list_3f)
        ret_5f = statistics.mean(low_indicator_list_5f)
        return ret_3f, ret_5f

    def class_converter(self, cls):
        class_list = [["新馬"],["未勝利"],["500万下","1勝"],["1000万下","2勝","1600万下","3勝","OP(L)","オープン","重賞","Ｇ３","Ｇ２","Ｇ１"]]
        idx = 0
        for i in range(len(class_list)):
            if cls in class_list[i]:
                idx = i
                break
        if idx == 0:
            return "新馬"
        elif idx == 1:
            return "未勝利"
        elif idx == 2:
            return "500万下' or class='1勝"
        elif idx == 3:
            return "1000万下' or class='2勝' or class='1600万下' or class='3勝' or class='OP(L)' or class='オープン' or class='重賞' or class='Ｇ３' or class='Ｇ２' or class='Ｇ１"
        else:
            return "未勝利"

#sp = SlowPace()
#sp.add_slow_pace_table()
