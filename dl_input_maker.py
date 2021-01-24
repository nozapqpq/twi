# coding: utf-8
import os
import re
from db import horse_race
from db import stallion
from db import trainer
from machine_learning import model_inout_data
from output_tools import output
import utility

def make_deeplearning_input_file():
    export_dict = {"input":[],"output":[],"rdate":[],"place":[],"race":[],"horsenum":[],"horsename":[],"goal_order":[]}
    no_output_flg = True
    output_tools = output.Output()
    util = utility.Utility()
    settings = output_tools.json_import("settings.json")["settings"]
    model_name = util.get_deep_model_name(settings)
    hr = horse_race.HorseRace(True)
    dl_model_inout = model_inout_data.ModelInOutData()
    dl_model_inout.set_stallion_table(stallion.Stallion().get_stallion_dict_list())
    dl_model_inout.set_trainer_table(trainer.Trainer().get_trainer_dict_list())
    output_tools = output.Output()

    source_list = get_source_data_list(hr, settings)
    print(len(source_list))
    # 解析(全件アウトプット無)か学習かの判断用フラグno_output_flgをセット
    for sl in source_list:
        for i in range(len(sl)):
            if len(sl[i]["horse_race_list"]) > 0:
                no_output_flg = False
                break
    for sl in source_list:
        for i in range(len(sl)):
            if check_adoptability_settings_and_source(settings,sl[i]):
                sl[i]["all_horse_past"] = [x["past_list"] for x in sl]
                single_in, single_out = dl_model_inout.make_model_in_out_list(sl[i])
                if len(single_in) > 0 and (len(single_out) > 0 and not no_output_flg or no_output_flg):
                    export_dict["input"].append(single_in)
                    if not no_output_flg:
                        export_dict["output"].append(single_out[0])
                        if len(sl[i]["horse_race_list"]) > 0:
                            gl_order = [x for x in sl[i]["horse_race_list"] if x["horsenum"] == i+1]
                            if len(gl_order) > 0:
                                export_dict["goal_order"].append(gl_order[0]["goal_order"])
                    export_dict["rdate"].append(sl[i]["rdate"])
                    export_dict["place"].append(sl[i]["place"])
                    export_dict["race"].append(sl[i]["race"])
                    export_dict["horsenum"].append(sl[i]["horsenum"])
                    export_dict["horsename"].append(sl[i]["horsename"])
    output_tools.json_export(model_name+"_input.json",export_dict)

# 日付、場所、レース番号、芝ダート、出走馬過去5走[馬番][過去走番号]、当日データ、出走馬SQLテーブルデータ[順不同馬番]を保持したリストを返す
def get_source_data_list(horse_race, settings):
    all_files = os.listdir("./")
    target_csvs = [x for x in all_files if re.match("\d+.csv_tmp",x)]
    all_list = []
    for target in target_csvs:
        print(target)
        p, t = horse_race.get_jvtarget_oneday_past_and_today_list(target)
        # 全データの使用は無駄が多く時間がかかるため、レース日から１年以内のデータのみ使用する
        horse_race.set_horse_race_dict_list("race_table.rdate between '"+t[0]['rdate']+"' - interval 400 day and '"+t[0]['rdate']+"'")
        for i in range(len(t)):
            # 時短したいため欲しいレースかチェック
            if check_adoptability_settings_and_source(settings, {"turf_dirt":t[i]["turf_dirt"],"place":t[i]["place"],"distance":int(t[i]["distance"])}):
                single_race_list = []
                r_l, hr_l = horse_race.get_single_race_and_horse_race_list(t[i]['rdate'],t[i]['place'],int(t[i]['race']))
                for j in range(len(p[i])):
                    horsename = p[i][j][0]["horsename"] if len(p[i][j]) > 0 else ""
                    history = horse_race.get_history_single_horse_list_without_newer_day(horsename,t[i]['rdate']) if len(p[i][j]) > 0 else []
                    single_horse_dict = {"rdate":t[i]['rdate'],"place":t[i]['place'],"race":int(t[i]['race']),"turf_dirt":t[i]['turf_dirt'],"distance":int(t[i]['distance']),"horsenum":j+1,"horsename":horsename,"past_list":p[i][j],"today_dict":t[i],"horse_race_list":hr_l,"history_horse_race_list":history}
                    single_race_list.append(single_horse_dict)
                all_list.append(single_race_list)
    return all_list

# settings.jsonの設定内容と合うレースのみ取り込むためのチェック
def check_adoptability_settings_and_source(settings, source):
    if not settings["turf_dirt_divide_flg"] and not settings["place_divide_flg"] and not settings["distance_divide_flg"]:
        return True
    if settings["turf_dirt_divide_flg"] and source["turf_dirt"] != settings["turf_dirt"]:
        return False
    if settings["place_divide_flg"] and source["place"] != settings["place"]:
        return False
    if settings["distance_divide_flg"] and source["distance"] != settings["distance"]:
        return False
    return True

if __name__ == "__main__":
    make_deeplearning_input_file()
