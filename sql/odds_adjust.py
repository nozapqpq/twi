from tqdm import tqdm_notebook as tqdm
import pandas as pd
import time
import re
import csv
from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class OddsTable:
    def __init__(self):
        self.odds_table = pd.DataFrame()

    def scrape_odds_table(self, year, place_w, race, mm, dd):
        place_dict = {"札幌":1,"函館":2,"福島":3,"新潟":4,"東京":5,"中山":6,"中京":7,"京都":8,"阪神":9,"小倉":10}
        Base = "https://race.sp.netkeiba.com/?pid=odds_view&type=b4&race_id="
        place = place_dict[place_w]
        options= ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        driver = Chrome(executable_path=r'/home/noza/chromedriver',options=options)
        for i in range(1,9):
            multi_continue = 0
            for j in range(1,13):
                if multi_continue > 0:
                    multi_continue = multi_continue - 1
                    continue
                url = Base + str(year) + self.numStr(place) + self.numStr(i) + self.numStr(j) + self.numStr(race) + "&housiki=c0&rf=shutuba_submenu"
                driver.get(url)

                # 指定した日付に対応する開催回・日を見つける
                racedetail_elements = driver.find_elements_by_class_name('Race_Detail_Info_Btn')
                if racedetail_elements == []:
                    continue
                CommonDate = racedetail_elements[0].find_elements_by_class_name('Change_Btn')[0].text if "Day" in racedetail_elements[0].find_elements_by_class_name('Change_Btn')[0].get_attribute('class') else ""
                splitted = re.split(r"/|\(", CommonDate)
                CommonMM = int(splitted[0])
                CommonDD = int(splitted[1])
                if CommonMM < mm-1:
                    break
                if CommonMM != mm or CommonDD != dd:
                    date_diff = dd-CommonDD
                    if CommonMM != mm:
                        date_diff = date_diff + 31
                    if date_diff > 7:
                        multi_continue = (int(date_diff/7)-1)*2
                        #print(str(multi_continue)+"days skip")
                    continue

                # オッズテーブルを作成する
                elements = driver.find_elements_by_class_name('RaceOdds_HorseList_Table')
                horsenum1 = 1
                horsenum2 = 0
                odds = 0
                odds_list = []
                for element in elements:
                    tds = element.find_elements_by_tag_name('td')
                    for td in tds:
                        if "Waku_Normal" in td.get_attribute('class'):
                            if int(td.text) <= horsenum2:
                                horsenum1 = horsenum1 + 1
                            horsenum2 = int(td.text)
                        if "Odds" in td.get_attribute('class'):
                            if td.text in ["取消","除外","中止"]:
                                odds_list.append({"num1":horsenum1,"num2":horsenum2,"odds":0})
                                odds_list.append({"num1":horsenum2,"num2":horsenum1,"odds":0})
                            else:
                                odds = float(td.text)
                                odds_list.append({"num1":horsenum1,"num2":horsenum2,"odds":odds})
                                odds_list.append({"num1":horsenum2,"num2":horsenum1,"odds":odds})
                time.sleep(1)
                driver.close()
                return odds_list

    def numStr(self, num):
        if num >= 10:
            return str(num)
        else:
            return '0' + str(num)

with open("../deeplearning_favorite_horses.csv","r") as f:
    fav_list = []
    reader = csv.reader(f)
    count = 0
    for row in reader:
        if count != 0:
            fav_list.append(row)
        count = count + 1

budget = 3000
date_splitted = re.split(r"-|\s", fav_list[0][5])
print(date_splitted)
year = int(date_splitted[0])
mm = int(date_splitted[1])
dd = int(date_splitted[2])
ot = OddsTable()

for fav in fav_list:
    # オッズテーブルを取得
    place = fav[3]
    race = int(fav[2])
    favorite_horse = int(fav[4])
    print(place+":"+str(race))
    odds_list = ot.scrape_odds_table(year,place,race,mm,dd)

    # 買い目の決定
    exclusion_list = []
    favorite_horse = int(fav[4])
    total_count = 0
    for i in range(7,len(fav)):
        if (i-7)%3 == 2:
            total_count = total_count + 1
            if float(fav[i]) <= 0.15:
                exclusion_list.append(fav[i-1])
    if total_count > 18:
        print("1開催日に対して実行してください")
        continue
    print(total_count)
    buy_list = []
    for t in range(total_count):
        if t+1 != favorite_horse:
            buy_candidate = [x for x in odds_list if x["num1"] == favorite_horse and x["num2"] == t+1][0]
            if not (t+1 in exclusion_list or buy_candidate["odds"] == 0):
                buy_list.append(buy_candidate)
    # 合成オッズ計算
    bunbo = 0
    for buy in buy_list:
        bunbo = bunbo + 1/buy["odds"]
    sync_odds = round(1/bunbo,2)
    print("合成オッズ : "+str(sync_odds))
    # 何円買うか
    for buy in buy_list:
        buy["bet"] = int(round(budget*sync_odds/buy["odds"],-1))
        print(buy)

