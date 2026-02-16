# storage.py
import csv
from itertools import zip_longest


def save_advanced_data(data_list, filename):
    if not data_list:
        print("❌ No data to save.")
        return

    # استخراج العناوين من أول قاموس
    keys = data_list[0].keys()

    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data_list)
    print(f"🎉 File saved successfully: {filename}")
