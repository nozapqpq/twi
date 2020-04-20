# coding: utf-8
import sql_pattern
import os
import csv
import parse
import numpy as np

class AnalyseResult():
    def __init__(self):
        self.pat = sql_pattern.SQLPattern()
        self.today_pred_target = []
        self.output_target_list = []
        self.output_target_date = ""

    def show_analyse_result(self, input_data):
        retlist = []
        retlist.append(self.analyse_pattern1(input_data,"福島","ダート"))
        retlist.append(self.analyse_pattern2(input_data,"福島","ダート"))
        retlist.append(self.analyse_pattern3(input_data,"福島","ダート"))
        retlist.append(self.analyse_pattern4(input_data,"福島","ダート"))
        retlist.append(self.analyse_pattern5(input_data,"福島","ダート"))
        retlist.append(self.analyse_pattern6(input_data,"福島","ダート"))
        retlist.append(self.analyse_pattern7(input_data,"福島","ダート"))
        retlist.append(self.analyse_pattern8(input_data,"福島","ダート"))
        retlist.append(self.analyse_pattern9(input_data,"福島","ダート"))
        retlist.append(self.analyse_pattern10(input_data,"福島","ダート"))
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
        retlist.append(self.analyse_pattern1(input_data,"福島","芝"))
        retlist.append(self.analyse_pattern2(input_data,"福島","芝"))
        retlist.append(self.analyse_pattern3(input_data,"福島","芝"))
        retlist.append(self.analyse_pattern4(input_data,"福島","芝"))
        retlist.append(self.analyse_pattern5(input_data,"福島","芝"))
        retlist.append(self.analyse_pattern6(input_data,"福島","芝"))
        retlist.append(self.analyse_pattern7(input_data,"福島","芝"))
        retlist.append(self.analyse_pattern8(input_data,"福島","芝"))
        retlist.append(self.analyse_pattern9(input_data,"福島","芝"))
        retlist.append(self.analyse_pattern10(input_data,"福島","芝"))
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
        dir_count = 0
        # フォルダ毎、main.csvを取得していく
        for dl in dir_list:
            rdate = self.get_rdate_from_dirname(dl)
            csv_list = self.get_maincsv_list_from_dir(dl)
            today_data = self.pat.get_sql_data("race_table.rdate='"+rdate+"'")
            baseinfo = self.get_baseinfo_from_distribution(dl)
            if dir_count == len(dir_list)-1:
                self.output_target_date = rdate
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
            dir_count = dir_count + 1
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
            if rate >= 35 and input_list["rdate"] == self.output_target_date:
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
        pattern_memo = "1着+2着が着外の2倍以上且つ実績10戦超"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if int(hd["result_total"]) > 10 and int(hd["result_1st"])+int(hd["result_2nd"]) >= int(hd["result_alsoran"])*2:
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
        pattern_memo = "ダート1600m,1800mで偏差値45以上で前半64s未満で上がり地点差0.5s以内で1勝以上の実績あり、40戦以上で着外率5割以上を除く"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if float(hd["div_score"]) >= 50 and hd["turf_dirt"] == "ダート" and (int(hd["distance"]) == 1600 or int(hd["distance"]) == 1800) and float(hd["rap5f"]) < 64 and float(hd["diff3f"]) <= 0.5 and int(hd["result_1st"]) > 0 and not (int(hd["result_total"]) > 40 and int(hd["result_alsoran"]) >= int(hd["result_total"])*0.5):
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,hd["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern5(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "データなし且つ偏差値55以上(10,11Rを除く)"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if int(hd["result_total"]) == 0 and float(hd["div_score"]) >= 55 and not (int(inp["race"]) == 10 or int(inp["race"]) == 11):
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,inp["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern6(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "ダート1400m以上で上がり地点差1.0s以内で勝ち数5以上、勝率1割以上、着外数70未満(10,11Rを除く)"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if hd["turf_dirt"] == "ダート" and float(hd["diff3f"]) <= 1.0 and int(hd["distance"]) >= 1400 and int(hd["result_1st"]) >= 5 and int(hd["result_1st"]) >= int(hd["result_total"])*0.1 and int(hd["result_alsoran"]) < 70 and int(hd["result_total"]) > 0 and not (int(inp["race"]) == 10 or int(inp["race"]) == 11):
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,hd["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern7(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "2勝以上で勝率8％以上(10R以降を除く)"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if int(hd["result_1st"]) >= 2 and int(hd["result_1st"]) >= int(hd["result_total"])*0.08 and int(inp["race"]) < 10:
                        if hd["goal_order"] == "":
                            self.high_expect_target_viewer(inp,retlist,pattern_memo)
                            break
                        else:
                            retlist = self.calc_goal_list(retlist,hd["goal_order"])
                            break
        return retlist+[place,turf_dirt,pattern_memo]

    def analyse_pattern8(self, input_data, place, turf_dirt):
        retlist = [0, 0, 0, 0, 0, 0]
        pattern_memo = "4戦以上で勝率5％以上かつ複勝率7割以上(不良馬場以外)"
        for inp in input_data+self.today_pred_target:
            if inp["today_place"] == place and inp["turf_dirt"] == turf_dirt:
                for hd in inp["horsedata"]:
                    if int(hd["result_total"]) >= 4 and int(hd["result_1st"]) >= int(hd["result_total"])*0.05 and int(hd["result_1st"])+int(hd["result_2nd"])+int(hd["result_3rd"]) >= int(hd["result_total"])*0.7 and not "不" in hd["course_condition"]:
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

    # deep learning "methods part"
    def affine(z, W, b):
        return np.dot(z, W) + b
    def affine_back(du, z, W, b):
        dz = np.dot(du, W.T)
        dW = np.dot(z.T, du)
        db = np.dot(np.ones(z.shape[0]).T, du)
        return dz, dW, db
    def relu(u):
        return np.maximum(0, u)
    def relu_back(dz, u):
        return dz * np.where(u > 0, 1, 0)
    def softmax(u):
        max_u = np.max(u, axis=1, keepdims=True)
        exp_u = np.exp(u-max_u)
        return exp_u/np.sum(exp_u, axis=1, keepdims=True)
    def cross_entropy_error(y, t):
        return -np.sum(t * np.log(np.maximum(y,1e-7)))/y.shape[0]
    def softmax_cross_entropy_error_back(y,t):
        return (y-t)/y.shape[0]
    def accuracy_rate(y, t):
        max_y = np.argmax(y, axis=1)
        max_t = np.argmax(t, axis=1)
        return np.sum(max_y == max_t)/y.shape[0]

    # deep learning "learn part"
    def learn(x, t, W1, b1, W2, b2, W3, b3, lr):
        u1 = affine(x, W1, b1)
        z1 = relu(u1)
        u2 = affine(z1, W2, b2)
        z2 = relu(u2)
        u3 = affine(z2, W3, b3)
        y = softmax(u3)

        dy = softmax_cross_entropy_error_back(y, t)
        dz2, dW3, db3 = affine_back(dy, z2, W3, b3)
        du2 = relu_back(dz2, u2)
        dz1, dW2, db2 = affine_back(du2, z1, W2, b2)
        du1 = relu_back(dz1, u1)
        dx, dW1, db1 = affine_back(du1, x, W1, b1)

        W1 = W1 - lr * dW1
        b1 = b1 - lr * db1
        W2 = W2 - lr * dW2
        b2 = b2 - lr * db2
        W3 = W3 - lr * dW3
        b3 = b3 - lr * db3

        return W1, b1, W2, b2, W3, b3

    def predict(x, W1, b1, W2, b2, W3, b3):
        u1 = affine(x, W1, b1)
        z1 = relu(u1)
        u2 = affine(z1, W2, b2)
        z2 = relu(u2)
        u3 = affine(z2, W3, b3)
        y = softmax(u3)
        return y

    def load(self):
        x_train = ""
        t_train = ""
        x_test = ""
        t_test = ""
        pat = sql_pattern.SQLPattern()
        pat.get_maindata_dict_from_csv("aaa.csv")
        return x_train, t_train, x_test, t_test

    # 画像解析仕様になっているので必要に応じて変える
    def deep_learning(self):
        x_train, t_train, x_test, t_test = load()

        nx_train = x_train/255
        nx_test = x_test/255

        d0 = nx_train.shape[1]
        d1 = 100 # 1層目のノード数
        d2 = 50  # 2層目のノード数
        d3 = 10

        np.random.seed(8)
        W1 = np.random.rand(d0, d1) * 0.2 - 0.1
        W2 = np.random.rand(d1, d2) * 0.2 - 0.1
        W3 = np.random.rand(d2, d3) * 0.2 - 0.1

        b1 = np.zeros(d1)
        b2 = np.zeros(d2)
        b3 = np.zeros(d3)

        lr = 0.5 # 学習率
        batch_size = 100 # バッチサイズ
        epoch = 50 # 学習回数

        # 予測(学習/テストデータ)
        y_train = predict(nx_train, W1, b1, W2, b2, W3, b3)
        y_test = predict(nx_test, W1, b1, W2, b2, W3, b3)

        # 正解率、誤差表示
        train_rate, train_err = accuracy_rate(y_train, t_train), cross_entropy_error(y_train, t_train)
        test_rate, test_err = accuracy_rate(y_test, t_test), cross_entropy_error(y_test, t_test)
        print("{0:3d} train_rate={1:6.2f}% test_rate={2:6.2f}% train_err={3:8.5f} test_err={4:8.5f}".format((0), train_rate*100, test_rate*100, train_err, test_err))

        for i in range(epoch):
            # 学習
            for j in range(0, nx_train.shape[0], batch_size):
                W1, b1, W2, b2, W3, b3 = learn(nx_train[j:j+batch_size], t_train[j:j+batch_size], W1, b1, W2, b2, W3, b3, lr)

            # 予測（学習データ）
            y_train = predict(nx_train, W1, b1, W2, b2, W3, b3)
            # 予測（テストデータ）
            y_test = predict(nx_test, W1, b1, W2, b2, W3, b3)
            # 正解率、誤差表示
            train_rate, train_err = accuracy_rate(y_train, t_train), cross_entropy_error(y_train, t_train)
            test_rate, test_err = accuracy_rate(y_test, t_test), cross_entropy_error(y_test, t_test)
            print("{0:3d} train_rate={1:6.2f}% test_rate={2:6.2f}% train_err={3:8.5f} test_err={4:8.5f}".format((i+1), train_rate*100, test_rate*100, train_err, test_err))

ar = AnalyseResult()
lst = ar.get_main_data_from_csv()
result = ar.show_analyse_result(lst)
#for r in result:
#    print(r)

