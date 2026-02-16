# storage.py
import csv
import logging


def save_to_csv(data, filename):
    if not data:
        print("⚠️ لا توجد مباريات في هذا التاريخ.")
        return

    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"✅ تم حفظ البيانات بنجاح في {filename}")
