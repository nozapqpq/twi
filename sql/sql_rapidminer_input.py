# coding: utf-8
import sql_manipulator
import sql_jockey
import csv
import datetime

class SQLRapidminerInput():
    def __init__(self, option=""):
        jk = sql_jockey.SQLJockey()
        data1 = jk.get_dictionary("国分恭介","阪神","ダート","1400")
        data2 = jk.get_dictionary("国分恭介","京都","ダート","1400")
        count = 0
        result = []
        for d in data1:
            rst = self.get_single_output(d)
            print(rst)
            result.append(rst)
        for d in data2:
            rst = self.get_single_output(d)
            print(rst)
            result.append(rst)
        with open('../for_rapidminer.csv','w') as f:
            writer = csv.writer(f)
            for r in result:
                writer.writerow(r)

    def get_single_output(self, single_data):
        ret_list = []
        sm = self.get_same_race_dictionary(single_data['rdate'],single_data['place'],single_data['race'])
        hd = self.get_horse_data_dictionary(single_data['rdate'],single_data['horsename'])
        goodat = False
        first_ride = True
        for h in hd:
            if h['place'] == single_data['place'] and h['turf_dirt'] == single_data['turf_dirt'] and h['distance'] == single_data['distance'] and (h['time_diff'] <= 0.5 or h['goal_order'] <= 5):
                goodat = True
            if h['jockey_name'] == single_data['jockey_name']:
                first_ride = False

        answer = True
        leading_count = 0
        # compare to time_diff of 3rd horse
        diff = sm[2]['time_diff']
        if single_data['time_diff'] > sm[2]['time_diff']:
            answer = False
        for s in sm:
            if self.is_leading(s['jockey_name']):
                leading_count = leading_count + 1

        ret_list.append(single_data['place'])
        ret_list.append(single_data['distance'])
        ret_list.append(single_data['rap5f'])
        ret_list.append(single_data['finish'])
        ret_list.append(self.convert_bool_to_zeroone(goodat))
        ret_list.append(self.convert_bool_to_zeroone(not first_ride))
        ret_list.append(self.convert_bool_to_zeroone(leading_count <= 3))
        ret_list.append(self.get_odds(sm,1))
        ret_list.append(self.get_odds(sm,2))
        ret_list.append(self.get_odds(sm,3))
        ret_list.append(single_data['odds'])
        ret_list.append(single_data['odds_order'])
        ret_list.append(self.convert_sex_to_zeroone(single_data['horse_sex']))
        ret_list.append(single_data['age'])
        ret_list.append(self.get_previous_order(hd))
        ret_list.append(self.convert_bool_to_zeroone(self.is_entry_within_a_year(single_data['rdate'],hd)))
        ret_list.append(self.convert_bool_to_zeroone(answer))
        return ret_list

    def is_leading(self, jk_name):
        leading_list = ["ルメール","川田将雅","武豊","福永祐一","松山弘平","戸崎圭太","Ｍ．デム","三浦皇成","田辺裕信","北村友一"]
        return jk_name in leading_list
    def is_entry_within_a_year(self, base_date, horse_data):
        if len(horse_data) == 0:
            return False
        return horse_data[0]['rdate'] > base_date - datetime.timedelta(days=365)
            
        
    def get_previous_order(self, horse_data):
        if len(horse_data) == 0:
            return 0
        return horse_data[0]['goal_order']
    def get_odds(self, dict_list, order):
        for dl in dict_list:
            if dl['odds_order'] == order:
                return dl['odds']
        return 0
    def convert_sex_to_zeroone(self, sex):
        if sex == "牝":
            return 1
        return 0
    def convert_bool_to_zeroone(self, bl):
        if bl:
            return 1
        else:
            return 0

    def get_horse_data(self, date, horsename):
        one_day_before = date + datetime.timedelta(days=-1)
        manipulator = sql_manipulator.SQLManipulator()
        select_msg = "select race_table.rdate,race_table.place,race_table.turf_dirt,race_table.distance,jockey_name,goal_order,time_diff "
        from_msg = "from horse_table "
        join_msg = "inner join race_table on horse_table.rdate = race_table.rdate and horse_table.place = race_table.place and horse_table.race = race_table.race "
        where_msg = "where race_table.rdate < '"+one_day_before.strftime('%Y-%m-%d')+"' and horsename = '"+horsename+"';"
        ret = manipulator.sql_manipulator(select_msg+from_msg+join_msg+where_msg)
        return ret

    def get_horse_data_dictionary(self, date, horsename):
        data = self.get_horse_data(date,horsename)
        ret_list = []
        for d in data:
            single_dict = {"rdate":d[0],"place":d[1],"turf_dirt":d[2],"distance":d[3],"jockey_name":d[4],"goal_order":d[5],"time_diff":d[6]}
            ret_list.append(single_dict)
        return ret_list

    def get_same_race_data(self, date, place, race):
        manipulator = sql_manipulator.SQLManipulator()
        select_msg = "select horsename,jockey_name,odds_order,odds,goal_order,time_diff "
        from_msg = "from horse_table "
        where_msg = "where race_time != 0 and rdate = '"+date.strftime('%Y/%m/%d')+"' and place='"+place+"' and race="+str(race)+";"
        ret = manipulator.sql_manipulator(select_msg+from_msg+where_msg)
        return ret

    def get_same_race_dictionary(self, date, place, race):
        data = self.get_same_race_data(date,place,race)
        ret_list = []
        for d in data:
            single_dict = {"horsename":d[0],"jockey_name":d[1],"odds_order":d[2],"odds":d[3],"goal_order":d[4],"time_diff":d[5]}
            ret_list.append(single_dict)
        return ret_list

srm = SQLRapidminerInput()
