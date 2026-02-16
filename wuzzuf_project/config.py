
# الإعدادات العامة للطلب
BASE_URL = "https://wuzzuf.net/search/jobs?q"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# إعدادات الحماية والأداء
MAX_RETRIES = 3
RETRY_DELAY = 5
TIMEOUT = 15
PAGES_COUNT = 5

# إعدادات التخزين
OUTPUT_FILE = "wuzzuf_final_report.csv"
