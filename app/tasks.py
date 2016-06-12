from __future__ import unicode_literals

from spider.vnpost_spider import VnpostSpider
from celery import task


@task()
def task_get_data_from_spider(parcel_id):
    vnpost = VnpostSpider(parcel_id)
    return vnpost.normalize()
