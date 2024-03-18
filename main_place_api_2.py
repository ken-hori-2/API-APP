
import googlemaps
import pprint # list型やdict型を見やすくprintするライブラリ

# key = 'Your API' # 上記で作成したAPIキーを入れる

# 必要モジュールのインポート
import os
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()

# os.environを用いて環境変数を表示させます
print(os.environ['API_KEY'])

key = os.environ['API_KEY']





client = googlemaps.Client(key) #インスタンス生成

geocode_result = client.geocode('東京都大森駅') # 位置情報を検索
loc = geocode_result[0]['geometry']['location'] # 軽度・緯度の情報のみ取り出す

# # place_result = client.places_nearby(location=loc, radius=200, type='food') #半径200m以内のレストランの情報を取得
# place_result = client.places_nearby(location=loc, radius=100, type='food') #半径100m以内のレストランの情報を取得
# pprint.pprint(place_result)

import pandas as pd

# # place_result.to_csv('test.csv')




url =  'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'

import urllib.request, json
import urllib.parse
import datetime
#Google Maps Platform Directions API endpoint
endpoint = url
# api_key = '<取得したAPIキー>'
api_key = key

#出発地、目的地を入力
# origin = input('出発地を入力: ').replace(' ','+')
# destination = input('目的地を入力: ').replace(' ','+')
# dep_time = input('出発時間を入力: yyyy/mm/dd hh:mm 形式 (nowの場合はenter): ')

#UNIX時間の算出
# dtime = datetime.datetime.strptime(dep_time, '%Y/%m/%d %H:%M')
dtime = datetime.datetime.now() # 2024/03/02 追加

#dtime = dtime + datetime.timedelta(hours=9)
#print(dtime.timestamp())
unix_time = int(dtime.timestamp())

# # nav_request = 'language=ja&origin={}&destination={}&departure_time={}&key={}'.format(origin,destination,unix_time,api_key)
# mode = 'driving'
# # mode = 'walking'
# # mode = 'transit'
# print(f"mode : {mode}")
language = 'en' # 'ja'

loc_x = 35.5688551
loc_y = 139.7395562
# 35.6987769,139.76471
lange = 200 # 300

# nav_request = 'language={}&origin={}&destination={}&departure_time={}&key={}&mode={}'.format(language, origin,destination,unix_time,api_key, mode)
nav_request = 'key={}&location={},{}&radius={}&language={}&keyword={}OR{}'.format(api_key, loc_x, loc_y, lange, language, 'カフェ', 'レストラン') # OR{} '公園', 'レストラン', '駅')
nav_request = urllib.parse.quote_plus(nav_request, safe='=&')
request = endpoint + nav_request

print('')
print('=====')
print('url')
print(request)
print('=====')

#Google Maps Platform Directions APIを実行
response = urllib.request.urlopen(request).read()

#結果(JSON)を取得
directions = json.loads(response)
# pprint.pprint(directions)

#所要時間を取得
name_list = []
# df = pd.DataFrame(index=['rating', 'user com num'])
df = pd.DataFrame(index=['place name', 'rating', 'user comments num'])

i = 0
for key in directions['results']:
    # print(key) # titleのみ参照
    # print(key['legs']) 
    # for key2 in key['name']:
    #     # print('')
    #     # print('===== name =====')
    #     # print(f'start :{key2['start_address']}')
    #     # # print(key2['mode']['text'])
    #     # print(key2['distance']['text'])
    #     # # print(key2['duration_in_traffic']['text']) # 日本ではバス、歩き、driving modeの時のみ
    #     # print(key2['duration']['text'])
    #     # print(f'end : {key2['end_address']}') # ['text'])
    #     # print("================")
    #     # for key3 in key2['steps']:
    #     #     print('  ===== steps =====')
    #     #     print(f'  instructions(この区間の <手段> と <目的地> ) : {key3['html_instructions']}')
    #     #     print(f'  travel mode : {key3['travel_mode']}')
    #     #     print('  =================')
    #     # print('================')
    #     print(key2)
    # # for key3 in key['rating']:
    # #     print(key3)
    print('===== name =====')
    print(key['name'])
    # name_list.append(key['name'])
    
    print(key['types'])
    try:
        print(f'price level : {key['price_level']}')
    except:
        print('not price place !')
    # print('===== rating =====')
    # print('☆')
    # print(key['rating'])
    print(f'★{key['rating']}')
    
    print(f'user_ratings_total : {key['user_ratings_total']}')
    # for key3 in key['rating']:
    #     print(key3)
    print('================')
    # pprint.pprint(key)
    # df[key['name']] = [key['rating'], key['user_ratings_total']]
    df[i] = [key['name'], key['rating'], key['user_ratings_total']]
    # df.set_index(['rate'], ['user com num'])

    i += 1

print("*****")
print(df)
import pyttsx3

engine = pyttsx3.init()
# engine.say("こんにちは。こんばんは。")
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[1].id)

rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)

# engine.setProperty('volume', 音量) # 0.0 ~ 1.0
engine.setProperty('volume', 1.0) # 0.0 ~ 1.0

# with open("file.txt",encoding="utf-8") as f:
#     s = f.read()
#     engine.save_to_file(s , 'japan.mp3')
#     engine.say(s)

i = 0
test = []
for key in directions['results']:
    # engine.say(df[key['name']])

    # engine.say(df[i]) # 実行中にアナウンス
    test.append(df[i]) # mp3に出力するためにtestに格納
    i += 1

engine.save_to_file(test , 'Guidance.mp3')
df.to_csv('Table.csv')
engine.runAndWait()