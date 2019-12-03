
import os
import env
import json

json_file_dir = "./resources/parking/"
json_file_path = json_file_dir+"parking-" + env.SUMMARY_KEY() + ".json"

error_json_path = json_file_dir+"/errors/" + env.SUMMARY_KEY() + ".errors.json"
error_csv_path = json_file_dir+"/errors/" + env.SUMMARY_KEY() + ".errors.csv"

errors = []
with open(error_json_path, 'r', encoding='utf-8') as file:
    errors = json.loads(file.read())

with open(error_csv_path, 'w', encoding='utf-8') as csv_file:
    csv_file.write("")

with open(error_csv_path, 'a', encoding='utf-8') as csv_file:
    for error in errors:
        id = error['row'][0]
        for i, msg in enumerate(error['errors']):
            row = []
            if i == 0:
                row.append('"'+id+'"')
            else:
                row.append('""')
            row.append('"'+msg+'"')
            csv_file.write(', '.join(row)+"\n")
