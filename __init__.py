from flask import Flask, render_template
from flask_celery import make_celery
from bs4 import BeautifulSoup
import requests, psycopg2

# VARIABLES
SitesURL = ['linuxiac.com', 'news.itsfoss.com', 'eff.org', 'thenextweb.com/latest', 'digg.com/technology', 'cnet.com/tech/']
SitesConatiner = [('h2', 'post-item-title wi-post-title fox-post-title post-header-section size-normal', 0),
                ('h3', 'entry-title', 0),
                ('h3', 'node__title', 0),
                ('h4', 'c-listArticle__heading', 0),
                ('a', 'namespace-scheme', 1),
                ('div', 'item c-universalLatest_item', 2, 'h3'),]
                # ('', ''),
                # ('', ''),
                # ('', ''),]
                # [block with heading, class of heading, type of heading building]
                # 0 - anchor in the headling
                # 1 - headling in the anchor
                # 2 - headlin and unwanted paragraph in the anchor

TablesNames = ['linuxiac', 'itsfoss', 'eff', 'thenextweb', 'digg', 'cnet']

# FLASK and CELERY CONFIGURATION
app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

@celery.task()
def check_articles(content, index):
    conn = psycopg2.connect("dbname=contaggr user=postgres")
    cur = conn.cursor()
    soup = BeautifulSoup(content, 'html.parser')
    articles = soup.find_all(SitesConatiner[index][0], {"class": SitesConatiner[index][1]})

    if SitesConatiner[index][2] == 0: get_articles_1(articles, index, cur)
    elif SitesConatiner[index][2] == 1: get_articles_2(articles, index, cur)
    elif SitesConatiner[index][2] == 2: get_articles_3(articles, index, cur)

    conn.commit()
    cur.close()
    conn.close()

@celery.task()
def get_articles_1(articles, index, cur):
    for article in articles:
        title = article.get_text().strip()
        anchor = article.find('a')['href']

        cur.execute(f"""INSERT INTO {TablesNames[index]} (title, anchor) VALUES (%s, %s)""", (title, anchor))

@celery.task()
def get_articles_2(articles, index, cur):
    for article in articles:
        title = article.get_text().strip()
        anchor = article['href']

        cur.execute(f"""INSERT INTO {TablesNames[index]} (title, anchor) VALUES (%s, %s)""", (title, anchor))

@celery.task()
def get_articles_3(articles, index, cur):
    for article in articles:
        title = article.find(SitesConatiner[index][3]).get_text().strip()
        anchor = article.find('a')['href']

        cur.execute(f"""INSERT INTO {TablesNames[index]} (title, anchor) VALUES (%s, %s)""", (title, anchor))

@celery.task()
def check_for_news():
    for index, site in enumerate(SitesURL):
        page = requests.get('https://' + site)
        if page.status_code == 200:
           check_articles(page.content, index)

@app.route('/')
def index():
    check_for_news()
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
