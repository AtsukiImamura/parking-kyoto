import json
import env
from constants.common import MAX_HOUR

json_file_path = "./resources/parking/parking-" + env.SUMMARY_KEY() + ".json"
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
        park['light_num'] = int(park['light_num'])
        park['has_roof'] = park['has_roof'] == "1"
        park['can_park_in'] = park['can_park_in'] == "1"
        park['multi_floors'] = park['multi_floors'] == "1"
        park['system'] = int(park['system'])
        # park['roads'] = ''
        park['roads'] = list(filter(lambda r: r > 0, map(
            lambda r: int(r), list(park['roads']))))
        park['entranses'] = list(filter(lambda r: r > 0, map(
            lambda r: int(r), list(park['entranses']))))
        park['coop'] = park['coop'] == "1"
        park['unit_price'] = int(park['unit_price'])
        park['unit_period'] = int(park['unit_period'])
        for hour in range(1, MAX_HOUR + 1):
            hour_key = str(hour)+"h"
            park['hourly_prices'][hour_key] = int(
                park['hourly_prices'][hour_key])

        errors = logical_check(park)
        if errors["size"] > 0:
            print("@@ NOTICE")
            print(park)
            print(errors)

    with open(out_file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(parks, ensure_ascii=False))


def logical_check(park):
    errors = {
        "size": 0,
        "notice": [],
        "caution": []
    }

    # TODO: 接する道路・面する道路の関係

    current_price = 0
    for hour in range(1, MAX_HOUR + 1):
        hour_key = str(hour) + "h"
        if park["hourly_prices"][hour_key] < current_price:
            errors["caution"].append(hour_key + ": 不自然な金額")
    if park["unit_price"] < 100:
        errors["notice"].append("unit_price: 単位時間との取り違えの可能性")
    if park["unit_period"] > 60:
        errors["notice"].append("unit_period: 単位価格との取り違えの可能性")

    errors["size"] = len(errors["notice"]) + len(errors["caution"])
    return errors
