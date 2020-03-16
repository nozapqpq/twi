# coding: utf-8
import sql_pattern
import sql_jockey

pat = sql_pattern.SQLPattern()
jk = sql_jockey.SQLJockey()
jockey_csvout = []
diviation_list = []
all_entry, all_target = pat.get_entry_target_data("../today.csv")
for a in range(len(all_entry)):
    jockey_csvout = []
    maindata_sum = []
    subdata_sum = []
    ent_count = 0
    for ent in all_entry[a]:
        pat.maindata = []
        pat.subdata = []
        if ent_count < len(all_entry[a])-1 and ent['jockey_name'] != all_entry[a][ent_count+1]['jockey_name'] or ent_count == len(all_entry[a])-1:
            jockey_csvout.append(jk.get_jockey_info(ent['jockey_name'],all_target[a]['place'],all_target[a]['turf_dirt'],all_target[a]['distance']))
        print(ent)
        self_data = pat.get_self_data(ent)
        pat.subdata = pat.get_similar_strength_horse_targetrace_data(ent,all_target[a],self_data)
        if len(self_data) == 0:
            diviation = "データなし"
        else:
            diviation,sigma,mean_diff,mean_level = pat.get_diviation_value(ent,self_data)
        for sd in pat.subdata:
            pat.distribution.append([ent['horsename'],sd['place'],sd['turf_dirt'],sd['distance'],sd['course_condition'],sd['class'],sd['rap5f'],sd['horse_last3f'],sd['time_diff'],sd['race_time']])
        goal = pat.get_sql_data("race_table.rdate='"+all_target[a]['rdate']+"' and race_table.place='"+all_target[a]['place']+"' and race_table.race="+all_target[a]['race']+" and horsename='"+ent['horsename']+"'")
        main_pastgoal = "" # get goal_order only if analyse past race
        if len(goal) > 0:
            main_pastgoal = str(goal[0]['goal_order'])
        if len(self_data) > 0:
            pat.maindata.append([ent['horsename'],ent['place'],ent['turf_dirt'],ent['course_condition'],ent['distance'],main_pastgoal]+[self_data['rap3f'],self_data['rap5f'],self_data['finish'],self_data['passorder3'],self_data['passorder4']]+[diviation,sigma,mean_diff,mean_level]+pat.get_finish_trend_list(pat.subdata))
            maindata_sum.append(pat.maindata)
        subdata_sum.append(pat.subdata)
        ent_count = ent_count + 1
    timediff_acc = pat.make_timediff_accumulation_list(subdata_sum,all_entry,a)
    placename = pat.convert_place_to_alpha(all_target[a]['place'])
    str_name_prefix = "_"+placename+all_target[a]['race']
    pat.write_list_to_csv_nest('../jockey'+str_name_prefix+'.csv',jockey_csvout)
    pat.write_list_to_csv_nest('../main'+str_name_prefix+'.csv',maindata_sum)
    pat.write_list_to_csv('../sub'+str_name_prefix+'.csv',timediff_acc)
    pat.write_list_to_csv('../distribution_map'+str_name_prefix+'.csv',pat.distribution)

