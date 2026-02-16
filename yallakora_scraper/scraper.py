# scraper.py
import requests
from bs4 import BeautifulSoup
from config import HEADERS


class YallaKoraScraper:
    def get_matches_page(self, date):
        url = f"https://www.yallakora.com/Match-Center/?date={date}"
        response = requests.get(url, headers=HEADERS)
        response.encoding = 'utf-8'
        return BeautifulSoup(response.content, 'lxml')

    def extract_matches_details(self, soup):
        matches_details = []
        championships = soup.find_all("div", {"class": "matchCard"})

        for champion in championships:
            # استخراج اسم البطولة
            champion_title = champion.contents[1].find('h2').text.strip()
            # استخراج جميع المباريات في هذه البطولة
            all_matches = champion.contents[3].find_all('div', {"class": "item future liItem"})

            for match in all_matches:
                team_a = match.find("div", {"class": "teamA"}).text.strip()
                team_b = match.find("div", {"class": "teamB"}).text.strip()

                # التعامل مع النتائج والوقت
                m_result = match.find("div", {"class": "MResult"})
                scores = m_result.find_all("span", {"class": "score"})
                score_str = f"{scores[0].text.strip()} - {scores[1].text.strip()}"
                match_time = m_result.find("span", {"class": "time"}).text.strip()

                matches_details.append({
                    "البطولة": champion_title,
                    "الفريق الأول": team_a,
                    "الفريق الثاني": team_b,
                    "الوقت": match_time,
                    "النتيجة": score_str
                })
        return matches_details
