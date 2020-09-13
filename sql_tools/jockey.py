# coding: utf-8
import os
import sys
import re
import sql_manipulator
import utility
import statistics
import math

class Jockey():
    def __init__(self):
        self.sql = sql_manipulator.SQLManipulator()
        self.utl = utility.Utility()
        self.small_turn_list = ["札幌","函館","福島","中山","小倉"]
        self.jockey_list = []
        self.jockey_list_miho = ["秋山稔樹","五十嵐雄","石神深一","石川裕紀","石橋脩","伊藤工真","井上敏樹","岩部純二","上野翔","内田博幸","江田照男","江田勇亮","蛯名正義","大江原圭","大塚海渡","大野拓弥","大庭和弥","小野寺祐","勝浦正樹","嘉藤貴行","金子光希","菊沢一樹","北村宏司","草野太郎","小林脩斗","小林凌大","木幡育也","木幡巧也","木幡初也","柴田大知","柴田善臣","嶋田純次","菅原隆一","菅原明良","杉原誠人","鈴木慶太","高野和馬","田中勝春","田辺裕信","丹内祐次","津村明秀","戸崎圭太","西田雄一","西村太一","野中悠太","原優介","原田和真","伴啓太","武士沢友","藤田菜七","松岡正海","的場勇人","黛弘人","丸田恭介","丸山元気","三浦皇成","蓑島靖典","宮崎北斗","武藤雅","村田一誠","山田敬士","山本康志","横山和生","横山武史","横山典弘","吉田隼人","吉田豊"]
        self.jockey_list_ritto = ["秋山真一","池添謙一","泉谷楓真","岩田望来","岩田康誠","植野貴也","岡田祥嗣","荻野極","荻野琢真","加藤祥太","亀田温心","川島信二","川須栄彦","川田将雅","川又賢治","北沢伸也","北村友一","城戸義政","熊沢重文","黒岩悠","国分恭介","国分優作","小坂忠士","小崎綾也","小牧太","斎藤新","酒井学","坂井瑠星","佐久間寛","鮫島克駿","鮫島良太","四位洋文","柴田未崎","柴山雄一","白浜雄造","高倉稜","高田潤","武豊","竹之下智","太宰啓介","田中健","田村太雅","団野大成","Ｍ．デム","富田暁","中居裕二","長岡禎仁","中谷雄太","中村将之","難波剛健","西谷誠","西村淳也","畑端省吾","服部寿希","浜中俊","菱田裕二","平沢健治","福永祐一","藤井勘一","藤岡康太","藤岡佑介","藤懸貴志","古川吉洋","松田大作","松山弘平","松若風馬","水口優也","三津谷隼","幸英明","森一馬","森裕太郎","ルメール","和田翼","和田竜二"]
        self.jockey_list_local = ["阿部龍","石川慎将","石川倭","岩橋勇二","岡部誠","落合玄太","鴨宮祥行","桑村真明","小松丈二","笹川翼","佐藤友則","鮫島克也","繁田健一","竹吉徹","田中純","服部茂史","藤原幹生","真島大輔","御神本訓","本橋孝太","森泰斗","山口勲","山本咲希","吉村智洋"]
        self.jockey_list_foreign = ["シュタル","ヒューイ","フォーリ","マーフィ","ミナリク","レーン","モレイラ","デットー"]
        self.jockey_list = self.jockey_list_miho+self.jockey_list_ritto+self.jockey_list_local+self.jockey_list_foreign
        self.distance_short_list = [False,True]
        self.small_turn_list = [False,True]
        self.turf_dirt_list = ["ダート","芝"]
        self.database = self.sql.get_horse_race_data("odds<=10.0 and race_table.rdate between '2016-01-01' and '2020-07-31';")

    def add_jockey_table(self):
        border = 0
        belongs = "不明"
        for jk in self.jockey_list:
            if jk in self.jockey_list_miho:
                belongs = "美浦"
            elif jk in self.jockey_list_ritto:
                belongs = "栗東"
            elif jk in self.jockey_list_local:
                belongs = "地方"
            elif jk in self.jockey_list_foreign:
                belongs = "海外"
            single_scores = []
            for sturn in self.small_turn_list:
                for td in self.turf_dirt_list:
                    for dist in self.distance_short_list:
                        app = self.get_approach_rate(jk,td,dist,sturn)
                        single_scores.append(app)
            self.sql.sql_manipulator("insert into jockey_table values ('"+jk+"','"+belongs+"',"+str(single_scores[0])+","+str(single_scores[1])+","+str(single_scores[2])+","+str(single_scores[3])+","+str(single_scores[4])+","+str(single_scores[5])+","+str(single_scores[6])+","+str(single_scores[7])+");")

    def get_approach_rate(self, jockey_name, td, dist_short_flg, small_turn):
        match_all_list = [x for x in self.database if x['jockey_name']==jockey_name and x['turf_dirt']==td]
        if small_turn:
            match_all_list = [x for x in match_all_list if "[G003]" in x['course_mark']]
        if dist_short_flg:
            match_all_list = [x for x in match_all_list if x['distance']>=1000 and x['distance']<=1400]
        else:
            match_all_list = [x for x in match_all_list if x['distance']>=1500 and x['distance']<=2400]
        match_good_list = [x for x in match_all_list if x['time_diff']<=0.3]
        if len(match_all_list) > 0:
            return round(len(match_good_list)/len(match_all_list)*100,1)
        else:
            return 0

jk = Jockey()
jk.add_jockey_table()
