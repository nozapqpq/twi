# coding: utf-8
import sql_manipulator
import sql_jockey
import csv

class SQLPattern():
    def __init__(self, option=""):
        self.maindata = []
        self.subdata = []
        self.distribution = []

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


    def make_timediff_accumulation_list(self,allmain,allsub,allentry,race_count):
        retlist = []
        race_range_list = ["~58.0","~60.0","~62.0","~64.0","~66.0","66.1~"]
        class_list = ["新馬","未勝利","500万下","1000万下","1600万下","1勝","2勝","3勝","その他"]
        for i in range(len(allsub)):
            diff_list = [[0] * 31 for i in range(len(race_range_list)*len(class_list))]
            if len(allmain[i]) > 0 and len(allmain[i][0][0]) > 0:
                temp_list = list([allmain[i][0][0][0][0]])+[allentry[race_count][i][1],allentry[race_count][i][2],allentry[race_count][i][4]]
                for sd in allsub[i]:
                    idx = self.get_accumulation_list_index(race_range_list,class_list,sd[1],sd[0])
                    if sd[6] >= 3.0:
                        diff_list[idx][len(diff_list[idx])-1] = diff_list[idx][len(diff_list[idx])-1] + 1
                    else:
                        diff_list[idx][int(sd[6]*10)] = diff_list[idx][int(sd[6]*10)] +1
                dl_count = 0
                for dl in diff_list: # accumulate
                    for i_d in range(len(dl)):
                        if i_d > 0:
                            dl[i_d] = dl[i_d] + dl[i_d-1]
                    if dl[len(dl)-1] >= 10:
                        for i_d in range(len(dl)):
                            dl[i_d] = dl[i_d]/dl[len(dl)-1]*10
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
        cond = self.convert_condition(entry[3])
        msg = "horsename='"+entry[5]+"' and race_time="+str(entry[0])+" and horse_table.place='"+entry[1]+"' and turf_dirt='"+entry[2]+"' and (course_condition='"+cond+"') and distance="+str(entry[4])
        return self.get_sql_data(msg,1)

    def get_similar_strength_horse_data(self,entry,self_data):
        cond = self.convert_condition(entry[3])
        if len(self_data) == 0:
            return ()
        # rap5f vs timediff
        msg = "rap5f>"+str(self_data[0][2]-0.2)+" and rap5f<"+str(self_data[0][2]+0.2)+" and class='"+self.analyse_class(self_data[0][8])+"' and time_diff>"+str(self_data[0][4]-0.2)+" and time_diff <"+str(self_data[0][4]+0.2)+" and horse_table.place='"+entry[1]+"' and turf_dirt='"+entry[2]+"' and (course_condition='"+cond+"') and finish='"+self_data[0][5]+"'"
        # rap5f vs race_time
        msg = "race_time>"+str(entry[0]-0.3)+" and race_time<"+str(entry[0]+0.3)+" and horse_table.place='"+entry[1]+"' and turf_dirt='"+entry[2]+"' and (course_condition=    '"+cond+"') and rap5f>"+str(self_data[0][2]-0.3)+" and rap5f<"+str(self_data[0][2]+0.3)+" and finish='"+self_data[0][5]+"'"
        return self.get_sql_data(msg,1)

    def get_similar_strength_horse_targetrace_data(self,entry,target,self_data):
        similar_power_horse = self.get_similar_strength_horse_data(entry,self_data)
        msg = "race_table.place='"+target[0]+"' and turf_dirt='"+target[1]+"' and distance="+str(target[2])+" and ("
        if len(similar_power_horse) == 0:
            return ()
        for i in range(len(similar_power_horse)):
            msg_or = " or "
            if i == len(similar_power_horse)-1:
                msg_or = ")"
            msg = msg + " (horsename='"+similar_power_horse[i][0]+"' and race_table.rdate > '"+similar_power_horse[i][7].strftime('%Y/%m/%d')+"' - INTERVAL 1 YEAR and race_table.rdate < '"+similar_power_horse[i][7].strftime('%Y-%m-%d')+"' + INTERVAL 1 YEAR)"+msg_or
        msg = msg + " and horsename != '"+entry[5]+"'"
        return self.get_sql_data(msg,2)

    def get_finish_trend(self, record):
        finish_list = []
        for r in record:
            finish_list.append(r[7])
        retval = [finish_list.count('逃げ'),finish_list.count('先行'),finish_list.count('中団'),finish_list.count('差し'),finish_list.count('後方'),finish_list.count('追込'),finish_list.count('マクリ')]
        return retval

    def get_finish_trend_list(self, record):
        fin = self.get_finish_trend(record)
        return ["逃"+str(fin[0]),"先"+str(fin[1]),"中"+str(fin[2]),"差"+str(fin[3]),"後"+str(fin[4]),"追"+str(fin[5]),"マクリ"+str(fin[6])] 

    def get_sql_data(self, condition_msg, select_pattern=0):
        manipulator = sql_manipulator.SQLManipulator()
        msg_select = "select "
        if select_pattern == 0:
            msg_select = msg_select + "race_table.rdate,race_table.place,race_table.race,race_table.turf_dirt,race_table.distance,horse_table.horsename,horse_table.race_time,horse_table.goal_order,horse_table.time_diff,race_table.level "
        elif select_pattern == 1:
            msg_select = msg_select + "horse_table.horsename, race_table.rap3f, race_table.rap5f, horse_table.race_time, horse_table.time_diff, horse_table.finish, race_table.level, race_table.rdate, race_table.class "
        elif select_pattern == 2:
            msg_select = msg_select + "race_table.class, race_table.rap5f, race_table.last3f, horse_table.goal_order, horse_table.horsename, horse_table.race_time, horse_table.time_diff, horse_table.finish, horse_table.last3f, race_table.level, race_table.rdate, race_table.place, race_table.turf_dirt, race_table.distance, race_table.course_condition "
        msg_from = "from horse_table "
        msg_join = "inner join race_table on horse_table.rdate = race_table.rdate and horse_table.place = race_table.place and horse_table.race = race_table.race "
        msg = msg_select+msg_from+msg_join+"where race_time != 0 and "+condition_msg+";"
        ret = manipulator.sql_manipulator(msg)
        return ret

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
                    target=[row[3],row[7],row[8],cls,row[4]]
                    all_target.append(target)
                    if row_count > 0:
                        all_entry.append(entry)
                        entry = []
                else:
                    if len(row) > 10 and len(row[10]) > 0 and row[17] != "----": # 1走前
                        entry.append([self.convert_race_time(row[17]),row[10],self.convert_turf_dirt(row[12]),row[15],row[13],row[3],row[6]])
                    if len(row) > 26 and len(row[26]) > 0 and row[33] != "----": # 2走前
                        entry.append([self.convert_race_time(row[33]),row[26],self.convert_turf_dirt(row[28]),row[31],row[29],row[3],row[6]])
                    if len(row) > 42 and len(row[42]) > 0 and row[49] != "----": # 3走前
                        entry.append([self.convert_race_time(row[49]),row[42],self.convert_turf_dirt(row[44]),row[47],row[45],row[3],row[6]])
                    if len(row) > 58 and len(row[58]) > 0 and row[65] != "----": # 4走前
                        entry.append([self.convert_race_time(row[65]),row[58],self.convert_turf_dirt(row[60]),row[63],row[61],row[3],row[6]])

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
        for p in range(len(place_kanji)):
            if place == place_kanji[p]:
                return place_alpha[p]
        return "unknown"

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
