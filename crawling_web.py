import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # InsecureRequestWarning 예외처리
from bs4 import BeautifulSoup
import requests
import re
from twilio.rest import Client
import pandas as pd
from datetime import datetime


def parsing_beautifulsoup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def extract_article_data(soup):
    articles = []
    base_url = 'https://rda.go.kr/board/board.do?'
    today_date = datetime.now().strftime('%Y-%m-%d')

    items = soup.select('table.g_list.boDo tr td div.news_txt')
    for row in items:
        title = row.select_one('div.title a').get_text(strip=True)
        date = row.select_one('span.date').get_text(strip=True)
        if date == today_date:
            content = row.select_one('div.txt a').get_text(strip=True)

            relative_url = row.select_one('div.title a')['href']
            cleaned_url = re.sub(r';jsessionid=[^?]*', '', relative_url)
            full_url = base_url + cleaned_url

            articles.append({
                "title": f"[농촌진흥청] {title}",
                "date": date,
                "content": f"「{content[:50]}...」",  # 50자만 표시
                "url": full_url
            })
    return articles

def extract_article_data_nongsaro(soup):
    base_url = "https://www.nongsaro.go.kr/portal/ps/psa/psac/farmLocalNewsDtl.ps?pageIndex=1&pageSize=1&menuId=PS03939&keyval={}&sType=&sSrchType=sSj&sText="
    articles = []
    today_date = datetime.now().strftime('%Y-%m-%d')

    news_items = soup.select('.photo_list li a')

    for news_item in news_items:
        # 제목, 내용, 날짜 가져오기
        title = news_item.select_one('.contBox strong').get_text(strip=True)
        content = news_item.select_one('.contBox p.txt').get_text(strip=True)[:50] + "..."
        date = news_item.select_one('.contBox em.date').get_text(strip=True)

        if date == today_date:
            # onclick 속성에서 숫자 추출
            onclick_attr = news_item['onclick']
            number = onclick_attr.split("'")[1]  # 숫자만 추출

            # base_url에 숫자 삽입하여 full_url 생성
            full_url = base_url.format(number)

            # articles 리스트에 추가
            articles.append({
                "title": f"[농사로] {title}",
                "date": date,
                "content": f"「{content}」",
                "url": full_url
            })
        return articles








