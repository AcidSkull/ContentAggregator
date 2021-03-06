from flask import Flask, render_template
from flask_celery import make_celery
from config import *
from lxml import html
import requests, psycopg2

# FLASK and CELERY CONFIGURATION
app = Flask(__name__)
celery = make_celery(app)

@celery.task()
def check_articles(content, index):
    conn = psycopg2.connect(f"dbname={DB_NAME} user={DB_USER}")
    cur = conn.cursor()

    # GETTING A FIRST RESULT FROM TABLE
    cur.execute(f"SELECT title FROM {TablesNames[index]} ORDER BY id DESC LIMIT 1")
    result = cur.fetchone()
    first_article = result[0] if result != None else ''

    print(f"> Getting data from {TablesNames[index]}")
    array = get_articles(content, index, first_article)
    array = array[::-1]
    print(f">> Successfully fetched data from {TablesNames[index]}")

    for a in array:
        cur.execute(f"""INSERT INTO {TablesNames[index]} (title, anchor) VALUES (%s, %s)""",(a[0], a[1]))

    conn.commit()
    cur.close()
    conn.close()

@celery.task()
def get_articles(content, index, breakpoint):
    tree = html.fromstring(content)
    max = SitesConatiner[index][3] + 1
    array = list()

    for i in range(1, max):
        xpath1 = SitesConatiner[index][0] + str(i) + SitesConatiner[index][1]
        xpath2 = SitesConatiner[index][0] + str(i) + SitesConatiner[index][2]

        try:
            title = tree.xpath(xpath1)[0].text.strip()
            if title == breakpoint: break;

            anchor = tree.xpath(xpath2)[0].attrib["href"]
            # Making sure we get correct link
            if anchor[:4].lower() != 'http': anchor = 'https://' + SitesURL_for_anchor[index] + anchor

            array.append((title, anchor))
        except:
            continue

    return array


@celery.task(name='check_for_news')
def check_for_news():
    for index, site in enumerate(SitesURL):
        page = requests.get('https://' + site)
        if page.status_code == 200:
           check_articles(page.content, index)

@app.route('/')
def index():
    check_for_news()
    # Getting news from database
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user='{DB_USER}'")
    cur = conn.cursor()

    result = list()
    for Table in TablesNames:
        cur.execute(f'SELECT title,anchor FROM {Table} LIMIT 10')
        result.append(cur.fetchall()[::-1])

    cur.close()
    conn.close()

    return render_template('index.html', every_news=result, headlings=TablesNamesHeadlings)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
