# coding: utf_8
import sql_manipulator

class SQLPattern():
    def __init__(self):
        entry = [[140.1,'京都','芝'],[116.1,'京都','ダート'],[113.7,'京都','ダート'],[116.1,'京都','ダート'],[86.9,'阪神','ダート']]
        target = ['京都','ダート',1800]
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
            record = self.get_sql_data("horsename='"+nm[0]+"' and race_table.place='"+target[0]+"' and turf_dirt='"+target[1]+"' and distance="+str(target[2]),2)
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
sp = SQLPattern()
