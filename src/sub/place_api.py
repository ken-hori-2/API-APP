
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

geocode_result = client.geocode('東京都渋谷駅') # 位置情報を検索
loc = geocode_result[0]['geometry']['location'] # 軽度・緯度の情報のみ取り出す
place_result = client.places_nearby(location=loc, radius=200, type='food') #半径200m以内のレストランの情報を取得
pprint.pprint(place_result)

# import pandas as pd

# place_result.to_csv('test.csv')




url =  'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key=xxx&location=35.6987769,139.76471&radius=300&language=ja&keyword=公園OR広場OR駅'

