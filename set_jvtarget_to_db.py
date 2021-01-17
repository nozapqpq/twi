# coding: utf-8
from db import horse_race

hr = horse_race.HorseRace()
hr.set_race_and_horse_data_from_jvtarget("./jv_target_tmp.csv")
#how to get csv data
#1. run race search using the range of target date with t/d, 1st horse only
#2. output data with expanded-output(Shift+F8), race result*2
#sm.convert_csv_to_db("../test1.csv")
#sm.convert_csv_to_db("../test2.csv")

