# scraper.py
import requests
from bs4 import BeautifulSoup
import logging
import time
from config import HEADERS, MAX_RETRIES, RETRY_DELAY, TIMEOUT


class WuzzufScraper:
    def fetch_page(self, url):
        """جلب محتوى الصفحة مع نظام إعادة المحاولة"""
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
                if response.status_code == 200:
                    return response.text
                logging.warning(f"⚠️ محاولة {attempt}: رجعت خطأ {response.status_code}")
            except requests.exceptions.RequestException as e:
                logging.error(f"❌ خطأ اتصال في المحاولة {attempt}: {e}")

            time.sleep(RETRY_DELAY)
        return None

    def parse_jobs(self, html_content):
        """تحليل الـ HTML واستخراج قائمة الوظائف"""
        soup = BeautifulSoup(html_content, 'lxml')
        job_containers = soup.find_all('div', {'class': 'css-ghe2tq e1v1l3u10'})

        extracted_jobs = []
        for container in job_containers:
            try:
                title = container.find('h2', {'class': 'css-193uk2c'}).get_text(strip=True)
                company = container.find('a', {'class': 'css-ipsyv7'}).get_text(strip=True)
                location = container.find('span', {'class': 'css-16x61xq'}).get_text(strip=True)

                extracted_jobs.append({
                    "Title": title,
                    "Company": company,
                    "Location": location
                })
            except AttributeError:
                continue
        return extracted_jobs
