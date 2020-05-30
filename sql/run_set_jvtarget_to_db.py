# coding: utf-8
import sql_manipulator

sm = sql_manipulator.SQLManipulator()
sm.convert_csv_to_db("../jv_target_tmp.csv")
#how to get csv data
#1. run race search using the range of target date with t/d, 1st horse only
#2. output data with expanded-output(Shift+F8), race result*2
#sm.convert_csv_to_db("../test1.csv")
#sm.convert_csv_to_db("../test2.csv")

