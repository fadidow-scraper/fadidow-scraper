# scraper.py
import requests
from bs4 import BeautifulSoup
import logging
import time
from config import HEADER, MAX_RETRIES, TIMEOUT, RETRY_DELAY


class ForasnaScraper:
    def fetch_page(self, page_num):
        url = f"https://forasna.com/%D9%88%D8%B8%D8%A7%D8%A6%D9%81-%D8%AE%D8%A7%D9%84%D9%8A%D8%A9?query={page_num}"
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = requests.get(url, headers=HEADER, timeout=TIMEOUT)
                if response.status_code == 200:
                    return response.text
                logging.warning(f"⚠️ صفحة {page_num} رجعت خطأ: {response.status_code}")
            except requests.exceptions.RequestException as e:
                logging.error(f"❌ محاولة {attempt} فشلت في صفحة {page_num}: {e}")
            time.sleep(RETRY_DELAY)
        return None

    def parse_jobs(self, html):
        soup = BeautifulSoup(html, 'lxml')
        job_containers = soup.find_all('div', {'class': 'result-wrp'})
        parsed_jobs = []

        for item in job_containers:
            try:
                title = item.find('h2', {'class': 'job-title'}).find('a').find('span').get_text(strip=True)

                # الشركة
                company_tag = item.find('span', {'class': 'company'})
                company_name = company_tag.a.get_text(strip=True) if company_tag and company_tag.a else "N/A"

                # الموقع وتنظيف الأقواس
                location_raw = item.find('span', {'class': 'location'}).get_text(strip=True)
                location_clean = location_raw.replace('(', '').replace(')', '').strip()

                # الراتب (باستخدام منطق البحث عن النص الذي كتبته)
                salary_label = item.find('span', string=lambda text: "الراتب الأساسي" in text if text else False)
                salary_value = salary_label.find_next('span').get_text(strip=True) if salary_label else "غير معلن"

                parsed_jobs.append({
                    "title": title,
                    "company": company_name,
                    "location": location_clean,
                    "salary": salary_value
                })
            except AttributeError:
                continue
        return parsed_jobs
