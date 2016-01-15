from flask import Flask
from flask_apscheduler import APScheduler
import os

class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__:job1',
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 5
        }
    ]

    SCHEDULER_VIEWS_ENABLED = True
    DEBUG = True


def job1(a, b):
    print(str(a) + ' fdasfa ' + str(b))

app = Flask(__name__)
app.config.from_object(Config())

if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
  scheduler = APScheduler()
  scheduler.init_app(app)
  scheduler.start()


app.run()
