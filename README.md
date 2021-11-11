### INTRODUCTION

This project is simply content aggregator build using FLASK python web framwork, Celery for background tasks , Redis as celery backend and Postgresql as database.

### DEPENDENCIES

- Flask
- Celery
- Requests
- BeatifulSoup

### INSTALATION

1. Download dependencies ```pip install flask celery requests bs4``` or ```pip3 install flask celery requests bs4```
2. Create postgres database and import **database-schema.sql**
3. Run celery beat -> ```celery -A __init__.celery beat```
4. Run celery -> ```celery -A __init__.celery worker -l INFO```
5. Finaly run flska application ```python __init__.py``` or ```python3 __init__.py```
6. Enjoy
