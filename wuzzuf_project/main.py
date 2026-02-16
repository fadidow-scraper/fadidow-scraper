# main.py
import logging
import time
from config import BASE_URL, PAGES_COUNT, OUTPUT_FILE
from scraper import WuzzufScraper
from storage import save_data_to_csv

# إعداد اللوجنج مرة واحدة فقط هنا
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def start_scraping():
    scraper = WuzzufScraper()
    all_jobs_data = []

    for page in range(0, PAGES_COUNT):
        # في Wuzzuf كل صفحة تزيد بمقدار 10 (0, 10, 20...)
        url = f"{BASE_URL}?start={page * 10}"
        logging.info(f"🌐 جاري معالجة الصفحة رقم {page + 1}...")

        html = scraper.fetch_page(url)
        if html:
            jobs = scraper.parse_jobs(html)
            all_jobs_data.extend(jobs)
            logging.info(f"✅ تم جمع {len(jobs)} وظيفة من الصفحة {page + 1}")

        time.sleep(2)  # احترام السيرفر

    save_data_to_csv(all_jobs_data, OUTPUT_FILE)
    logging.info(f"🏁 المهمة انتهت. إجمالي الوظائف المجمعة: {len(all_jobs_data)}")


if __name__ == "__main__":
    start_scraping()
