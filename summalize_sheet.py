from sheet.sheet import GoogleSpreadSheet
import json
import env

json_file_path = "./results/parking/parking-"+ env.PARKING_INFO_ID() +".json"
SPREADSHEET_ID= "1Zzh2g9QMutBrGGzlVUNSut_LGzV18PqrFP7n7CQkftA"
RANGE_NAME = 'S13!A5:K1000'

print("json_file_path = "+json_file_path)
SHEET_NAMES = ["S6", "S7", "S8", "S9", "S13", "S14", "N21", "N22", "N23" , "N26"]

# SHEET_NAMES = ["N22"]
COLUMN_KEYS = [
    "id",
    "num",
    "light_num",
    "has_roof",
    "can_park_in",
    "multi_floors",
    "roads",
    "entranses",
    "system",
    "coop",
    "coop_target"
]

def main():
    sheet = GoogleSpreadSheet(SPREADSHEET_ID)

    target_objects = []
    for sheet_name in SHEET_NAMES:
        rows = sheet.get(sheet_name + "!A5:K1000")
        for rowIndex, row in enumerate(rows):
            target_obj = {}
            # if len(row) != len(COLUMN_KEYS):
            #     print("Length of row must be equals to that of COLUMN_KEYS.  rowIndex = "+str(rowIndex))
            #     print(row)
            #     return
            if len(row) == 0:
                continue
            for i, col in enumerate(row):
                if i >= len(COLUMN_KEYS):
                    print("Length of row must be less than length of column keys.")
                    return
                col_key = COLUMN_KEYS[i]
                target_obj[col_key] = col
            errors = check_row(target_obj)
            if len(errors) > 0:
                print("@@ ERROR")
                print(row)
                print(errors)
                # continue
            target_objects.append(target_obj)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(target_objects, ensure_ascii=False))


import re
def check_row(target):
    errors = []
    # キーの存在チェック
    for col_key in COLUMN_KEYS:
        if col_key not in target and col_key != "coop_target":
            errors.append(col_key +": 要入力")
    if len(errors) > 0:
        return errors

    # 形式・制約チェック
    if not re.match(r"[SN][1-9][0-9]*-[1-9][0-9]*", target["id"]):
        errors.append("ID: 形式違反")
    if not re.match(r"[0-9]*", target["num"]):
        errors.append("num: ニューメリックチェック違反")
    if not re.match(r"[0-9]*", target["light_num"]):
        errors.append("light_num: ニューメリックチェック違反")
    if not re.match(r"[01]", target["has_roof"]):
        errors.append("has_roof: 形式違反")
    if not re.match(r"[01]", target["can_park_in"]):
        errors.append("can_park_in: 形式違反")
    if not re.match(r"[01]", target["multi_floors"]):
        errors.append("multi_floors: 形式違反")
    if not re.match(r"[0-9]{4}", target["roads"]):
        errors.append("roads: 形式違反")
    if not re.match(r"[0-9]{4}", target["entranses"]):
        errors.append("entranses: 形式違反")
    if not re.match(r"[012]", target["system"]):
        errors.append("system: 形式違反")
    if not re.match(r"[01]", target["coop"]):
        errors.append("coop: 形式違反")
    if target["coop"] == 1 and ("coop_target" not in target or target["coop_target"] == ""):
        errors.append("target: 要記入")

    return errors




# main()