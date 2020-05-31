# coding: utf-8
import sql_pattern
import sql_jockey
import utility

# this program output main.csv
pat = sql_pattern.SQLPattern()
jk = sql_jockey.SQLJockey()
util = utility.Utility()
jockey_csvout = []
diviation_list = []
div_dict = {}
all_entry, all_target = pat.get_entry_target_data("../today_tmp.csv")
for a in range(len(all_entry)):
    jockey_csvout = []
    maindata_sum = []
    subdata_sum = []
    ent_count = 0
    for ent in all_entry[a]:
        maindata = []
        subdata = []
        self_data = pat.get_self_data(ent)
        subdata = pat.get_similar_strength_horse_targetrace_data(ent,all_target[a],self_data)
        div_dict = util.get_diviation_value(ent,self_data)
        # get goal_order when analyse past race data.
        goal = util.get_sql_data("race_table.rdate='"+all_target[a]['rdate']+"' and race_table.place='"+all_target[a]['place']+"' and race_table.race="+all_target[a]['race']+" and horsename='"+ent['horsename']+"'")
        main_pastgoal = ""
        main_triple = ""
        if len(goal) > 0:
            main_pastgoal = str(goal[0]['goal_order'])
            main_triple = goal[0]['triple_dividend']
        if len(self_data) > 0:
            single_maindata = pat.set_single_maindata(ent, all_target[a], self_data, div_dict, main_pastgoal, main_triple)
            maindata.append(single_maindata)
            maindata_sum.append(maindata)
        ent_count = ent_count + 1
    placename = util.convert_place_to_alpha(all_target[a]['place'])
    str_name_prefix = "_"+placename+all_target[a]['race']
    util.write_list_to_csv_nest('../main'+str_name_prefix+'.csv',maindata_sum)

# set SQL data1
#pat = sql_pattern.SQLPattern()
#pat.set_race_level()

# set SQL data2
#sp = sql_pattern.SQLPattern()
#sp.set_race_last3f_correction()

