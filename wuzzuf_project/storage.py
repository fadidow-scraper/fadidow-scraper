
import csv
import logging


def save_data_to_csv(data, filename):
    """حفظ البيانات في ملف CSV بترميز يدعم العربية"""
    if not data:
        logging.error("❌ لا توجد بيانات لحفظها.")
        return

    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=["Title", "Company", "Location"])
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"🎉 تم الحفظ بنجاح في: {filename}")
    except Exception as e:
        logging.error(f"❌ فشل حفظ الملف: {e}")

