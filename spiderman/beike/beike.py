import scrapy

from scrapy.http import Request, FormRequest
from scrapy.selector import Selector


class QuotesSpider(scrapy.Spider):
    name = "beike"

    def start_requests(self):
        # self.chengjiao()
        # return [Request(
        #     'https://su.ke.com/ershoufang/zhangjiagang/pg2/',
        #     meta={},
        #     callback=self.parse_people,
        #     # errback=self.parse_err,
        # )]
        HEADER = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'su.ke.com',
            'Referer': 'https://su.ke.com/ershoufang/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Reqests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        COOKIE = {
            'SECKEY_ABVK': 'aeXkIf7wcr63OG8HnXiv6HP1F6w1KgsoefAhbHeQMTQ%3D',
            'BMAP_SECKEY': 'wjAFck9zd5zpnA3A78bJnzRoCZNxHVa73qsQwZnH6Xc6s5pdmt9RZ-vUiTkM2PQdjzROhIQiejhyfOTWpU7FQwSqevAF_2VuydrjlvooLy2GahSEROu-zaomqMYrBZDIvGy0P9j7OT_Div3JFxaEcluwtU8v1AhTaW6QzSpqPTRkLoZ0LppfjOcqACLBVzG5',
            'lianjia_uuid': '37c0b42b-2329-40d5-8ce0-674e2f4adb7e',
            'Hm_lvt_9152f8221cb6243a53c83b956842be8a': '1675646646',
            'sajssdk_2015_cross_new_user': '1',
            'hy_data_2020_id': '1862462339768-0485feda2bc2de-26021051-3686400-18624623398104c',
            'hy_data_2020_js_sdk': '%7B%22distinct_id%22%3A%221862462339768-0485feda2bc2de-26021051-3686400-18624623398104c%22%2C%22site_id%22%3A341%2C%22user_company%22%3A236%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%221862462339768-0485feda2bc2de-26021051-3686400-18624623398104c%22%7D',
            'sajssdk_2020_cross_new_user': '1',
            'crosSdkDT2019DeviceId': '-3ehvlu-fcmjkf-wbhnm4lczapf5ez-bjgju9uv2',
            'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%221862452b6041090-0540935e650e44-26021051-3686400-1862452b6051064%22%2C%22%24device_id%22%3A%221862452b6041090-0540935e650e44-26021051-3686400-1862452b6051064%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_utm_source%22%3A%22baidu%22%2C%22%24latest_utm_medium%22%3A%22pinzhuan%22%2C%22%24latest_utm_campaign%22%3A%22wysuzhou%22%2C%22%24latest_utm_content%22%3A%22biaotimiaoshu%22%2C%22%24latest_utm_term%22%3A%22biaoti%22%7D%7D',
            'lianjia_ssid': '82f8b969-9ef1-4fac-96fd-a67415ff3aaa',
            'select_city': '320500',
            'login_ucid': '2000000252945550',
            'lianjia_token': '2.0012f539657943f00703581054ae7e915c',
            'lianjia_token_secure': '2.0012f539657943f00703581054ae7e915c',
            'security_ticket': 'rh3NWOtYFDxcM+oORtI+ftjizpxGGZHNLCDQjU1hmttv4JEkjEoEOM9AyeUweGUvMgXPNyg+XuC2GDtM5BqmOs4UK7nINNmfeVfEqi09sxlgRJb1Hj+Y4t1fqsR+HltfVwjxRgL9wkx9TCn+vA9XYNEkm+4zwFvTLa5HsfTUtz0=',
            'Hm_lpvt_9152f8221cb6243a53c83b956842be8a': '1675664498',
            'srcid': 'eyJ0Ijoie1wiZGF0YVwiOlwiY2UzNmVjM2YzNzZhZGRjNzllNTA4MzM3Y2E4ZjUzMzZiNWZkZmZkODA0ZDE2ODU4ZmVjYzU0NTFkNTJkMDQ5ZjZiY2M4OWRkMGFhMWE1ZjJhY2FjZDA1NWQyNjZhZjIxODU0YWJiNDFmNGY2MmVjMjA4NTM1NDIxN2YxYjFiMTFjNWE0OWIwMmMzOGY3OTA4OTJhZjlkZjFhN2IwN2NhNDgzNTBhMmNiNzEyYjUzYTRjYjg0NzE2OWFhNGQ0ZjYwYjg1MzNiNTFiOWY5OWExYzc2YTk4OTNjZTc2OGM5MGVhOThlMmNkZDc4YmYyNGU3Mzk5YzM1ZGEwMDEzMGI5M1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI1NjY5YzFkMVwifSIsInIiOiJodHRwczovL3N1LmtlLmNvbS9jaGVuZ2ppYW8vIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0='
        }
        return [Request(
            'https://su.ke.com/chengjiao/zhangjiagang/',
            headers=HEADER, cookies=COOKIE,
            callback=self.parse_chengjiao,
        )]

    def parse_people(self, response):
        selector = Selector(response)
        title = selector.xpath(
            '//*[@class="sellListContent"]/li//*[@class="title"]/a/text()').extract()
        titlehref = selector.xpath(
            '//*[@class="sellListContent"]/li//*[@class="title"]/a/@href').extract()
        price = selector.xpath(
            '//*[@class="sellListContent"]/li//div[@class="totalPrice totalPrice2"]/span/text()').extract()
        position = selector.xpath(
            '//*[@class="sellListContent"]/li//div[@class="positionInfo"]/a/text()').extract()
        positionhref = selector.xpath(
            '//*[@class="sellListContent"]/li//div[@class="positionInfo"]/a/@href').extract()
        houseInfo = selector.xpath(
            '//*[@class="sellListContent"]/li//div[@class="houseInfo"]/text()').extract()
        for a in houseInfo:
            a = a.replace('\n', '').replace('\r', '').replace(' ', '')
            if a != '':
                print(a)
        unitPrice = selector.xpath(
            '//*[@class="sellListContent"]/li//div[@class="unitPrice"]/span/text()').extract()
        followInfo = selector.xpath(
            '//*[@class="sellListContent"]/li//div[@class="followInfo"]/text()').extract()
        for a in followInfo:
            a = a.replace('\n', '').replace('\r', '').replace(' ', '')
            if a != '':
                print(a)
        # print(title)
        print(titlehref)
        # print(price)
        # print(position)
        # print(positionhref)
        # print(houseInfo)
        # print(followInfo)

    def chengjiao(self):
        for i in range(48):
            print(i)
            if i == 0:
                yield [Request(
                    'https://su.ke.com/chengjiao/zhangjiagang/',
                    callback=self.parse_chengjiao,
                )]
            else:
                yield [Request(
                    'https://su.ke.com/chengjiao/zhangjiagang/pg'+(i+1),
                    callback=self.parse_chengjiao,
                )]

    def parse_chengjiao(self, response):
        selector = Selector(response)
        title = selector.xpath(
            '//*[@class="listContent"]/li//*[@class="dealDate"]/text()').extract()
        for a in title:
            a = a.replace('\n', '').replace('\r', '').replace(' ', '')
            if a != '':
                print(a)        
