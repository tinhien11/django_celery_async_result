import scrapy
from scrapy.http import Request, FormRequest


class FshareSpider(scrapy.Spider):
    name = 'fshare_spider'
    start_urls = ['https://www.fshare.vn/login']
    user_agent = ('Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) '
                  'AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 '
                  'Mobile/9A334 Safari/7534.48.3')

    # custom_settings = {
    #     "DOWNLOAD_DELAY": 3,
    # }

    def parse(self, response):
        return scrapy.FormRequest.from_response(response,
                                                formdata={'LoginForm[email]': 'thanhtinpk092007@gmail.com',
                                                          'LoginForm[password]': '721992'},
                                                callback=self.after_login,
                                                method='POST',
                                                url='https://www.fshare.vn/login')

    def after_login(self, response):
        yield scrapy.FormRequest.from_response(response,
                                               formdata={
                                                   'DownloadForm[pwd]': '',
                                                   'DownloadForm[linkcode]': ''},
                                               callback=self.after_post,
                                               method='HEAD',
                                               url='https://www.fshare.vn/file/IXYOB8VHIUHI')

    def after_post(self, response):
        print response.url
