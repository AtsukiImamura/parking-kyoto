# kmlファイルのパス
import os
import json
from util import google_maps_kml
import env


kml_file_path = os.path.abspath("./resources/"+env.one("SUMMARY_KEY")+".kml")
# 保存先ディレクトリ
json_dir_path = "./results/place_info"
# jsonファイルのパス
json_file_path = os.path.abspath(
    json_dir_path + '/place-' + env.one('SUMMARY_KEY') + '.json')


def main():
    """
    kmlファイルを読み込んで場所に関する情報だけを抽出し、json形式で保存する
    """
    print("json_file_path = "+json_file_path)

    place_info_list = google_maps_kml.place_info_list(kml_file_path)
    targets = []
    for place_info in place_info_list:
        targets.append(place_info.to_obj())

    if not os.path.exists(json_dir_path):
        os.mkdir(json_dir_path)

    with open(json_file_path, 'w') as file:
        file.write(json.dumps(targets))
