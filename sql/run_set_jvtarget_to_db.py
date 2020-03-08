# coding: utf-8
import sql_manipulator

sm = sql_manipulator.SQLManipulator()
sm.convert_csv_to_db("../jv_target.csv")
#how to get csv data
#1. run race search using the range of target date with t/d, 1st horse only
#2. output data with expanded-output(Shift+F8), race result*2
#sm.convert_csv_to_db("../test.csv")
#sm.convert_csv_to_db("../test2.csv")
#sm.convert_csv_to_db("../test3.csv")
#sm.convert_csv_to_db("../test4.csv")
#sm.convert_csv_to_db("../test5.csv")
#sm.convert_csv_to_db("../test6.csv")
#sm.convert_csv_to_db("../test7.csv")

