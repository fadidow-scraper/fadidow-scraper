# scraper.py
import requests
from bs4 import BeautifulSoup
import time
import logging
from config import HEADERS, TIMEOUT, MAX_RETRIES, RETRY_DELAY


class WuzzufAdvancedScraper:
    def get_soup(self, url):
        """جلب محتوى الصفحة مع نظام إعادة محاولة في حال الـ Timeout"""
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
                if response.status_code == 200:
                    return BeautifulSoup(response.content, 'lxml')
                logging.warning(f"⚠️ محاولة {attempt}: كود الحالة {response.status_code}")
            except requests.exceptions.RequestException as e:
                logging.error(f"❌ خطأ في المحاولة {attempt}: {e}")

            time.sleep(RETRY_DELAY)
        return None

    def scrape_page_data(self, page_url):
        """المنطق الجديد: ابحث عن الحاويات أولاً ثم فككها واحدة تلو الأخرى"""
        soup = self.get_soup(page_url)
        if not soup:
            return []

        # 1. البحث عن كل حاويات الوظائف في الصفحة أولاً
        job_containers = soup.find_all('div', {'class':'css-ghe2tq e1v1l3u10'})
        logging.info(f"✅ وجدنا {len(job_containers)} حاوية وظيفة في الصفحة.")

        page_results = []

        # 2. المرور على كل حاوية واستخراج بياناتها الأساسية ورابطها
        for container in job_containers:
            try:
                # 1. ابحث عن وسم h2 أولاً
                h2_tag =container.find('h2', {'class': 'css-193uk2c'})

                # 2. ابحث عن وسم a داخل h2 واستخرج النص منه
                if h2_tag and h2_tag.a:
                    title = h2_tag.find('a').get_text(strip=True)
                else:
                    title = "N/A"

                if h2_tag and h2_tag.a:



                # استخراج الرابط من داخل العنوان
                  link_tag = h2_tag.find('a', {'class':'css-o171kl'})
                  job_link = link_tag.get('href') if link_tag else None

                company = container.find('a', {'class': 'css-ipsyv7'}).get_text(strip=True)
                location = container.find('span', {'class': 'css-16x61xq'}).get_text(strip=True)

                # 3. إذا وجدنا رابط، ندخل فوراً لسحب الراتب والمتطلبات
                salary = "غير معلن"
                requirements = "لا يوجد"

                if job_link:
                    # إضافة الدومين إذا كان الرابط نسبياً (Relative URL)
                    full_link = job_link if job_link.startswith('http') else f"https://wuzzuf.net{job_link}"
                    logging.info(f"🔍 الدخول لسحب تفاصيل: {title}")
                    salary, requirements = self.get_internal_details(full_link)

                # إضافة كل البيانات لقاموس واحد يمثل هذه الوظيفة
                page_results.append({
                    "Title": title,
                    "Company": company,
                    "Location": location,
                    "Salary": salary,
                    "Requirements": requirements,
                    "Link": job_link
                })

                # تأخير بسيط جداً بين الدخول لكل رابط ورابط لعدم الحظر
                time.sleep(1)

            except AttributeError:
                continue

        return page_results

    def get_internal_details(self, job_url):
        """الدخول للرابط الداخلي لسحب الراتب والمتطلبات"""
        inner_soup = self.get_soup(job_url)
        if not inner_soup:
            return "N/A", "N/A"

        # استخراج الراتب
        salary_tag = inner_soup.find("span", {"class": "css-iu2m7n"})
        salary = salary_tag.get_text(strip=True) if salary_tag else "Confidential"

        # استخراج المتطلبات
        req_container = inner_soup.find("div", {'class': 'css-1lqavbg'})
        requirements = req_container.get_text(strip=True) if req_container else "Requirements not listed"

        return salary, requirements

