# main.py
import logging
from config import BASE_URL, START_PAGE, OUTPUT_FILE
from scraper import WuzzufAdvancedScraper
from storage import save_advanced_data

# إعداد الـ Logging ليظهر لك ما يحدث في الـ Terminal
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def run_scraper():
    scraper = WuzzufAdvancedScraper()

    # بناء الرابط بشكل صحيح (start=0 للصفحة الأولى، start=10 للثانية...)
    # يمكنك تغيير START_PAGE من ملف config
    url = f"{BASE_URL}?q=python&start={START_PAGE * 10}"

    logging.info(f"🌐 Processing Page: {START_PAGE + 1}...")

    # تم تغيير المنطق هنا لمناداة الدالة الجديدة الشاملة
    final_jobs_list = scraper.scrape_page_data(url)

    if final_jobs_list:
        # حفظ البيانات
        save_advanced_data(final_jobs_list, OUTPUT_FILE)
    else:
        logging.error("❌ لم يتم العثور على بيانات، تأكد من اتصال الإنترنت أو الكلاسات.")


if __name__ == "__main__":
    run_scraper()

