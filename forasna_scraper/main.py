# main.py
import logging
import time
from config import PAGES_RANGE, OUTPUT_FILE
from scraper import ForasnaScraper
from storage import save_to_csv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    scraper = ForasnaScraper()
    all_final_jobs = []

    for page in PAGES_RANGE:
        logging.info(f"🌐 جاري معالجة صفحة فرصنا رقم {page}...")
        html = scraper.fetch_page(page)

        if html:
            jobs = scraper.parse_jobs(html)
            all_final_jobs.extend(jobs)
            logging.info(f"✅ تم استخراج {len(jobs)} وظيفة من صفحة {page}")

        time.sleep(2)

    save_to_csv(all_final_jobs, OUTPUT_FILE)


if __name__ == '__main__':
    main()
