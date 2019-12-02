import glob
import json
import re

# ルート情報から道路名を抽出して、 IDとともに付与して更新する
# '__roads.json' に道路名の情報を保持する

json_file_paths = glob.glob(".\\resources\\routes\\route-*-[0-9].json")
roads_json_path = "./resources/routes/__roads.json"

with open(roads_json_path, 'r', encoding='utf-8') as file:
    road_info_list = json.loads(file.read())
# 駐車場ごと
for path in json_file_paths:
    with open(path, 'r', encoding='utf-8') as file:
        info_list = json.loads(file.read())
    # ルートごと
    for info in info_list:
        steps = info['steps']
        # ステップごと
        for s_idnex, step in enumerate(steps):
            # 道路名抽出
            html_instructions = step['html_instructions']
            p = re.compile('<b>([^<>]*)</b>(/<wbr/><b>.*)?に入る')
            matches = re.search(p, html_instructions)
            if matches is None:
                continue
            road_name = matches.group(1)
            if road_name == "":
                continue
            road_info = None

            # 初めての道路ならリストに加える
            if [road_info['name'] for road_info in road_info_list].count(road_name) == 1:
                road_info = [
                    road_info for road_info in road_info_list if road_info['name'] == road_name]
            else:
                road_info = {
                    'name': road_name,
                    'id': len(road_info_list)
                }
                road_info_list.append(road_info)
            if road_info == None and s_idnex > 0:
                road_info = {
                    'name': '',
                    'id': -1
                }
            if road_info == None:
                continue

            # 情報を挿入
            step['road'] = road_info

    with open(path, 'w', encoding='utf-8') as loaded:
        loaded.write(json.dumps(
            info_list, ensure_ascii=False))

# 道路情報を更新
with open(roads_json_path, 'w', encoding='utf-8') as loaded:
    loaded.write(json.dumps(
        road_info_list, ensure_ascii=False))
