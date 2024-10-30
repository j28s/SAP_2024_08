import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # InsecureRequestWarning 예외처리
from bs4 import BeautifulSoup
import requests
import re
from twilio.rest import Client
import pandas as pd


def parsing_beautifulsoup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def extract_article_data(soup):
    articles = []
    base_url = 'https://rda.go.kr/board/board.do?'

    for row in soup.select('table.g_list.boDo tr td div.news_txt')[:5]:  # 최신 5개만
        title = row.select_one('div.title a').get_text(strip=True)
        date = row.select_one('span.date').get_text(strip=True)
        content = row.select_one('div.txt a').get_text(strip=True)

        relative_url = row.select_one('div.title a')['href']
        cleaned_url = re.sub(r';jsessionid=[^?]*', '', relative_url)
        full_url = base_url + cleaned_url

        articles.append({
            "title": title,
            "date": date,
            "content": f"「{content[:50]}...」",  # 50자만 표시
            "url": full_url
        })
    return articles

def extract_article_data_nongsaro(soup):
    # url = "https://www.nongsaro.go.kr/portal/ps/psa/psac/farmLocalNewsLst.ps?pageIndex=1&pageSize=1&menuId=PS03939&keyval=&sType=&sSrchType=sSj&sText="
    base_url = "https://www.nongsaro.go.kr/portal/ps/psa/psac/farmLocalNewsDtl.ps?pageIndex=1&pageSize=1&menuId=PS03939&keyval={}&sType=&sSrchType=sSj&sText="

    articles = []

    # 가장 최근 뉴스 항목 선택
    news_item = soup.select_one('.photo_list li a')

    if news_item:
        # 제목, 내용, 날짜 가져오기
        title = news_item.select_one('.contBox strong').get_text(strip=True)
        content = news_item.select_one('.contBox p.txt').get_text(strip=True)[:50] + "..."
        date = news_item.select_one('.contBox em.date').get_text(strip=True)

        # onclick 속성에서 숫자 추출
        onclick_attr = news_item['onclick']
        number = onclick_attr.split("'")[1]  # 숫자만 추출

        # base_url에 숫자 삽입하여 full_url 생성
        full_url = base_url.format(number)

        # articles 리스트에 추가
        articles.append({
            "title": title,
            "date": date,
            "content": f"「{content}」",
            "url": full_url
        })
        return articles








