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
        msg = "horsename='"+entry['horsename']+"' and race_table.rdate='"+entry['rdate']+"'"
        ret = self.util.get_sql_data(msg)
        if len(ret) > 0:
            return ret[0]
        else:
            return []

    def get_similar_strength_horse_data(self,entry,self_data):
        return []
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
        return []
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
                    target={"rdate":row[0]+"-"+row[1]+"-"+row[2],"place":row[3],"turf_dirt":row[7],"distance":row[8],"class":row[5],"class_condition":cls,"race":row[4],"horse_total":row[9],"course_mark":row[11],"course_condition":row[12]}
                    all_target.append(target)
                    if row_count > 0:
                        all_entry.append(entry)
                        entry = []
                else:
                    basic_dict = {"horsenum":row[0],"horsename":row[1],"stallion":row[2],"horse_sex":row[3],"horse_age":row[4],"jockey_name":row[5],"trainer":row[6],"odds":row[7],"jockey_weight":row[8],"zi":row[11],"span":row[13],"castration":row[14],"transfer":row[15],"color":row[16],"owner":row[17],"broodmaresire":row[18]}
                    if (len(row)-19)%27 == 0: # オッズ未取得など不完全な状態で出馬表を取得しているときはデータを捨てる
                        for i in range(5):
                            a = 27*i
                            if len(row) > 20+a and len(row[20+a]) > 0 and row[27+a] != "----":
                                single_race_dict = {"rdate":self.util.convert_date_format(row[19+a]),"place":row[20+a],"turf_dirt":self.util.convert_turf_dirt(row[22+a]),"distance":row[23+a],"class":row[24+a],"course_condition":row[25+a],"goal_order":row[26+a],"race_time":self.util.convert_race_time(row[27+a]),"time_diff":row[28+a],"past_horsenum":row[29+a],"population":row[30+a],"passorder1":row[31+a],"passorder2":row[32+a],"passorder3":row[33+a],"passorder4":row[34+a],"last3f":row[35+a],"past_odds":row[36+a],"finish":row[37+a],"past_span":row[38+a],"diff3f":row[39+a],"pci":row[40+a],"rpci":row[41+a],"brinker":row[42+a],"course_mark":row[43+a],"horseweight":row[44+a],"weightdiff":self.util.remove_pm_space(row[45+a]),"pastnum":i+1}
                                single_race_dict.update(basic_dict)
                                entry.append(single_race_dict)
                row_count = row_count+1
            all_entry.append(entry)
            all_target.append(target)
        return all_entry,all_target

    def set_single_maindata(self, entry, target, self_data, div_dict, goal, today_time_diff, triple):
        single_maindata = []
        single_maindata.append(target['rdate'])
        single_maindata.append(target['race'])
        single_maindata.append(target['place'])
        single_maindata.append(target['turf_dirt'])
        single_maindata.append(target['distance'])
        single_maindata.append(target['class'])
        single_maindata.append(target['horse_total'])
        single_maindata.append(target['course_condition'])
        single_maindata.append(target['course_mark'])
        single_maindata.append(entry['horsenum'])
        single_maindata.append(entry['horsename'])
        single_maindata.append(entry['horse_sex'])
        single_maindata.append(entry['horse_age'])
        single_maindata.append(entry['odds'])
        single_maindata.append(entry['span'])
        single_maindata.append(entry['jockey_name'])
        single_maindata.append(entry['jockey_weight'])
        single_maindata.append(entry['stallion'])
        single_maindata.append(entry['broodmaresire'])
        single_maindata.append(entry['trainer'])
        single_maindata.append(entry['owner'])
        single_maindata.append(self_data['breeder'])
        single_maindata.append(entry['color'])
        single_maindata.append(entry['transfer'])
        single_maindata.append(entry['castration'])
        single_maindata.append(entry['zi'])

        single_maindata.append(entry['pastnum'])
        single_maindata.append(entry['rdate'])
        single_maindata.append(self_data['race'])
        single_maindata.append(self_data['place'])
        single_maindata.append(self_data['turf_dirt'])
        single_maindata.append(self_data['distance'])
        single_maindata.append(self_data['class'])
        single_maindata.append(self_data['horse_total'])
        single_maindata.append(self_data['horsenum'])
        single_maindata.append(self_data['odds'])
        single_maindata.append(self_data['span'])
        single_maindata.append(self_data['jockey_name'])
        single_maindata.append(self_data['jockey_weight'])
        single_maindata.append(self_data['course_condition'])
        single_maindata.append(self_data['course_mark'])
        single_maindata.append(self_data['rap3f'])
        single_maindata.append(self_data['rap5f'])
        single_maindata.append(self_data['diff3f'])
        single_maindata.append(entry['race_time'])
        single_maindata.append(entry['time_diff'])
        #single_maindata.append(div_dict['mean_diff'])
        #single_maindata.append(div_dict['mean_goal'])
        #single_maindata.append(div_dict['diviation'])
        #single_maindata.append(div_dict['sigma'])
        #single_maindata.append(div_dict['total'])
        single_maindata.append(self_data['passorder1'])
        single_maindata.append(self_data['passorder2'])
        single_maindata.append(self_data['passorder3'])
        single_maindata.append(self_data['passorder4'])
        single_maindata.append(self_data['horse_last3f'])
        single_maindata.append(self_data['race_last3f'])
        single_maindata.append(self_data['rpci'])
        single_maindata.append(self_data['pci'])
        single_maindata.append(self_data['triple_dividend'])
        single_maindata.append(self_data['castration'])
        single_maindata.append(self_data['level'])
        single_maindata.append(self_data['last3f_correct'])
        single_maindata.append(goal)
        single_maindata.append(today_time_diff)
        single_maindata.append(triple)
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
                main_dict["today_class"] = row[5]
                main_dict["today_horse_total"] = int(row[6])
                main_dict["today_course_condition"] = row[7]
                main_dict["today_course_mark"] = row[8]
                main_dict["today_horsenum"] = int(row[9])
                main_dict["horsename"] = row[10]
                main_dict["horse_sex"] = row[11]
                main_dict["horse_age"] = int(row[12])
                main_dict["today_odds"] = self.util.convert_not_float_to_zero(row[13])
                main_dict["today_span"] = self.util.convert_span_word(row[14])
                main_dict["today_jockey_name"] = row[15]
                main_dict["today_jockey_weight"] = self.util.convert_not_float_to_zero(row[16])
                main_dict["stallion"] = row[17]
                main_dict["broodmaresire"] = row[18]
                main_dict["trainer"] = row[19]
                main_dict["owner"] = row[20]
                main_dict["breeder"] = row[21]
                main_dict["color"] = row[22]
                main_dict["transfer"] = row[23]
                main_dict["castration"] = row[24]
                main_dict["today_zi"] = int(row[25])

                main_dict["pastnum"] = int(row[26])
                main_dict["past_rdate"] = datetime.datetime.strptime(row[27], '%Y-%m-%d')
                main_dict["past_race"] = int(row[28])
                main_dict["past_place"] = row[29]
                main_dict["past_turf_dirt"] = row[30]
                main_dict["past_distance"] = int(row[31])
                main_dict["past_class"] = row[32]
                main_dict["past_horse_total"] = int(row[33])
                main_dict["past_horsenum"] = int(row[34])
                main_dict["past_odds"] = float(row[35])
                main_dict["past_span"] = int(row[36])
                main_dict["past_jockey_name"] = row[37]
                main_dict["past_jockey_weight"] = float(row[38])
                main_dict["past_course_condition"] = row[39]
                main_dict["past_course_mark"] = row[40]
                main_dict["past_rap3f"] = float(row[41])
                main_dict["past_rap5f"] = float(row[42])
                main_dict["past_diff3f"] = float(row[43])
                main_dict["past_race_time"] = float(row[44])
                main_dict["past_time_diff"] = float(row[45])
                #if 0 diviation no longer use
                #analyse_avail_list = [0,0,0,0]
                #if float(row[52]) > 0:
                #    analyse_avail_list = [float(row[50]),float(row[51]),float(row[52]),float(row[53])]
                #main_dict["past_mean_diff"] = analyse_avail_list[0]
                #main_dict["past_mean_goal"] = analyse_avail_list[1]
                #main_dict["past_diviation"] = analyse_avail_list[2]
                #main_dict["past_sigma"] = analyse_avail_list[3]
                #main_dict["past_total"] = int(row[54])
                main_dict["past_passorder1"] = int(row[46])
                main_dict["past_passorder2"] = int(row[47])
                main_dict["past_passorder3"] = int(row[48])
                main_dict["past_passorder4"] = int(row[49])
                main_dict["past_horse_last3f"] = float(row[50])
                main_dict["past_race_last3f"] = float(row[51])
                main_dict["past_rpci"] = float(row[52])
                main_dict["past_pci"] = float(row[53])
                main_dict["past_triple_dividend"] = int(row[54])
                main_dict["past_castration"] = row[55]
                main_dict["past_level"] = int(row[56])
                main_dict["past_last3f_correct"] = float(row[57])
                try:
                    main_dict["today_goal"] = int(row[58])
                    main_dict["today_time_diff"] = float(row[59])
                    main_dict["today_triple_dividend"] = int(row[60])
                except ValueError:
                    main_dict["today_goal"] = 0
                    main_dict["today_time_diff"] = 0
                    main_dict["today_triple_dividend"] = 0
                main_dict_list.append(main_dict)
        return main_dict_list

