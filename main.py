import os
from datetime import datetime
from pytz import timezone
from crawling_web import extract_article_data_nongsaro
from crawling_web import parsing_beautifulsoup, extract_article_data
from github_utils import get_github_repo, upload_github_issue
from sms_sender import send_sms

if __name__ == "__main__":
    access_token = os.environ['MY_GITHUB_TOKEN']
    # access_token = os.environ.get('MY_GITHUB_TOKEN', None)
    # access_token = os.getenv('GIT_ACTION_KEY')
    if not access_token:
        print("Error: GIT_ACTION_KEY is not set.")
    repository_name = "SAP_2024_08"

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")

    # 농촌진흥청 보도자료 크롤링
    rda_news_url = "https://rda.go.kr/board/board.do?mode=list&prgId=day_farmprmninfoEntry"
    # BeautifulSoup으로 페이지 파싱 및 데이터 추출
    rda_soup = parsing_beautifulsoup(rda_news_url)
    rda_articles = extract_article_data(rda_soup)


    nongsaro_url = "https://www.nongsaro.go.kr/portal/ps/psa/psac/farmLocalNewsLst.ps?pageIndex=1&pageSize=1&menuId=PS03939&keyval=&sType=&sSrchType=sSj&sText="
    nongsaro_soup = parsing_beautifulsoup(nongsaro_url)

    # 농사로 공지사항 크롤링
    nongsaro_articles = extract_article_data_nongsaro(nongsaro_soup)

    all_articles = rda_articles + nongsaro_articles


    issue_title = f"보도자료 알림({today_date})"
    upload_contents = "\n\n".join(
        [f"### {article['title']} ({article['date']})\n- URL: {article['url']}\n- 내용: {article['content']}" for article in all_articles]
    )

    # GitHub에 Issue 업로드
    repo = get_github_repo(access_token, repository_name)
    # repo = get_github_repo(repository_name)
    upload_github_issue(repo, issue_title, upload_contents)
    print("Upload Github Issue Success!")

    # SMS로 전송
    sms_body = f"보도자료 알림({today_date})\n" + "\n".join([f"{article['title']} ({article['date']}): {article['url']}" for article in all_articles])
    send_sms(sms_body)