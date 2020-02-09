# coding: utf_8
import sql_manipulator
import csv

class SQLPattern():
    def __init__(self):
        entry = [[140.1,'京都','芝'],[116.1,'京都','ダート'],[113.7,'京都','ダート'],[116.1,'京都','ダート'],[86.9,'阪神','ダート']]
        target = ['京都','ダート',1800,'未勝利']
        entry, target = self.get_entry_target_data("../today.csv")
        for ent in entry:
            self.get_targetrace_statistics(ent,target)

    def get_targetrace_statistics(self, entry, target):
        result = [0,0]
        print(entry)
        msg = "race_time>"+str(entry[0]-0.3)+" and race_time<"+str(entry[0]+0.3)+" and horse_table.place='"+entry[1]+"' and turf_dirt='"+entry[2]+"'"
        similar_power_name = self.get_sql_data(msg,1)
        count = 0
        for nm in similar_power_name:
            count = count + 1
            if count > 100:
                break
            record = self.get_sql_data("horsename='"+nm[0]+"' and race_table.place='"+target[0]+"' and turf_dirt='"+target[1]+"' and distance="+str(target[2])+" and class='"+target[3]+"'",2)
            if len(record) > 0:
                result[1] = result[1] + 1
                if record[0][6] < 1.0:
                    result[0] = result[0] + 1
            if count%50 == 0 or count == len(similar_power_name)-2:
                print("progress: "+str(result[0])+" / "+str(result[1])+" / "+str(count)+" / "+str(len(similar_power_name)))

    def get_sql_data(self, condition_msg, select_pattern=0):
        manipulator = sql_manipulator.SQLManipulator()
        msg_select = "select "
        if select_pattern == 0:
            msg_select = msg_select + "race_table.rdate,race_table.place,race_table.race,race_table.turf_dirt,race_table.distance,horse_table.horsename,horse_table.race_time,horse_table.goal_order,horse_table.time_diff "
        elif select_pattern == 1:
            msg_select = msg_select + "horse_table.horsename "
        elif select_pattern == 2:
            msg_select = msg_select + "race_table.class, race_table.rap5f, race_table.last3f, horse_table.goal_order, horse_table.horsename, horse_table.race_time, horse_table.time_diff, horse_table.finish, horse_table.last3f "
        msg_from = "from horse_table "
        msg_join = "inner join race_table on horse_table.rdate = race_table.rdate and horse_table.place = race_table.place and horse_table.race = race_table.race "
        msg = msg_select+msg_from+msg_join+"where "+condition_msg+";"
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
                    target=[row[3],row[7],row[8],row[5]]
                else:
                    if len(row) > 14: # 1走前
                        cls = self.analyse_class(row[14])
                        for c in cls: 
                            entry.append([self.convert_race_time(row[21]),row[14],self.convert_turf_dirt(row[16]),c,row[19],row[7]])
                    if len(row) > 30: # 2走前
                        cls = self.analyse_class(row[30])
                        for c in cls:
                            entry.append([self.convert_race_time(row[37]),row[14],self.convert_turf_dirt(row[32]),c,row[35],row[7]])
                row_count = row_count+1
        return entry,target

    def analyse_class(self, cls):
        if cls=="500万" or cls=="1勝":
            return ["500万","1勝"]
        if cls=="未勝利":
            return ["未勝利"]
        if cls=="1000万" or cls=="2勝":
            return ["1000万","2勝"]
        else:
            return ["1000万","1600万","2勝","3勝","オープン"]

    def convert_turf_dirt(self, s):
        if s=="T":
            return "芝"
        elif s=="D":
            return "ダート"
        else:
            return "その他"

    def convert_race_time(self, s):
        if (len(s) == 3 or len(s) == 4) and s != "----":
            return round((int(int(s)/1000)*600+int(s[-3:]))*0.1,1)
        else:
            return "0.0"
sp = SQLPattern()
