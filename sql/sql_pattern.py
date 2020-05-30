# coding: utf-8
import sql_manipulator
import sql_jockey
from utility import Utility
import csv
import datetime

class SQLPattern():
    def __init__(self, option=""):
        self.util = Utility()

    def get_self_data(self, entry):
        cond = self.util.convert_condition(entry['course_condition'])
        msg = "horsename='"+entry['horsename']+"' and race_time="+str(entry['race_time'])+" and horse_table.place='"+entry['place']+"' and turf_dirt='"+entry['turf_dirt']+"' and (course_condition='"+cond+"') and distance="+str(entry['distance'])
        ret = self.util.get_sql_data(msg)
        if len(ret) > 0:
            return ret[0]
        else:
            return []

    def get_similar_strength_horse_data(self,entry,self_data):
        cond = self.util.convert_condition(entry['course_condition'])
        if len(self_data) == 0:
            return []
        # similar racetime, rap5f, diff3f
        msg = "race_time>"+str(entry['race_time']-0.3)+" and race_time<"+str(entry['race_time']+0.3)+" and diff3f>"+str(self_data['diff3f']-0.3)+" and diff3f<"+str(self_data['diff3f']+0.3)+" and horse_table.place='"+entry['place']+"' and turf_dirt='"+entry['turf_dirt']+"' and (course_condition='"+cond+"') and rap5f>"+str(self_data['rap5f']-0.3)+" and rap5f<"+str(self_data['rap5f']+0.3)
        ret =  self.util.get_sql_data(msg)
        if len(ret) > 0:
            return ret
        else:
            return []

    def get_similar_strength_horse_targetrace_data(self,entry,target,self_data):
        similar_power_horse = self.get_similar_strength_horse_data(entry,self_data)
        msg = "race_table.place='"+target['place']+"' and turf_dirt='"+target['turf_dirt']+"' and distance="+str(target['distance'])+" and ("
        if len(similar_power_horse) == 0:
            return []
        for i in range(len(similar_power_horse)):
            msg_or = " or "
            if i == len(similar_power_horse)-1:
                msg_or = ")"
            msg = msg + " (horsename='"+similar_power_horse[i]['horsename']+"' and race_table.rdate > '"+similar_power_horse[i]['rdate'].strftime('%Y/%m/%d')+"' - INTERVAL 1 YEAR and race_table.rdate < '"+similar_power_horse[i]['rdate'].strftime('%Y-%m-%d')+"' + INTERVAL 1 YEAR)"+msg_or
        msg = msg + " and horsename != '"+entry['horsename']+"'"
        ret = self.util.get_sql_data(msg)
        if len(ret) > 0:
            return ret
        else:
            return []

    def get_entry_target_data(self, csvfile):
        row_count = 0
        all_entry = []
        all_target = []
        entry = []
        target = []
        with open(csvfile, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                # 1列目が1980を超えているならレースデータ（年月日）と判定
                if int(row[0]) >= 1980:
                    cls = self.util.analyse_class(row[5])
                    target={"rdate":row[0]+"-"+row[1]+"-"+row[2],"place":row[3],"turf_dirt":row[7],"distance":row[8],"class":row[5],"class_condition":cls,"race":row[4],"horse_total":row[9],"course_mark":row[11]}
                    all_target.append(target)
                    if row_count > 0:
                        all_entry.append(entry)
                        entry = []
                else:
                    basic_dict = {"horsenum":row[0],"horsename":row[1],"stallion":row[2],"horse_sex":row[3],"horse_age":row[4],"jockey_name":row[5],"trainer":row[6],"odds":row[7],"jockey_weight":row[8],"zi":row[11],"horseweight":row[13],"weightdiff":row[14],"span":row[15],"castration":row[16],"transfer":row[17],"color":row[18],"owner":row[19],"broodmaresire":row[20]}
                    for i in range(5):
                        a = 27*i
                        if len(row) > 22+a and len(row[22+a]) > 0 and row[29+a] != "----":
                            single_race_dict = {"rdate":row[21+a].replace('.','-'),"place":row[22+a],"turf_dirt":self.util.convert_turf_dirt(row[24+a]),"distance":row[25+a],"class":row[26+a],"course_condition":row[27+a],"goal_order":row[28+a],"race_time":self.util.convert_race_time(row[29+a]),"time_diff":row[30+a],"past_horsenum":row[31+a],"population":row[32+a],"passorder1":row[33+a],"passorder2":row[34+a],"passorder3":row[35+a],"passorder4":row[36+a],"last3f":row[37+a],"past_odds":row[38+a],"finish":row[39+a],"past_span":row[40+a],"diff3f":row[41+a],"pci":row[42+a],"rpci":row[43+a],"brinker":row[44+a],"course_mark":row[45+a],"horseweight":row[46+a],"weightdiff":row[47+a],"pastnum":i+1}
                            single_race_dict.update(basic_dict)
                            entry.append(single_race_dict)
                row_count = row_count+1
            all_entry.append(entry)
            all_target.append(target)
        return all_entry,all_target

    def set_single_maindata(self, entry, target, self_data, div_dict, goal):
        single_maindata = []
        single_maindata.append(target['rdate'])
        single_maindata.append(target['race'])
        single_maindata.append(target['place'])
        single_maindata.append(target['turf_dirt'])
        single_maindata.append(target['distance'])
        single_maindata.append(entry['horsename'])
        single_maindata.append(target['class'])
        single_maindata.append(entry['jockey_name'])
        single_maindata.append(entry['jockey_weight'])
        single_maindata.append(entry['zi'])

        single_maindata.append(entry['pastnum'])
        single_maindata.append(str(self_data['rdate']))
        single_maindata.append(self_data['race'])
        single_maindata.append(self_data['place'])
        single_maindata.append(self_data['turf_dirt'])
        single_maindata.append(self_data['distance'])
        single_maindata.append(self_data['class'])
        single_maindata.append(self_data['course_condition'])
        single_maindata.append(self_data['horseweight'])
        single_maindata.append(self_data['rap3f'])
        single_maindata.append(self_data['rap5f'])
        single_maindata.append(self_data['diff3f'])
        single_maindata.append(self_data['time_diff'])
        single_maindata.append(div_dict['mean_diff'])
        single_maindata.append(div_dict['mean_goal'])
        single_maindata.append(div_dict['diviation'])
        single_maindata.append(div_dict['sigma'])
        single_maindata.append(div_dict['total'])
        single_maindata.append(self_data['horse_last3f'])
        single_maindata.append(self_data['race_last3f'])
        single_maindata.append(goal)
        return single_maindata

    def get_maindata_dict_from_csv(self, csvfile):
        main_dict_list = []
        with open(csvfile, 'r') as f:
            reader = csv.reader(f)
            header_flg = 0
            for row in reader:
                if header_flg == 0:
                    header_flg = 1
                    continue
                main_dict = {}
                main_dict["today_rdate"] = datetime.datetime.strptime(row[0], '%Y-%m-%d')
                main_dict["today_race"] = int(row[1])
                main_dict["today_place"] = row[2]
                main_dict["today_turf_dirt"] = row[3]
                main_dict["today_distance"] = int(row[4])
                main_dict["horsename"] = row[5]
                main_dict["today_class"] = row[6]
                main_dict["today_jockey_name"] = row[7]
                main_dict["today_jockey_weight"] = float(row[8])
                main_dict["today_zi"] = int(row[9])

                main_dict["pastnum"] = int(row[10])
                main_dict["past_rdate"] = datetime.datetime.strptime(row[11], '%Y-%m-%d')
                main_dict["past_race"] = int(row[12])
                main_dict["past_place"] = row[13]
                main_dict["past_turf_dirt"] = row[14]
                main_dict["past_distance"] = int(row[15])
                main_dict["past_class"] = row[16]
                main_dict["past_course_condition"] = row[17]
                main_dict["past_horseweight"] = int(row[18])
                main_dict["past_rap3f"] = float(row[19])
                main_dict["past_rap5f"] = float(row[20])
                main_dict["past_diff3f"] = float(row[21])
                main_dict["past_time_diff"] = float(row[22])
                analyse_avail_list = [0,0,0,0]
                if float(row[25]) > 0:
                    analyse_avail_list = [float(row[23]),float(row[24]),float(row[25]),float(row[26])]
                main_dict["past_mean_diff"] = analyse_avail_list[0]
                main_dict["past_mean_goal"] = analyse_avail_list[1]
                main_dict["past_diviation"] = analyse_avail_list[2]
                main_dict["past_sigma"] = analyse_avail_list[3]
                main_dict["past_total"] = int(row[27])
                main_dict["past_horse_last3f"] = float(row[28])
                main_dict["past_race_last3f"] = float(row[29])
                try:
                    main_dict["today_goal"] = int(row[30])
                except ValueError:
                    main_dict["today_goal"] = 0
                main_dict_list.append(main_dict)
        return main_dict_list

