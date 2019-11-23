# @see https://orangain.hatenablog.com/entry/namespaces-in-xpath

# kmlファイルからポイントの情報を抽出し、以下の形式のデータにする
# [{'name': 'SA-001', 'coordinates': ['135.7581336', '35.0148731', '0']}, {'name': 'SA-002', 'coordinates': ['135.7581335', '35.0143678', '0']}]

from lxml import etree
from map import step
from map import place


def get_doc(file_name):
    """
    XMlファイルを読み込む
    """
    with open(file_name, 'rt', encoding="utf-8") as myfile:
        doc = myfile.read().encode("utf-8")
        return doc


def get_xml_root(file_name):
    """
    XMlファイルのrootを取得する
    """
    try:
        doc = get_doc(file_name)
        return etree.fromstring(doc)
    except:
        print("====== Failed to read file...")


def get_place_marks(root):
    return root.xpath(
        '//kml:Placemark', namespaces={'kml': 'http://www.opengis.net/kml/2.2'})  #/kml:Folder


def get_place_marks_by_file_name(file_name):
    root = get_xml_root(file_name)
    return get_place_marks(root)


def get_name(place_mark):
    """
    与えられた特定の場所情報を能わすxmlファイル情報から地点名称を抽出する
    """
    obj = place_mark.xpath(
        './kml:name', namespaces={'kml': 'http://www.opengis.net/kml/2.2'})
    if(len(obj) == 0):
        return ""

    return obj[0].text


def get_coordinates(place_mark):
    """
    与えられた特定の場所情報を表すxmlファイル情報から地点の位置情報を抽出する

    Parameters
    ------------
    place_mark: xml object
        場所情報を表すxmlオブジェクト。 "Placemark" タグの部分。

    Returns
    ------------
    coordinates: string[]
        通常は長さ3のリスト。google mapsで位置指定に使用可能な情報
    """
    obj = place_mark.xpath(
        './kml:Point/kml:coordinates', namespaces={'kml': 'http://www.opengis.net/kml/2.2'})
    if(len(obj) == 0):
        return []

    return str.strip(obj[0].text).split(",")


def place_info_list(file_name):
    """
    KMLファイルから場所に関する情報を抽出する

    Parameters
    -------------
    file_name : string
        KMLのファイル名（パス）

    Returns
    -------------
    place_info_list : dict[]
        場所に関する情報のリスト。場所情報は name:string, coordinates: string[] を含む。
        coordinatesは通常サイズが３で、google mapsで場所の指定に使用可能
    """
    res = []
    place_marks = get_place_marks_by_file_name(file_name)
    print("place_marks = "+str(len(place_marks)))
    for place_mark in place_marks:
        name = get_name(place_mark)
        coordinates = get_coordinates(place_mark)
        res.append(place.Place({
            "name": name,
            "coordinates": coordinates
        }))
    print(str(len(res))+" places found in kml file.")
    return res
