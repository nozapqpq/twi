# coding: utf-8
import os
import sys
import re
import sql_manipulator

class Stallion():
    def __init__(self):
        self.sql = sql_manipulator.SQLManipulator()
        self.stallion_list1 = [["ディープインパクト","ロイヤルチャージャー系","その他","ニアークティック系","その他"],["ロードカナロア","ネイティヴダンサー系","ニアークティック系","ニアークティック系","セントサイモン系"],["ハーツクライ","ロイヤルチャージャー系","その他","ナスルーラ系","ニアークティック系"],["ルーラーシップ","ネイティヴダンサー系","ニアークティック系","ナスルーラ系","ニアークティック系"],["オルフェーヴル","ロイヤルチャージャー系","その他","トウルビヨン系","ニアークティック系"],["キングカメハメハ","ネイティヴダンサー系","ニアークティック系","ニアークティック系","トウルビヨン系"],["ダイワメジャー","ロイヤルチャージャー系","その他","ニアークティック系","その他"],["ヘニーヒューズ","ニアークティック系","その他","セントサイモン系","マンノウォー系"],["ゴールドアリュール","ロイヤルチャージャー系","その他","ニアークティック系","ニアークティック系"],["キンシャサノキセキ","ロイヤルチャージャー系","セントサイモン系","セントサイモン系","ニアークティック系"],["ハービンジャー","ニアークティック系","ニアークティック系","ネイティヴダンサー系","ニアークティック系"],["クロフネ","ニアークティック系","セントサイモン系","その他","ニアークティック系"],["ヴィクトワールピサ","ロイヤルチャージャー系","ネイティヴダンサー系","ネイティヴダンサー系","その他"],["ステイゴールド","ロイヤルチャージャー系","その他","その他","ニアークティック系"],["サウスヴィグラス","ネイティヴダンサー系","ニアークティック系","ナスルーラ系","ナスルーラ系"],["キズナ","ロイヤルチャージャー系","ニアークティック系","ニアークティック系","その他"],["ジャスタウェイ","ロイヤルチャージャー系","ナスルーラ系","ニアークティック系","その他"],["スクリーンヒーロー","ロイヤルチャージャー系","ニアークティック系","ロイヤルチャージャー系","ニアークティック系"],["エイシンフラッシュ","ネイティヴダンサー系","その他","その他","ネイティヴダンサー系"],["ブラックタイド","ロイヤルチャージャー系","その他","ニアークティック系","その他"],["アイルハヴアナザー","ネイティヴダンサー系","ネイティヴダンサー系","ロイヤルチャージャー系","セントサイモン系"],["パイロ","ナスルーラ系","ネイティヴダンサー系","ニアークティック系","その他"],["エピファネイア","ロイヤルチャージャー系","ナスルーラ系","ロイヤルチャージャー系","ニアークティック系"],["ノヴェリスト","その他","その他","ニアークティック系","ニアークティック系"],["エンパイアメーカー","ネイティヴダンサー系","セントサイモン系","ニアークティック系","マンノウォー系"],["ディープブリランテ","ロイヤルチャージャー系","ニアークティック系","ナスルーラ系","その他"],["タートルボウル","ニアークティック系","ロイヤルチャージャー系","その他","ナスルーラ系"],["ネオユニヴァース","ロイヤルチャージャー系","その他","ネイティヴダンサー系","セントサイモン系"],["シニスターミニスター","ナスルーラ系","その他","ニアークティック系","ロイヤルチャージャー系"],["マンハッタンカフェ","ロイヤルチャージャー系","その他","セントサイモン系","その他"],["ヨハネスブルグ","ニアークティック系","その他","その他","ネイティヴダンサー系"],["メイショウボーラー","ロイヤルチャージャー系","ニアークティック系","ニアークティック系","ナスルーラ系"],["スマートファルコン","ロイヤルチャージャー系","ニアークティック系","その他","ネイティヴダンサー系"],["ダンカーク","ネイティヴダンサー系","ナスルーラ系","ナスルーラ系","ネイティヴダンサー系"],["アドマイヤムーン","ネイティヴダンサー系","ニアークティック系","ロイヤルチャージャー系","ネイティヴダンサー系"],["カジノドライヴ","ナスルーラ系","ネイティヴダンサー系","ニアークティック系","ナスルーラ系"],["ワークフォース","ネイティヴダンサー系","その他","ニアークティック系","セントサイモン系"],["ゴールドシップ","ロイヤルチャージャー系","その他","トウルビヨン系","ニアークティック系"],["シンボリクリスエス","ロイヤルチャージャー系","セントサイモン系","ナスルーラ系","その他"],["エスポワールシチー","ロイヤルチャージャー系","ニアークティック系","ロイヤルチャージャー系","ナスルーラ系"]]
        self.stallion_list2 = [["キングズベスト","ネイティヴダンサー系","ニアークティック系","その他","その他"],["カネヒキリ","ロイヤルチャージャー系","セントサイモン系","ニアークティック系","ネイティヴダンサー系"],["スウェプトオーヴァーボード","ネイティヴダンサー系","ニアークティック系","その他","トウルビヨン系"],["ゼンノロブロイ","ロイヤルチャージャー系","その他","ネイティヴダンサー系","ニアークティック系"],["マツリダゴッホ","ロイヤルチャージャー系","その他","ナスルーラ系","ネイティヴダンサー系"],["ロージズインメイ","ロイヤルチャージャー系","ネイティヴダンサー系","セントサイモン系","その他"],["ジャングルポケット","ナスルーラ系","その他","ニアークティック系","その他"],["ベルシャザール","ネイティヴダンサー系","ニアークティック系","ロイヤルチャージャー系","ニアークティック系"],["マジェスティックウォーリアー","ナスルーラ系","ナスルーラ系","ネイティヴダンサー系","ニアークティック系"],["メイショウサムソン","ニアークティック系","その他","ニアークティック系","ナスルーラ系"],["モンテロッソ","ネイティヴダンサー系","ナスルーラ系","ニアークティック系","その他"],["ダノンシャンティ","ロイヤルチャージャー系","セントサイモン系","ナスルーラ系","ロイヤルチャージャー系"],["トーセンホマレボシ","ロイヤルチャージャー系","ニアークティック系","ニアークティック系","ネイティヴダンサー系"],["ドリームジャーニー","ロイヤルチャージャー系","その他","トウルビヨン系","ニアークティック系"],["トゥザグローリー","ネイティヴダンサー系","ニアークティック系","ロイヤルチャージャー系","ニアークティック系"],["リアルインパクト","ロイヤルチャージャー系","ニアークティック系","セントサイモン系","マンノウォー系"],["ベーカバド","ニアークティック系","トウルビヨン系","ネイティヴダンサー系","ナスルーラ系"],["ヴァーミリアン","ネイティヴダンサー系","ニアークティック系","ロイヤルチャージャー系","ニアークティック系"],["カレンブラックヒル","ロイヤルチャージャー系","ニアークティック系","ネイティヴダンサー系","ニアークティック系"],["プリサイスエンド","ネイティヴダンサー系","ニアークティック系","セントサイモン系","ナスルーラ系"],["キングヘイロー","ニアークティック系","ロイヤルチャージャー系","ロイヤルチャージャー系","ロイヤルチャージャー系"],["フリオーソ","ロイヤルチャージャー系","セントサイモン系","ネイティヴダンサー系","ニアークティック系"],["ストロングリターン","ロイヤルチャージャー系","ナスルーラ系","ネイティヴダンサー系","ニアークティック系"],["エスケンデレヤ","ニアークティック系","ナスルーラ系","ナスルーラ系","ネイティヴダンサー系"],["バトルプラン","ネイティヴダンサー系","ニアークティック系","ネイティヴダンサー系","ニアークティック系"],["ローエングリン","ニアークティック系","ロイヤルチャージャー系","ナスルーラ系","セントサイモン系"],["グランプリボス","ナスルーラ系","ニアークティック系","ロイヤルチャージャー系","ナスルーラ系"],["タイキシャトル","ロイヤルチャージャー系","その他","ニアークティック系","その他"],["トランセンド","ニアークティック系","セントサイモン系","ナスルーラ系","ニアークティック系"],["ケープブランコ","ニアークティック系","ネイティヴダンサー系","ナスルーラ系","セントサイモン系"],["リーチザクラウン","ロイヤルチャージャー系","ニアークティック系","ナスルーラ系","ネイティヴダンサー系"],["ディープスカイ","ロイヤルチャージャー系","ナスルーラ系","ニアークティック系","セントサイモン系"],["バゴ","ナスルーラ系","その他","ニアークティック系","ネイティヴダンサー系"],["フェノーメノ","ロイヤルチャージャー系","その他","ニアークティック系","その他"],["Frankel","ニアークティック系","ネイティヴダンサー系","ニアークティック系","ナスルーラ系"],["アグネスデジタル","ネイティヴダンサー系","マンノウォー系","ニアークティック系","セントサイモン系"],["ケイムホーム","ネイティヴダンサー系","ナスルーラ系","ニアークティック系","ナスルーラ系"]]
        self.stallion_list3 = [["ローズキングダム","ネイティヴダンサー系","ニアークティック系","ロイヤルチャージャー系","ナスルーラ系"],["アサクサキングス","ニアークティック系","その他","ロイヤルチャージャー系","ナスルーラ系"],["ワールドエース","ロイヤルチャージャー系","ニアークティック系","その他","ニアークティック系"],["トビーズコーナー","ニアークティック系","その他","その他","ネイティヴダンサー系"],["ジョーカプチーノ","ロイヤルチャージャー系","セントサイモン系","ニアークティック系","ナスルーラ系"],["ロジユニヴァース","ロイヤルチャージャー系","ネイティヴダンサー系","ニアークティック系","ネイティヴダンサー系"],["アポロキングダム","ネイティヴダンサー系","ナスルーラ系","ニアークティック系","ニアークティック系"],["ストーミングホーム","ネイティヴダンサー系","ロイヤルチャージャー系","ニアークティック系","ネイティヴダンサー系"],["タニノギムレット","ロイヤルチャージャー系","セントサイモン系","ナスルーラ系","ネイティヴダンサー系"],["フレンチデピュティ","ニアークティック系","その他","セントサイモン系","ナスルーラ系"],["トーセンラー","ロイヤルチャージャー系","ニアークティック系","ネイティヴダンサー系","ニアークティック系"],["トゥザワールド","ネイティヴダンサー系","ニアークティック系","ロイヤルチャージャー系","ニアークティック系"],["サマーバード","ネイティヴダンサー系","ニアークティック系","ニアークティック系","ネイティヴダンサー系"],["ナカヤマフェスタ","ロイヤルチャージャー系","その他","セントサイモン系","ニアークティック系"],["Speightstown","ネイティヴダンサー系","ナスルーラ系","ニアークティック系","ナスルーラ系"],["スズカコーズウェイ","ニアークティック系","ナスルーラ系","ニアークティック系","ナスルーラ系"],["トーセンジョーダン","ナスルーラ系","ニアークティック系","ニアークティック系","ネイティヴダンサー系"],["スズカマンボ","ロイヤルチャージャー系","その他","ネイティヴダンサー系","ニアークティック系"],["ストリートセンス","ネイティヴダンサー系","その他","ニアークティック系","セントサイモン系"],["アルデバラン2","ネイティヴダンサー系","ナスルーラ系","その他","ニアークティック系"],["ダノンバラード","ロイヤルチャージャー系","ニアークティック系","ネイティヴダンサー系","ロイヤルチャージャー系"],["ショウナンカンプ","ナスルーラ系","ニアークティック系","ニアークティック系","その他"],["Uncle Mo","ナスルーラ系","ニアークティック系","ロイヤルチャージャー系","ニアークティック系"],["Tapit","ナスルーラ系","ネイティヴダンサー系","ネイティヴダンサー系","ニアークティック系"],["レッドスパーダ","ロイヤルチャージャー系","ニアークティック系","ニアークティック系","ロイヤルチャージャー系"],["スズカフェニックス","ロイヤルチャージャー系","その他","ニアークティック系","セントサイモン系"],["American Pharoah","ネイティヴダンサー系","その他","ニアークティック系","ネイティヴダンサー系"],["サムライハート","ロイヤルチャージャー系","その他","ナスルーラ系","ニアークティック系"],["ホワイトマズル","ニアークティック系","ロイヤルチャージャー系","その他","ナスルーラ系"],["ロードアルティマ","ネイティヴダンサー系","その他","ナスルーラ系","その他"],["ハードスパン","ニアークティック系","その他","ネイティヴダンサー系","ロイヤルチャージャー系"],["タイムパラドックス","ロイヤルチャージャー系","セントサイモン系","ニアークティック系","ナスルーラ系"],["ノボジャック","ニアークティック系","セントサイモン系","ネイティヴダンサー系","ロイヤルチャージャー系"],["ヴァンセンヌ","ロイヤルチャージャー系","ニアークティック系","ロイヤルチャージャー系","ニアークティック系"],["ドゥラメンテ","ネイティヴダンサー系","ニアークティック系","ロイヤルチャージャー系","ナスルーラ系"],["スピルバーグ","ロイヤルチャージャー系","ニアークティック系","ネイティヴダンサー系","ニアークティック系"]]
        self.stallion_list4 = [["グラスワンダー","ロイヤルチャージャー系","その他","ニアークティック系","セントサイモン系"],["Into Mischief","ニアークティック系","ネイティヴダンサー系","ニアークティック系","ロイヤルチャージャー系"],["Declaration of War","ニアークティック系","ネイティヴダンサー系","ナスルーラ系","ネイティヴダンサー系"],["Shamardal","ニアークティック系","ナスルーラ系","ネイティヴダンサー系","その他"],["モーリス","ロイヤルチャージャー系","ロイヤルチャージャー系","ニアークティック系","ニアークティック系"],["キャプテントゥーレ","ロイヤルチャージャー系","ナスルーラ系","ナスルーラ系","ニアークティック系"],["ローレルゲレイロ","ニアークティック系","ロイヤルチャージャー系","ニアークティック系","ネイティヴダンサー系"],["Fastnet Rock","その他","その他","その他","その他"],["パドトロワ","ネイティヴダンサー系","その他","ロイヤルチャージャー系","ナスルーラ系"],["Daiwa Major","ロイヤルチャージャー系","その他","ニアークティック系","その他"],["アドマイヤオーラ","ロイヤルチャージャー系","ナスルーラ系","ニアークティック系","ロイヤルチャージャー系"],["アドマイヤマックス","ロイヤルチャージャー系","その他","ニアークティック系","トウルビヨン系"],["シングンオペラ","ニアークティック系","その他","その他","その他"],["Dubawi","ネイティヴダンサー系","ニアークティック系","ナスルーラ系","ニアークティック系"],["トーセンファントム","ロイヤルチャージャー系","ネイティヴダンサー系","ナスルーラ系","ニアークティック系"],["Malibu Moon","ナスルーラ系","ナスルーラ系","ネイティヴダンサー系","ニアークティック系"],["アンライバルド","ロイヤルチャージャー系","ネイティヴダンサー系","ニアークティック系","その他"],["War Front","ニアークティック系","その他","ネイティヴダンサー系","その他"],["Scat Daddy","ニアークティック系","その他","ネイティヴダンサー系","ニアークティック系"],["Pioneerof the Nile","ネイティヴダンサー系","ニアークティック系","その他","ナスルーラ系"],["Will Take Charge","ネイティヴダンサー系","ナスルーラ系","ニアークティック系","ネイティヴダンサー系"],["Bernerdini","ナスルーラ系","ナスルーラ系","ネイティヴダンサー系","ナスルーラ系"],["Cairo Prince","ネイティヴダンサー系","その他","その他","その他"],["Shanghai Bobby","ニアークティック系","ネイティヴダンサー系","ナスルーラ系","ネイティヴダンサー系"],["ゴールドヘイロー","ロイヤルチャージャー系","その他","ネイティヴダンサー系","ニアークティック系"],["フサイチセブン","ネイティヴダンサー系","ニアークティック系","ニアークティック系","ロイヤルチャージャー系"],["Siyouni","ニアークティック系","ナスルーラ系","ニアークティック系","ネイティヴダンサー系"],["バンブーエール","ネイティヴダンサー系","その他","ナスルーラ系","ナスルーラ系"],["アーネストリー","ロイヤルチャージャー系","ニアークティック系","ナスルーラ系","ニアークティック系"],["リオンディーズ","ネイティヴダンサー系","ニアークティック系","ロイヤルチャージャー系","ニアークティック系"],["The Factor","ニアークティック系","ネイティヴダンサー系","ネイティヴダンサー系","ニアークティック系"],["Distorted Humor","ネイティヴダンサー系","セントサイモン系","ニアークティック系","ロイヤルチャージャー系"],["ミッキーアイル","ロイヤルチャージャー系","ニアークティック系","ニアークティック系","ニアークティック系"],["ブレイクランアウト","ネイティヴダンサー系","ロイヤルチャージャー系","ニアークティック系","ニアークティック系"],["Majestic Warrior","ナスルーラ系","ナスルーラ系","ネイティヴダンサー系","ニアークティック系"],["ワイルドラッシュ","ニアークティック系","その他","セントサイモン系","ロイヤルチャージャー系"],["Curlin","ネイティヴダンサー系","ロイヤルチャージャー系","ニアークティック系","ロイヤルチャージャー系"],["ファスリエフ","ニアークティック系","その他","ネイティヴダンサー系","ナスルーラ系"],["シビルウォー","ネイティヴダンサー系","その他","ニアークティック系","ナスルーラ系"],["ダンスインザダーク","ロイヤルチャージャー系","その他","ニアークティック系","セントサイモン系"],["Le Havre","ナスルーラ系","ニアークティック系","その他","セントサイモン系"],["Temple City","ロイヤルチャージャー系","セントサイモン系","ニアークティック系","ネイティヴダンサー系"],["Invincible Spirit","ニアークティック系","ロイヤルチャージャー系","ネイティヴダンサー系","セントサイモン系"]]
        self.stallion_list5 = [["Take Charge Indy","ナスルーラ系","ナスルーラ系","ニアークティック系","ネイティヴダンサー系"],["サクラプレジデント","ロイヤルチャージャー系","その他","ニアークティック系","セントサイモン系"],["ラブリーデイ","ネイティヴダンサー系","ニアークティック系","ロイヤルチャージャー系","ナスルーラ系"],["Ghostzapper","ニアークティック系","ナスルーラ系","マンノウォー系","その他"],["Animal Kingdom","ナスルーラ系","トウルビヨン系","その他","ニアークティック系"],["No Nay Never","ニアークティック系","ネイティヴダンサー系","ネイティヴダンサー系","その他"],["Spring At Last","ニアークティック系","ネイティヴダンサー系","ロイヤルチャージャー系","セントサイモン系"],["Violence","ニアークティック系","その他","ネイティヴダンサー系","ニアークティック系"],["キモンノカシワ","ロイヤルチャージャー系","ニアークティック系","ネイティヴダンサー系","ロイヤルチャージャー系"],["コンデュイット","ナスルーラ系","ネイティヴダンサー系","ニアークティック系","ナスルーラ系"],["Giant`s Causeway","ニアークティック系","ナスルーラ系","ナスルーラ系","ロイヤルチャージャー系"],["トーセンブライト","ロイヤルチャージャー系","セントサイモン系","ネイティヴダンサー系","ニアークティック系"],["Kingman","ニアークティック系","ネイティヴダンサー系","ネイティヴダンサー系","ニアークティック系"],["Point of Entry","ロイヤルチャージャー系","セントサイモン系","ネイティヴダンサー系","セントサイモン系"],["Smart Strike","ネイティヴダンサー系","ナスルーラ系","ロイヤルチャージャー系","その他"],["スペシャルウィーク","ロイヤルチャージャー系","その他","ニアークティック系","その他"],["ウインバリアシオン","ロイヤルチャージャー系","ナスルーラ系","ニアークティック系","その他"],["First Samurai","ニアークティック系","ナスルーラ系","ニアークティック系","ネイティヴダンサー系"],["Pivotal","ニアークティック系","セントサイモン系","ナスルーラ系","その他"],["ブラックタキシード","ロイヤルチャージャー系","その他","ニアークティック系","その他"],["ディスクリートキャット","ニアークティック系","セントサイモン系","その他","マンノウォー系"],["アッミラーレ","ロイヤルチャージャー系","その他","ナスルーラ系","セントサイモン系"],["エイシンアポロン","ニアークティック系","ナスルーラ系","ニアークティック系","ニアークティック系"],["Kitten`s Joy","ニアークティック系","ロイヤルチャージャー系","ロイヤルチャージャー系","その他"],["Teofilo","ニアークティック系","ネイティヴダンサー系","ニアークティック系","ネイティヴダンサー系"],["オウケンブルースリ","ナスルーラ系","ニアークティック系","ニアークティック系","ニアークティック系"],["Raven`s Pass","ネイティヴダンサー系","ニアークティック系","その他","セントサイモン系"],["Street Cry","ネイティヴダンサー系","ロイヤルチャージャー系","その他","ナスルーラ系"],["ダノンレジェンド","その他","ナスルーラ系","ニアークティック系","マンノウォー系"],["スタチューオブリバティ","ニアークティック系","ナスルーラ系","ナスルーラ系","その他"],["Golden Horn","ニアークティック系","トウルビヨン系","ネイティヴダンサー系","ニアークティック系"],["オーシャンブルー","ロイヤルチャージャー系","その他","ナスルーラ系","ニアークティック系"],["アジアエクスプレス","ニアークティック系","セントサイモン系","ナスルーラ系","ナスルーラ系"],["More Than Ready","ロイヤルチャージャー系","ニアークティック系","ネイティヴダンサー系","ナスルーラ系"]]
        self.stallion_list6 = [["New Approach","ニアークティック系","ネイティヴダンサー系","トウルビヨン系","その他"],["Tapizar","ナスルーラ系","ネイティヴダンサー系","ニアークティック系","ニアークティック系"],["Tanino Gimlet","ロイヤルチャージャー系","セントサイモン系","ナスルーラ系","ネイティヴダンサー系"],["Mineshaft","ナスルーラ系","ナスルーラ系","ネイティヴダンサー系","セントサイモン系"],["Dansili","ニアークティック系","セントサイモン系","ニアークティック系","その他"],["Dawn Approach","ニアークティック系","トウルビヨン系","ニアークティック系","セントサイモン系"],["Square Eddie","ネイティヴダンサー系","ロイヤルチャージャー系","ニアークティック系","その他"],["Gleneagles","ニアークティック系","ネイティヴダンサー系","ニアークティック系","ナスルーラ系"],["スクワートルスクワート","ネイティヴダンサー系","ニアークティック系","セントサイモン系","ロイヤルチャージャー系"],["サクラバクシンオー","ナスルーラ系","ナスルーラ系","ニアークティック系","トウルビヨン系"],["ヒルノダムール","ロイヤルチャージャー系","セントサイモン系","ニアークティック系","ニアークティック系"],["カンパニー","ナスルーラ系","ニアークティック系","ニアークティック系","ネイティヴダンサー系"],["Carpe Diem","ニアークティック系","ナスルーラ系","ネイティヴダンサー系","ニアークティック系"],["シルポート","ニアークティック系","その他","ロイヤルチャージャー系","ネイティヴダンサー系"],["ファルブラヴ","ニアークティック系","ロイヤルチャージャー系","ナスルーラ系","セントサイモン系"],["マクフィ","ネイティヴダンサー系","ナスルーラ系","ニアークティック系","ナスルーラ系"],["テイエムオペラオー","ニアークティック系","その他","ナスルーラ系","ナスルーラ系"],["ザサンデーフサイチ","ロイヤルチャージャー系","ニアークティック系","ナスルーラ系","ニアークティック系"],["フサイチリシャール","ニアークティック系","その他","ロイヤルチャージャー系","ネイティヴダンサー系"],["Exceed And Excel","ニアークティック系","セントサイモン系","ニアークティック系","その他"]]
        self.stallion_list7 = [["クレスコグランド","ロイヤルチャージャー系","ナスルーラ系","ロイヤルチャージャー系","セントサイモン系"],["Authorized","ニアークティック系","その他","ナスルーラ系","ニアークティック系"],["War Command","ニアークティック系","ネイティヴダンサー系","ロイヤルチャージャー系","セントサイモン系"],["ワンダーアキュート","ニアークティック系","ロイヤルチャージャー系","セントサイモン系","セントサイモン系"],["Blame","ロイヤルチャージャー系","ニアークティック系","ネイティヴダンサー系","ニアークティック系"],["オンファイア","ロイヤルチャージャー系","その他","ニアークティック系","その他"],["Central Banker","ネイティヴダンサー系","ニアークティック系","セントサイモン系","ロイヤルチャージャー系"],["アドマイヤコジーン","ナスルーラ系","セントサイモン系","ニアークティック系","ナスルーラ系"],["アポロソニック","ニアークティック系","ニアークティック系","ニアークティック系","ロイヤルチャージャー系"],["Rulership","ネイティヴダンサー系","ニアークティック系","ナスルーラ系","ニアークティック系"],["マヤノトップガン","ロイヤルチャージャー系","セントサイモン系","ナスルーラ系","その他"],["バーディバーディ","ロイヤルチャージャー系","セントサイモン系","ネイティヴダンサー系","セントサイモン系"],["Mastercraftsman","ニアークティック系","ネイティヴダンサー系","ネイティヴダンサー系","ニアークティック系"],["Dark Angel","ニアークティック系","トウルビヨン系","ネイティヴダンサー系","ニアークティック系"],["フジキセキ","ロイヤルチャージャー系","その他","セントサイモン系","マンノウォー系"],["Henny Hughes","ニアークティック系","その他","セントサイモン系","マンノウォー系"],["ゴスホークケン","ニアークティック系","ネイティヴダンサー系","ネイティヴダンサー系","ロイヤルチャージャー系"],["オレハマッテルゼ","ロイヤルチャージャー系","その他","ナスルーラ系","ニアークティック系"],["Run Away and Hide","ネイティヴダンサー系","マンノウォー系","ナスルーラ系","セントサイモン系"],["Mayson","ニアークティック系","ネイティヴダンサー系","ニアークティック系","その他"],["エーシンフォワード","ニアークティック系","ネイティヴダンサー系","ロイヤルチャージャー系","ナスルーラ系"],["トウケイヘイロー","ロイヤルチャージャー系","ネイティヴダンサー系","ナスルーラ系","ニアークティック系"],["Camelot","ニアークティック系","その他","ネイティヴダンサー系","ニアークティック系"],["Honor Code","ナスルーラ系","ナスルーラ系","ニアークティック系","ネイティヴダンサー系"],["スマートロビン","ロイヤルチャージャー系","ニアークティック系","ニアークティック系","ニアークティック系"],["オペラハウス","ニアークティック系","ロイヤルチャージャー系","その他","トウルビヨン系"],["トワイニング","ネイティヴダンサー系","セントサイモン系","ナスルーラ系","マンノウォー系"],["Goldencents","ニアークティック系","ニアークティック系","ネイティヴダンサー系","ナスルーラ系"],["サンライズペガサス","ロイヤルチャージャー系","その他","ロイヤルチャージャー系","ネイティヴダンサー系"],["Hard Spun","ニアークティック系","その他","ネイティヴダンサー系","ロイヤルチャージャー系"],["Tonalist","ナスルーラ系","ネイティヴダンサー系","セントサイモン系","ニアークティック系"],["エイシンヒカリ","ロイヤルチャージャー系","ニアークティック系","ニアークティック系","ナスルーラ系"],["Fed Biz","ニアークティック系","ナスルーラ系","ニアークティック系","ネイティヴダンサー系"],["Jimmy Creed","ネイティヴダンサー系","ニアークティック系","ニアークティック系","ネイティヴダンサー系"],["Graydar","ネイティヴダンサー系","ナスルーラ系","ニアークティック系","ネイティヴダンサー系"],["ティンバーカントリー","ネイティヴダンサー系","その他","その他","その他"],["グランデッツァ","ロイヤルチャージャー系","ナスルーラ系","ニアークティック系","ロイヤルチャージャー系"],["スターリングローズ","ネイティヴダンサー系","その他","ニアークティック系","その他"],["タイセイレジェンド","ネイティヴダンサー系","ニアークティック系","トウルビヨン系","ナスルーラ系"],["ハイアーゲーム","ロイヤルチャージャー系","その他","セントサイモン系","その他"],["フォーティナイナーズサン","ネイティヴダンサー系","ニアークティック系","セントサイモン系","ネイティヴダンサー系"],["ニホンピロアワーズ","ニアークティック系","その他","ロイヤルチャージャー系","ニアークティック系"],["Medaglia d`Oro","ニアークティック系","ロイヤルチャージャー系","その他","セントサイモン系"],["サウンドボルケーノ","ニアークティック系","セントサイモン系","ロイヤルチャージャー系","ニアークティック系"],["カルストンライトオ","マンノウォー系","ロイヤルチャージャー系","ナスルーラ系","ネイティヴダンサー系"],["Sea The Stars","ニアークティック系","トウルビヨン系","ネイティヴダンサー系","その他"],["ラブイズブーシェ","ロイヤルチャージャー系","セントサイモン系","トウルビヨン系","ニアークティック系"],["Noble Mission","ニアークティック系","ネイティヴダンサー系","ニアークティック系","ナスルーラ系"],["コパノリチャード","ロイヤルチャージャー系","ニアークティック系","ナスルーラ系","ニアークティック系"],["Street Sense","ネイティヴダンサー系","その他","ニアークティック系","セントサイモン系"],["サダムパテック","ロイヤルチャージャー系","セントサイモン系","ニアークティック系","ネイティヴダンサー系"],["カフェラピード","ロイヤルチャージャー系","セントサイモン系","ニアークティック系","ネイティヴダンサー系"],["マーベラスサンデー","ロイヤルチャージャー系","その他","ニアークティック系","その他"],["アスカクリチャン","ネイティヴダンサー系","ニアークティック系","ニアークティック系","ニアークティック系"],["スウィフトカレント","ロイヤルチャージャー系","その他","ネイティヴダンサー系","その他"],["Discreet Cat","ニアークティック系","セントサイモン系","その他","マンノウォー系"],["ホッコータルマエ","ネイティヴダンサー系","ニアークティック系","ナスルーラ系","ネイティヴダンサー系"],["デュランダル","ロイヤルチャージャー系","その他","ニアークティック系","その他"],["アドマイヤジャパン","ロイヤルチャージャー系","その他","ニアークティック系","ロイヤルチャージャー系"],["サンカルロ","ロイヤルチャージャー系","ナスルーラ系","ネイティヴダンサー系","ニアークティック系"],["ブライアンズタイム","ロイヤルチャージャー系","ナスルーラ系","セントサイモン系","その他"]]
        self.stallion_list = self.stallion_list1+self.stallion_list2+self.stallion_list3+self.stallion_list4+self.stallion_list5+self.stallion_list6+self.stallion_list7

    def add_stallion_table(self):
        for st in self.stallion_list:
            self.sql.sql_manipulator("insert into stallion_table values ('"+st[0]+"','"+st[1]+"','"+st[2]+"','"+st[3]+"','"+st[4]+"');")
st = Stallion()
st.add_stallion_table()
