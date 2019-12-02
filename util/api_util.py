from urllib.parse import urlencode
from urllib.request import urlopen
import json


def get(url, params):
    """
    GETメソッドでリクエストする

    Parameters
    ------------
    url: string
        URL。スキーマも必要。URLエンコードは事前に必要。
    params: dict
        パラメータの辞書リスト。URLエンコードされるためそのまま渡してよい

    Returns
    -----------
    res: jsonObj
        レスポンスのjsonオブジェクト。辞書型配列になって返る
    """
    # URIパラメータの文字列の作成
    paramStr = urlencode(params)
    url = url + "?" + paramStr
    readObj = urlopen(url)
    # webAPIからのJSONを取得
    response = readObj.read()
    return json.loads(response)
