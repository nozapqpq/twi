# coding: utf-8
import os
import sys
import re
from .sql_manipulator import SQLManipulator

class Trainer():
    def __init__(self):
        self.sql = SQLManipulator()
        self.trainer_dict_list = self.get_trainer_dict_list_from_db()
        self.trainer_list = []
        self.trainer_list_miho = ["相沢郁","青木孝文","浅野洋一","池上昌和","伊坂重信","石栗龍彦","石毛善彦","伊藤圭三","伊藤伸一","伊藤大士","稲垣幸雄","岩戸孝樹","上原博之","蛯名利弘","大江原哲","大竹正博","大和田成","小笠倫弘","尾形和幸","奥平雅士","奥村武","尾関知人","小野次郎","粕谷昌央","加藤和宏","加藤士津","加藤征弘","金成貴史","萱野浩二","菊川正達","菊沢隆徳","木村哲也","国枝栄","久保田貴","栗田徹","黒岩陽一","古賀史生","古賀慎明","小島茂之","小手川準","小西一男","小桧山悟","斎藤誠","佐藤吉勝","鹿戸雄一","清水英克","新開幸一","杉浦宏昭","鈴木慎太","鈴木伸尋","勢司和浩","高市圭二","高木登","高橋文雅","高橋裕","高橋義博","高橋祥泰","高柳瑞樹","武井亮","武市康男","竹内正洋","田島俊明","田中清隆","田中剛","田中博康","田村康仁","柄崎孝","辻哲英","土田稔","手塚貴久","天間昭一","戸田博文","中川公成","中舘英二","中野栄治","根本康広","萩原清","畠山吉宏","林徹","深山雅史","藤沢和雄","藤原辰雄","星野忍","堀宣行","堀井雅広","本間忍","牧光二","松永康利","松山将樹","的場均","水野貴広","南田美知","宮田敬介","武藤善則","宗像義忠","矢野英一","和田正一","和田勇介","和田雄二"]
        self.trainer_list_ritto = ["浅見秀一","安達昭夫","荒川義之","飯田祐史","飯田雄三","五十嵐忠","池江泰寿","池添兼雄","池添学","石坂公一","石坂正","石橋守","上村洋行","梅田智之","大久保龍","大根田裕","大橋勇樹","岡田稲男","奥村豊","音無秀孝","加用正","河内洋","川村禎彦","北出成人","木原一良","小崎憲","昆貢","今野貞一","齋藤崇史","坂口智康","作田誠二","佐々木晶","笹田和秀","鮫島一歩","四位洋文","清水久詞","庄野靖志","新谷功一","須貝尚介","杉山晴紀","杉山佳明","鈴木孝志","角居勝彦","高野友和","高橋康之","高橋義忠","高橋亮","高柳大輔","武幸四郎","武英智","田所秀孝","田中克典","谷潔","千田輝彦","茶木太樹","辻野泰之","角田晃一","寺島良","友道康夫","中内田充","中尾秀正","中竹和也","西浦勝一","西園正都","西橋豊治","西村真幸","野中賢二","橋口慎介","橋田満","長谷川浩","羽月友彦","服部利之","浜田多実","平田修","藤岡健一","藤沢則雄","本田優","牧浦充徳","牧田和弥","松下武士","松田国英","松永昌博","松永幹夫","南井克巳","宮徹","宮本博","村山明","森秀行","森田直行","安田翔伍","安田隆行","矢作芳人","山内研二","湯窪幸雄","吉岡辰弥","吉田直弘","吉村圭司","渡辺薫彦"]
        self.trainer_list_local = ["荒山勝徳","池田忠好","石川浩文","井上孝彦","小野望","角川秀樹","川田孝好","河津裕昭","斎藤正弘","坂本和也","菅原勲","須田和伸","田中正二","田中淳司","長南和宏","角田輝也","手島勝利","林和弘","桧森邦夫","福永敏","真島元徳","松本隆宏","村上正知","矢野義幸","山中尊徳","米川昇","米谷康秀","渡辺博文"]
        self.trainer_list = self.trainer_list_miho + self.trainer_list_ritto + self.trainer_list_local

    def get_trainer_dict_list(self):
        return self.trainer_dict_list

    def get_trainer_dict_list_from_db(self):
        select_msg = "select * "
        from_msg = "from trainer_table"
        msg = select_msg+from_msg+";"
        tpl = self.sql.sql_manipulator(msg)
        retlist = []
        for t in tpl:
            single_dict = {"name":t[0],"belongs":t[1]}
            retlist.append(single_dict)
        return retlist

    def add_trainer_table(self):
        border = 0
        belongs = "不明"
        for tr in self.trainer_list:
            if tr in self.trainer_list_miho:
                belongs = "美浦"
            elif tr in self.trainer_list_ritto:
                belongs = "栗東"
            elif tr in self.trainer_list_local:
                belongs = "地方"
            single_scores = []
            self.sql.sql_manipulator("insert into trainer_table values ('"+tr+"','"+belongs+"');")
#tr = Trainer()
#tr.add_trainer_table()
