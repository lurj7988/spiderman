import scrapy

from scrapy.http import Request, FormRequest
from scrapy.selector import Selector


class QuotesSpider(scrapy.Spider):
    name = "zhihu"

    def start_requests(self):
        HEADER = {
            "authority":"www.zhihu.com",
            "method":"GET",
            "path":"/api/v4/members/zhang-xiao-yun-43-14/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=0&limit=20",
            "scheme":"https",
            "accept":"*/*",
            "accept-encoding":"gzip, deflate, br",
            "accept-language":"zh-CN,zh;q=0.9",
            'Cookie': '_zap=469b702d-38fe-4264-84e4-5e17c1cdcf53; d_c0=AHDWZqZmQBaPTpr-xui5Ch1W1eAr1UMs0EA=|1675058998; YD00517437729195%3AWM_TID=89OKO2dFFcFAQRQRRBaUfEFCqBR8WgPK; __snaker__id=O9MgXXoTP40MCoT3; q_c1=69ccff9c399c448da0dc00314aef11e4|1675131851000|1675131851000; _xsrf=de38cd4e-0afb-42c1-8aa0-471ace1feafd; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1675059000,1675067976,1675131832,1675135444; arialoadData=false; SESSIONID=tMaZESHr7wgkpcEs7m4n1sPOnxX3z38NHk7CgNJGNpk; JOID=Vl4dAE8PkBAl4PaRawkiyzpFl9NxedN6eKWn1xI45XlFl5XWFihbxEHi-pRnkZWDE9cgZj9Z_uLmWd7FNrDFHA4=; osd=Wl0XCkMDkxov7PqSYQMuxzlPnd99etlwdKmk3Rg06XpPnZnaFSJRyE3h8J5rnZaJGdssZTVT8u7lU9TJOrPPFgI=; gdxidpyhxdE=AC%2BJUzxD%2FJ3Z%2Bmd8Kn%2B1Jrv3uvnrDE3aB%5CD5RPBGGGZ79bvBGfCgcZf9WdKefCHJSowz5oo3I5TLqfdpiyBaJJVGQLcjvhy5gXtBEV8T9C%2BJ8zRQfVI1HQTawt1SwBL5gShY9ZXW%5C8NgxY4rIgSisAh7uCyHAQmY%2BIePdw2mZHR%2F9%5CJG%3A1675153842991; YD00517437729195%3AWM_NI=UKk1JexP8M0yYcx41%2F%2FrPN1aYdFdIeGOfDkrF5wnUILaAmxwm8QkPdcbb36pCqSECvcK7xlyz8rFE4wCHqk0B%2FsO82auu87oteUWeZL6T9IMIk9jyyEXw%2BnelRkxaP2DNEY%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eed1f7648eaafda7ce74a8928bb6c54f828a8b82d16e868bbc92db52f7bd81a8bb2af0fea7c3b92a9795a5d2c96fbc90f8aeb3739bbdb8d5b425edaea0afb46b9bbc8a85cc6f8591aaa5ea7a86ebb98fd84390bf8f8efb7dafe89f8cd370a1beaed4b57c81af9da6c27ea195f999ef73bae8bea7c840b59d8892ea3c82f1bdb0bb3aa3abbbd9b665b8bb9bb8e85290ea9cdacc478bb5f78bfc738788b9cced6fb08ea599e45cf29c82a6dc37e2a3; captcha_session_v2=2|1:0|10:1675152974|18:captcha_session_v2|88:OGtNZnpjbkFPbFpzWCtzZzRTVmU5ZG1CVnE3QWE3WVVTaHR5MG1FSWRJYjZGQlg2cVp5cVBFbHVEUEpsTm1VVw==|961310ed630b663dac66b3334e6d0608bf315ed42f540566d6ea8927419a24fd; captcha_ticket_v2=2|1:0|10:1675153002|17:captcha_ticket_v2|704:eyJ2YWxpZGF0ZSI6IkNOMzFfWVEuMXJid21BMFZldGx5N1FnOE9YRmkxT1lOQXN3MmZNXzRTcFlsTEZLS1I2c05WNi1uRHdhNEdXNmhqZ2lfbE1uS0ZYRklLT1g5bUJzaFJoaV9kSDlEUVVLU3prQ0RjVEtLZUpXNzE1RUQ1RnNFZlUtdmJsZG9EU0ZhQ2lOdHQ5LlNBQjhVOFhyQnNRWExtTFhVSVFVanJoMTRGdWM2MG5oOV9NTV85cWlub1hLLTZ0OGFEejZJbjJTaHg4bW5EZEU0SmJLTjZJZl9JR2YwQ1E4Q1lCenhUQ21qdDI1c0suaGthejhvVEl5SWR3TU85SEUueU1JeV9pQ2lJRThDSERLYXB1NU1hVS1aclgtYXk2bldqRXVYckRucXE4dTdMWmdBY0FYb3FaUlNyNW8xdGViX3h4eDkxRnh0amgwaWUyRkc3S0ZsUU5VZ21pdlgua1JqRHBwMG5SR0RuazFVR1BSdjVnNXdseXZtTWtIUFlsd283em5jeDdzQUNnRDVfWXhLbHpwbGtuVzQua0NCQXZqMUFiUS1vQXBhTFNmUVdRNzFCczhycjYtN0NrSzhCX3VZbk42b0o3aHJNQmYwdWFhQkwxX0ducDhEQ3haLjVZWGVlLmc5ZC5xaDQ2eE9HeHhIU3dZclU3V1ZsMHBTR3ZHNXNCTXZ4N3pxMyJ9|254c901b8e0be759d51c2b5a8ad3755aff8aa71710b4b41c014657614c15923d; z_c0=2|1:0|10:1675153002|4:z_c0|92:Mi4xTWdGS0F3QUFBQUFBY05abXBtWkFGaVlBQUFCZ0FsVk5haHpHWkFEQUgybXprT1hOQUo0eVFDNVJHeHh5WTRvaVR3|ff03975ea5970a5665c083b1462d8533becd853fc2ffea026caf15f9bdbdb5c4; tst=r; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1675153006; KLBRSID=2177cbf908056c6654e972f5ddc96dc2|1675153008|1675152934',
            "referer":"https://www.zhihu.com/people/zhang-xiao-yun-43-14/followers",
            "sec-ch-ua":'"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile":"?0",
            "sec-ch-ua-platform":'"Windows"',
            "sec-fetch-dest":"empty",
            "sec-fetch-mode":"cors",
            "sec-fetch-site":"same-origin",
            "x-ab-param":"",
            "x-ab-pb":"CmQIABsAPwBHALQAaQFqAXQBOwLMAtcC2AK3A9YEEQVRBYsFjAWeBTAGMQbrBicHdAh2CHkIPwlgCfQJBApJCmUKawq+Cv4KQwtxC4cLjQvXC+AL5QvmCzgMcQyPDKwMwwzJDPgMEjIBAAAAAAIAAAAAAAAABAAAAAABAAEAAAAABgACAwAAAAAAAAEAAAUCAAAAAgQAAAIAAA==",
            "x-requested-with":"fetch",
            "x-zse-93":"101_3_3.0",
            "x-zse-96":"2.0_GP2AvUzInCQU4dSvRtSI43=MqynzeLwpXJ83FNBRHXiPAGeqTj8mQ4jQ44usTHbO",
        }
        """
        登陆页面 获取xrsf
        """
        #https://www.zhihu.com/api/v4/members/cuishite/followers?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=0&limit=20
        #https://www.zhihu.com/api/v4/members/cuishite/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=0&limit=20
        return [Request(
            'https://www.zhihu.com/api/v4/members/zhang-xiao-yun-43-14/followers?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&offset=0&limit=20',
            #'https://www.zhihu.com/people/ffitman',
            #meta={'cookiejar': 1},
            #headers=HEADER,
            meta={},
            callback=self.parse_people,
            #errback=self.parse_err,
        )]

    def parse_people(self, response):
        """
        解析用户主页
        """
        print(11111111111111111)
        print(response.body)
        # selector = Selector(response)
        # print(selector.xpath(
        #     '//*[@id="ProfileHeader"]/div/div[2]/div/div[2]/div[1]/h1/span[1]').extract()[0])
        # nickname = selector.xpath(
        #     '//span[@class="ProfileHeader-name"]/text()'
        # ).extract_first()
        # print(nickname)

    def parse_err(self, response):
        print(22222)
        print(response)



