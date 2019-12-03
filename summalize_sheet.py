import re
from sheet.sheet import GoogleSpreadSheet
import json
import env
from constants.common import MAX_HOUR
import os

json_dir_path = "./resources/parking/"
json_file_path = json_dir_path + "parking-" + env.SUMMARY_KEY() + ".json"
json_error_path = json_dir_path + "errors/" + env.SUMMARY_KEY() + ".error.json"
SPREADSHEET_ID = "1Zzh2g9QMutBrGGzlVUNSut_LGzV18PqrFP7n7CQkftA"
RANGE_NAME = 'S13!A5:K1000'

print("json_file_path = "+json_file_path)
SHEET_NAMES = ["S6", "S7", "S8", "S9", "S12", "S13", "S14", "N6", "N7",
               "N8", "N9", "N13", "N14", "N15", "N16", "N20", "N21", "N22", "N23", "N26", "N27", "N28", "N29"]

# SHEET_NAMES = ["N29"]
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
    "coop_target",
    "unit_price",
    "unit_period",
    "1h",
    "2h",
    "3h",
    "4h",
    "5h",
    "6h",
    "7h",
    "8h",
]


def main():
    sheet = GoogleSpreadSheet(SPREADSHEET_ID)

    target_objects = []
    saving_errors = []
    for sheet_name in SHEET_NAMES:
        try:
            rows = sheet.get(sheet_name + "!A5:U1000")
            print("sheet: "+sheet_name+"  rows: "+str(len(rows)))
        except:
            print("ERROR! Can not get sheet: "+sheet_name)
        for row in rows:
            try:
                target_obj = {}
                # if len(row) != len(COLUMN_KEYS):
                #     print("Length of row must be equals to that of COLUMN_KEYS.  rowIndex = "+str(rowIndex))
                #     print(row)
                #     return
                if len(row) == 0:
                    continue
                for i, col in enumerate(row):
                    if i >= len(COLUMN_KEYS):
                        print(
                            "Length of row must be less than length of column keys.")
                        return
                    col_key = COLUMN_KEYS[i]
                    target_obj[col_key] = col
                errors = check_row(target_obj)
                if len(errors) > 0:
                    saving_errors.append({
                        'row': row,
                        'errors': errors
                    })
                    continue
                target_objects.append(target_obj)
            except:
                saving_errors.append({
                    'row': row,
                    'errors': ['例外発生']
                })

    for target_obj in target_objects:
        price_info = {}
        errors = []
        for hour in range(1, MAX_HOUR + 1):
            hour_key = str(hour)+"h"
            if hour_key not in target_obj:
                errors.append('hour_key '+hour_key +
                              ' not found in '+target_obj['id'])
                continue
            price_info[hour_key] = target_obj.pop(hour_key)
        target_obj["hourly_prices"] = price_info
        if len(errors) > 0:
            saving_errors.append(errors)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(target_objects, ensure_ascii=False, indent=2))
    with open(json_error_path, 'w', encoding='utf-8') as file:
        file.write(json.dumps(saving_errors, ensure_ascii=False, indent=2))


def check_row(target):
    errors = []
    # キーの存在チェック
    for col_key in COLUMN_KEYS:
        if col_key not in target and col_key != "coop_target":
            errors.append(col_key + ": 要入力")
    if len(errors) > 0:
        return errors

    # 形式・制約チェック
    if not re.match(r"[SN][1-9][0-9]*-[1-9][0-9]*", target["id"]):
        errors.append("ID: 形式違反")
    if re.match(r"[0-9]*", target["num"]).group() == '':
        errors.append("num: ニューメリックチェック違反")
    if re.match(r"[0-9]*", target["light_num"]).group() == '':
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
    if not re.match(r"[1-9][0-9]*", target["unit_price"]):
        errors.append("unit_price: 形式違反")
    if not re.match(r"[1-9][0-9]*", target["unit_period"]):
        errors.append("unit_period: 形式違反")
    for hour in range(1, MAX_HOUR + 1):
        hour_key = str(hour) + "h"
        if not re.match(r"[1-9][0-9]*", target[hour_key]):
            errors.append(hour_key + ": 形式違反")

    return errors


# main()
