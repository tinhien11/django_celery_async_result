from __future__ import unicode_literals

from celery import task

from spider.ghn_spider import GHNSpider
from spider.vnpost_spider import VnpostSpider


@task()
def task_get_data_from_spider(parcel_id):
    if len(parcel_id) == 13:
        res = VnpostSpider(parcel_id)
    else:
        res = GHNSpider(parcel_id)
    return res.normalize()
