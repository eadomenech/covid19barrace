import os
from datetime import date

from celery import Celery

from build import build_confirmed, build_deceased


BROKER_URL = 'redis://localhost:6379/0'
app = Celery('tasks', broker=BROKER_URL)

@app.task
def build():

    date_end = str(date.today())

    os.system(
        'wget -O static/covid19cuba.zip https://github.com/covid19cubadata/covid19cubadata.github.io/raw/master/data/covid19cuba.zip')

    os.system('unzip -o static/covid19cuba.zip')

    with open("download/update.txt", mode="w") as log:
        content = f"{date.today()}"
        log.write(content)
    
    build_confirmed(date_end, intermediate_days=5)
    build_deceased(date_end, intermediate_days=5)

    os.system('mv -u static/deceased.gif download/deceased.gif')
    os.system('mv -u static/confirmed.gif download/confirmed.gif')