from __future__ import unicode_literals

from spider.vnpost_spider import parse_main, normalize
from celery import task


@task()
def task_get_data_from_spider(parcel_id):
    html = parse_main(parcel_id)
    return normalize(html)
