from flask import Flask, render_template
from flask_celery import make_celery
from bs4 import BeautifulSoup
import requests, psycopg2

# VARIABLES
SitesURL = ['linuxiac.com', 'news.itsfoss.com', 'eff.org', 'thenextweb.com/latest', 'digg.com/technology']
SitesConatiner = [('h2', 'post-item-title wi-post-title fox-post-title post-header-section size-normal'),
                ('h3', 'entry-title'),
                ('h3', 'node__title'),
                ('h4', 'c-listArticle__heading'),
                ('a', 'namespace-scheme'),]
                # ('', ''),
                # ('', ''),
                # ('', ''),
                # ('', ''),]

# POSTGRESQL
conn = psycopg2.connect("dbname=contaggr user=postgres")
cur = conn.cursor()
TablesNames = ['linuxiac', 'itsfoss', 'eff', 'thenextweb', 'digg']

# FLASK and CELERY CONFIGURATION
app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

@celery.task()
def get_articles(content, index):
    soup = BeautifulSoup(content, 'html.parser')
    articles = soup.find_all(SitesConatiner[index][0], {"class": SitesConatiner[index][1]})

    for article in articles:
        title = article.get_text().strip()

        if SitesConatiner[index][0] == 'a':
            anchor = article['href']
        else :
            anchor = article.find('a')['href']

        cur.execute(f"""INSERT INTO {TablesNames[index]} (title, anchor) VALUES (%s, %s)""", (title, anchor))
        conn.commit()

@celery.task()
def check_for_news():
    for index, site in enumerate(SitesURL):
        page = requests.get('https://' + site)
        if page.status_code == 200:
           get_articles(page.content, index)

@app.route('/')
def index():
    cur.execute("SELECT * FROM linuxiac LIMIT 10")
    res = cur.fetchall()
    check_for_news()
    return render_template('index.html', res=res)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
