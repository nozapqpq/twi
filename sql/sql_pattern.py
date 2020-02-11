# coding: utf-8
import sql_manipulator
import csv

class SQLPattern():
    def __init__(self, option=""):
        if option == "set_level":
            self.set_race_level()
        else:
            entry, target = self.get_entry_target_data("../today.csv")
            print(target)
            maindata_sum = []
            subdata_sum = []
            for ent in entry:
                maindata, subdata = self.get_targetrace_statistics(ent,target)
                maindata_sum.append(maindata)
                subdata_sum.append(subdata)
            with open('../main.csv','w') as f:
                writer = csv.writer(f)            
                for mds in maindata_sum:
                    for md in mds:
                        writer.writerow([md])
            with open('../sub.csv','w') as f:
                i = 0
                writer = csv.writer(f)
                for sds in subdata_sum:
                    writer.writerow([maindata_sum[i]])
                    i = i + 1
                    count = 0
                    for sd in sds:
                        writer.writerow(sd)
                        count = count + 1
                        if count == 15:
                            break


    def get_targetrace_statistics(self, entry, target):
        maindata = []
        result = [[0 for i in range(4)] for j in range(4)]
        print(entry)
        cond = self.convert_condition(entry[3])
        msg = "race_time>"+str(entry[0]-0.4)+" and race_time<"+str(entry[0]+0.4)+" and horse_table.place='"+entry[1]+"' and turf_dirt='"+entry[2]+"' and (course_condition='"+cond+"') and distance="+str(entry[4])
        msg2 = "horsename='"+entry[5]+"' and "+msg
        self_data = self.get_sql_data(msg2,1)
        if len(self_data) == 0:
            return [], []
        msg3 = msg+" and rap5f>"+str(self_data[0][2]-0.4)+" and rap5f<"+str(self_data[0][2]+0.4)+" and finish='"+self_data[0][5]+"'"
        similar_power_name = self.get_sql_data(msg3,1)
        #msg = "race_table.place='"+target[0]+"' and turf_dirt='"+target[1]+"' and distance="+str(target[2])+" and (class='"+target[3]+"') and ("
        msg = "race_table.place='"+target[0]+"' and turf_dirt='"+target[1]+"' and distance="+str(target[2])+" and ("
        for i in range(len(similar_power_name)):
            msg_or = " or "
            if i == len(similar_power_name)-1:
                msg_or = ")"
            msg = msg + " horsename='"+similar_power_name[i][0]+"'"+msg_or
        record = self.get_sql_data(msg,2)
        comment = ""
        if len(record) <= 2:
            comment = "情報少、要注意"
        print_msg = str(self_data)+" "+str(len(similar_power_name))+" > "+str(len(record))+" "+comment
        print(print_msg)
        maindata.append(print_msg)
        total_num = 0
        goodrace_num = 0
        nice_num = 0
        for rc in record:
            strategy = 0
            time_diff = 0
            total_num = total_num+1
            if rc[7] == '逃げ' or rc[7] == '先行':
                strategy = 0
            elif rc[7] == '中団':
                strategy = 1
            elif rc[7] == '追込' or rc[7] == '後方':
                strategy = 2
            else:
                strategy = 3
            if rc[6] < 0.3:
                time_diff = 0
                goodrace_num = goodrace_num+1
            elif rc[6] < 0.8:
                nice_num = nice_num+1
                time_diff = 1
            elif rc[6] < 1.5:
                time_diff = 2
            else:
                time_diff = 3
            result[strategy][time_diff] = result[strategy][time_diff] + 1
        if total_num > 0:
            print_msg = str(result)+" 0.3s内："+str(round(goodrace_num/total_num*100,1))+"％ 0.8s内: "+str(round((goodrace_num+nice_num)/total_num*100,1))+"％"
            print(print_msg)
            maindata.append(print_msg)
        return maindata, record

    def get_sql_data(self, condition_msg, select_pattern=0):
        manipulator = sql_manipulator.SQLManipulator()
        msg_select = "select "
        if select_pattern == 0:
            msg_select = msg_select + "race_table.rdate,race_table.place,race_table.race,race_table.turf_dirt,race_table.distance,horse_table.horsename,horse_table.race_time,horse_table.goal_order,horse_table.time_diff,race_table.level "
        elif select_pattern == 1:
            msg_select = msg_select + "horse_table.horsename, race_table.rap3f, race_table.rap5f, horse_table.race_time, horse_table.time_diff, horse_table.finish, race_table.level "
        elif select_pattern == 2:
            msg_select = msg_select + "race_table.class, race_table.rap5f, race_table.last3f, horse_table.goal_order, horse_table.horsename, horse_table.race_time, horse_table.time_diff, horse_table.finish, horse_table.last3f, race_table.level "
        msg_from = "from horse_table "
        msg_join = "inner join race_table on horse_table.rdate = race_table.rdate and horse_table.place = race_table.place and horse_table.race = race_table.race "
        msg = msg_select+msg_from+msg_join+"where race_time != 0 and "+condition_msg+";"
        ret = manipulator.sql_manipulator(msg)
        return ret

    def get_entry_target_data(self, csvfile):
        row_count = 0
        entry = []
        target = []
        with open(csvfile, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row_count == 0:
                    cls = self.analyse_class(row[5])
                    target=[row[3],row[7],row[8],cls]
                else:
                    if len(row) > 14 and len(row[14]) > 0 and row[21] != "----": # 1走前
                        entry.append([self.convert_race_time(row[21]),row[14],self.convert_turf_dirt(row[16]),row[19],row[17],row[7]])
                    if len(row) > 30 and len(row[30]) > 0 and row[37] != "----": # 2走前
                        entry.append([self.convert_race_time(row[37]),row[30],self.convert_turf_dirt(row[32]),row[35],row[33],row[7]])
                    if len(row) > 46 and len(row[46]) > 0 and row[53] != "----": # 3走前
                        entry.append([self.convert_race_time(row[53]),row[46],self.convert_turf_dirt(row[48]),row[51],row[49],row[7]])
                row_count = row_count+1
        return entry,target

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
sp = SQLPattern()
