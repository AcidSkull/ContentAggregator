from flask import Flask, render_template
from flask_celery import make_celery
from lxml import html
import requests, psycopg2

# VARIABLES
SitesURL = ['linuxiac.com', 'news.itsfoss.com/category/featured/', 'eff.org',
            'thenextweb.com/latest', 'digg.com/technology', 'cnet.com/tech/',
            'wired.com/most-recent', 'axios.com/technology', 'techradar.com/news']
SitesURL_for_anchor = ['linuxiac.com', 'news.itsfoss.com/category/featured/', 'eff.org',
            'thenextweb.com/latest', 'digg.com', 'cnet.com',
            'wired.com', 'axios.com/technology', 'techradar.com/news']

SitesConatiner = [('//*[@id="wi-bf"]/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/article[', ']/div[2]/div/div/div[1]/h2/a', ']/div[2]/div/div/div[1]/h2/a',10),
                  ('/html/body/div/div/section/main/article[', ']/div/header/h2/a', ']/div/header/h2/a', 6),
                  ('/html/body/div[6]/div[2]/div[2]/div/div/div/div[6]/div/div[1]/div[', ']/article/header/h3/a', ']/article/header/h3/a',10),
                  ('//*[@id="articleList"]/article[', ']/div/h4/a', ']/div/h4/a', 7),
                  ('/html/body/div/main/section[2]/div/article[', ']/div/header/a/h2', ']/div/header/a' ,20),
                  ('/html/body/div[2]/div[2]/div[3]/section/div[2]/div[1]/div[1]/div[', ']/div/a/div/h3', ']/div/a', 10),
                  ('/html/body/div[3]/div/div[3]/div/div[2]/div/div[1]/div/div/ul/li[', ']/div/a/h2', ']/div/a', 10),
                  ('/html/body/div[3]/div[1]/amp-layout[', ']/div/div/h3/a', ']/div/div/h3/a', 4),
                  ('//*[@id="content"]/section[2]/div/div[', ']/a[1]/article/div[2]/header/h3', ']/a[1]', 20),]
                  # (common xpath, xpath to title, xpath to link)
                  # -------------------------------------------
                  # EXAMPLE:
                  # Xpath to title ->/html/body/div[2]/div[2]/div[3]/section/div[2]/div[1]/div[1]/div[1]/div/a/div/h3
                  # Xpath to link -> /html/body/div[2]/div[2]/div[3]/section/div[2]/div[1]/div[1]/div[1]/div/a
                  # --------------------------------------------
                  # common path -> /html/body/div[2]/div[2]/div[3]/section/div[2]/div[1]/div[1]/div[
                  # xpath to title -> ]/div[1]/div/a/div/h3
                  # xpath to link -> ]/div/a

TablesNames = ['linuxiac', 'itsfoss', 'eff', 'thenextweb', 'digg', 'cnet', 'wired', 'axios', 'techradar']
TablesNamesHeadlings = ['Linuxiac', 'It\'s foss', 'EFF', 'The Next Web', 'Digg', 'Cnet', 'Wired', 'Axios', 'The Tech Radar']

# FLASK and CELERY CONFIGURATION
app = Flask(__name__)
celery = make_celery(app)

@celery.task()
def check_articles(content, index):
    conn = psycopg2.connect("dbname=contaggr user=postgres")
    cur = conn.cursor()

    # GETTING A FIRST RESULT FROM TABLE
    cur.execute(f"SELECT title FROM {TablesNames[index]} LIMIT 1")
    result = cur.fetchone()
    first_article = result[0] if result != None else ''

    print(f"> Getting data from {TablesNames[index]}\n-----------------------------------")
    get_articles(content, index, cur, first_article)
    print(f">> Successfully fetched data from {TablesNames[index]}\n-----------------------------------")

    conn.commit()
    cur.close()
    conn.close()

@celery.task()
def get_articles(content, index, cur, breakpoint):
    tree = html.fromstring(content)
    max = SitesConatiner[index][3] + 1

    for i in range(1, max):
        xpath1 = SitesConatiner[index][0] + str(i) + SitesConatiner[index][1]
        xpath2 = SitesConatiner[index][0] + str(i) + SitesConatiner[index][2]

        try:
            title = tree.xpath(xpath1)[0].text.strip()
            if title == breakpoint: break;

            anchor = tree.xpath(xpath2)[0].attrib["href"]
            # Making sure we get full link
            if anchor[:4].lower() != 'http': anchor = 'https://' + SitesURL_for_anchor[index] + anchor
        except:
            continue;

        cur.execute(f"""INSERT INTO {TablesNames[index]} (title, anchor) VALUES (%s, %s)""", (title, anchor))


@celery.task(name='check_for_news')
def check_for_news():
    for index, site in enumerate(SitesURL):
        page = requests.get('https://' + site)
        if page.status_code == 200:
           check_articles(page.content, index)

@app.route('/')
def index():
    # Getting news from database
    conn = psycopg2.connect('dbname=contaggr user=postgres')
    cur = conn.cursor()

    result = list()
    for Table in TablesNames:
        cur.execute(f'SELECT title,anchor FROM {Table} LIMIT 10')
        result.append(cur.fetchall())

    cur.close()
    conn.close()
    
    return render_template('index.html', every_news=result, headlings=TablesNamesHeadlings)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
