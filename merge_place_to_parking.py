import json
import env


place_info_path = "./results/place_info/place-"+env.one("PLACE_INFO_ID") +".json"
parking_info_path = "./results/parking/parking-"+ env.PARKING_INFO_ID() +".json"
parking_info_out_path = "./results/parking/parking-"+ env.PARKING_INFO_ID() +"-r.json"


def main():
    with open(parking_info_path, 'r', encoding='utf-8') as file:
        parks_json = file.read().encode("utf-8")
    with open(place_info_path, 'r', encoding='utf-8') as file:
        places_json = file.read().encode("utf-8")

    if parks_json == None:
        print("parks_json not found.")
        return
    
    if places_json == None:
        print("places_json not found.")
        return

    parks = json.loads(parks_json)
    places = json.loads(places_json)

    place_per_id = {}
    for place in places:
        place_per_id[place["name"]] = place

    summalized_parks = []
    for park in parks:
        if park["id"] not in place_per_id:
            print("ID "+park["id"] +" の駐車場位置データがありません")
            continue
        park["coordinates"] = place_per_id[park["id"]]["coordinates"]
        summalized_parks.append(park)

    with open(parking_info_out_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(summalized_parks, ensure_ascii=False))