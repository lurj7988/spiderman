# -*- encoding: utf-8 -*-

from tenacity import *
from typing import Union
from bs4 import BeautifulSoup
import pandas as pd
import configparser
import asyncio
import platform
import aiohttp
import os
# import sys
# sys.path.append("./")
# from IpProxyUtils import *


class ScrapyAnJuKe:

    """__________________________________________⬇️initialization(初始化)⬇️______________________________________"""

    # 初始化/initialization
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "sec-ch-ua": "\"Not_A Brand\";v=\"99\", \"Google Chrome\";v=\"109\", \"Chromium\";v=\"109\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "cookie": "wmda_uuid=b694539edd10d293c574dfadb2950d3d; wmda_new_uuid=1; wmda_visited_projects=%3B6289197098934; sessid=A42F2D0E-2D8B-CF2D-2D9D-BAECEF0EF190; aQQ_ajkguid=9EA0E5F3-4D8C-E41A-D939-B391CADD3895; ctid=19; twe=2; id58=CrIW6mPp7IqAm6JAsg2YAg==; ajk-appVersion=; fzq_h=0352b8b1181f091e958f761f67b69f47_1676274829099_ade8a7aef1064811b03ae11c701e8951_3657709330; fzq_js_anjuke_ershoufang_pc=f050605fcf90cd47f9a4110ab0705425_1676276545734_23; obtain_by=2; fzq_js_anjuke_xiaoqu_pc=dabc70124bc30ddae054cbcd6755d7de_1676278561279_25; xxzl_cid=fd1cba0cab2e40b3b46ea39eeee715fd; xxzl_deviceid=s9Uvve4KigvCPU7piQOb/PrJ9PTnvpgO/5kyH5mY1Kck5KEMU6Xi0uv/zXaLU6kU",
            "Referer": "https://suzhou.anjuke.com/community/?from=navigation",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }
        self.cookies = {

        }
        # 判断配置文件是否存在/Check if the configuration file exists
        if os.path.exists('config.ini'):
            self.config = configparser.ConfigParser()
            self.config.read('config.ini', encoding='utf-8')
            # 判断是否使用代理
            if self.config['Scraper']['Proxy_switch'] == 'False':
                # http://kaito-kidd.com/2015/11/02/proxies-service/
                # https://www.freesion.com/article/863735470/
                # https://github.com/jhao104/proxy_pool
                # http://demo.spiderpy.cn/get/
                # 开源项目获取ip代理
                # self.proxies = 'http://125.66.100.112:9091'
                self.proxies = None
            else:
                self.proxies = None
        # 配置文件不存在则不使用代理/If the configuration file does not exist, do not use the proxy
        else:
            self.proxies = None
        # 针对Windows系统的异步事件规则/Asynchronous event rules for Windows systems
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy())

    @retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=2))
    async def get_page_html(self, original_url: str) -> Union[str, None]:
        # print(original_url)
        # print(self.proxies)
        try:
            async with aiohttp.ClientSession() as session:
                # https://docs.aiohttp.org/en/stable/client_advanced.html#proxy-support
                async with session.get(original_url, headers=self.headers, proxy=self.proxies) as response:
                    if response.status == 200:
                        x = await response.content.read()
                        return str(x, 'utf-8')
                    return None
        except Exception as e:
            print('获取数据失败！原因:{}'.format(e))
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=2))
    async def get_community(self,  id: str, cityId: str, lat: str, lng: str) -> Union[str, None]:
        original_url = str.format(
            'https://suzhou.anjuke.com/esf-ajax/community/pc/near_community?city_id={0}&comm_id={1}&lat={2}&lng={3}', cityId, id, lat, lng)
        # print(original_url)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(original_url, timeout=10) as response:
                    if response.status == 200:
                        response = await response.json()
                        return response
        except Exception as e:
            print('获取数据失败！原因:{}'.format(e))
            return None


async def async_test2():
    html = await api.get_page_html(original_url='https://suzhou.anjuke.com/community/zhangjiagang/p1/')
    # print(html)
    if html is not None:
        soup = BeautifulSoup(html, 'lxml')
        cells = soup.find(attrs={'class': 'list-cell'})
        # print(cells)
        if cells is not None:
            for li in cells.find_all(attrs={'class': 'li-row'}):
                print(li.attrs['href'])


async def async_test(dics: dict, id: str, cityId: str, lat: str, lng: str) -> None:
    data = await api.get_community(id, cityId, lat, lng)
    communities = data['data']['communities']
    for community in communities:
        # print(community['base']['name'], community['base']['cityId'], community['base']['id'],
        #       community['base']['lat'], community['base']['lng'])
        if community['base']['id'] not in dics:
            dics[community['base']['id']] = {
                'id': community['base']['id'],
                'name': community['base']['name'],
                'cityId': community['base']['cityId'],
                'lat:': community['base']['lat'],
                'lng': community['base']['lng']
            }
            await async_test(dics=dics, id=community['base']['id'], cityId=community['base']['cityId'],
                             lat=community['base']['lat'], lng=community['base']['lng'])

if __name__ == '__main__':
    api = ScrapyAnJuKe()
    # dic = {}
    # asyncio.run(async_test(dics=dic, id=1073182, cityId=19,
    #             lat=31.871486, lng=120.499649))
    # print(dic)
    asyncio.run(async_test2())
