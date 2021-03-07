import os
from datetime import date

from celery import Celery

from covid19.build import build_confirmed, build_deceased
from utils.constants import QUALITY
from utils.utils import pretty_resolution


BROKER_URL = 'redis://localhost:6379/0'
app = Celery('tasks', broker=BROKER_URL)

@app.task
def build():

    date_end = str(date.today())

    # os.system(
    #     'wget -O static/covid19cuba.zip https://github.com/covid19cubadata/covid19cubadata.github.io/raw/master/data/covid19cuba.zip')

    os.system('unzip -o static/covid19cuba.zip')

    with open("download/update.txt", mode="w") as log:
        content = f"{date.today()}"
        log.write(content)

    intermediate_days_list = [3, 5, 10]
    for q in QUALITY:
        pretty_q = pretty_resolution(q)
        for intermediate_days in intermediate_days_list:
            build_confirmed(
                date_end, intermediate_days=intermediate_days,
                figsize=q)
            build_deceased(
                date_end, intermediate_days=intermediate_days,
                figsize=q)
            os.system(f"mv -u static/deceased_{pretty_q}_{intermediate_days}.gif download/deceased_{pretty_q}_{intermediate_days}.gif")
            os.system(f"mv -u static/confirmed_{pretty_q}_{intermediate_days}.gif download/confirmed_{pretty_q}_{intermediate_days}.gif")