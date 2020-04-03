# coding: utf-8
import sql_pattern
import os
import csv
import parse

class AnalyseResult():
    def __init__(self):
        self.pat = sql_pattern.SQLPattern()
        self.today_pred_target = []
        self.output_target_list = []

    def show_analyse_result(self, input_data):
        retlist = []
        retlist.append(self.analyse_pattern1(input_data,"中京","ダート"))
        retlist.append(self.analyse_pattern2(input_data,"中京","ダート"))
        retlist.append(self.analyse_pattern3(input_data,"中京","ダート"))
        retlist.append(self.analyse_pattern4(input_data,"中京","ダート"))
        retlist.append(self.analyse_pattern5(input_data,"中京","ダート"))
        retlist.append(self.analyse_pattern6(input_data,"中京","ダート"))
        retlist.append(self.analyse_pattern7(input_data,"中京","ダート"))
        retlist.append(self.analyse_pattern8(input_data,"中京","ダート"))
        retlist.append(self.analyse_pattern9(input_data,"中京","ダート"))
        retlist.append(self.analyse_pattern10(input_data,"中京","ダート"))
        retlist.append(self.analyse_pattern1(input_data,"中山","ダート"))
        retlist.append(self.analyse_pattern2(input_data,"中山","ダート"))
        retlist.append(self.analyse_pattern3(input_data,"中山","ダート"))
        retlist.append(self.analyse_pattern4(input_data,"中山","ダート"))
        retlist.append(self.analyse_pattern5(input_data,"中山","ダート"))
        retlist.append(self.analyse_pattern6(input_data,"中山","ダート"))
        retlist.append(self.analyse_pattern7(input_data,"中山","ダート"))
        retlist.append(self.analyse_pattern8(input_data,"中山","ダート"))
        retlist.append(self.analyse_pattern9(input_data,"中山","ダート"))
        retlist.append(self.analyse_pattern10(input_data,"中山","ダート"))
        retlist.append(self.analyse_pattern1(input_data,"阪神","ダート"))
        retlist.append(self.analyse_pattern2(input_data,"阪神","ダート"))
        retlist.append(self.analyse_pattern3(input_data,"阪神","ダート"))
        retlist.append(self.analyse_pattern4(input_data,"阪神","ダート"))
        retlist.append(self.analyse_pattern5(input_data,"阪神","ダート"))
        retlist.append(self.analyse_pattern6(input_data,"阪神","ダート"))
        retlist.append(self.analyse_pattern7(input_data,"阪神","ダート"))
        retlist.append(self.analyse_pattern8(input_data,"阪神","ダート"))
        retlist.append(self.analyse_pattern9(input_data,"阪神","ダート"))
        retlist.append(self.analyse_pattern10(input_data,"阪神","ダート"))
        retlist.append(self.analyse_pattern1(input_data,"中京","芝"))
        retlist.append(self.analyse_pattern2(input_data,"中京","芝"))
        retlist.append(self.analyse_pattern3(input_data,"中京","芝"))
        retlist.append(self.analyse_pattern4(input_data,"中京","芝"))
        retlist.append(self.analyse_pattern5(input_data,"中京","芝"))
        retlist.append(self.analyse_pattern6(input_data,"中京","芝"))
        retlist.append(self.analyse_pattern7(input_data,"中京","芝"))
        retlist.append(self.analyse_pattern8(input_data,"中京","芝"))
        retlist.append(self.analyse_pattern9(input_data,"中京","芝"))
        retlist.append(self.analyse_pattern10(input_data,"中京","芝"))
        retlist.append(self.analyse_pattern1(input_data,"中山","芝"))
        retlist.append(self.analyse_pattern2(input_data,"中山","芝"))
        retlist.append(self.analyse_pattern3(input_data,"中山","芝"))
        retlist.append(self.analyse_pattern4(input_data,"中山","芝"))
        retlist.append(self.analyse_pattern5(input_data,"中山","芝"))
        retlist.append(self.analyse_pattern6(input_data,"中山","芝"))
        retlist.append(self.analyse_pattern7(input_data,"中山","芝"))
        retlist.append(self.analyse_pattern8(input_data,"中山","芝"))
        retlist.append(self.analyse_pattern9(input_data,"中山","芝"))
        retlist.append(self.analyse_pattern10(input_data,"中山","芝"))
        retlist.append(self.analyse_pattern1(input_data,"阪神","芝"))
        retlist.append(self.analyse_pattern2(input_data,"阪神","芝"))
        retlist.append(self.analyse_pattern3(input_data,"阪神","芝"))
        retlist.append(self.analyse_pattern4(input_data,"阪神","芝"))
        retlist.append(self.analyse_pattern5(input_data,"阪神","芝"))
        retlist.append(self.analyse_pattern6(input_data,"阪神","芝"))
        retlist.append(self.analyse_pattern7(input_data,"阪神","芝"))
        retlist.append(self.analyse_pattern8(input_data,"阪神","芝"))
        retlist.append(self.analyse_pattern9(input_data,"阪神","芝"))
        retlist.append(self.analyse_pattern10(input_data,"阪神","芝"))
        self.pat.write_list_to_csv("../analyse_result.csv",self.output_target_list)

        return retlist

    def get_main_data_from_csv(self):
        entry_horses_list = []
        all_files = os.listdir(path='..')
        # 名前が日付になっているフォルダを取得
        dir_list = [f for f in all_files if os.path.isdir(os.path.join('..',f)) and f[0].isdigit()]
        print(dir_list)
        # フォルダ毎、main.csvを取得していく
        for dl in dir_list:
            rdate = self.get_rdate_from_dirname(dl)
            csv_list = self.get_maincsv_list_from_dir(dl)
            today_data = self.pat.get_sql_data("race_table.rdate='"+rdate+"'")
            baseinfo = self.get_baseinfo_from_distribution(dl)
            count = 0
            for fl in csv_list:
                fn_parse = parse.parse("main_{place:D}{race:d}.csv",fl)
                main_lst = self.get_mainlist_from_csv("../"+dl+"/"+fl)
                horsename = ""
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
                            if single_horse_dict["horsedata"][0]["goal_order"] == "":
                                self.today_pred_target.append(single_horse_dict)
                            else:
                                entry_horses_list.append(single_horse_dict)
                        single_horse_dict = {"rdate":rdate,"today_place":self.pat.convert_place_to_kanji(fn_parse["place"]),"race":str(fn_parse["race"]),"horsename":single_dict["horsename"],"horsedata":""}
                        self_data = ()
                        for today in today_data:
                            if today["place"] == single_horse_dict["today_place"]:
                                if str(today["race"]) == single_horse_dict["race"]:
                                    if today["horsename"] == single_horse_dict["horsename"]:
                                        self_data = today
                                        break
                        odds_order = 100
                        turf_dirt = baseinfo[count]["turf_dirt"]
                        if len(self_data) > 0:
                            odds_order = self_data["odds_order"]
                            turf_dirt = self_data["turf_dirt"]
                        single_horse_dict["turf_dirt"] = turf_dirt 
                        single_horse_dict["odds_order"] = odds_order
                        single_horse_dict["goal_order"] = single_dict["goal_order"]
                        print(single_horse_dict)
                    if single_horse_dict["horsedata"] == "":
                        single_horse_dict["horsedata"] = [single_dict]
                    else:
                        single_horse_dict["horsedata"].append(single_dict)
                    horsename = single_dict["horsename"]
                if single_horse_dict != {}:
                    if single_horse_dict["horsedata"][0]["goal_order"] == "":
                        self.today_pred_target.append(single_horse_dict)
                    else:
                        entry_horses_list.append(single_horse_dict)
                count = count + 1
        return entry_horses_list


    def get_rdate_from_dirname(self, dirname):
        yyyymmdd = "20"+dirname[0:2]+"-"+dirname[2:4]+"-"+dirname[4:6]
        return yyyymmdd

    def get_maincsv_list_from_dir(self, dirname):
        pathname = "../"+dirname
        all_files = os.listdir(path=pathname)
        file_list = [f for f in all_files if "main_" in f]
        return file_list

    def get_baseinfo_from_distribution(self, dirname):
        retlist = []
        pathname = "../"+dirname
        all_files = os.listdir(path=pathname)
        file_list = [f for f in all_files if "distribution_map_" in f]
        for f in file_list:
            fn_parse = parse.parse("distribution_map_{place:D}{race:d}.csv",f)
            lst = self.get_mainlist_from_csv("../"+dirname+"/"+f)
            dic = {"today_place":lst[0][1],"turf_dirt":lst[0][2],"distance":lst[0][3]}
            retlist.append(dic)
        return retlist



    def get_mainlist_from_csv(self, filename):
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

    def calc_goal_list(self, inplist, goal):
        retlist = [0, 0, 0, 0, 0, 0]
        if int(goal) >= 1 and int(goal) <= 5:
            retlist[int(goal)-1] = retlist[int(goal)-1] + 1
        elif int(goal) > 5:
            retlist[5] = retlist[5] + 1
        retlist = [x+y for (x,y) in zip(inplist,retlist)]
        return retlist

    def high_expect_target_viewer(self, input_list, distribution, memo):
        within = sum(distribution[0:3])
        total = sum(distribution)
        if total > 0: # 最終的には70%以上のデータのみを表示していきたい
            rate = round(within/total*100,2)
            if rate > 35:
                self.output_target_list.append([input_list["today_place"],input_list["race"],input_list["horsename"],str(rate),str(total),memo])
                print(input_list["today_place"]+str(input_list["race"])+": "+str(input_list["horsename"])+" "+str(rate)+"% / "+str(total)+" ("+memo+")")

    def analyse_pattern1(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "1~3番人気でデータが少ない"
        for inp in input_data+self.today_pred_target:
            flg = 0
            goal = "0"
            if int(inp["odds_order"]) >= 1 and int(inp["odds_order"]) <= 3 and inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                if inp["horsedata"][0]["goal_order"] == "":
                    self.high_expect_target_viewer(inp,retlist,pattern_memo)
                else:
                    for hd in inp["horsedata"]:
                        if int(hd["result_total"]) <= 3:
                            flg = flg + 1
                            goal = hd["goal_order"]
                    if len(inp["horsedata"]) == flg:
                        retlist = self.calc_goal_list(retlist,goal)
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern2(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "1着+2着が着外の2倍以上且つ実績15戦以上"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if int(hd["result_total"]) >= 15 and int(hd["result_1st"])+int(hd["result_2nd"]) >= int(hd["result_alsoran"])*2:
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,hd["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern3(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "2戦以上で連対率100％"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if int(hd["result_total"]) >= 2 and int(hd["result_3rd"]) == 0 and int(hd["result_4th"]) == 0 and int(hd["result_5th"]) == 0 and int(hd["result_alsoran"]) == 0:
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,hd["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern4(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "ダート1800mで前半62s以内で上がり地点差0.3s以内で偏差値55以上"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if float(hd["div_score"]) >= 55 and hd["turf_dirt"] == "ダート" and int(hd["distance"]) >= 1800 and float(hd["rap5f"]) >= 62 and float(hd["diff3f"]) <= 0.3:
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,hd["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern5(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "データなし且つ偏差値65以上"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if int(hd["result_total"]) == 0 and float(hd["div_score"]) >= 65:
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,inp["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern6(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "ダートで上がり地点差0.4s以内で勝率3.5割以上"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if hd["turf_dirt"] == "ダート" and float(hd["diff3f"]) <= 0.4 and int(hd["result_1st"]) >= int(hd["result_total"])*0.35 and int(hd["result_total"]) > 0:
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,hd["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern7(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "5戦以上で勝率5割以上"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if int(hd["result_total"]) >= 5 and int(hd["result_1st"]) >= int(hd["result_total"])*0.5:
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,hd["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern8(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "別場で勝率4割以上"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if int(hd["result_total"]) > 0 and hd["place"] != inp["today_place"] and int(hd["result_1st"]) >= int(hd["result_total"])*0.4:
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,hd["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern9(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "6R以前で上がり地点差0.3s以内でデータなしで偏差値55以上"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if int(hd["result_total"]) == 0 and int(inp["race"]) <= 6 and float(hd["diff3f"]) <= 0.3 and float(hd["div_score"]) >= 55:
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,hd["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern10(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "5戦以上で連対率5割以上"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if int(hd["result_total"]) >= 5 and int(hd["result_1st"])+int(hd["result_2nd"]) >= int(hd["result_total"])*0.5:
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,hd["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

ar = AnalyseResult()
lst = ar.get_main_data_from_csv()

result = ar.show_analyse_result(lst)
#for r in result:
#    print(r)

