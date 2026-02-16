# storage.py
import csv
import logging


def save_to_csv(jobs_data, filename):
    if not jobs_data:
        logging.error("❌ لا توجد بيانات لحفظها.")
        return

    fieldnames = ['title', 'company', 'location', 'salary']
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs_data)
    logging.info(f"🎉 تم حفظ {len(jobs_data)} وظيفة في {filename}")
