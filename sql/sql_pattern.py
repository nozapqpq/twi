# coding: utf-8
import sql_manipulator
import sql_jockey
import csv
import datetime

class SQLPattern():
    def __init__(self, option=""):
        self.maindata = []
        self.subdata = []
        self.distribution = []
        self.place_kanji = ["札幌","函館","福島","新潟","中山","東京","中京","京都","阪神","小倉"]
        self.place_alpha = ["sapporo","hakodate","fukushima","niigata","nakayama","tokyo","chukyo","kyoto","hanshin","kokura"]

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

    def get_diviation_value(self,entry,self_data):
        if len(self_data) == 0:
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
                mean_level = mean_level+sp['level']
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

    # race5f * class
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

    def get_self_data(self, entry):
        cond = self.convert_condition(entry['course_condition'])
        msg = "horsename='"+entry['horsename']+"' and race_time="+str(entry['race_time'])+" and horse_table.place='"+entry['place']+"' and turf_dirt='"+entry['turf_dirt']+"' and (course_condition='"+cond+"') and distance="+str(entry['distance'])
        ret = self.get_sql_data(msg)
        if len(ret) > 0:
            return ret[0]
        else:
            return []

    def get_similar_strength_horse_data(self,entry,self_data):
        cond = self.convert_condition(entry['course_condition'])
        if len(self_data) == 0:
            return []
        # similar racetime, rap5f, diff3f
        msg = "race_time>"+str(entry['race_time']-0.3)+" and race_time<"+str(entry['race_time']+0.3)+" and diff3f>"+str(self_data['diff3f']-0.3)+" and diff3f<"+str(self_data['diff3f']+0.3)+" and horse_table.place='"+entry['place']+"' and turf_dirt='"+entry['turf_dirt']+"' and (course_condition='"+cond+"') and rap5f>"+str(self_data['rap5f']-0.3)+" and rap5f<"+str(self_data['rap5f']+0.3)
        ret =  self.get_sql_data(msg)
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
        ret = self.get_sql_data(msg)
        if len(ret) > 0:
            return ret
        else:
            return []

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

    def get_finish_trend(self, record):
        finish_list = []
        for r in record:
            finish_list.append(r['finish'])
        retval = [finish_list.count('逃げ'),finish_list.count('先行'),finish_list.count('中団'),finish_list.count('差し'),finish_list.count('後方'),finish_list.count('追込'),finish_list.count('マクリ')]
        return retval

    def get_finish_trend_list(self, record):
        fin = self.get_finish_trend(record)
        return ["逃"+str(fin[0]),"先"+str(fin[1]),"中"+str(fin[2]),"差"+str(fin[3]),"後"+str(fin[4]),"追"+str(fin[5]),"マクリ"+str(fin[6])] 

    def get_sql_data(self, condition_msg):
        manipulator = sql_manipulator.SQLManipulator()
        msg_select = "select race_table.rdate,race_table.place,race_table.race,class,turf_dirt,distance,course_condition,rap3f,rap5f,race_table.last3f,course_class,horse_total,level,goal_order,brinker,horsenum,horsename,horse_sex,age,jockey_weight,jockey_name,race_time,time_diff,passorder1,passorder2,passorder3,passorder4,finish,horse_table.last3f,diff3f,odds_order,odds,horseweight,weightdiff,trainer,carrier,owner,breeder,stallion,broodmaresire,color,span "
        msg_from = "from horse_table "
        msg_join = "inner join race_table on horse_table.rdate = race_table.rdate and horse_table.place = race_table.place and horse_table.race = race_table.race "
        msg = msg_select+msg_from+msg_join+"where race_time != 0 and "+condition_msg+";"
        tpl = manipulator.sql_manipulator(msg)
        retlist = []
        for t in tpl:
            single_dict = {"rdate":t[0],"place":t[1],"race":t[2],"class":t[3],"turf_dirt":t[4],"distance":t[5],"course_condition":t[6],"rap3f":t[7],"rap5f":t[8],"race_last3f":t[9],"course_class":t[10],"horse_total":t[11],"level":t[12],"goal_order":t[13],"brinker":t[14],"horsenum":t[15],"horsename":t[16],"horse_sex":t[17],"age":t[18],"jockey_weight":t[19],"jockey_name":t[20],"race_time":t[21],"time_diff":t[22],"passorder1":t[23],"passorder2":t[24],"passorder3":t[25],"passorder4":t[26],"finish":t[27],"horse_last3f":t[28],"diff3f":t[29],"odds_order":t[30],"odds":t[31],"horseweight":t[32],"weightdiff":t[33],"trainer":t[34],"carrier":t[35],"owner":t[36],"breeder":t[37],"stallion":t[38],"broodmaresire":t[39],"color":t[40],"span":t[41]}
            retlist.append(single_dict)
        return retlist

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
                    cls = self.analyse_class(row[5])
                    target={"rdate":row[0]+"-"+row[1]+"-"+row[2],"place":row[3],"turf_dirt":row[7],"distance":row[8],"class":row[5],"class_condition":cls,"race":row[4]}
                    all_target.append(target)
                    if row_count > 0:
                        all_entry.append(entry)
                        entry = []
                else:
                    if len(row) > 14 and len(row[14]) > 0 and row[21] != "----": # 1走前
                        entry.append({"race_time":self.convert_race_time(row[21]),"place":row[14],"turf_dirt":self.convert_turf_dirt(row[16]),"course_condition":row[19],"distance":row[17],"horsename":row[3],"jockey_name":row[6],"jockey_weight":row[7],"zi":row[10],"horsenum":row[2],"pastnum":1})
                    if len(row) > 30 and len(row[30]) > 0 and row[37] != "----": # 2走前
                        entry.append({"race_time":self.convert_race_time(row[37]),"place":row[30],"turf_dirt":self.convert_turf_dirt(row[32]),"course_condition":row[35],"distance":row[33],"horsename":row[3],"jockey_name":row[6],"jockey_weight":row[7],"zi":row[10],"horsenum":row[2],"pastnum":2})
                    if len(row) > 46 and len(row[46]) > 0 and row[53] != "----": # 3走前
                        entry.append({"race_time":self.convert_race_time(row[53]),"place":row[46],"turf_dirt":self.convert_turf_dirt(row[48]),"course_condition":row[51],"distance":row[49],"horsename":row[3],"jockey_name":row[6],"jockey_weight":row[7],"zi":row[10],"horsenum":row[2],"pastnum":3})
                    if len(row) > 62 and len(row[62]) > 0 and row[69] != "----": # 4走前
                        entry.append({"race_time":self.convert_race_time(row[69]),"place":row[62],"turf_dirt":self.convert_turf_dirt(row[64]),"course_condition":row[67],"distance":row[65],"horsename":row[3],"jockey_name":row[6],"jockey_weight":row[7],"zi":row[10],"horsenum":row[2],"pastnum":4})

                row_count = row_count+1
            all_entry.append(entry)
            all_target.append(target)
        return all_entry,all_target

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
        print(place)
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

    def set_race_level(self):
        hoge = 3
        place = ["札幌","函館","福島","新潟","中山","東京","中京","京都","阪神","小倉"]
        cond = ["良","稍","重","不"]
        td = ["芝","ダート"]
        distance = [1000,1150,1200,1300,1400,1500,1600,1700,1800,1900,2000,2100,2200,2300,2400,2500,2600,3000,3200,3600]
        for a in range(len(place)):
            for b in range(len(cond)):
                for c in range(len(td)):
                    for d in range(len(distance)):
                        msg_pattern = ["rap3f","last3f"]
                        if distance[d] >= 1600:
                            msg_pattern = ["rap5f","last3f"]
                        output_pattern = []
                        manipulator = sql_manipulator.SQLManipulator()
                        where_msg = "where place='"+place[a]+"' and course_condition='"+cond[b]+"' and turf_dirt='"+td[c]+"' and distance="+str(distance[d])
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
