# coding: utf-8

class Utility():
    def __init__(self):
        i=0

    def get_deep_model_name(self, settings):
        place_list = ["札幌","函館","福島","新潟","中山","東京","中京","京都","阪神","小倉"]
        td_list = ["芝","ダート"]
        if settings["place_divide_flg"] == False and settings["turf_dirt_divide_flg"] == False:
            return "deep_model000"
        if settings["place_divide_flg"] == False or settings["place"] == "":
            p_index = 99
        else:
            p_index = place_list.index(settings["place"])
        if settings["turf_dirt_divide_flg"] == False or settings["turf_dirt"] == "":
            td_index = 9
        else:
            td_index = td_list.index(settings["turf_dirt"])
        if settings["distance_divide_flg"] == False or settings["distance"] == 0:
            dist_index = 9999
        else:
            dist_index = settings["distance"]
        return "deep_model"+str(p_index).zfill(2)+str(td_index)+str(dist_index)

