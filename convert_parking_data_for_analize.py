import json
import env

json_file_path = "./results/parking/parking-"+ env.PARKING_INFO_ID() +".json"
out_file_path = json_file_path


def main():
    with open(json_file_path, 'r', encoding='utf-8') as file:
        parks_json = file.read().encode("utf-8")

    if parks_json == None:
        return

    parks = json.loads(parks_json)
    for park in parks:
        # print(park)
        park['num'] = int(park['num'])
        park['light_num'] = int (park['light_num'])
        park['has_roof'] = park['has_roof'] == "1"
        park['can_park_in'] = park['can_park_in'] == "1"
        park['multi_floors'] = park['multi_floors'] == "1"
        park['system'] = int(park['system'])
        # park['roads'] = ''
        park['roads'] = list(filter(lambda r:r>0, map(lambda r:int(r), list(park['roads']))))
        park['entranses'] = list(filter(lambda r:r > 0, map(lambda r:int(r), list(park['entranses']))))
        park['coop'] = park['coop'] == "1"

    with open(out_file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(parks, ensure_ascii=False))