

import urllib.request, json
import urllib.parse
import datetime

# 必要モジュールのインポート
import os
from dotenv import load_dotenv

# .envファイルの内容を読み込見込む
load_dotenv()

# os.environを用いて環境変数を表示させます
print(os.environ['API_KEY'])



#Google Maps Platform Directions API endpoint
endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
# api_key = '<取得したAPIキー>'

api_key = os.environ['API_KEY']

#出発地、目的地を入力
origin = input('出発地を入力: ').replace(' ','+')
destination = input('目的地を入力: ').replace(' ','+')
dep_time = input('出発時間を入力: yyyy/mm/dd hh:mm 形式 (nowの場合はenter): ')

#UNIX時間の算出
# dtime = datetime.datetime.strptime(dep_time, '%Y/%m/%d %H:%M')
dtime = datetime.datetime.now() # 2024/03/02 追加

#dtime = dtime + datetime.timedelta(hours=9)
#print(dtime.timestamp())
unix_time = int(dtime.timestamp())

print('')
print('=====')
print('unixtime')
print(unix_time)
print('=====')

# nav_request = 'language=ja&origin={}&destination={}&departure_time={}&key={}'.format(origin,destination,unix_time,api_key)
mode = 'driving'
# mode = 'walking'
mode = 'transit'
print(f"mode : {mode}")
language = 'ja'

nav_request = 'language={}&origin={}&destination={}&departure_time={}&key={}&mode={}'.format(language, origin,destination,unix_time,api_key, mode)
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

#所要時間を取得
for key in directions['routes']:
    # print(key) # titleのみ参照
    # print(key['legs']) 
    for key2 in key['legs']:
        print('')
        print('===== legs =====')
        print(f'start :{key2['start_address']}')
        # print(key2['mode']['text'])
        print(key2['distance']['text'])
        # print(key2['duration_in_traffic']['text']) # 日本ではバス、歩き、driving modeの時のみ
        print(key2['duration']['text'])
        print(f'end : {key2['end_address']}') # ['text'])
        print("================")
        for key3 in key2['steps']:
            print('  ===== steps =====')
            print(f'  instructions(この区間の <手段> と <目的地> ) : {key3['html_instructions']}')
            print(f'  travel mode : {key3['travel_mode']}')
            print('  =================')
        print('================')
    # for key3 in key['steps']:
    #     print(key3['travel_mode'])
    #     print(key3['html_instructions'])

