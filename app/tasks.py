from spider.fshare_spider_urllib import login_cookies, get_download_url
from celery import task


@task()
def task_get_link_fshare(fshare_url):
    opener = login_cookies()
    response = get_download_url(opener, fshare_url)
    return response.geturl()
