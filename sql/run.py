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
        if ent_count < len(all_entry[a])-1 and ent[6] != all_entry[a][ent_count+1][6] or ent_count == len(all_entry[a])-1:
            jockey_csvout.append(jk.get_jockey_info(ent[6],all_target[a][0],all_target[a][1],all_target[a][2]))
        print(ent)
        self_data = pat.get_self_data(ent)
        pat.subdata = pat.get_similar_strength_horse_targetrace_data(ent,all_target[a],self_data)
        if len(self_data) == 0:
            diviation = "データなし"
        else:
            diviation,sigma,mean_diff = pat.get_diviation_value(ent,self_data[0])
        for sd in pat.subdata:
            pat.distribution.append([ent[5],sd[11],sd[12],sd[13],sd[14],sd[0],sd[1],sd[8],sd[6],sd[5]])
        pat.maindata.append([ent[5]]+ent[1:5]+list(self_data[0][1:3])+[diviation,sigma,mean_diff,self_data]+pat.get_finish_trend_list(pat.subdata))
        maindata_sum.append(pat.maindata)
        subdata_sum.append(pat.subdata)
        ent_count = ent_count + 1
    timediff_acc = pat.make_timediff_accumulation_list(subdata_sum,all_entry,a)
    placename = pat.convert_place_to_alpha(all_target[a][0])
    str_name_prefix = "_"+placename+all_target[a][4]
    pat.write_list_to_csv_nest('../jockey'+str_name_prefix+'.csv',jockey_csvout)
    pat.write_list_to_csv_nest('../main'+str_name_prefix+'.csv',maindata_sum)
    pat.write_list_to_csv('../sub'+str_name_prefix+'.csv',timediff_acc)
    pat.write_list_to_csv('../distribution_map'+str_name_prefix+'.csv',pat.distribution)

