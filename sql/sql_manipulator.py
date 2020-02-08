# coding: utf_8
import MySQLdb
import os
import csv

class SQLManipulator():
    def __init__(self, ):
        i=0

    def sql_manipulator(self, msg):
        connection = MySQLdb.connect(
            host='localhost',
            user='noza',
            passwd='Pass_123',
            db='horse',
            use_unicode=True,
            charset='utf8')
        cursor = connection.cursor()

        cursor.execute(msg)
        retval = cursor.fetchall()
        connection.commit()
        connection.close()

        return retval

    def convert_csv_to_db(self, csvfile):
        read_mode = 0
        horse_count = 0
        race_summary = []
        race_detail = []
        temp =[]
        temp_yyyymmdd = '0000-00-00'
        temp_place = ''
        temp_race = 0
        with open(csvfile, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if read_mode == 1:
                    race_summary.append(row)
                    temp_yyyymmdd = row[0]+"-"+row[1]+"-"+row[2]
                    temp_place = row[3]
                    temp_race = row[4]
                    read_mode = 0
                if read_mode == 2 and row[0] != "年":
                    row.append(temp_yyyymmdd)
                    row.append(temp_place)
                    row.append(temp_race)
                    temp.append(row)
                    horse_count = horse_count+1
                if row[0] == "年":
                    if horse_count > 0:
                        race_detail.append(temp)
                        horse_count = 0
                        temp = []
                    read_mode = 1
                elif row[0] == "入線順位":
                    read_mode = 2
        for i in range(len(race_summary)):
            msg = self.make_race_message(race_summary[i])
            ret = self.sql_manipulator(msg)
        for i in range(len(race_detail)):
            if i%200==0:
                print("progress : "+str(i)+" / "+str(len(race_detail)))
            for j in range(len(race_detail[i])):
                msg = self.make_horse_data_message(race_detail[i][j])
                ret = self.sql_manipulator(msg)
        print("import "+csvfile+" is finished.")

    def make_race_message(self, race_sm):
        out_date = race_sm[0]+"-"+race_sm[1]+"-"+race_sm[2]
        out_place = race_sm[3]
        out_race = race_sm[4]
        out_class = race_sm[6]
        out_td = race_sm[7]
        out_distance = race_sm[8]
        out_condition = race_sm[10]
        out_time3f = race_sm[11]
        out_time5f = race_sm[12]
        out_last5f = race_sm[13]
        out_course_class = race_sm[14]
        out_horse_total = race_sm[15]
        msg = "insert into race_table values('"+out_date+"','"+out_place+"',"+out_race+",'"+out_class+"','"+out_td+"',"+out_distance+",'"+out_condition+"',"+out_time3f+","+out_time5f+","+out_last5f+",'"+out_course_class+"',"+out_horse_total+");"
        return msg

    def make_horse_data_message(self,race_dt):
        out_date = race_dt[-3]
        out_place = race_dt[-2]
        out_race = self.convert_blank_number(race_dt[-1])
        out_order = self.convert_blank_number(race_dt[0])
        out_brinker = race_dt[2]
        out_horsenum = self.convert_blank_number(race_dt[4])
        out_horsename = race_dt[5]
        out_sex = race_dt[6]
        out_age = self.convert_blank_number(race_dt[7])
        out_jockey_weight = self.adjust_jockey_weight_expression(race_dt[8])
        out_jockey_name = race_dt[9]
        out_time = self.convert_time_to_doublestr(race_dt[10])
        out_time_diff = self.convert_blank_number(race_dt[13])
        out_passorder1 = self.convert_blank_number(race_dt[14])
        out_passorder2 = self.convert_blank_number(race_dt[15])
        out_passorder3 = self.convert_blank_number(race_dt[16])
        out_passorder4 = self.convert_blank_number(race_dt[17])
        out_finish = race_dt[18]
        out_last3f = race_dt[20].replace("----","0")
        out_diff3f = self.convert_blank_number(race_dt[21])
        out_odds_order = self.convert_blank_number(race_dt[23])
        out_odds = race_dt[24]
        out_horseweight = self.convert_blank_number(race_dt[25].replace("---","0"))
        out_weightdiff = str(int(self.convert_blank_number(race_dt[26])))
        out_trainer = race_dt[29]
        out_carrier = self.convert_blank_number(race_dt[30])
        out_owner = race_dt[31].replace("'","`")
        out_breeder = race_dt[32].replace("'","`")
        out_stallion = race_dt[33].replace("'","`")
        out_broodmaresire = race_dt[34].replace("'","`")
        out_color = race_dt[35]
        out_span = self.convert_blank_number(race_dt[37]).replace("不明","999")
        msg = "insert into horse_table values('"+out_date+"','"+out_place+"',"+out_race+","+out_order+",'"+out_brinker+"',"+out_horsenum+",'"+out_horsename+"','"+out_sex+"',"+out_age+","+out_jockey_weight+",'"+out_jockey_name+"',"+out_time+","+out_time_diff+","+out_passorder1+","+out_passorder2+","+out_passorder3+","+out_passorder4+",'"+out_finish+"',"+out_last3f+","+out_diff3f+","+out_odds_order+","+out_odds+","+out_horseweight+","+out_weightdiff+",'"+out_trainer+"',"+out_carrier+",'"+out_owner+"','"+out_breeder+"','"+out_stallion+"','"+out_broodmaresire+"','"+out_color+"',"+out_span+");"
        return msg

    def adjust_jockey_weight_expression(self, weight_str):
        return weight_str.strip()[0:2]

    def convert_time_to_doublestr(self, time_str):
        if "------" in time_str:
            return str(0.0)
        sep_str = time_str.split('.')
        retval = int(sep_str[0])*60+int(sep_str[1])+int(sep_str[2])/10
        return str(retval)

    def convert_blank_number(self, str):
        if str == "":
            return "0"
        return str

#sm = SQLManipulator()
#sm.convert_csv_to_db("../test.csv")
#sm.convert_csv_to_db("../test2.csv")
#sm.convert_csv_to_db("../test3.csv")
#sm.convert_csv_to_db("../test4.csv")
#sm.convert_csv_to_db("../test5.csv")
#sm.convert_csv_to_db("../test6.csv")
#sm.convert_csv_to_db("../test7.csv")
