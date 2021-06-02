import requests
from bs4 import BeautifulSoup
from lxml import html
import re

def GetCampusmate():
    urlName = "https://ku-portal.kyushu-u.ac.jp/campusweb/wbaskopr.do?buttonName=delayedSearchKokaiOhirase"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Host": "ku-portal.kyushu-u.ac.jp",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "ja-JP,ja;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    session = requests.Session()
    req = session.get(urlName, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")

    lxml_coverted_data = html.fromstring(str(soup))

    top_data = lxml_coverted_data.xpath('//a/text()')
    return top_data[0]

def GetMoodle():
    urlName = "https://moodle.s.kyushu-u.ac.jp/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    }
    cookie = {}

    session = requests.Session()
    req = session.get(urlName, headers=headers, cookies=cookie)
    soup = BeautifulSoup(req.text, "html.parser")

    lxml_coverted_data = html.fromstring(str(soup))

    top_data = lxml_coverted_data.xpath('//h3/text()')
    return top_data[0]

def GetHomePage():
    urlName = "https://www.kyushu-u.ac.jp/ja/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    }
    cookie = {}

    session = requests.Session()
    req = session.get(urlName, headers=headers, cookies=cookie)
    soup = BeautifulSoup(req.text, "html.parser")

    lxml_coverted_data = html.fromstring(str(soup))

    top_data = lxml_coverted_data.xpath('//div[contains(@class, "img_float")]//dd/a/text()')
    url_data = lxml_coverted_data.xpath('//div[contains(@class, "img_float")]//dd/a/@href')

    return top_data[0], "https://www.kyushu-u.ac.jp/"+url_data[0]

# print(GetHomePage())