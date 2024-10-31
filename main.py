import os
from datetime import datetime
from pytz import timezone
from app import extract_article_data_nongsaro, extract_article_data_me
from app import parsing_beautifulsoup, extract_article_data
from github_utils import get_github_repo, upload_github_issue
from sms_sender import send_sms
import subprocess


def run_streamlit_app():
    """스트림릿 애플리케이션을 실행합니다."""
    subprocess.Popen(["streamlit", "run", "app.py"])


if __name__ == "__main__":
    access_token = os.environ['MY_GITHUB_TOKEN']
    if not access_token:
        print("Error: GIT_ACTION_KEY is not set.")
        exit()

    repository_name = "SAP_2024_08"

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")

    # 농촌진흥청 보도자료 크롤링
    rda_news_url = "https://rda.go.kr/board/board.do?mode=list&prgId=day_farmprmninfoEntry"
    rda_soup = parsing_beautifulsoup(rda_news_url)
    rda_articles = extract_article_data(rda_soup)

    # 농사로 공지사항 크롤링
    nongsaro_url = "https://www.nongsaro.go.kr/portal/ps/psa/psac/farmLocalNewsLst.ps?pageIndex=1&pageSize=1&menuId=PS03939&keyval=&sType=&sSrchType=sSj&sText="
    nongsaro_soup = parsing_beautifulsoup(nongsaro_url)
    nongsaro_articles = extract_article_data_nongsaro(nongsaro_soup)

    # 환경부 데이터 수집
    me_url = "https://www.me.go.kr/home/web/board/read.do?pagerOffset=0&maxPageItems=10&maxIndexPages=10&searchKey=&searchValue=&menuId=10525&orgCd=&boardId=1705390&boardMasterId=1&boardCategoryId=&decorator="
    me_soup = parsing_beautifulsoup(me_url)
    me_articles = extract_article_data_me(me_soup)

    # 모든 기사들을 합치기
    all_articles = rda_articles + nongsaro_articles + me_articles

    issue_title = f"{today_date} 보도자료"
    upload_contents = "\n\n".join(
        [f"### {article['title']} ({article['date']})\n- URL: {article['url']}\n- 내용: {article['content']}" for article
         in all_articles]
    )

    # GitHub에 Issue 업로드
    repo = get_github_repo(access_token, repository_name)
    upload_github_issue(repo, issue_title, upload_contents)
    print("Upload Github Issue Success!")

    # 새로운 기사 확인 및 SMS 전송
    if all_articles:
        send_sms("새로운 소식이 있습니다!")

    # 스트림릿 앱 실행
    run_streamlit_app()
