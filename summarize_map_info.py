from util import map
import json
import env


json_file_path = "./resources/parking/parking-" + env.SUMMARY_KEY() + "-r.json"
out_file_dir_path = "./resources/routes/"

# レベル１交差点
start_points = {}
with open("./resources/routes/definitions/start_points.json", 'r', encoding='utf-8') as file:
    start_points = json.loads(file.read())

# 処理済み駐車場IDリスト
loaded_parking_ids = []
with open("./resources/routes/__loaded.json", 'r', encoding='utf-8') as file:
    loaded_parking_ids = json.loads(file.read())


def search_nearest_intersection(coordinates):
    """
    与えられた座標に最も近いレベル１交差点を抽出する
    """
    res = None
    current_min_len = None
    for point in start_points:
        p_coor = point['coordinates']

        length = (p_coor[0] - coordinates[0])**2 + \
            (p_coor[1] - coordinates[1]) ** 2
        if current_min_len == None or length < current_min_len:
            current_min_len = length
            res = point
    return res


def main():
    with open(json_file_path, 'r', encoding='utf-8') as file:
        parks_json = file.read().encode("utf-8")
        parks = json.loads(parks_json)

        try:
            # 駐車場ごとに処理
            for park in parks:
                park_id = park['id']

                # 処理済みの駐車場ならパス
                if park_id in loaded_parking_ids:
                    # print("pass...")
                    continue
                coordinates = park['coordinates'][0:2]
                coordinates.reverse()

                # 最寄りのレベル1交差点
                nearrest_intersection = search_nearest_intersection(
                    coordinates)
                is_east = nearrest_intersection['coordinates'][1] > coordinates[1]
                is_north = nearrest_intersection['coordinates'][0] > coordinates[0]

                # 位置関係に応じてどの方向から交差点に進入するか判断
                target_ids = []
                if is_east and is_north:
                    target_ids = [0, 1]
                elif is_east and not is_north:
                    target_ids = [1, 2]
                elif not is_east and is_north:
                    target_ids = [0, 3]
                elif not is_east and not is_north:
                    target_ids = [2, 3]
                park_route_info_list = []
                for target_id in target_ids:
                    target_start_point = nearrest_intersection['start_points'][target_id]
                    route_info = map.route(
                        target_start_point['coordinates'], coordinates)
                    json_route = {
                        'start': target_start_point,
                        'finish': {
                            'coordinates': coordinates
                        },
                        'distance': route_info['distance'],
                        'time': route_info['time'],
                        'steps': [step.step for step in route_info['steps']]
                    }
                    park_route_info_list.append(json_route)
                with open(out_file_dir_path+"route-"+park_id+".json", 'w', encoding='utf-8') as res_file:
                    res_file.write(json.dumps(
                        park_route_info_list, ensure_ascii=False))
                loaded_parking_ids.append(park_id)
                break
        except:
            print("ERROR!!")
        finally:
            # 処理済み駐車場のIDを保存
            with open("./resources/routes/__loaded.json", 'w', encoding='utf-8') as loaded:
                loaded.write(json.dumps(
                    loaded_parking_ids, ensure_ascii=False))


main()
