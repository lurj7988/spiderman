# -*- encoding: utf-8 -*-
import os
import aiohttp
import platform
import asyncio
import configparser
import pandas as pd
import pymysql.cursors

from bs4 import BeautifulSoup
from typing import Union
from tenacity import *


class ScrapyBeiKe:
    """__________________________________________⬇️initialization(初始化)⬇️______________________________________"""

    # 初始化/initialization
    def __init__(self):
        self.headers = {
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
            'sec-ch-ua-platform': '"Windows"'
        }
        self.cookies = {
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
        self.conn = pymysql.connect(
            host='192.168.220.236',  # 与本地数据库建立连接，可以尝试其他电脑的ip地址
            port=3306,  # 端口可写可不写，默认3306
            user='root',
            password="Gepoint",
            database="scrapy",  # 选择一个库，关键字可以简化为db
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )  # 更多参数可以点进connect的源码去看
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

    @retry(stop=stop_after_attempt(3), wait=wait_random(min=1, max=2))
    async def get_page_html(self, original_url: str) -> Union[str, None]:
        print(original_url)
        try:
            async with aiohttp.ClientSession(cookies=self.cookies) as session:
                async with session.get(original_url, headers=self.headers, proxy=self.proxies, timeout=10) as response:
                    if response.status == 200:
                        x = await response.content.read()
                        return str(x, 'utf-8')
                    return None
        except Exception as e:
            print('获取数据失败！原因:{}'.format(e))
            return None

    async def get_xiaoqu(self, url: str, page: int = 100) -> Union[list, None]:
        result = []
        for i in range(page):
            param = url + 'pg' + str(i + 1) + '/'
            # print(param)
            html = await self.get_page_html(param)
            if html is not None:
                items = await self.parse_xiaoqu(html)
                if items is None:
                    break
                else:
                    for item in items:
                        result.append(item)
                    time.sleep(1)
        return result

    async def parse_xiaoqu(self, html):
        soup = BeautifulSoup(html, 'lxml')
        listContent = soup.find(attrs={'class': 'listContent'})
        if listContent is None:
            return None
        res = []
        for li in listContent.select('li'):
            info = li.find(attrs={'class': 'info'})
            houseInfo = info.find(attrs={'class': 'houseInfo'}).find_all('a')
            if len(houseInfo) > 1:
                rent = houseInfo[1].text.strip().replace(
                    '正在出租', '').replace('套', '')
            else:
                rent = '0'
            res.append({
                "plot": info.find(attrs={'class': 'maidian-detail'}).text.strip(),
                "deal": houseInfo[0].text.strip().replace('90天成交', '').replace('套', ''),
                "rent": rent,
                "district": li.find(attrs={'class': 'district'}).text.strip(),
                "bizcircle": li.find(attrs={'class': 'bizcircle'}).text.strip(),
                'pricedesc': li.find(attrs={'class': 'priceDesc'}).text.strip(),
                "price": li.find(attrs={'class': 'totalPrice'}).span.text.strip(),
                # li.find(attrs={'class': 'sellCountDesc'}).text.strip()+':'+
                "sellcount": li.find(attrs={'class': 'totalSellCount'}).span.text.strip(),
                "href": info.find(attrs={'class': 'maidian-detail'}).attrs['href'],
                'id': li.attrs['data-id']
            })
        return res

    async def get_sell(self, url: str, id: str, page: int = 100) -> Union[list, None]:
        result = []
        for i in range(page):
            param = url + 'pg' + str(i + 1) + 'c' + id
            # print(param)
            html = await self.get_page_html(param)
            if html is not None:
                items = await self.parse_sell(html)
                if items is None:
                    break
                else:
                    for item in items:
                        result.append(item)
                    time.sleep(1)
        return result

    async def parse_sell(self, html):
        soup = BeautifulSoup(html, 'lxml')
        sellListContent = soup.find(attrs={'class': 'sellListContent'})
        # print(sellListContent)
        if sellListContent is None:
            return None
        res = []
        # print(sellListContent.select('li'))
        for li in sellListContent.select('li'):
            info = li.find(attrs={'class': 'info clear'})
            if info is not None:
                # print(info)
                detail = info.find(
                    attrs={'class': 'VIEWDATA CLICKDATA maidian-detail'}).text.strip()
                isVrFutureHome = info.find(attrs={'class': 'isVrFutureHome'})
                if isVrFutureHome is not None:
                    isVr = isVrFutureHome.text.strip()
                else:
                    isVr = ''
                res.append({
                    'detail': detail.replace(' ', ''),
                    'positionInfo': info.find(attrs={'class': 'positionInfo'}).a.text.strip(),
                    'houseInfo': info.find(attrs={'class': 'houseInfo'}).text.strip().replace('\r', '').replace('\n', '').replace(' ', ''),
                    'followInfo': info.find(attrs={'class': 'followInfo'}).text.strip().replace('\r', '').replace('\n', '').replace(' ', ''),
                    'isVrFutureHome': isVr,
                    'totalPrice': info.find(attrs={'class': 'totalPrice totalPrice2'}).span.text.strip(),
                    'unitPrice': info.find(attrs={'class': 'unitPrice'}).span.text.strip().replace('元/平', ''),
                    'href': info.find(attrs={'class': 'VIEWDATA CLICKDATA maidian-detail'}).attrs['href'],
                    'id': info.find(attrs={'class': 'VIEWDATA CLICKDATA maidian-detail'}).attrs['data-maidian']
                })
        return res

    async def get_deal(self, url: str, id: str, page: int = 100) -> Union[list, None]:
        result = []
        for i in range(page):
            param = url + 'pg' + str(i + 1) + 'c' + id
            # print(param)
            html = await self.get_page_html(param)
            if html is not None:
                items = await self.parse_deal(html)
                if items is None:
                    break
                else:
                    for item in items:
                        result.append(item)
                    time.sleep(1)
        return result

    async def parse_deal(self, html):
        soup = BeautifulSoup(html, 'lxml')
        listContent = soup.find(attrs={'class': 'listContent'})
        # print(listContent.findChild('li'))
        if listContent.findChild('li') is None:
            return None
        res = []
        for li in listContent.select('li'):
            info = li.find(attrs={'class': 'info'})
            title = info.find(
                attrs={'class': 'CLICKDATA maidian-detail'}).text.strip()
            dealCycleTxt = info.find(
                attrs={'class': 'dealCycleTxt'}).find_all('span')
            res.append({
                "plot": title.split(' ')[0],  # 小区
                "type": title.split(' ')[1],  # 房型"
                "area": title.split(' ')[2].replace('平米', ''),  # 建筑面积
                # 总价
                'totalPrice': info.find(attrs={'class': 'totalPrice'}).span.text.strip(),
                # 单价
                'unitPrice': info.find(attrs={'class': 'unitPrice'}).span.text.strip(),
                # 房源成交时间
                'dealDate': info.find(attrs={'class': 'dealDate'}).text.strip(),
                # 挂牌价
                'dealPrice': dealCycleTxt[0].text.strip().replace('挂牌', '').replace('万', ''),
                # 成交周期
                'dealTime': dealCycleTxt[1].text.strip().replace('成交周期', '').replace('天', ''),
                'houseInfo': info.find(attrs={'class': 'houseInfo'}).text.strip(),
                'positionInfo': info.find(attrs={'class': 'positionInfo'}).text.strip(),
                "href": info.find(attrs={'class': 'CLICKDATA maidian-detail'}).attrs['href'],
                'id': info.find(attrs={'class': 'CLICKDATA maidian-detail'}).attrs['data-maidian'],
            })
        return res

    async def export_excel(self, table_name: str, export_data: list, columns_map: dict, order: list):
        with pd.ExcelWriter('./output/'+table_name) as writer:
            pf = pd.DataFrame(list(export_data))  # 将字典列表转换为DataFrame
            pf = pf[order]
            pf.rename(columns=columns_map, inplace=True)
            pf.fillna(" ", inplace=True)  # 替换空单元格
            pf.to_excel(writer, sheet_name="Sheet1", index=False)
            # writer.save()  # 不要用save会提示内容错误

    async def insert_plots(self, plots: list):
        try:
            with self.conn.cursor() as cursor:
                for plot in plots:
                    print(plot)
                    sql = f"INSERT INTO scrapy.suzhou_plots (id, plot, deal, rent, district, bizcircle, pricedesc, price, sellcount, href) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                    cursor.execute(
                        sql, (plot['id'], plot['plot'], plot['deal'], plot['rent'], plot['district'], plot['bizcircle'], plot['pricedesc'], plot['price'], plot['sellcount'], plot['href']))
                self.conn.commit()  # 提交
        except Exception as e:
            self.conn.rollback()  # 回滚事务
            print('数据插入失败！原因:{}'.format(e))
            print(sys.exc_info())  # 打印错误信息
        finally:
            self.conn.close()


async def async_test(original_url: str = None) -> None:
    # print(await api.get_xiaoqu(url=original_url, page=1))
    # print(await api.get_sell('https://su.ke.com/ershoufang/', '2320033135776302'))
    # print(await api.get_deal('https://su.ke.com/chengjiao/', '2320033135776302'))
    xiaoqus = await api.get_xiaoqu(url=original_url, page=1)
    await api.insert_plots(xiaoqus)
    for xiaoqu in xiaoqus:
        id = xiaoqu['id']
        plot = xiaoqu['plot']
        print(plot)
        sells = await api.get_sell('https://su.ke.com/ershoufang/', id=id)
        if len(sells) > 0:
            await api.export_excel(table_name=plot+'在售.xlsx', export_data=sells, columns_map={
                "detail": "详情",
                "positionInfo": "位置",
                "houseInfo": "房屋信息",
                "followInfo": "关注",
                "isVrFutureHome": "VR看房",
                "totalPrice": "总价",
                "unitPrice": "单价",
                "href": "地址",
                'id': 'id'
            }, order=[
                "detail",
                "positionInfo",
                "houseInfo",
                "followInfo",
                "isVrFutureHome",
                "totalPrice",
                "unitPrice",
                "href",
                "id"
            ])
        deals = await api.get_deal('https://su.ke.com/chengjiao/', id=id)
        if len(deals) > 0:
            await api.export_excel(table_name=plot+'成交.xlsx', export_data=deals, columns_map={
                "plot": "小区",
                "type": "房型",
                "area": "建筑面积(平米)",
                "totalPrice": "总价",
                "unitPrice": "单价",
                "dealDate": "出售时间",
                "dealPrice": "挂牌(万)",
                "dealTime": "成交周期(天)",
                "houseInfo": "位置",
                "positionInfo": "房源描述",
                "href": "地址",
                'id': 'id'
            }, order=[
                "plot",
                "type",
                "area",
                "totalPrice",
                "unitPrice",
                "dealDate",
                "dealPrice",
                "dealTime",
                "houseInfo",
                "positionInfo",
                "href",
                'id'
            ])


def get_conn():
    conn = pymysql.connect(
        host='192.168.220.236',  # 与本地数据库建立连接，可以尝试其他电脑的ip地址
        port=3306,  # 端口可写可不写，默认3306
        user='root',
        password="Gepoint",
        database="scrapy",  # 选择一个库，关键字可以简化为db
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )  # 更多参数可以点进connect的源码去看
    return conn


def mysql_test_insert():
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            sql = f"INSERT INTO scrapy.suzhou_plots (id, plot, deal, rent, district, bizcircle, pricedesc, price, sellcount, href) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            cursor.execute(sql, ('1', '2', 5, 3, '4',
                           '5', '6', '99.99', 3, '2'))
            conn.commit()  # 提交
    except Exception as e:
        conn.rollback()  # 回滚事务
        print('数据插入失败！原因:{}'.format(e))
        print(sys.exc_info())  # 打印错误信息
    finally:
        conn.close()


def mysql_test_query():
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            sql = f"SELECT * FROM suzhou_plots;"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
    except Exception as e:
        print('数据查询失败！原因:{}'.format(e))
        print(sys.exc_info())  # 打印错误信息
    finally:
        conn.close()


def mysql_test_update():
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            sql = f"update suzhou_plots set deal=%s;"
            cursor.execute(sql, (100))
            conn.commit()  # 提交
    except Exception as e:
        conn.rollback()  # 回滚事务
        print('数据更新失败！原因:{}'.format(e))
        print(sys.exc_info())  # 打印错误信息
    finally:
        conn.close()


def mysql_test_delete():
    conn = get_conn()
    try:
        with conn.cursor() as cursor:
            sql = f"delete from suzhou_plots where id=%s;"
            cursor.execute(sql, ('1'))
            conn.commit()  # 提交
    except Exception as e:
        conn.rollback()  # 回滚事务
        print('数据更新失败！原因:{}'.format(e))
        print(sys.exc_info())  # 打印错误信息
    finally:
        conn.close()


if __name__ == '__main__':
    api = ScrapyBeiKe()
    # 在售小区
    chushou_url = 'https://su.ke.com/ershoufang/c2320033135776302/'
    # 已售小区
    chenjiao_url = 'https://su.ke.com/chengjiao/c2320033135776302/'
    asyncio.run(async_test(
        original_url='https://su.ke.com/xiaoqu/zhangjiagang/'))
    # mysql_test_insert()
    # mysql_test_query()
    # mysql_test_update()
    # mysql_test_delete()
