# coding: utf-8
import sql_pattern
import sql_jockey

# this program output main.csv
pat = sql_pattern.SQLPattern()
jk = sql_jockey.SQLJockey()
jockey_csvout = []
diviation_list = []
div_dict = {}
all_entry, all_target = pat.get_entry_target_data("../today.csv")
for a in range(len(all_entry)):
    jockey_csvout = []
    maindata_sum = []
    subdata_sum = []
    ent_count = 0
    for ent in all_entry[a]:
        pat.maindata = []
        pat.subdata = []
        print(ent)
        self_data = pat.get_self_data(ent)
        pat.subdata = pat.get_similar_strength_horse_targetrace_data(ent,all_target[a],self_data)
        div_dict = pat.get_diviation_value(ent,self_data)
        # get goal_order when analyse past race data.
        goal = pat.get_sql_data("race_table.rdate='"+all_target[a]['rdate']+"' and race_table.place='"+all_target[a]['place']+"' and race_table.race="+all_target[a]['race']+" and horsename='"+ent['horsename']+"'")
        main_pastgoal = ""
        if len(goal) > 0:
            main_pastgoal = str(goal[0]['goal_order'])
        if len(self_data) > 0:
            single_maindata = []
            single_maindata.append(all_target[a]['rdate'])
            single_maindata.append(all_target[a]['race'])
            single_maindata.append(all_target[a]['place'])
            single_maindata.append(all_target[a]['turf_dirt'])
            single_maindata.append(all_target[a]['distance'])
            single_maindata.append(ent['horsename'])
            single_maindata.append(all_target[a]['class'])
            single_maindata.append(ent['jockey_name'])
            single_maindata.append(ent['jockey_weight'])
            single_maindata.append(ent['zi'])

            single_maindata.append(ent['pastnum'])
            single_maindata.append(str(self_data['rdate']))
            single_maindata.append(self_data['race'])
            single_maindata.append(self_data['place'])
            single_maindata.append(self_data['turf_dirt'])
            single_maindata.append(self_data['distance'])
            single_maindata.append(self_data['class'])
            single_maindata.append(self_data['course_condition'])
            single_maindata.append(self_data['horseweight'])
            single_maindata.append(self_data['rap3f'])
            single_maindata.append(self_data['rap5f'])
            single_maindata.append(self_data['diff3f'])
            single_maindata.append(self_data['time_diff'])
            single_maindata.append(div_dict['mean_diff'])
            single_maindata.append(div_dict['mean_goal'])
            single_maindata.append(div_dict['diviation'])
            single_maindata.append(div_dict['sigma'])
            single_maindata.append(div_dict['total'])
            single_maindata.append(self_data['horse_last3f'])
            single_maindata.append(self_data['race_last3f'])
            single_maindata.append(main_pastgoal)
            pat.maindata.append(single_maindata)
            print(single_maindata)
            #pat.maindata.append([ent['horsename'],ent['place'],ent['turf_dirt'],ent['course_condition'],ent['distance'],main_pastgoal]+[self_data['rap3f'],self_data['rap5f'],self_data['passorder3'],self_data['passorder4']]+[div_dict['diviation'],div_dict['diff3f'],div_dict['horse_last3f'],div_dict['class'],min_val,max_val,div_dict['mean_diff']]+g_order_list+pat.get_finish_trend_list(pat.subdata))
            maindata_sum.append(pat.maindata)
        ent_count = ent_count + 1
    placename = pat.convert_place_to_alpha(all_target[a]['place'])
    str_name_prefix = "_"+placename+all_target[a]['race']
    pat.write_list_to_csv_nest('../main'+str_name_prefix+'.csv',maindata_sum)

