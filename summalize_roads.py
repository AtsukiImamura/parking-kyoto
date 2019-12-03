import glob
import json
import re

# ルート情報から道路名を抽出して、 IDとともに付与して更新する
# '__roads.json' に道路名の情報を保持する

json_file_paths = glob.glob(".\\resources\\routes\\route-*-[0-9]*.json")
roads_json_path = "./resources/routes/roads/__roads.json"

with open(roads_json_path, 'r', encoding='utf-8') as file:
    road_info_list = json.loads(file.read())
# 駐車場ごと
for path in json_file_paths:
    print(path)
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
            target = html_instructions.replace(' ', '')
            matches = re.search(p, target)
            if matches is None:
                # print(target)
                continue
            road_name = matches.group(1)
            if road_name == "":
                # print("@  "+target)
                continue
            road_info = None

            # 初めての道路ならリストに加える
            if [road_info['name'] for road_info in road_info_list].count(road_name) == 1:
                rs = [
                    road_info for road_info in road_info_list if road_info['name'] == road_name]
                road_info = rs[0]
            else:
                road_info = {
                    'name': road_name,
                    'id': len(road_info_list),
                    'level': 0
                }
                road_info_list.append(road_info)
            if road_info is None and s_idnex > 0:
                road_info = {
                    'name': '',
                    'id': -1,
                    'level': 0
                }
                # print(html_instructions)
            if road_info == None:
                # print("++ "+html_instructions)
                continue

            # 情報を挿入
            info['steps'][s_idnex]['road'] = road_info

    with open(path, 'w', encoding='utf-8') as loaded:
        loaded.write(json.dumps(
            info_list, ensure_ascii=False, indent=2))

# 道路情報を更新
with open(roads_json_path, 'w', encoding='utf-8') as loaded:
    loaded.write(json.dumps(
        road_info_list, ensure_ascii=False, indent=2))
