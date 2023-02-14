# Scrapy settings for spiderman project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spiderman'

SPIDER_MODULES = ['spiderman.spiders']
NEWSPIDER_MODULE = 'spiderman.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/49.0.2623.87 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = True

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#   'Accept-Language': 'zh-CN,zh;q=0.9',
#   'Cookie': '_zap=469b702d-38fe-4264-84e4-5e17c1cdcf53; d_c0=AHDWZqZmQBaPTpr-xui5Ch1W1eAr1UMs0EA=|1675058998; YD00517437729195%3AWM_TID=89OKO2dFFcFAQRQRRBaUfEFCqBR8WgPK; __snaker__id=O9MgXXoTP40MCoT3; q_c1=69ccff9c399c448da0dc00314aef11e4|1675131851000|1675131851000; _xsrf=de38cd4e-0afb-42c1-8aa0-471ace1feafd; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1675059000,1675067976,1675131832,1675135444; arialoadData=false; SESSIONID=tMaZESHr7wgkpcEs7m4n1sPOnxX3z38NHk7CgNJGNpk; JOID=Vl4dAE8PkBAl4PaRawkiyzpFl9NxedN6eKWn1xI45XlFl5XWFihbxEHi-pRnkZWDE9cgZj9Z_uLmWd7FNrDFHA4=; osd=Wl0XCkMDkxov7PqSYQMuxzlPnd99etlwdKmk3Rg06XpPnZnaFSJRyE3h8J5rnZaJGdssZTVT8u7lU9TJOrPPFgI=; gdxidpyhxdE=AC%2BJUzxD%2FJ3Z%2Bmd8Kn%2B1Jrv3uvnrDE3aB%5CD5RPBGGGZ79bvBGfCgcZf9WdKefCHJSowz5oo3I5TLqfdpiyBaJJVGQLcjvhy5gXtBEV8T9C%2BJ8zRQfVI1HQTawt1SwBL5gShY9ZXW%5C8NgxY4rIgSisAh7uCyHAQmY%2BIePdw2mZHR%2F9%5CJG%3A1675153842991; YD00517437729195%3AWM_NI=UKk1JexP8M0yYcx41%2F%2FrPN1aYdFdIeGOfDkrF5wnUILaAmxwm8QkPdcbb36pCqSECvcK7xlyz8rFE4wCHqk0B%2FsO82auu87oteUWeZL6T9IMIk9jyyEXw%2BnelRkxaP2DNEY%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed1f7648eaafda7ce74a8928bb6c54f828a8b82d16e868bbc92db52f7bd81a8bb2af0fea7c3b92a9795a5d2c96fbc90f8aeb3739bbdb8d5b425edaea0afb46b9bbc8a85cc6f8591aaa5ea7a86ebb98fd84390bf8f8efb7dafe89f8cd370a1beaed4b57c81af9da6c27ea195f999ef73bae8bea7c840b59d8892ea3c82f1bdb0bb3aa3abbbd9b665b8bb9bb8e85290ea9cdacc478bb5f78bfc738788b9cced6fb08ea599e45cf29c82a6dc37e2a3; captcha_session_v2=2|1:0|10:1675152974|18:captcha_session_v2|88:OGtNZnpjbkFPbFpzWCtzZzRTVmU5ZG1CVnE3QWE3WVVTaHR5MG1FSWRJYjZGQlg2cVp5cVBFbHVEUEpsTm1VVw==|961310ed630b663dac66b3334e6d0608bf315ed42f540566d6ea8927419a24fd; captcha_ticket_v2=2|1:0|10:1675153002|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfWVEuMXJid21BMFZldGx5N1FnOE9YRmkxT1lOQXN3MmZNXzRTcFlsTEZLS1I2c05WNi1uRHdhNEdXNmhqZ2lfbE1uS0ZYRklLT1g5bUJzaFJoaV9kSDlEUVVLU3prQ0RjVEtLZUpXNzE1RUQ1RnNFZlUtdmJsZG9EU0ZhQ2lOdHQ5LlNBQjhVOFhyQnNRWExtTFhVSVFVanJoMTRGdWM2MG5oOV9NTV85cWlub1hLLTZ0OGFEejZJbjJTaHg4bW5EZEU0SmJLTjZJZl9JR2YwQ1E4Q1lCenhUQ21qdDI1c0suaGthejhvVEl5SWR3TU85SEUueU1JeV9pQ2lJRThDSERLYXB1NU1hVS1aclgtYXk2bldqRXVYckRucXE4dTdMWmdBY0FYb3FaUlNyNW8xdGViX3h4eDkxRnh0amgwaWUyRkc3S0ZsUU5VZ21pdlgua1JqRHBwMG5SR0RuazFVR1BSdjVnNXdseXZtTWtIUFlsd283em5jeDdzQUNnRDVfWXhLbHpwbGtuVzQua0NCQXZqMUFiUS1vQXBhTFNmUVdRNzFCczhycjYtN0NrSzhCX3VZbk42b0o3aHJNQmYwdWFhQkwxX0ducDhEQ3haLjVZWGVlLmc5ZC5xaDQ2eE9HeHhIU3dZclU3V1ZsMHBTR3ZHNXNCTXZ4N3pxMyJ9|254c901b8e0be759d51c2b5a8ad3755aff8aa71710b4b41c014657614c15923d; z_c0=2|1:0|10:1675153002|4:z_c0|92:Mi4xTWdGS0F3QUFBQUFBY05abXBtWkFGaVlBQUFCZ0FsVk5haHpHWkFEQUgybXprT1hOQUo0eVFDNVJHeHh5WTRvaVR3|ff03975ea5970a5665c083b1462d8533becd853fc2ffea026caf15f9bdbdb5c4; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1675153006; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1675153008|1675152934',
#   #'Referer': 'https://www.zhihu.com',
#   'Referer': 'https://www.zhihu.com/people/ha-la-la-73/following',
#   'x-ab-pb': 'CmQIABsAPwBHALQAaQFqAXQBOwLMAtcC2AK3A9YEEQVRBYsFjAWeBTAGMQbrBicHdAh2CHkIPwlgCfQJBApJCmUKawq+Cv4KQwtxC4cLjQvXC+AL5QvmCzgMcQyPDKwMwwzJDPgMEjIBAAAAAAIAAAAAAAAABAAAAAABAAEAAAAABgACAwAAAAAAAAEAAAUCAAAAAgQAAAIAAA==',
#   "accept": "*/*",
#   "accept-language": "zh-CN,zh;q=0.9",
#   "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
#   "sec-ch-ua-mobile": "?0",
#   "sec-ch-ua-platform": "\"Windows\"",
#   "sec-fetch-dest": "empty",
#   "sec-fetch-mode": "cors",
#   "sec-fetch-site": "same-origin",
#   "x-ab-param": "",
#   "x-ab-pb": "CmQIABsAPwBHALQAaQFqAXQBOwLMAtcC2AK3A9YEEQVRBYsFjAWeBTAGMQbrBicHdAh2CHkIPwlgCfQJBApJCmUKawq+Cv4KQwtxC4cLjQvXC+AL5QvmCzgMcQyPDKwMwwzJDPgMEjIBAAAAAAIAAAAAAAAABAAAAAABAAEAAAAABgACAwAAAAAAAAEAAAUCAAAAAgQAAAIAAA==",
#   "x-requested-with": "fetch",
#   "x-zse-93": "101_3_3.0",
#   "x-zse-96": "2.0_GP2AvUzInCQU4dSvRtSI43=MqynzeLwpXJ83FNBRHXiPAGeqTj8mQ4jQ44usTHbO",
#   "referrerPolicy": "no-referrer-when-downgrade",
# }
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'SECKEY_ABVK=aeXkIf7wcr63OG8HnXiv6HP1F6w1KgsoefAhbHeQMTQ=; BMAP_SECKEY=wjAFck9zd5zpnA3A78bJnzRoCZNxHVa73qsQwZnH6Xc6s5pdmt9RZ-vUiTkM2PQdjzROhIQiejhyfOTWpU7FQwSqevAF_2VuydrjlvooLy2GahSEROu-zaomqMYrBZDIvGy0P9j7OT_Div3JFxaEcluwtU8v1AhTaW6QzSpqPTRkLoZ0LppfjOcqACLBVzG5; lianjia_uuid=37c0b42b-2329-40d5-8ce0-674e2f4adb7e; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1675646646; sajssdk_2015_cross_new_user=1; hy_data_2020_id=1862462339768-0485feda2bc2de-26021051-3686400-18624623398104c; hy_data_2020_js_sdk={"distinct_id":"1862462339768-0485feda2bc2de-26021051-3686400-18624623398104c","site_id":341,"user_company":236,"props":{},"device_id":"1862462339768-0485feda2bc2de-26021051-3686400-18624623398104c"}; sajssdk_2020_cross_new_user=1; crosSdkDT2019DeviceId=-3ehvlu-fcmjkf-wbhnm4lczapf5ez-bjgju9uv2; sensorsdata2015jssdkcross={"distinct_id":"1862452b6041090-0540935e650e44-26021051-3686400-1862452b6051064","$device_id":"1862452b6041090-0540935e650e44-26021051-3686400-1862452b6051064","props":{"$latest_traffic_source_type":"直接流量","$latest_referrer":"","$latest_referrer_host":"","$latest_search_keyword":"未取到值_直接打开","$latest_utm_source":"baidu","$latest_utm_medium":"pinzhuan","$latest_utm_campaign":"wysuzhou","$latest_utm_content":"biaotimiaoshu","$latest_utm_term":"biaoti"}}; lianjia_ssid=82f8b969-9ef1-4fac-96fd-a67415ff3aaa; select_city=320500; login_ucid=2000000252945550; lianjia_token=2.0012f539657943f00703581054ae7e915c; lianjia_token_secure=2.0012f539657943f00703581054ae7e915c; security_ticket=rh3NWOtYFDxcM+oORtI+ftjizpxGGZHNLCDQjU1hmttv4JEkjEoEOM9AyeUweGUvMgXPNyg+XuC2GDtM5BqmOs4UK7nINNmfeVfEqi09sxlgRJb1Hj+Y4t1fqsR+HltfVwjxRgL9wkx9TCn+vA9XYNEkm+4zwFvTLa5HsfTUtz0=; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1675664498; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiY2UzNmVjM2YzNzZhZGRjNzllNTA4MzM3Y2E4ZjUzMzZiNWZkZmZkODA0ZDE2ODU4ZmVjYzU0NTFkNTJkMDQ5ZjZiY2M4OWRkMGFhMWE1ZjJhY2FjZDA1NWQyNjZhZjIxODU0YWJiNDFmNGY2MmVjMjA4NTM1NDIxN2YxYjFiMTFjNWE0OWIwMmMzOGY3OTA4OTJhZjlkZjFhN2IwN2NhNDgzNTBhMmNiNzEyYjUzYTRjYjg0NzE2OWFhNGQ0ZjYwYjg1MzNiNTFiOWY5OWExYzc2YTk4OTNjZTc2OGM5MGVhOThlMmNkZDc4YmYyNGU3Mzk5YzM1ZGEwMDEzMGI5M1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI1NjY5YzFkMVwifSIsInIiOiJodHRwczovL3N1LmtlLmNvbS9jaGVuZ2ppYW8vIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=',
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
    'sec-ch-ua-platform': '"Windows"'
}

HTTPERROR_ALLOWED_CODES = [403]
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'spiderman.middlewares.SpidermanSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'spiderman.middlewares.SpidermanDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'spiderman.pipelines.SpidermanPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
