# coding: utf-8
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import sql_manipulator
import csv
import re
import seaborn as sns

class Utility():
    def __init__(self):
        self.place_kanji = ["札幌","函館","福島","新潟","中山","東京","中京","京都","阪神","小倉"]
        self.place_alpha = ["sapporo","hakodate","fukushima","niigata","nakayama","tokyo","chukyo","kyoto","hanshin","kokura"]
        self.cond_list = ["良","稍","重","不"]
        self.td_list = ["芝","ダート"]
        self.distance_list = [1000,1150,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,3000,3200,3600]

    ## csv input/output
    def write_list_to_csv(self,filename,target):
        with open(filename,'w') as f:
            writer = csv.writer(f)
            writer.writerow(["a","b","c"])
            for a in target:
                writer.writerow(a)
    def write_list_to_csv_nest(self,filename,target):
        with open(filename,'w') as f:
            writer = csv.writer(f)
            writer.writerow(["a","b","c"])
            for a in target:
                for b in a:
                    writer.writerow(b)

    ## SQL data
    def get_sql_data(self, condition_msg):
        manipulator = sql_manipulator.SQLManipulator()
        msg_select = "select race_table.rdate,race_table.place,race_table.race,class,turf_dirt,distance,course_condition,rap3f,rap5f,race_table.last3f,race_table.horse_total,race_table.rpci,race_table.dividend,race_table.course_mark,race_table.early_rap2,race_table.early_rap3,race_table.early_rap4,race_table.last_rap1,race_table.last_rap2,race_table.last_rap3,race_table.last_rap4,goal_order,brinker,horsenum,horsename,horse_sex,age,jockey_weight,jockey_name,race_time,time_diff,passorder1,passorder2,passorder3,passorder4,finish,horse_table.last3f,diff3f,odds_order,odds,horseweight,weightdiff,trainer,carrier,owner,breeder,stallion,broodmaresire,color,span,castration,pci "
        msg_from = "from horse_table "
        msg_join = "inner join race_table on horse_table.rdate = race_table.rdate and horse_table.place = race_table.place and horse_table.race = race_table.race "
        msg = msg_select+msg_from+msg_join+"where race_time != 0 and "+condition_msg+";"
        tpl = manipulator.sql_manipulator(msg)
        retlist = []
        for t in tpl:
            single_dict = {"rdate":t[0],"place":t[1],"race":t[2],"class":t[3],"turf_dirt":t[4],"distance":t[5],"course_condition":t[6],"rap3f":t[7],"rap5f":t[8],"race_last3f":t[9],"horse_total":t[10],"rpci":t[11],"dividend":t[12],"course_mark":t[13],"early_rap2":t[14],"early_rap3":t[15],"early_rap4":t[16],"last_rap1":t[17],"last_rap2":t[18],"last_rap3":t[19],"last_rap4":t[20],"goal_order":t[21],"brinker":t[22],"horsenum":t[23],"horsename":t[24],"horse_sex":t[25],"age":t[26],"jockey_weight":t[27],"jockey_name":t[28],"race_time":t[29],"time_diff":t[30],"passorder1":t[31],"passorder2":t[32],"passorder3":t[33],"passorder4":t[34],"finish":t[35],"horse_last3f":t[36],"diff3f":t[37],"odds_order":t[38],"odds":t[39],"horseweight":t[40],"weightdiff":t[41],"trainer":t[42],"carrier":t[43],"owner":t[44],"breeder":t[45],"stallion":t[46],"broodmaresire":t[47],"color":t[48],"span":t[49],"castration":t[50],"pci":t[51]}
            retlist.append(single_dict)
        return retlist
    def set_race_level(self):
        hoge = 3
        for a in range(len(self.place_kanji)):
            for b in range(len(self.cond_list)):
                for c in range(len(self.td_list)):
                    for d in range(len(self.distance_list)):
                        msg_pattern = ["rap3f","last3f"]
                        if distance[d] >= 1600:
                            msg_pattern = ["rap5f","last3f"]
                        output_pattern = []
                        manipulator = sql_manipulator.SQLManipulator()
                        where_msg = "where place='"+self.place_kanji[a]+"' and course_condition='"+self.cond_list[b]+"' and turf_dirt='"+self.td_list[c]+"' and distance="+str(self.distance_list[d])
                        print(where_msg)
                        for mp in msg_pattern:
                            msg = "select "+mp+" from race_table " + where_msg
                            output_pattern.append(manipulator.sql_manipulator(msg+";"))
                        if len(output_pattern[0]) == 0:
                            continue
                        standard_time = (min(output_pattern[0])[0]+max(output_pattern[0])[0]+min(output_pattern[1])[0]+max(output_pattern[1])[0])/2
                        level_pattern = []
                        for i in range(11):
                            level_pattern.append(round(standard_time-2.5+i*0.5,1))
                        for i in range(10):
                            time_cond1 = " and "+msg_pattern[0]+"+last3f > "+str(level_pattern[i])
                            time_cond2 = " and "+msg_pattern[0]+"+last3f <= "+str(level_pattern[i+1])
                            if i == 0:
                                time_cond1 = ""
                            elif i == 9:
                                time_cond2 = ""
                            #msg2 = "select class from race_table " + where_msg + time_cond1 + time_cond2 + ";"
                            msg2 = "update race_table set level="+str(10-i)+ " "+where_msg + time_cond1 + time_cond2
                            set_level = manipulator.sql_manipulator(msg2+";")
    def set_race_last3f_correction(self):
        pattern_list = [] # 各コース情報
        date_list = [] # 日付リスト
        manipulator = sql_manipulator.SQLManipulator()
        pattern_msg = "select distinct place,turf_dirt,course_condition,distance,class from race_table;"
        date_msg = "select distinct rdate from race_table order by rdate ASC;"
        for tpl in manipulator.sql_manipulator(date_msg):
            date_list.append(str(tpl[0]).replace('-','/'))
        for tpl in manipulator.sql_manipulator(pattern_msg):
            single_dic = {"place":tpl[0],"turf_dirt":tpl[1],"course_condition":tpl[2],"distance":tpl[3],"class":tpl[4],"average":None,"sigma":None,"size":None}
            pattern_list.append(single_dic)
        count = 0
        for lst in pattern_list:
            if lst["distance"] > 2200:
                lst["average"] = 0
                lst["sigma"] = 0 
                lst["size"] = 0
            else:
                msg = "select rap5f,last3f from race_table where place='"+lst["place"]+"' and turf_dirt='"+lst["turf_dirt"]+"' and course_condition='"+lst["course_condition"]+"' and distance="+str(lst["distance"])+" and class='"+lst["class"]+"';"
                races = manipulator.sql_manipulator(msg)
                if len(races) < 15:
                    pattern_list[count]["average"] = 0
                    pattern_list[count]["sigma"] = 0
                    pattern_list[count]["size"] = len(races)
                else:
                    average = 0
                    sigma = 0
                    time_list = []
                    for single in races:
                        single_dict = {"rap5f":single[0],"last3f":single[1]}
                        average = average + single_dict["rap5f"] + single_dict["last3f"]
                        time_list.append(single_dict["rap5f"]+single_dict["last3f"])
                    average = round(average / len(races),1)
                    for tl in time_list:
                        sigma = sigma + pow(tl-average,2)
                    sigma = round(pow(sigma/len(races),0.5),3)
                    pattern_list[count]["average"] = average
                    pattern_list[count]["sigma"] = sigma
                    pattern_list[count]["size"] = len(races)
                    print(pattern_list[count])
            count = count + 1
        for dt in date_list:
            single_date_msg = "select * from race_table where rdate='"+dt+"';"
            single_date_list = manipulator.sql_manipulator(single_date_msg)
            count_dict = {"turf_plus":0,"turf_minus":0,"dirt_plus":0,"dirt_minus":0}
            single_date_list_detail = []
            for sd in single_date_list:
                single_dict = {"rdate":sd[0],"place":sd[1],"race":sd[2],"class":sd[3],"turf_dirt":sd[4],"distance":sd[5],"course_condition":sd[6],"rap5f":sd[8],"last3f":sd[9],"diff":0,"average":0}
                for pl in pattern_list:
                    flg_place = single_dict["place"] == pl["place"]
                    flg_td = single_dict["turf_dirt"] == pl["turf_dirt"]
                    flg_cond = single_dict["course_condition"] == pl["course_condition"]
                    flg_dist = single_dict["distance"] == pl["distance"]
                    flg_cls = single_dict["class"] == pl["class"]
                    if flg_place and flg_td and flg_cond and flg_dist and flg_cls and pl["average"] != 0:
                        if single_dict["rap5f"]+single_dict["last3f"] > pl["average"]:
                            if single_dict["turf_dirt"] == "芝":
                                count_dict["turf_plus"] = count_dict["turf_plus"] + 1
                            elif single_dict["turf_dirt"] == "ダート":
                                count_dict["dirt_plus"] = count_dict["dirt_plus"] + 1
                        else:
                            if single_dict["turf_dirt"] == "芝":
                                count_dict["turf_minus"] = count_dict["turf_minus"] + 1
                            elif single_dict["turf_dirt"] == "ダート":
                                count_dict["dirt_minus"] = count_dict["dirt_minus"] + 1
                        single_dict["average"] = pl["average"]
                        single_dict["diff"] = round(single_dict["rap5f"]+single_dict["last3f"]-pl["average"],2)
                        break
                single_date_list_detail.append(single_dict)
            turf_time_correct = 0
            dirt_time_correct = 0
            turf_plus_flg = count_dict["turf_plus"] > count_dict["turf_minus"]*1.5
            turf_minus_flg = count_dict["turf_minus"] > count_dict["turf_plus"]*1.5
            dirt_plus_flg = count_dict["dirt_plus"] > count_dict["dirt_minus"]*1.5
            dirt_minus_flg = count_dict["dirt_minus"] > count_dict["dirt_plus"]*1.5
            for sd in single_date_list_detail:
                if sd["turf_dirt"] == "芝":
                    if turf_plus_flg and sd["diff"] > 0:
                        turf_time_correct = turf_time_correct + sd["diff"]/count_dict["turf_plus"]
                    elif turf_minus_flg and sd["diff"] <= 0:
                        turf_time_correct = turf_time_correct + sd["diff"]/count_dict["turf_minus"]
                elif sd["turf_dirt"] == "ダート":
                    if dirt_plus_flg and sd["diff"] > 0:
                        dirt_time_correct = dirt_time_correct + sd["diff"]/count_dict["dirt_plus"]
                    if dirt_minus_flg and sd["diff"] <= 0:
                        dirt_time_correct = dirt_time_correct + sd["diff"]/count_dict["dirt_minus"]
            for sd in single_date_list_detail:
                msg = ""
                if sd["distance"] > 2200:
                    msg = "UPDATE race_table SET last3f_correct=0 where rdate='"+str(sd["rdate"].strftime('%Y/%m/%d'))+"' and race="+str(sd["race"])+" and place='"+sd["place"]+"';"
                elif sd["turf_dirt"] == "芝":
                    msg = "UPDATE race_table SET last3f_correct="+str(round(turf_time_correct,1))+" where rdate='"+str(sd["rdate"].strftime('%Y/%m/%d'))+"' and race="+str(sd["race"])+" and place='"+sd["place"]+"';"
                elif sd["turf_dirt"] == "ダート":
                    msg = "UPDATE race_table SET last3f_correct="+str(round(dirt_time_correct,1))+" where rdate='"+str(sd["rdate"].strftime('%Y/%m/%d'))+"' and race="+str(sd["race"])+" and place='"+sd["place"]+"';"
                if msg != "":
                    print(msg)
                    manipulator.sql_manipulator(msg)

    ## make list
    def make_timediff_accumulation_list(self,allsub,allentry,race_count):
        retlist = []
        race_range_list = ["~58.0","~60.0","~62.0","~64.0","~66.0","66.1~"]
        class_list = ["新馬","未勝利","500万","1000万","1600万","1勝","2勝","3勝","その他"]
        for i in range(len(allsub)):
            diff_list = [[0] * 31 for i in range(len(race_range_list)*len(class_list))]
            temp_list = [allentry[race_count][i]['horsename'],allentry[race_count][i]['place'],allentry[race_count][i]['turf_dirt'],allentry[race_count][i]['distance']]
            for sd in allsub[i]:
                idx = self.get_accumulation_list_index(race_range_list,class_list,sd['rap5f'],sd['class'])
                if sd['time_diff'] >= 3.0:
                    diff_list[idx][len(diff_list[idx])-1] = diff_list[idx][len(diff_list[idx])-1] + 1
                else:
                    diff_list[idx][int(sd['time_diff']*10)] = diff_list[idx][int(sd['time_diff']*10)] +1
            dl_count = 0
            for dl in diff_list: # accumulate
                for i_d in range(len(dl)):
                    if i_d > 0:
                        dl[i_d] = dl[i_d] + dl[i_d-1]
                if dl[len(dl)-1] >= 10:
                    for i_d in range(len(dl)):
                        dl[i_d] = dl[i_d]/dl[len(dl)-1]*10
                if dl[len(dl)-1] > 0:
                    retlist.append(temp_list+[race_range_list[int(dl_count%len(race_range_list))],class_list[int(dl_count/(len(class_list)-1))]]+dl)
                dl_count = dl_count + 1
        return retlist
    # ディープラーニング学習データの出力をフラグに従って変更(一括/芝ダート分け/場所分け)
    def make_usedlset_dictlist(self, place_list, all_place_flg, all_td_flg):
        dict_list = []
        if all_place_flg:
            place_list = ["all"]
        for pl in place_list:
            if all_td_flg:
                dict_list.append({"place":pl,"turf_dirt":"all"})
            else:
                dict_list.append({"place":pl,"turf_dirt":"芝"})
                dict_list.append({"place":pl,"turf_dirt":"ダート"})
        return dict_list
    def get_accumulation_list_index(self,l_5f,l_class,t5f,cls):
        t5f_num = 0
        cls_num = len(l_class)-1
        if t5f <= 58.0:
            t5f_num = 0
        elif t5f <= 60.0:
            t5f_num = 1
        elif t5f <= 62.0:
            t5f_num = 2
        elif t5f <= 64.0:
            t5f_num = 3
        elif t5f <= 66.0:
            t5f_num = 4
        else:
            t5f_num = 5
        for c in range(len(l_class)-1):
            if cls in l_class[c]:
                cls_num = c
                break
        return int(t5f_num+(cls_num*len(l_5f)))
    def get_target_goal_order_list(self,target,sub):
        retlist = [0] * 6
        if len(target) == 0:
            return retlist
        for s in sub:
            if s['class'] in target['class_condition']:
                for i in range(5):
                    if s['goal_order'] == i+1:
                        retlist[i] = retlist[i] + 1
                if s['goal_order'] > 5:
                    retlist[5] = retlist[5]+1
        return retlist
    def get_finish_trend_list(self, record):
        fin = self.get_finish_trend(record)
        return ["逃"+str(fin[0]),"先"+str(fin[1]),"中"+str(fin[2]),"差"+str(fin[3]),"後"+str(fin[4]),"追"+str(fin[5]),"マクリ"+str(fin[6])]

    ## make parameter
    def get_diviation_value(self,entry,self_data):
        #if len(self_data) == 0:
        return {"diviation":0,"sigma":0,"total":0,"mean_value":0,"mean_diff":0,"mean_level":0,"mean_goal":0,"diff3f":0,"horse_last3f":0,"class":''}
        class_dict = {"lv1":"未勝利' or class='新馬","lv2":"500万' or class='1勝","lv3":"1000万' or class='2勝","lv4":"1600万' or class='3勝' or class='オープン' or class='OP(L)' or class='Ｇ３' or class='Ｇ２' or class='Ｇ１"}
        ret_dict = {}
        lv = "lv4"
        if self_data['class'] == "未勝利" or self_data['class'] == "新馬":
            lv = "lv1"
        elif self_data['class'] == "500万" or self_data['class'] == "1勝":
            lv = "lv2"
        elif self_data['class'] == "1000万" or self_data['class'] == "2勝":
            lv = "lv3"
        target = "rap3f"
        if int(entry['distance']) > 1500:
            target = "rap5f"
        target_time = self_data[target]
        cond = self.convert_condition(entry['course_condition'])
        msg = "race_table.place='"+entry['place']+"' and turf_dirt='"+entry['turf_dirt']+"' and distance="+str(entry['distance'])+" and (race_table.course_condition='"+cond+"') and diff3f>="+str(self_data['diff3f']-0.1)+" and diff3f<="+str(self_data['diff3f']+0.1)+" and "+target+">="+str(target_time-0.3)+" and "+target+"<="+str(target_time+0.3)+" and (class='"+class_dict[lv]+"')"
        sim_pos = self.get_sql_data(msg)
        if len(sim_pos) < 30:
            ret_dict = {"diviation":0,"sigma":"-","total":len(sim_pos),"mean_value":"-","mean_diff":"-","mean_level":"-","mean_goal":"-","diff3f":self_data['diff3f'],"horse_last3f":self_data['horse_last3f'],"class":self_data['class']}
        else:
            mean_value = 0
            mean_diff = 0
            mean_level = 0
            mean_goal = 0
            target_str = 'horse_last3f'
            for sp in sim_pos:
                mean_value = mean_value+sp[target_str]
                #mean_value = mean_value+(sp['horse_last3f']-sp['race_last3f'])
                mean_diff = mean_diff+sp['time_diff']
                #mean_level = mean_level+sp['level']
                if sp['goal_order'] > 0:
                    mean_goal = mean_goal+sp['goal_order']
            mean_value = round(mean_value/len(sim_pos),3)
            mean_diff = round(mean_diff/len(sim_pos),3)
            mean_level = round(mean_level/len(sim_pos),3)
            mean_goal = round(mean_goal/len(sim_pos),3)
            sigma = 0
            for sp in sim_pos:
                sigma = sigma + (sp[target_str]-mean_value)**2
                #sigma = sigma + ((sp['horse_last3f']-sp['race_last3f'])-mean_value)**2
            sigma = round(sigma/len(sim_pos),3)
            diviation = round(-(self_data[target_str]-mean_value)/sigma*10+50,3)
            #diviation = -((self_data['horse_last3f']-self_data['race_last3f'])-mean_value)/sigma*10+50
            ret_dict = {"diviation":diviation,"sigma":sigma,"total":len(sim_pos),"mean_value":mean_value,"mean_diff":mean_diff,"mean_level":mean_level,"mean_goal":mean_goal,"diff3f":self_data['diff3f'],"horse_last3f":self_data['horse_last3f'],"class":self_data['class']}
        return ret_dict
    def get_finish_trend(self, record):
        finish_list = []
        for r in record:
            finish_list.append(r['finish'])
        retval = [finish_list.count('逃げ'),finish_list.count('先行'),finish_list.count('中団'),finish_list.count('差し'),finish_list.count('後方'),finish_list.count('追込'),finish_list.count('マクリ')]
        return retval

    # count_dict={"total","1st","2nd","3rd"}の形式で引数に与えること
    def get_quinella_rate(self, count_dict):
        quinella = count_dict["1st"] + count_dict["2nd"]
        win_rate = round(quinella/count_dict["total"],3)
        return win_rate
    def get_double_win_rate(self, count_dict):
        double_win = count_dict["1st"] + count_dict["2nd"] + count_dict["3rd"]
        double_win_rate = round(double_win/count_dict["total"],3)
        return double_win_rate
    def analyse_class(self, cls):
        if cls=="500万" or cls=="1勝":
            return "500万' or class='1勝' or class='1000万"
        elif cls=="未勝利" or cls=="新馬":
            return "未勝利' or class='500万"
        elif cls=="1000万" or cls=="2勝":
            return "1000万' or class='2勝' or class='500万"
        else:
            return "500万' or class='1000万' or class='2勝' or class='1600万' or class='3勝' or class='オープン' or class='Ｇ３' or class='Ｇ１' or class='Ｇ２"
    def convert_turf_dirt(self, s):
        if s=="T":
            return "芝"
        elif s=="D":
            return "ダート"
        else:
            return "その他"
    def convert_condition(self, s):
        if s=="良" or s=="稍":
            return "良' or course_condition='稍"
        else:
            return "重' or course_condition='不"
    def convert_race_time(self, s):
        if (len(s) == 3 or len(s) == 4) and s != "----":
            return round((int(int(s)/1000)*600+int(s[-3:]))*0.1,1)
        else:
            return "0.0"
    def convert_place_to_alpha(self, place):
        place_kanji = ["札幌","函館","福島","新潟","中山","東京","中京","京都","阪神","小倉"]
        place_alpha = ["sapporo","hakodate","fukushima","niigata","nakayama","tokyo","chukyo","kyoto","hanshin","kokura"]
        for p in range(len(self.place_kanji)):
            if place == self.place_kanji[p]:
                return self.place_alpha[p]
        return "unknown"
    def convert_place_to_kanji(self, place):
        for p in range(len(self.place_kanji)):
            if place == self.place_alpha[p]:
                return self.place_kanji[p]
        return "unknown"
    def convert_span_word(self, span):
        if "連" in span:
            return 1
        try:
            return int(span)
        except ValueError:
            print("span : ValueError")
            return 0
    def convert_not_int_to_zero(self, num):
        try:
            return int(num)
        except ValueError:
            return 0
    def convert_not_float_to_zero(self, num):
        try:
            return float(num)
        except ValueError:
            return 0
    def convert_date_format(self, dt):
        # target format 0000.0.0 -> 0000-00-00
        lst = re.findall("\d+",dt)
        ret = lst[0].zfill(4)+"-"+lst[1].zfill(2)+"-"+lst[2].zfill(2)
        return ret
    def remove_pm_space(self, pm):
        return pm.replace(" ","")

    ## parameter check
    def check_level_range(self,level_idx,level):
        if level == None:
            if level_idx == 0:
                return True
            else:
                return False
        if level_idx == 0 and (level >= 1 and level <= 3):
            return True
        elif level_idx == 1 and (level >= 4 and level <= 6):
            return True
        elif level_idx == 2 and (level >= 7 and level <= 10):
            return True
        elif level_idx == 3:
            return True
        return False

    # matplotでaccuracyとlossをプロットして出力
    def compare_TV(self, history):
        # Setting Parameters
        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        epochs = range(len(acc))

        # 1) Accracy Plt
        plt.plot(epochs, acc, 'bo' ,label = 'training acc')
        plt.plot(epochs, val_acc, 'b' , label= 'validation acc')
        plt.title('Training and Validation acc')
        plt.legend()
        plt.figure()

        # 2) Loss Plt
        plt.plot(epochs, loss, 'bo' ,label = 'training loss')
        plt.plot(epochs, val_loss, 'b' , label= 'validation loss')
        plt.title('Training and Validation loss')
        plt.legend()

        plt.show()
    # 正答と予測のconfusion_matrixをプロットして出力
    def plot_confusion_matrix(self, labels, predictions, p):
        matrix_y = np.array([x[0] for x in labels])
        matrix_pred = np.array([x[0] for x in predictions])
        cm = confusion_matrix(matrix_y, matrix_pred > p)
        plt.figure(figsize=(5,5))
        sns.heatmap(cm, annot=True, fmt="d")
        plt.title('Confusion matrix @{:.2f}'.format(p))
        plt.ylabel('Actual label')
        plt.xlabel('Predicted label')
        plt.show()
