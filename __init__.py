from flask import Flask, render_template
from flask_celery import make_celery
from bs4 import BeautifulSoup
import requests, psycopg2

# POSTGRESQL
conn = psycopg2.connect("dbname=contaggr user=postgres")
cur = conn.cursor()

# FLASK and CELERY CONFIGURATION
app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

@celery.task()
def get_articles(content):
    soup = BeautifulSoup(content, 'html.parser')
    articles = soup.find_all("h2", {"class": "post-item-title wi-post-title fox-post-title post-header-section size-normal"})
    for article in articles:
        title = article.get_text().strip()
        anchor = article.find('a')['href']
        
        cur.execute('INSERT INTO linuxiac (title, anchor) VALUES (%s, %s)', (title, anchor))
        conn.commit()

@celery.task()
def check_for_news():
    page = requests.get('https://linuxiac.com')
    if page.status_code == 200:
       get_articles(page.content)

@app.route('/')
def index():
    check_for_news()
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")