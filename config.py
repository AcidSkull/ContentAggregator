from celery.schedules import crontab

# CELERY

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
PERIOD_BETWEEN_TASK = crontab(hour="*/6")
TIMEZONE = 'Europe/Warsaw'

# DATABASE

DB_NAME = 'contaggr'
DB_USER = 'postgres'
DB_PASSWORD = ''
DB_HOST = ''
DB_PORT = ''

# SITES VARIABLES

# URL for the sites to send requests
SitesURL = ['linuxiac.com', 'news.itsfoss.com/category/featured/', 'eff.org',
            'thenextweb.com/latest', 'digg.com/technology', 'cnet.com/tech/',
            'wired.com/most-recent', 'axios.com', 'techradar.com/news']
# URL to use when getting links for articles
SitesURL_for_anchor = ['linuxiac.com', 'news.itsfoss.com/category/featured/', 'eff.org',
            'thenextweb.com/latest', 'digg.com', 'cnet.com',
            'wired.com', 'axios.com/technology', 'techradar.com/news']

# Xpath to title and a tag
SitesConatiner = [('//*[@id="wi-bf"]/div[2]/div/div/div/div[1]/div/div[1]/div/div[1]/article[', ']/div[2]/div/div/div[1]/h2/a', ']/div[2]/div/div/div[1]/h2/a',10),
                  ('/html/body/div/div/section/main/article[', ']/div/header/h2/a', ']/div/header/h2/a', 6),
                  ('/html/body/div[6]/div[2]/div[2]/div/div/div/div[6]/div/div[1]/div[', ']/article/header/h3/a', ']/article/header/h3/a',10),
                  ('//*[@id="articleList"]/article[', ']/div/h4/a', ']/div/h4/a', 7),
                  ('/html/body/div/main/section[2]/div/article[', ']/div/header/a/h2', ']/div/header/a' ,20),
                  ('/html/body/div[2]/div[2]/div[3]/section/div[2]/div[1]/div[1]/div[', ']/div/a/div/h3', ']/div/a', 10),
                  ('/html/body/div[3]/div/div[3]/div/div[2]/div/div[1]/div/div/ul/li[', ']/div/a/h2', ']/div/a', 10),
                  ('/html/body/div[2]/div/section[3]/amp-layout[', ']/div/div/h3/a', ']/div/div/h3/a', 12),
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

# Name of the table in database
TablesNames = ['linuxiac', 'itsfoss', 'eff', 'thenextweb', 'digg', 'cnet', 'wired', 'axios', 'techradar']
# Headling for the site in the HTML file
TablesNamesHeadlings = ['Linuxiac', 'It\'s foss', 'EFF', 'The Next Web', 'Digg', 'Cnet', 'Wired', 'Axios', 'The Tech Radar']
