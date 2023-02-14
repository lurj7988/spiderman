# 利用BeautifulSoup抓取二手房成交数据

import time
import json
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from scrapy.selector import Selector
import pandas as pd


def get_one_page(url):
    try:
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            # 'Cookie': 'SECKEY_ABVK=aeXkIf7wcr63OG8HnXiv6HP1F6w1KgsoefAhbHeQMTQ=; BMAP_SECKEY=wjAFck9zd5zpnA3A78bJnzRoCZNxHVa73qsQwZnH6Xc6s5pdmt9RZ-vUiTkM2PQdjzROhIQiejhyfOTWpU7FQwSqevAF_2VuydrjlvooLy2GahSEROu-zaomqMYrBZDIvGy0P9j7OT_Div3JFxaEcluwtU8v1AhTaW6QzSpqPTRkLoZ0LppfjOcqACLBVzG5; lianjia_uuid=37c0b42b-2329-40d5-8ce0-674e2f4adb7e; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1675646646; sajssdk_2015_cross_new_user=1; hy_data_2020_id=1862462339768-0485feda2bc2de-26021051-3686400-18624623398104c; hy_data_2020_js_sdk={"distinct_id":"1862462339768-0485feda2bc2de-26021051-3686400-18624623398104c","site_id":341,"user_company":236,"props":{},"device_id":"1862462339768-0485feda2bc2de-26021051-3686400-18624623398104c"}; sajssdk_2020_cross_new_user=1; crosSdkDT2019DeviceId=-3ehvlu-fcmjkf-wbhnm4lczapf5ez-bjgju9uv2; sensorsdata2015jssdkcross={"distinct_id":"1862452b6041090-0540935e650e44-26021051-3686400-1862452b6051064","$device_id":"1862452b6041090-0540935e650e44-26021051-3686400-1862452b6051064","props":{"$latest_traffic_source_type":"直接流量","$latest_referrer":"","$latest_referrer_host":"","$latest_search_keyword":"未取到值_直接打开","$latest_utm_source":"baidu","$latest_utm_medium":"pinzhuan","$latest_utm_campaign":"wysuzhou","$latest_utm_content":"biaotimiaoshu","$latest_utm_term":"biaoti"}}; lianjia_ssid=82f8b969-9ef1-4fac-96fd-a67415ff3aaa; select_city=320500; login_ucid=2000000252945550; lianjia_token=2.0012f539657943f00703581054ae7e915c; lianjia_token_secure=2.0012f539657943f00703581054ae7e915c; security_ticket=rh3NWOtYFDxcM+oORtI+ftjizpxGGZHNLCDQjU1hmttv4JEkjEoEOM9AyeUweGUvMgXPNyg+XuC2GDtM5BqmOs4UK7nINNmfeVfEqi09sxlgRJb1Hj+Y4t1fqsR+HltfVwjxRgL9wkx9TCn+vA9XYNEkm+4zwFvTLa5HsfTUtz0=; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1675664498; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiY2UzNmVjM2YzNzZhZGRjNzllNTA4MzM3Y2E4ZjUzMzZiNWZkZmZkODA0ZDE2ODU4ZmVjYzU0NTFkNTJkMDQ5ZjZiY2M4OWRkMGFhMWE1ZjJhY2FjZDA1NWQyNjZhZjIxODU0YWJiNDFmNGY2MmVjMjA4NTM1NDIxN2YxYjFiMTFjNWE0OWIwMmMzOGY3OTA4OTJhZjlkZjFhN2IwN2NhNDgzNTBhMmNiNzEyYjUzYTRjYjg0NzE2OWFhNGQ0ZjYwYjg1MzNiNTFiOWY5OWExYzc2YTk4OTNjZTc2OGM5MGVhOThlMmNkZDc4YmYyNGU3Mzk5YzM1ZGEwMDEzMGI5M1wiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCI1NjY5YzFkMVwifSIsInIiOiJodHRwczovL3N1LmtlLmNvbS9jaGVuZ2ppYW8vIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0=',
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
        cookies = {
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

        response = requests.get(url, headers=headers, cookies=cookies)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_two_page(html):
    soup = BeautifulSoup(html, 'lxml')

    items = soup.find_all(attrs={'class': 'img CLICKDATA maidian-detail'})
    items1 = soup.find_all(attrs={'class': 'CLICKDATA maidian-detail'})
    items2 = soup.find_all(attrs={'class': 'houseInfo'})
    items3 = soup.find_all(attrs={'class': 'positionInfo'})
    items4 = soup.find_all(attrs={'class': 'totalPrice'})
    items5 = soup.find_all(attrs={'class': 'unitPrice'})
    items6 = soup.find_all(attrs={'class': 'dealCycleTxt'})
    items7 = soup.find_all(attrs={'class': 'dealDate'})

    i = 0
    for item in items:
        title = items1[i].text.strip()
        yield {
            "plot": title.split(' ')[0],  # 小区
            "type": title.split(' ')[1],  # 房型"
            "area": title.split(' ')[2],  # 建筑面积
            'totalPrice': items4[i].span.text + '万',  # 总价
            'unitPrice': items5[i].span.text + '元/平米',  # 单价
            'dealDate': items7[i].text.strip(),  # 房源成交时间
            'dealPrice': items6[i].span.text,  # 挂牌价
            'dealTime': parse_chengjiao(items6, i),  # 成交周期
            'href': item.attrs['href'],  # 跳转链接
            'image': item.img['data-original'],  # 图片
            # 房源描述
            'houseInfo': items2[i].text.strip() + items3[i].text.strip(),
        }
        i += 1


def parse_chengjiao(items6, i):
    guaTime = ''
    for item in items6[i]:
        strDf = str(item)
        if (strDf.find('成交周期', 0, len(strDf)) > -1):
            guaTime = strDf[6:len(strDf) - 7]
    return guaTime


def write_to_file(content):
    with open('deal.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def startGetData(page, *district):
    url = 'https://su.ke.com/chengjiao/'

    addrParam = ''
    for param in district:
        addrParam = str(param)
    if (len(addrParam) > 0):
        url = url + addrParam + '/pg'
    else:
        url = url + 'pg'
    result = []
    for i in range(page):
        param = url + str(i + 1) + '/'
        html = get_one_page(param)
        if html is None:
            return
        for item in parse_two_page(html):
            # print(item)
            result.append(item)
            # write_to_file(item)
        time.sleep(1)
    export_excel(result)


def export_excel(export_list):
    table_name = "张家港二手房交易.xlsx"
    with pd.ExcelWriter(table_name) as writer:
        pf_failed = format_excel(export_list)
        pf_failed.to_excel(writer, sheet_name="Sheet1", index=False)
        writer.save()  # 保存表格


def format_excel(export_data: list):
    columns_map = {
        "plot": "小区",
        "type": "房型",
        "area": "建筑面积",
        "totalPrice": "总价",
        "unitPrice": "单价",
        "dealDate": "出售时间",
        "dealPrice": "挂牌",
        "dealTime": "成交周期",
        "href": "地址",
        "image": "图片",
        "houseInfo": "房源描述",
    }   # 将列名替换为中文
    order = [
        "plot",
        "type",
        "area",
        "totalPrice",
        "unitPrice",
        "dealDate",
        "dealPrice",
        "dealTime",
        "href",
        "image",
        "houseInfo",
    ]  # 指定字段顺序
    pf = pd.DataFrame(list(export_data))  # 将字典列表转换为DataFrame
    pf = pf[order]
    pf.rename(columns=columns_map, inplace=True)
    pf.fillna(" ", inplace=True)  # 替换空单元格
    return pf


def export_e(table_name: str, export_data: list, columns_map: dict, order: list):
    with pd.ExcelWriter(table_name) as writer:
        pf = pd.DataFrame(list(export_data))  # 将字典列表转换为DataFrame
        pf = pf[order]
        pf.rename(columns=columns_map, inplace=True)
        pf.fillna(" ", inplace=True)  # 替换空单元格
        pf.to_excel(writer, sheet_name="Sheet1", index=False)
        writer.save()  # 保存表格


def startGetXiaoQuData(page, table_name, *district):
    url = 'https://su.ke.com/xiaoqu/'
    addrParam = ''
    for param in district:
        addrParam = str(param)
    if (len(addrParam) > 0):
        url = url + addrParam + '/pg'
    else:
        url = url + 'pg'
    result = []
    for i in range(page):
        param = url + str(i + 1) + '/'
        # print(param)
        html = get_one_page(param)
        if html is None:
            return
        for item in parse_XiaoQu(html):
            result.append(item)
        time.sleep(1)
    export_e(table_name+'小区.xlsx', result, {
        "plot": '小区',
        "deal": '90天成交(套)',
        "rent": '正在出租(套)',
        "district": '地点',
        "bizcircle": '位置',
        'priceDesc': '参考月份',
        "price": '成交价(元/平方米)',
        "sellCount": '在售二手房(套)',
        "href": '链接'
    }, ['plot', 'deal', 'rent', 'district', 'bizcircle', 'priceDesc', 'price', 'sellCount', 'href'])


def parse_XiaoQu(html):
    soup = BeautifulSoup(html, 'lxml')
    listContent = soup.find(attrs={'class': 'listContent'})
    res = []
    for li in listContent.select('li'):
        info = li.find(attrs={'class': 'info'})
        houseInfo = info.find(attrs={'class': 'houseInfo'}).find_all('a')
        if len(houseInfo) > 1:
            rent = houseInfo[1].text.strip().replace(
                '正在出租', '').replace('套', '')
        else:
            rent = ''

        res.append({
            "plot": info.find(attrs={'class': 'maidian-detail'}).text.strip(),
            "deal": houseInfo[0].text.strip().replace('90天成交', '').replace('套', ''),
            "rent": rent,
            "district": li.find(attrs={'class': 'district'}).text.strip(),
            "bizcircle": li.find(attrs={'class': 'bizcircle'}).text.strip(),
            'priceDesc': li.find(attrs={'class': 'priceDesc'}).text.strip(),
            "price": li.find(attrs={'class': 'totalPrice'}).span.text.strip(),
            # li.find(attrs={'class': 'sellCountDesc'}).text.strip()+':'+
            "sellCount": li.find(attrs={'class': 'totalSellCount'}).span.text.strip(),
            "href": info.find(attrs={'class': 'maidian-detail'}).attrs['href']
        })
    return res


def startGetChengJiaoData(page, table_name, *district):
    url = 'https://su.ke.com/chengjiao/'

    addrParam = ''
    for param in district:
        addrParam = str(param)
    if (len(addrParam) > 0):
        url = url + addrParam + '/pg'
    else:
        url = url + 'pg'
    result = []
    for i in range(page):
        param = url + str(i + 1) + '/'
        html = get_one_page(param)
        if html is None:
            return
        for item in parse_ChengJiao(html):
            # print(item)
            result.append(item)
            # write_to_file(item)
        time.sleep(1)
    export_e(table_name+'成交.xlsx', result, {
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
    }, [
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
    ])


def parse_ChengJiao(html):
    soup = BeautifulSoup(html, 'lxml')
    listContent = soup.find(attrs={'class': 'listContent'})
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
            "href": info.find(attrs={'class': 'CLICKDATA maidian-detail'}).attrs['href']
        })
    return res


if __name__ == '__main__':
    # 抓取数据 参数一：总页数，参数二：区县，可选、不传默认全部
    # startGetData(48, 'zhangjiagang')
    # startGetXiaoQuData(14, '工业园区.xlsx', 'gongyeyuan')
    #startGetChengJiaoData(48, '张家港', 'zhangjiagang')
    startGetChengJiaoData(100, '工业园区', 'gongyeyuan')
    # response = get_one_page('https://su.ke.com/chengjiao/zhangjiagang/')
    # selector = Selector(response)
    # title = selector.xpath(
    #     '//*[@class="listContent"]/li//*[@class="title"]/a/text()').extract()
    # houseInfo = selector.xpath(
    #     '//*[@class="listContent"]/li//*[@class="houseInfo"]/text()').extract()
    # totalPrice = selector.xpath(
    #     '//*[@class="listContent"]/li//*[@class="totalPrice"]/span/text()').extract()
    # dealDate = selector.xpath(
    #     '//*[@class="listContent"]/li//*[@class="dealDate"]/text()').extract()
    # positionInfo = selector.xpath(
    #     '//*[@class="listContent"]/li//*[@class="positionInfo"]/text()').extract()
    # unitPrice = selector.xpath(
    #     '//*[@class="listContent"]/li//*[@class="unitPrice"]/span/text()').extract()
    # dealCycleTxt1 = selector.xpath(
    #     '//*[@class="listContent"]/li//*[@class="dealCycleTxt"]/span[1]/text()').extract()
    # dealCycleTxt2 = selector.xpath(
    #     '//*[@class="listContent"]/li//*[@class="dealCycleTxt"]/span[2]/text()').extract()
    # for a in title:
    #     a = a.replace('\n', '').replace('\r', '').replace(' ', '')
    #     if a != '':
    #         print(a)
