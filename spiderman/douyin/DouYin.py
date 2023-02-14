# -*- encoding: utf-8 -*-
import re
import os
import aiohttp
import platform
import asyncio
import configparser

from typing import Union
from tenacity import *


class DouYin:

    """__________________________________________⬇️initialization(初始化)⬇️______________________________________"""

    # 初始化/initialization
    def __init__(self):
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66"
        }
        self.douyin_cookies = {
            'Cookie': 'msToken=tsQyL2_m4XgtIij2GZfyu8XNXBfTGELdreF1jeIJTyktxMqf5MMIna8m1bv7zYz4pGLinNP2TvISbrzvFubLR8khwmAVLfImoWo3Ecnl_956MgOK9kOBdwM=; odin_tt=6db0a7d68fd2147ddaf4db0b911551e472d698d7b84a64a24cf07c49bdc5594b2fb7a42fd125332977218dd517a36ec3c658f84cebc6f806032eff34b36909607d5452f0f9d898810c369cd75fd5fb15; ttwid=1%7CfhiqLOzu_UksmD8_muF_TNvFyV909d0cw8CSRsmnbr0%7C1662368529%7C048a4e969ec3570e84a5faa3518aa7e16332cfc7fbcb789780135d33a34d94d2'
        }
        self.tiktok_api_headers = {
            'User-Agent': 'com.ss.android.ugc.trill/494+Mozilla/5.0+(Linux;+Android+12;+2112123G+Build/SKQ1.211006.001;+wv)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Version/4.0+Chrome/107.0.5304.105+Mobile+Safari/537.36'
        }
        # 判断配置文件是否存在/Check if the configuration file exists
        if os.path.exists('config.ini'):
            self.config = configparser.ConfigParser()
            self.config.read('config.ini', encoding='utf-8')
            # 判断是否使用代理
            if self.config['Scraper']['Proxy_switch'] == 'True':
                # 判断是否区别协议选择代理
                if self.config['Scraper']['Use_different_protocols'] == 'False':
                    self.proxies = {
                        'all': self.config['Scraper']['All']
                    }
                else:
                    self.proxies = {
                        'http': self.config['Scraper']['Http_proxy'],
                        'https': self.config['Scraper']['Https_proxy'],
                    }
            else:
                self.proxies = None
        # 配置文件不存在则不使用代理/If the configuration file does not exist, do not use the proxy
        else:
            self.proxies = None
        # 针对Windows系统的异步事件规则/Asynchronous event rules for Windows systems
        if platform.system() == 'Windows':
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy())

    """__________________________________________⬇️utils(实用程序)⬇️______________________________________"""

    # 检索字符串中的链接
    @staticmethod
    def get_url(text: str) -> Union[str, None]:
        try:
            # 从输入文字中提取索引链接存入列表/Extract index links from input text and store in list
            url = re.findall(
                'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
            # 判断是否有链接/Check if there is a link
            if len(url) > 0:
                return url[0]
        except Exception as e:
            print('Error in get_url:', e)
            return None

    # 转换链接/convert url
    @retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=2))
    async def convert_share_urls(self, url: str) -> Union[str, None]:
        """
        用于将分享链接(短链接)转换为原始链接/Convert share links (short links) to original links
        :return: 原始链接/Original link
        """
        # 检索字符串中的链接/Retrieve links from string
        url = self.get_url(url)
        # 判断是否有链接/Check if there is a link
        if url is None:
            print('无法检索到链接/Unable to retrieve link')
            return None
        # 判断是否为抖音分享链接/judge if it is a douyin share link
        if 'douyin' in url:
            """
            抖音视频链接类型(不全)：
            1. https://v.douyin.com/MuKhKn3/
            2. https://www.douyin.com/video/7157519152863890719
            3. https://www.iesdouyin.com/share/video/7157519152863890719/?region=CN&mid=7157519152863890719&u_code=ffe6jgjg&titleType=title&timestamp=1600000000&utm_source=copy_link&utm_campaign=client_share&utm_medium=android&app=aweme&iid=123456789&share_id=123456789
            抖音用户链接类型(不全)：
            1. https://www.douyin.com/user/MS4wLjABAAAAbLMPpOhVk441et7z7ECGcmGrK42KtoWOuR0_7pLZCcyFheA9__asY-kGfNAtYqXR?relation=0&vid=7157519152863890719
            2. https://v.douyin.com/MuKoFP4/
            抖音直播链接类型(不全)：
            1. https://live.douyin.com/88815422890
            """
            if 'v.douyin' in url:
                # 转换链接/convert url
                # 例子/Example: https://v.douyin.com/rLyAJgf/8.74
                url = re.compile(r'(https://v.douyin.com/)\w+',
                                 re.I).match(url).group()
                print('正在通过抖音分享链接获取原始链接...')
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=self.headers, proxy=self.proxies, allow_redirects=False,
                                               timeout=10) as response:
                            if response.status == 302:
                                url = response.headers['Location'].split('?')[0] if '?' in response.headers[
                                    'Location'] else \
                                    response.headers['Location']
                                print('获取原始链接成功, 原始链接为: {}'.format(url))
                                return url
                except Exception as e:
                    print('获取原始链接失败！')
                    print(e)
                    return None
            else:
                print('该链接为原始链接,无需转换,原始链接为: {}'.format(url))
                return url
        # 判断是否为TikTok分享链接/judge if it is a TikTok share link
        elif 'tiktok' in url:
            """
            TikTok视频链接类型(不全)：
            1. https://www.tiktok.com/@tiktok/video/6950000000000000000
            2. https://www.tiktok.com/t/ZTRHcXS2C/
            TikTok用户链接类型(不全)：
            1. https://www.tiktok.com/@tiktok
            """
            if '@' in url:
                print('该链接为原始链接,无需转换,原始链接为: {}'.format(url))
                return url
            else:
                print('正在通过TikTok分享链接获取原始链接...')
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url, headers=self.headers, proxy=self.proxies, allow_redirects=False,
                                               timeout=10) as response:
                            if response.status == 301:
                                url = response.headers['Location'].split('?')[0] if '?' in response.headers[
                                    'Location'] else \
                                    response.headers['Location']
                                print('获取原始链接成功, 原始链接为: {}'.format(url))
                                return url
                except Exception as e:
                    print('获取原始链接失败！')
                    print(e)
                    return None

    """__________________________________________⬇️Douyin methods(抖音方法)⬇️______________________________________"""

    # 获取抖音视频ID/Get Douyin video ID
    async def get_douyin_video_id(self, original_url: str) -> Union[str, None]:
        """
        获取视频id
        :param original_url: 视频链接
        :return: 视频id
        """
        # 正则匹配出视频ID
        try:
            video_url = await self.convert_share_urls(original_url)
            # 链接类型:
            # 视频页 https://www.douyin.com/video/7086770907674348841
            if '/video/' in video_url:
                key = re.findall('/video/(\d+)?', video_url)[0]
                print('获取到的抖音视频ID为: {}'.format(key))
                return key
            # 发现页 https://www.douyin.com/discover?modal_id=7086770907674348841
            elif 'discover?' in video_url:
                key = re.findall('modal_id=(\d+)', video_url)[0]
                print('获取到的抖音视频ID为: {}'.format(key))
                return key
            # 直播页
            elif 'live.douyin' in video_url:
                # https://live.douyin.com/1000000000000000000
                video_url = video_url.split(
                    '?')[0] if '?' in video_url else video_url
                key = video_url.replace('https://live.douyin.com/', '')
                print('获取到的抖音直播ID为: {}'.format(key))
                return key
            # note
            elif 'note' in video_url:
                # https://www.douyin.com/note/7086770907674348841
                key = re.findall('/note/(\d+)?', video_url)[0]
                print('获取到的抖音笔记ID为: {}'.format(key))
                return key
        except Exception as e:
            print('获取抖音视频ID出错了:{}'.format(e))
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=2))
    async def get_douyin_video_comment(self, video_id: str, cursor: int, count: int) -> Union[dict, None]:
        try:
            api_url = f"https://www.iesdouyin.com/aweme/v1/web/comment/list/?aweme_id={video_id}&cursor={cursor}&count={count}&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333&Github=Evil0ctal&words=FXXK_U_ByteDance"
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=self.headers, proxy=self.proxies, timeout=10) as response:
                    response = await response.json()
                    # print(response['comments'])
                    return response

        except Exception as e:
            print('获取抖音视频数据失败！原因:{}'.format(e))
            return None

    @retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=2))
    async def get_douyin_video_reply(self, video_id: str, comment_id: str, cursor: int, count: int) -> Union[dict, None]:
        try:
            api_url = f"https://www.iesdouyin.com/aweme/v1/web/comment/list/reply/?item_id={video_id}&comment_id={comment_id}&cursor={cursor}&count={count}&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333&Github=Evil0ctal&words=FXXK_U_ByteDance"
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url, headers=self.headers, proxy=self.proxies, timeout=10) as response:
                    response = await response.json()
                    # print(response['comments'])
                    return response
        except Exception as e:
            print('获取抖音视频数据失败！原因:{}'.format(e))
            return None


async def async_test(douyin_url: str = None) -> None:
    # 异步测试/Async test
    start_time = time.time()
    print("正在进行异步测试...")

    print("正在测试异步获取抖音视频ID方法...")
    douyin_id = await api.get_douyin_video_id(douyin_url)
    print("正在测试异步获取抖音视频数据方法...")
    # douyin_data = await api.get_douyin_video_data(douyin_id)
    # 评论总数
    # comment_count = douyin_data['statistics']['comment_count']

    # print(comment_count)
    # 总共299个评论
    i = 0
    size = 50
    # douyin_comment = await api.get_douyin_video_comment(douyin_id, i, 10)
    comments = []
    while comments is not None:
        douyin_comment = await api.get_douyin_video_comment(douyin_id, i*size, size)
        comments = douyin_comment['comments']
        if comments is not None:
            for comment in comments:
                # print(comment['aweme_id'], comment['cid'], comment['ip_label'],
                #       comment['reply_comment_total'], comment['text'].replace('\r', '').replace('\n', ''), comment['user']['nickname'])
                # print(comment['user']['nickname'], ':',
                #       comment['text'].replace('\r', '').replace('\n', ''))
                write_to_file(comment['text'].replace('\r', '').replace('\n', ''))
                if comment['reply_comment_total'] > 0:
                    replys = []
                    j = 0
                    while replys is not None:
                        douyin_reply = await api.get_douyin_video_reply(douyin_id, comment['cid'], j*size, size)
                        replys = douyin_reply['comments']
                        if replys is not None:
                            for reply in replys:
                                # print(reply['user']['nickname'], ':',
                                #       reply['text'].replace('\r', '').replace('\n', ''))
                                write_to_file(reply['text'].replace(
                                    '\r', '').replace('\n', ''))
                        j += 1
        i += 1
    # 总耗时/Total time
    total_time = round(time.time() - start_time, 2)
    print("异步测试完成，总耗时: {}s".format(total_time))

async def write_to_file(content):
    with open('douyin.txt', 'a', encoding='utf-8') as f:
        f.write(content + '\n')

if __name__ == '__main__':
    api = DouYin()
    # 运行测试
    douyin_url = 'https://v.douyin.com/BNS6xHX/'
    asyncio.run(async_test(douyin_url=douyin_url))
