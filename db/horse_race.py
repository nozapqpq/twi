# coding: utf-8
import MySQLdb
import os
import csv
import sys
import re
from datetime import datetime
from .sql_manipulator import SQLManipulator
from .utility import Utility
#reload(sys)
#sys.setdefaultencoding('utf-8')
print(sys.getdefaultencoding())
class HorseRace():
    def __init__(self, setting_flg=False):
        self.manipulator = SQLManipulator()
        self.utility = Utility()
        self.horse_race_dict_list = []
        if setting_flg:
            # self.horse_race_dict_list = self.get_horse_race_dict_list_from_db()
            self.race_dict_list = self.get_race_dict_list_from_db()
            self.horse_dict_list = self.get_horse_dict_list_from_db()

    # ***** horse race data list get processes (users could use this 5 methods in external files) *****
    def get_history_single_horse_list_without_newer_day(self, horsename, today):
        converted_today = datetime.strptime(today, '%Y-%m-%d').date()
        history = [x for x in self.horse_race_dict_list if x['horsename'] == horsename and x['rdate'] < converted_today]
        return history

    def get_single_horse_list(self, horsename):
        return [x for x in self.horse_race_dict_list if x['horsename'] == horsename]
                      
    def get_today_horses_list(self, today, horsenames):
        converted_today = self.convert_date_str_to_date(today)
        return [x for x in self.horse_race_dict_list if converted_today == x['rdate'] and x['horsename'] in horsenames]
                      
    def get_single_race_and_horse_race_list(self, rdate, place, race):
        converted_rdate = self.convert_date_str_to_date(rdate)
        race_list = [x for x in self.race_dict_list if converted_rdate == x['rdate'] and place == x['place'] and race == x['race']]
        horse_race_list = [x for x in self.horse_race_dict_list if converted_rdate == x['rdate'] and place == x['place'] and race == x['race']]
        return race_list, horse_race_list    

    def get_jvtarget_oneday_past_and_today_list(self, csvfile):
        row_count = 0                                  
        all_past = [] 
        all_today = []
        past_list = []
        today_list = []
        with open(csvfile, 'r') as f:
            reader = csv.reader(f)   
            for row in reader:       
                # 1列目が1980を超えているならレースデータ（年月日）と判定
                if int(row[0]) >= 1980:
                    cls = self.utility.analyse_class(row[5])
                    today_list={"rdate":row[0]+"-"+row[1]+"-"+row[2],"place":row[3],"turf_dirt":row[7],"distance":row[8],"class":row[5],"class_condition":cls,"race":row[4],"horse_total":row[9],"course_mark":row[11],"course_condition":row[12]}
                    all_today.append(today_list)
                    if row_count > 0:
                        all_past.append(past_list)
                        past_list = []
                else: 
                    basic_dict = {"horsenum":self.convert_to_int_or_blank(row[0]),"horsename":row[1],"stallion":row[2],"horse_sex":row[3],"horse_age":row[4],"jockey_name":row[5],"trainer":row[6],"odds":self.convert_odds(row[7]),"jockey_weight":row[8],"zi":row[11],"span":self.convert_span(row[13]),"castration":row[14],"transfer":row[15],"color":row[16],"owner":row[17],"broodmaresire":row[18]}
                    if (len(row)-19)%27 == 0: # オッズ未取得など不完全な状態で出馬表を取得しているときはデータを捨てる
                        past_single_list = []
                        for i in range(5):        
                            a = 27*i
                            if len(row) > 20+a and len(row[20+a]) > 0 and row[27+a] != "----":
                                single_race_dict = {"rdate":self.utility.convert_date_format(row[19+a]),"place":row[20+a],"turf_dirt":self.utility.convert_turf_dirt(row[22+a]),"distance":row[23+a],"class":row[24+a],"course_condition":row[25+a],"goal_order":row[26+a],"race_time":self.utility.convert_race_time(row[27+a]),"time_diff":self.convert_time(row[28+a]),"past_horsenum":self.convert_to_int_or_blank(row[29+a]),"population":row[30+a],"passorder1":row[31+a],"passorder2":row[32+a],"passorder3":row[33+a],"passorder4":row[34+a],"last3f":self.convert_time(row[35+a]),"past_odds":self.convert_odds(row[36+a]),"finish":row[37+a],"past_span":self.convert_span(row[38+a]),"diff3f":self.convert_time(row[39+a]),"pci":row[40+a],"rpci":row[41+a],"brinker":row[42+a],"course_mark":row[43+a],"horseweight":row[44+a],"weightdiff":self.utility.remove_pm_space(row[45+a]),"pastnum":i+1}
                                single_race_dict.update(basic_dict)
                                past_single_list.append(single_race_dict)
                        past_list.append(past_single_list)
                row_count = row_count+1           
            all_past.append(past_list)
        return all_past,all_today

    # ** utilities **
    def compare_two_date(self, date1, date2):
        return self.convert_date_str_to_date(date1) == self.convert_date_str_to_date(date2)
 
    def convert_date_str_to_date(self, input_date):
        ret_date = ""
        if type(input_date) is str:
            if "-" in input_date:
                ret_date = datetime.strptime(input_date,'%Y-%m-%d').date()
            else:
                ret_date = datetime.strptime(input_date,'%y%m%d').date()
        else:
            ret_date = input_date
        return ret_date
    def convert_time(self, t):
        if t == "" or "----" in t:
            return ""
        return float(t)
    def convert_odds(self, odds):
        if odds == "" or "取消" in odds:
            return ""
        return float(odds)
    def convert_span(self, span):
        if "連" in span:
            return 1
        elif "初" in span or span == "":
            return 0
        else:
            return int(span)
    def convert_to_int_or_blank(self, i):
        if i == "":
            return ""
        else:
            return int(i)
    # ** utilities end **
    # ***** horse race data list get processes end *****

    # ***** get race_table and horse_table data methods *****
    def get_race_data(self):        
        return self.race_dict_list  
                                    
    def get_horse_data(self):       
        return self.horse_dict_list 

    def get_horse_race_data(self):
        return self.horse_race_dict_list

    def set_horse_race_dict_list(self, condition_msg="1=1"):
        self.horse_race_dict_list = self.get_horse_race_dict_list_from_db(condition_msg)

    def get_horse_race_dict_list_from_db(self, condition_msg="1=1"):
        msg_select = "select race_table.rdate,race_table.place,race_table.race,class,turf_dirt,distance,course_condition,rap3f,rap5f,race_table.last3f,race_table.horse_total,race_table.rpci,race_table    .dividend,race_table.course_mark,race_table.early_rap2,race_table.early_rap3,race_table.early_rap4,race_table.last_rap1,race_table.last_rap2,race_table.last_rap3,race_table.last_rap4,goal_order,brinker,horsenum,horsename,horse_sex,age,jockey_weight,jockey_name,race_time,time_diff,passorder1,passorder2,passorder3,passorder4,finish,horse_table.last3f,diff3f,odds_order,odds,horseweight,weightdiff,trainer,carrier,owner,breeder,stallion,broodmaresire,color,span,castration,pci "
        msg_from = "from horse_table "
        msg_join = "inner join race_table on horse_table.rdate = race_table.rdate and horse_table.place = race_table.place and horse_table.race = race_table.race "
        msg = msg_select+msg_from+msg_join+"where race_time != 0 and "+condition_msg+";"
        tpl = self.manipulator.sql_manipulator(msg)
        retlist = []
        for t in tpl:
            single_dict = {"rdate":t[0],"place":t[1],"race":t[2],"class":t[3],"turf_dirt":t[4],"distance":t[5],"course_condition":t[6],"rap3f":t[7],"rap5f":t[8],"race_last3f":t[9],"horse_total":t[10],"rpci":t[11],"dividend":t[12],"course_mark":t[13],"early_rap2":t[14],"early_rap3":t[15],"early_rap4":t[16],"last_rap1":t[17],"last_rap2":t[18],"last_rap3":t[19],"last_rap4":t[20],"goal_order":t[21],"brinker":t[22],"horsenum":int(t[23]),"horsename":t[24],"horse_sex":t[25],"age":t[26],"jockey_weight":t[27],"jockey_name":t[28],"race_time":t[29],"time_diff":t[30],"passorder1":t[31],"passorder2":t[32],"passorder3":t[33],"passorder4":t[34],"finish":t[35],"horse_last3f":t[36],"diff3f":t[37],"odds_order":t[38],"odds":t[39],"horseweight":t[40],"weightdiff":t[41],"trainer":t[42],"carrier":t[43],"owner":t[44],"breeder":t[45],"stallion":t[46],"broodmaresire":t[47],"color":t[48],"span":t[49],"castration":t[50],"pci":t[51]}
            retlist.append(single_dict)
        return retlist
 
    def get_horse_dict_list_from_db(self, condition_msg="1=1"):
        msg_select = "select rdate, place, race, horsenum, horsename, horse_sex, age, jockey_weight, jockey_name, time_diff, odds, trainer, carrier, owner, breeder, stallion, broodmaresire, race_time, last3f, diff3f, goal_order "
        msg_from = "from horse_table "
        msg = msg_select+msg_from+"where "+condition_msg+";"
        tpl = self.manipulator.sql_manipulator(msg)
        retlist = []                 
        for t in tpl:                
            single_dict = {"rdate":t[0],"place":t[1],"race":t[2],"horsenum":int(t[3]),"horsename":t[4],"horse_sex":t[5],"age":t[6],"jockey_weight":t[7],"jockey_name":t[8],"time_diff":t[9],"odds":t[10],"trainer":t[11],"carrier":t[12],"owner":t[13],"breeder":t[14],"stallion":t[15],"broodmaresire":t[16],"race_time":t[17],"last3f":t[18],"diff3f":t[19],"goal_order":t[20]}
            retlist.append(single_dict)
        return retlist                                                                                                                                                                     
 
    def get_race_dict_list_from_db(self, condition_msg="1=1"):
        msg_select = "select rdate, place, race, class, turf_dirt, distance, course_condition, rap3f, rap5f, last3f, horse_total, rpci, dividend, course_mark, early_rap2, early_rap3, early_rap4, last_rap1, last_rap2, last_rap3, last_rap4 "
        msg_from = "from race_table "
        msg = msg_select+msg_from+"where "+condition_msg+";"
        tpl = self.manipulator.sql_manipulator(msg)
        retlist = []
        for t in tpl:
            single_dict = {"rdate":t[0],"place":t[1],"race":t[2],"class":t[3],"turf_dirt":t[4],"distance":t[5],"course_condition":t[6],"rap3f":t[7],"rap5f":t[8],"last3f":t[9],"horse_total":t[10],"rpci":t[11],"dividend":t[12],"course_mark":t[13],"early_rap2":t[14],"early_rap3":t[15],"early_rap4":t[16],"last_rap1":t[17],"last_rap2":t[18],"last_rap3":t[19],"last_rap4":t[20]}
            retlist.append(single_dict)
        return retlist
    # **** get race_table and horse_table data methods end *****

    # ***** race_table and horse_table setting start *****
    # use this method to setup using jv_target 
    def set_race_and_horse_data_from_jvtarget(self, csvfile):
        racedata, horsedata = self.get_race_and_horse_list_from_csv(csvfile)
        self.set_race_data_to_db(racedata)
        self.set_horse_data_to_db(horsedata)
        print("import "+csvfile+" is finished.")

    def get_race_and_horse_list_from_csv(self, csvfile):
        read_mode = 0
        horse_count = 0
        race_list = []
        horse_list = []
        temp =[]
        temp_yyyymmdd = '0000-00-00'
        temp_place = ''
        temp_race = 0
        with open(csvfile, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if read_mode == 1:
                    race_list.append(row)
                    temp_yyyymmdd = row[0]+"-"+row[1]+"-"+row[2]
                    temp_place = row[3]
                    temp_race = row[4]
                    read_mode = 0
                if read_mode == 2 and row[0] != "年":
                    row.append(temp_yyyymmdd)
                    row.append(temp_place)
                    row.append(temp_race)
                    temp.append(row)
                    horse_count = horse_count+1
                if row[0] == "年":
                    if horse_count > 0:
                        horse_list.append(temp)
                        horse_count = 0
                        temp = []
                    read_mode = 1
                elif row[0] == "入線順位":
                    read_mode = 2
            # last race horse data append
            horse_list.append(temp)
        return race_list, horse_list

    def set_race_data_to_db(self, racedata):
        all_at_once_msg = ""
        for i in range(len(racedata)):
            all_at_once_msg = all_at_once_msg + self.make_race_message(racedata[i]) + ","
        ret = self.manipulator.sql_manipulator("insert into race_table values "+all_at_once_msg[0:-1])

    def set_horse_data_to_db(self, horsedata):
        all_at_once_msg = ""
        for i in range(len(horsedata)):
            if i%1000==0 and i > 0:
                print("progress : "+str(i)+" / "+str(len(horsedata)))
                ret = self.manipulator.sql_manipulator("insert into horse_table values "+all_at_once_msg[0:-1])
                all_at_once_msg = ""
            for j in range(len(horsedata[i])):
                all_at_once_msg = all_at_once_msg + self.make_horse_data_message(horsedata[i][j]) + ","
        ret = self.manipulator.sql_manipulator("insert into horse_table values "+all_at_once_msg[0:-1])

    # ** utilities **
    def make_race_message(self, race_sm):
        out_dict = {"date":race_sm[0]+"-"+race_sm[1]+"-"+race_sm[2],"place":race_sm[3],"race":race_sm[4],"class":race_sm[6],"td":race_sm[7],"distance":race_sm[8],"condition":race_sm[10],"time3f":race_sm[11],"time5f":race_sm[12],"last5f":race_sm[13],"horse_total":race_sm[15],"rpci":race_sm[16],"dividend":self.convert_dividend(race_sm[17]),"course_mark":race_sm[18],"early_rap2":race_sm[19],"early_rap3":race_sm[20],"early_rap4":race_sm[21],"last_rap1":self.get_last_rap(race_sm[19:-1],1),"last_rap2":self.get_last_rap(race_sm[19:-1],2),"last_rap3":self.get_last_rap(race_sm[19:-1],3),"last_rap4":self.get_last_rap(race_sm[19:-1],4)}
        # last 2 column(level) is blank
        # last 1 column(last3f_correct) is blank
        msg = "('"+out_dict["date"]+"','"+out_dict["place"]+"',"+out_dict["race"]+",'"+out_dict["class"]+"','"+out_dict["td"]+"',"+out_dict["distance"]+",'"+out_dict["condition"]+"',"+out_dict["time3f"]+","+out_dict["time5f"]+","+out_dict["last5f"]+","+out_dict["horse_total"]+","+out_dict["rpci"]+","+out_dict["dividend"]+",'"+out_dict["course_mark"]+"',"+out_dict["early_rap2"]+","+out_dict["early_rap3"]+","+out_dict["early_rap4"]+","+out_dict["last_rap1"]+","+out_dict["last_rap2"]+","+out_dict["last_rap3"]+","+out_dict["last_rap4"]+")"
        return msg
 
    def make_horse_data_message(self,race_dt):
        out_date = race_dt[-3]
        out_place = race_dt[-2]
        out_race = self.convert_blank_number(race_dt[-1])
        out_order = self.convert_blank_number(race_dt[0])
        out_brinker = race_dt[2]
        out_horsenum = self.convert_blank_number(race_dt[4])
        out_horsename = race_dt[5]
        out_sex = race_dt[6]
        out_age = self.convert_blank_number(race_dt[7])
        out_jockey_weight = self.adjust_jockey_weight_expression(race_dt[8])
        out_jockey_name = race_dt[9]
        out_time = self.convert_time_to_doublestr(race_dt[10])
        out_time_diff = self.convert_blank_number(race_dt[13])
        out_passorder1 = self.convert_blank_number(race_dt[14])
        out_passorder2 = self.convert_blank_number(race_dt[15])
        out_passorder3 = self.convert_blank_number(race_dt[16])
        out_passorder4 = self.convert_blank_number(race_dt[17])
        out_finish = race_dt[18]
        out_last3f = race_dt[20].replace("----","0")
        out_diff3f = self.convert_blank_number(race_dt[21])
        out_odds_order = self.convert_blank_number(race_dt[23])
        out_odds = race_dt[24]
        out_horseweight = self.convert_blank_number(race_dt[25].replace("---","0"))
        out_weightdiff = str(int(self.convert_blank_number(race_dt[26])))
        out_trainer = race_dt[29]
        out_carrier = self.convert_blank_number(race_dt[30])
        out_owner = race_dt[31].replace("'","`")
        out_breeder = race_dt[32].replace("'","`")
        out_stallion = race_dt[33].replace("'","`")
        out_broodmaresire = race_dt[34].replace("'","`")
        out_color = race_dt[35]
        out_span = self.convert_blank_number(race_dt[37]).replace("不明","999")
        out_castration = race_dt[38]
        out_pci = self.convert_blank_number(race_dt[39])
        msg = "('"+out_date+"','"+out_place+"',"+out_race+","+out_order+",'"+out_brinker+"',"+out_horsenum+",'"+out_horsename+"','"+out_sex+"',"+out_age+","+out_jockey_weight+",'"+out_jockey_name+"',"+out_time+","+out_time_diff+","+out_passorder1+","+out_passorder2+","+out_passorder3+","+out_passorder4+",'"+out_finish+"',"+out_last3f+","+out_diff3f+","+out_odds_order+","+out_odds+","+out_horseweight+","+out_weightdiff+",'"+out_trainer+"',"+out_carrier+",'"+out_owner+"','"+out_breeder+"','"+out_stallion+"','"+out_broodmaresire+"','"+out_color+"',"+out_span+",'"+out_castration+"',"+out_pci+")"
        return msg

    def adjust_jockey_weight_expression(self, weight_str):
        return weight_str.strip()[0:2]

    def convert_time_to_doublestr(self, time_str):
        if "------" in time_str:
            return str(0.0)
        sep_str = time_str.split('.')
        retval = int(sep_str[0])*60+int(sep_str[1])+int(sep_str[2])/10
        return str(retval)

    def convert_blank_number(self, str):
        if str == "":
            return "0"
        return str

    def convert_dividend(self, div):
        yen = re.search(r'\\\d+', div)
        ret = yen.group()[1:]
        if not ret.isdecimal():
            ret = 0
        return ret

    def get_last_rap(self, rap_list, rap_num):
        rap_list = [x for x in rap_list if x != '']
        target_rap = rap_num*(-1)
        return rap_list[target_rap]
    # ** utilities end **
    # ***** race_table and horse_table setting end *****
