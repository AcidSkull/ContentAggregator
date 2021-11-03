from flask import Flask, render_template
from flask_celery import make_celery
from bs4 import BeautifulSoup
import requests, psycopg2

# VARIABLES
SitesURL = ['linuxiac.com', 'news.itsfoss.com', 'eff.org',
            'thenextweb.com/latest', 'digg.com/technology', 'cnet.com/tech/',
            'wired.com/most-recent/', 'axios.com/technology', 'techradar.com/news']
SitesConatiner = [('h2', 'post-item-title wi-post-title fox-post-title post-header-section size-normal', 0),
                ('h3', 'entry-title', 0),
                ('h3', 'node__title', 0),
                ('h4', 'c-listArticle__heading', 0),
                ('a', 'namespace-scheme', 1),
                ('div', 'item c-universalLatest_item', 2, 'h3'),
                ('li', 'archive-item-component', 2, 'h2'),
                ('h3', 'font-regular leading-tight mt-0 md:text-h5 lg:text-h4 col-1-13 mb-12 text-h6', 0),
                ('article', None, 3, 'h3'),]
                # [block with heading, class of heading, type of heading building]
                # 0 - link block in the headling
                # 1 - headling in the link block
                # 2 - headling and unwanted tags in the link block
                # 3 - headling and unwanted tags in the link block (but we use tag that is in the link block)

TablesNames = ['linuxiac', 'itsfoss', 'eff', 'thenextweb', 'digg', 'cnet', 'wired', 'axios', 'techradar']

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

    if SitesConatiner[index][1] != None:
        articles = soup.find_all(SitesConatiner[index][0], {"class": SitesConatiner[index][1]})
    else:
        articles = soup.find_all(SitesConatiner[index][0])

    if SitesConatiner[index][2] == 0: get_articles_1(articles, index, cur)
    elif SitesConatiner[index][2] == 1: get_articles_2(articles, index, cur)
    elif SitesConatiner[index][2] == 2: get_articles_3(articles, index, cur)
    elif SitesConatiner[index][2] == 3: get_articles_4(articles, index, cur)

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
def get_articles_4(articles, index, cur):
    for article in articles:
        print(article)
        print('---------------------------------------------------------')
        title = article.find(SitesConatiner[index][3]).get_text().strip()
        anchor = article.find_parent('a')['href']

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
