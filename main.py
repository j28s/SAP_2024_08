import os
from datetime import datetime
from pytz import timezone
from crawling_rda import parsing_beautifulsoup, extract_article_data
from github_utils import get_github_repo, upload_github_issue

if __name__ == "__main__":
    # access_token = os.environ['MY_GITHUB_TOKEN']
    # access_token = os.environ.get('MY_GITHUB_TOKEN', None)
    access_token = os.getenv('MY_GITHUB_TOKEN')
    if not access_token:
        print("Error: MY_GITHUB_TOKEN is not set.")
    repository_name = "SAP_2024_08"

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")

    rda_news_url = "https://rda.go.kr/board/board.do?mode=list&prgId=day_farmprmninfoEntry"

    # BeautifulSoup으로 페이지 파싱 및 데이터 추출
    soup = parsing_beautifulsoup(rda_news_url)
    articles = extract_article_data(soup)

    issue_title = f"농촌진흥청 보도자료 알림({today_date})"
    upload_contents = "\n\n".join(
        [f"### {article['title']} ({article['date']})\n- URL: {article['url']}\n- 내용: {article['content']}" for article in articles]
    )

    # GitHub 업로드 대신 콘솔에 출력
    print("Issue Title:", issue_title)
    print("Upload Contents:")
    print(upload_contents)
    print("Upload Github Issue Success!")  # 실제로 업로드하지 않고 성공 메시지 출력

    # GitHub에 Issue 업로드
    repo = get_github_repo(access_token, repository_name)
    # repo = get_github_repo(repository_name)
    upload_github_issue(repo, issue_title, upload_contents)
    print("Upload Github Issue Success!")