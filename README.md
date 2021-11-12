### INTRODUCTION

This project is simply content aggregator build using FLASK python web framwork, Celery for background tasks , Redis as celery backend and Postgresql as database.

### DEPENDENCIES

- Flask
- Celery
- Requests
- BeatifulSoup

### SUPORTED SITES

- Linuxiac
- It's foss
- EFF
- The Next Web
- Digg
- Techradar
- Wired
- Axios
- Cnet

### INSTALATION

1. Download dependencies ```pip install flask celery requests bs4``` or ```pip3 install flask celery requests bs4```
2. Create postgres database and import **database-schema.sql**
3. Run celery beat -> ```celery -A app.celery beat```
4. Run celery -> ```celery -A app.celery worker -l INFO```
5. Finaly run flska application ```python app.py``` or ```python3 app.py```
6. Enjoy
