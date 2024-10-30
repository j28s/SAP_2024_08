import os
from datetime import datetime
from pytz import timezone
from crawling_rda import parsing_beautifulsoup, extract_article_data
from github_utils import get_github_repo, upload_github_issue

if __name__ == "__main__":
    access_token = os.environ['MY_GITHUB_TOKEN']
    repository_name = "github-action-with-python"

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

    # GitHub에 Issue 업로드
    repo = get_github_repo(access_token, repository_name)
    upload_github_issue(repo, issue_title, upload_contents)
    print("Upload Github Issue Success!")