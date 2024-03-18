import urllib.request
from bs4 import BeautifulSoup
import urllib.request, json
import urllib.parse
import datetime
import csv

def getspotdata(dep_time,region,origin,csvpath):

    #行き先をURLを格納する配列(リスト)
    arrspot= []

    #いこーよの週間ランキングは1ページ 10件 x 3なので
    #これを3回繰り返す
    for i in range(1, 4):

        #URLを設定
        url = "https://iko-yo.net/rankings/regions/" + str(region) + "/weekly?page=" + str(i)

        #URLリンクを開く
        response = urllib.request.urlopen(url)
        html = response.read()

        # htmlをBeautifulSoupで扱う
        soup = BeautifulSoup(html, "html.parser")

        # a 要素全てをリストに格納
        span = soup.find_all("a")

        #取得件数のカウント件数の初期化
        i = 0

        #a 要素全てを確認して、名称とURLを取得
        for tag in span:

            #a 要素にある classの値を取得
            tagstring = tag.get("class")

            #class がないのはNone で返るのでその対応
            if tagstring is not None:

                #c-link--underlineがあるかの判断
                if tagstring.count("c-link--underline") > 0:

                    target = tag.string

                    #口コミ　○○件 のclassも"c-link--underline" なので除外
                    if target.find("口コミ") == -1 :

                        #取得件数のカウント
                        i += 1

                        #リストに行き先名、情報リンクを取得、格納する
                        #print(tag.string)
                        #print(tag.get("href"))
                        arrspot.append([tag.string, "https://iko-yo.net" + tag.get("href")])                

                        #1ページあたり10件の情報なので、10件取得したら処理を抜ける
                        if i > 9:
                            break


    #Google Maps Platform Direction API から情報取得

    #Google MapsDdirections API endpoint
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    # api_key = '<申請したAPIキーを設定>'
    # 必要モジュールのインポート
    import os
    from dotenv import load_dotenv

    # .envファイルの内容を読み込見込む
    load_dotenv()

    # os.environを用いて環境変数を表示させます
    print(os.environ['API_KEY'])
    api_key = os.environ['API_KEY']

    #google map url 
    googlemap_api = "https://www.google.com/maps/dir/?api=1"

    #出発時間をいれたURL
    googlemap_uncertify = "https://www.google.com/maps/dir/"

    #UNIX時間の算出
    dtime = datetime.datetime.strptime(dep_time, '%Y/%m/%d %H:%M')
    plus_jst = dtime + datetime.timedelta(hours=9) #JSTなので +9時間
    unix_time = int(dtime.timestamp()) #UNIX時間を算出
    plus_jst  = int(plus_jst.timestamp()) #UNIX時間をJSTで算出 ※GoogleMapのURLに設定する


    #現在時間のUNIX時間算出
    now = datetime.datetime.now()
    #now = now + datetime.timedelta(hours=9) #JSTなので +9時間
    now_ts = int(now.timestamp())    

    #指定した時間が現在よりも過去の場合、現在時間を設定
    if now_ts > unix_time:
        unix_time = now_ts   
        dep_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M')

    #csv出力用リスト
    datalist=[]
    datalist.append(['ランキング','行き先','行き先情報リンク','距離','所要時間','GoogleMapリンク','出発時間(' + str(dep_time) + ')設定 GoogleMapリンク'])


    #１～30位までの行き先の所要時間を Direction API から取得する
    ranking =0

    for s in arrspot:

        #目的地を取得
        destination=s[0].replace(' ','+')

        #Building the URL for the request
        nav_request = 'language=ja&origin={}&destination={}&departure_time={}&key={}'.format(origin,destination,unix_time,api_key)
        nav_request = urllib.parse.quote_plus(nav_request, safe='=&')
        request = endpoint + nav_request

        #Sends the request and reads the response.
        response = urllib.request.urlopen(request).read()   

        #Loads response as JSON
        directions = json.loads(response)

        for key in directions['routes']:
            #print(key) # titleのみ参照
            #print(key['legs']) 
            for key2 in key['legs']:
                print(destination + " : " + key2['duration_in_traffic']['text'])               

                #Google Maps URLs を参考にしたURL
                googlemapurl_p = '&origin={}&destination={}&travelmode=driving'.format(origin,destination)
                googlemap_url = googlemap_api + googlemapurl_p

                #出発時間を設定したURL 
                googlemap_uncertify_p ='{}/{}/data=!4m6!4m5!2m3!6e0!7e2!8j{}!3e0'.format(origin,destination,plus_jst)
                googlemap_url_uncertify = googlemap_uncertify + googlemap_uncertify_p

                #行き先リンク
                #'=HYPERLINK を埋め込む設定
                spoturl='=HYPERLINK("' + s[1] +'","リンク")'
                gglmap ='=HYPERLINK("' + googlemap_url +'","リンク")'
                gglmap_u ='=HYPERLINK("' + googlemap_url_uncertify +'","リンク")'
                ranking += 1

                datalist.append([ranking,s[0], spoturl,key2['distance']['text'],key2['duration_in_traffic']['text'], gglmap,gglmap_u]) 

    #CSV出力
    csvpath = r"'"+ csvfile + "'"
    csvpath = csvpath.replace("'","")

    with open(csvpath, 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(datalist)

if __name__ == '__main__':

    #いつ出発するか
    dep_time = input('いつ出発?(過去時間は現在時刻に変換します): yyyy/mm/dd hh:mm 形式　例)2018/10/06 10:00 ＞ ')

    #どの地域か
    region = input('地域を入力：例)  1:北海道:東北、2:北陸:甲信越、3:関東、4:東海、5:関西、6:中国:四国、7:九州:沖縄＞ ')

    #どこから出発するかを入力
    origin = input('どこから出発?: 例)東京駅、大宮駅 等 ＞ ').replace(' ','+')

    #お出かけスポット一覧のcsv名
    csvfile = input('お出かけスポット一覧出力csv名: 例)d:\list.csv ＞ ')


    getspotdata(dep_time,region,origin,csvfile)

