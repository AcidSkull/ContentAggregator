from flask import Flask, render_template
from flask_celery import make_celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

@celery.task()
def add_together(a, b):
    return a + b

@app.route('/')
def index():
    return f"{add_together(6,10)}"
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")