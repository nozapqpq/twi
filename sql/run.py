# coding: utf-8
import sql_pattern
import sql_jockey
import utility
import os
import re
import shutil

def make_dpinput_from_racecard(csvfile):
    pat = sql_pattern.SQLPattern()
    jk = sql_jockey.SQLJockey()
    util = utility.Utility()
    jockey_csvout = []
    diviation_list = []
    div_dict = {}
    all_entry, all_target = pat.get_entry_target_data(csvfile)
    oneday_horsenames = []
    for race in all_entry:
        for horse in race:
            oneday_horsenames.append(horse["horsename"])
    oneday_horsenames = list(set(oneday_horsenames))
    all_self_data = pat.get_self_data_oneday(all_target[0]["rdate"],oneday_horsenames)
    for a in range(len(all_entry)):
        jockey_csvout = []
        maindata_sum = []
        ent_count = 0
        if len(all_entry[a]) > 0: # date,place,racenum output
            print(str(all_target[a]["rdate"])+" "+all_entry[a][0]["place"]+" "+str((a%12)+1)+"R")
        for ent in all_entry[a]:
            maindata = []
            self_data = [x for x in all_self_data if x["horsename"] == ent["horsename"] and str(x["rdate"]) == ent["rdate"]]
            if len(self_data) > 0:
                self_data = self_data[0]
            else:
                break
            #div_dict = util.get_diviation_value(ent,self_data)
            div_dict = {}
            # get goal_order when analyse past race data.
            goal = util.get_sql_data("race_table.rdate='"+all_target[a]['rdate']+"' and race_table.place='"+all_target[a]['place']+"' and race_table.race="+all_target[a]['race']+" and horsename='"+ent['horsename']+"'")
            main_pastgoal = ""
            main_today_time_diff = ""
            main_triple = ""
            if len(goal) > 0:
                main_pastgoal = str(goal[0]['goal_order'])
                main_today_time_diff = str(goal[0]['time_diff'])
                main_triple = goal[0]['triple_dividend']
            if len(self_data) > 0:
                single_maindata = pat.set_single_maindata(ent, all_target[a], self_data, div_dict, main_pastgoal, main_today_time_diff, main_triple)
                maindata.append(single_maindata)
                maindata_sum.append(maindata)
                #print(single_maindata)
            ent_count = ent_count + 1
        placename = util.convert_place_to_alpha(all_target[a]['place'])
        str_name_prefix = "_"+placename+all_target[a]['race']
        util.write_list_to_csv_nest('../main'+str_name_prefix+'.csv',maindata_sum)

# HOW TO USE THIS APP
# 1. prepare 000000.csv files in parent dir
# 1. execute pattern.sh
all_parent_files = os.listdir("../")
for f in all_parent_files:
    if re.match("\d+.csv_tmp",f): # f: 000000.csv_tmp
        mkdir_name = re.search("\d+",f) # mkdir_nmae: 000000
        make_dpinput_from_racecard("../"+f)
        os.mkdir("../"+mkdir_name.group())
        all_parent_files2 = os.listdir("../")
        for f2 in all_parent_files2: # f2: main_xxxxx0.csv
            if re.match("main_\w+.csv",f2):
                shutil.move('../'+f2,'../'+mkdir_name.group())
        print(mkdir_name.group())
# set SQL data1
#pat = sql_pattern.SQLPattern()
#pat.set_race_level()

# set SQL data2
#sp = sql_pattern.SQLPattern()
#sp.set_race_last3f_correction()

