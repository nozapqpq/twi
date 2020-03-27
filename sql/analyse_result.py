# coding: utf-8
import sql_pattern
import os
import csv
import parse

class AnalyseResult():
    def __init__(self):
        self.pat = sql_pattern.SQLPattern()
    def get_main_data_from_csv(self):
        all_files = os.listdir(path='..')
        # 名前が日付になっているフォルダを取得
        dir_list = [f for f in all_files if os.path.isdir(os.path.join('..',f)) and f[0].isdigit()]
        print(dir_list)
        # フォルダ毎、main.csvを取得していく
        for dl in dir_list:
            rdate = self.get_rdate_from_dirname(dl)
            csv_list = self.get_maincsv_list_from_dir(dl)
            
            for fl in csv_list:
                fn_parse = parse.parse("main_{place:D}{race:d}.csv",fl)
                main_lst = self.get_maindata_from_csv("../"+dl+"/"+fl)
                horsename = ""
                entry_horses_list = []
                single_horse_dict = {}
                for ml in main_lst:
                    single_dict = {}
                    single_dict["horsename"] = ml[0]
                    single_dict["place"] = ml[1]
                    single_dict["turf_dirt"] = ml[2]
                    single_dict["course_condition"] = ml[3]
                    single_dict["distance"] = ml[4]
                    single_dict["goal_order"] = ml[5]
                    single_dict["rap3f"] = ml[6]
                    single_dict["rap5f"] = ml[7]
                    single_dict["passorder3"] = ml[8]
                    single_dict["passorder4"] = ml[9]
                    single_dict["div_score"] = self.convert_nondigit_to_strzero(ml[10])
                    single_dict["diff3f"] = ml[11]
                    single_dict["last3f"] = ml[12]
                    single_dict["class"] = ml[13]
                    single_dict["low_1sigma"] = self.convert_nondigit_to_strzero(ml[14])
                    single_dict["high_1sigma"] = self.convert_nondigit_to_strzero(ml[15])
                    single_dict["sigma"] = self.convert_nondigit_to_strzero(ml[16])
                    single_dict["result_1st"] = ml[17]
                    single_dict["result_2nd"] = ml[18]
                    single_dict["result_3rd"] = ml[19]
                    single_dict["result_4th"] = ml[20]
                    single_dict["result_5th"] = ml[21]
                    single_dict["result_alsoran"] = ml[22]
                    single_dict["result_total"] = str(int(ml[17])+int(ml[18])+int(ml[19])+int(ml[20])+int(ml[21])+int(ml[22]))
                    if horsename == "" or horsename != single_dict["horsename"]:
                        if horsename != "":
                            entry_horses_list.append(single_horse_dict)
                        single_horse_dict = {"rdate":rdate,"today_place":self.pat.convert_place_to_kanji(fn_parse["place"]),"race":fn_parse["race"],"horsename":single_dict["horsename"],"horsedata":""}
                    if single_horse_dict["horsedata"] == "":
                        entry_horses_list.append(single_horse_dict)
                        single_horse_dict["horsedata"] = [single_dict]
                    else:
                        single_horse_dict["horsedata"].append(single_dict)
                    horsename = single_dict["horsename"]
                entry_horses_list.append(single_horse_dict)
        print(entry_horses_list[0])
        return entry_horses_list


    def get_rdate_from_dirname(self, dirname):
        yyyymmdd = "20"+dirname[0:2]+"-"+dirname[2:4]+"-"+dirname[4:6]
        return yyyymmdd

    def get_maincsv_list_from_dir(self, dirname):
        pathname = "../"+dirname
        all_files = os.listdir(path=pathname)
        file_list = [f for f in all_files if "main_" in f]
        return file_list

    def get_maindata_from_csv(self, filename):
        with open(filename,'r') as f:
            retlist = []
            reader = csv.reader(f)
            count = 0
            for row in reader:
                if count != 0:
                    retlist.append(row)
                count = count + 1
        return retlist

    def convert_nondigit_to_strzero(self, target):
        if not target.isdecimal():
            try:
                float(target)
                return target
            except ValueError:
                return "0"
        else:
            return target

#pat = sql_pattern.SQLPattern()
#self_data = pat.get_self_data(ent)
ar = AnalyseResult()
lst = ar.get_main_data_from_csv()
#lst = ar.get_main_data_from_csv()
#pat.write_list_to_csv('../sample.csv',lst)

