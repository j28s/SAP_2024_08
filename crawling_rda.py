import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # InsecureRequestWarning 예외처리
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

# 요청할 URL 설정
# url = 'https://rda.go.kr/board/board.do?mode=list&prgId=day_farmprmninfoEntry'
# base_url = 'https://rda.go.kr/board/board.do?'


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


# # 필요한 데이터를 담을 리스트 초기화
# articles = []
#
# # print(soup.prettify())
# for idx, row in enumerate(soup.select('table.g_list.boDo tr td div.news_txt')):
#     if idx >= 5:  # 5개 이상일 때 루프 종료
#         break
#
#     # 제목 추출
#     title = row.select_one('div.title a').get_text(strip=True)
#     # 날짜 추출
#     date = row.select_one('span.date').get_text(strip=True)
#     # 내용 추출
#     content = "「" + row.select_one('div.txt a').get_text(strip=True)[:50] + " ···」"
#
#     # URL 추출 및 세션 ID 제거
#     relative_url = row.select_one('div.title a')['href']
#     cleaned_url = re.sub(r';jsessionid=[^?]*', '', relative_url)
#     full_url = base_url + cleaned_url  # 절대 URL 생성
#
#     # 기사 정보를 딕셔너리로 저장
#     articles.append({
#         "제목": title,
#         "날짜": date,
#         "내용": content,
#         "URL": full_url
#     })
# # DataFrame으로 변환
# df = pd.DataFrame(articles)
#
# # CSV 파일로 저장
# df.to_csv('real_latest_articles.csv', index=False, encoding='utf-8-sig')
#
# print("CSV 파일로 저장이 완료되었습니다.")









