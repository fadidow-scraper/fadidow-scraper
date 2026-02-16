# config.py
BASE_URL = "https://wuzzuf.net/search/jobs"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
TIMEOUT = 40
MAX_RETRIES = 5
RETRY_DELAY = 3
OUTPUT_FILE = "wuzzuf_advanced_data.csv"
START_PAGE = 0  # الصفحة التي يبدأ منها الكود كما حددت
