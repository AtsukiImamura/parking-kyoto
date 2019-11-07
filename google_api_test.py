# import urllib
from urllib.parse import urlencode
from urllib.request import urlopen
import json
import sys
import codecs

# https://qiita.com/tamago324/items/3b189a87342ae6120b1c


# sys.stdout = codecs.getwriter(sys.stdout.encoding)(sys.stdout, errors='ignore')

# URIスキーム
# url = 'http://api.twitcasting.tv/api/commentlist?'
url = 'https://maps.googleapis.com/maps/api/directions/json?'
param = {
    'origin': 'Disneyland',
    'destination': 'Universal+Studios+Hollywood',
    'key': ''
}

# URIパラメータの文字列の作成
paramStr = urlencode(param)  # type=json&user=tamago324_pad と整形される
print(paramStr)

# 読み込むオブジェクトの作成
readObj = urlopen(url + paramStr)
# print(str(readObj))

# webAPIからのJSONを取得
response = readObj.read()
res = json.loads(response)

path = './test.txt'

with open(path, mode='w', encoding="utf-8") as f:
    routes = res['routes']
    for route in routes:
        legs = route['legs']
        for leg in legs:
            steps = leg['steps']
            for step in steps:
                # detail_steps = step['steps']
                f.write("\n\n")
                f.write(str(step))
                # for detail_step in detail_steps:
                #     f.write("\n")
                #     f.write(str(detail_step))

   # for item in res:
   #     f.write(str(item))
