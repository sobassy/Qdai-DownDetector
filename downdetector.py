import urllib.request
import urllib.error
from datetime import datetime, timedelta
from scraper import GetHomePage, GetCampusmate, GetMoodle
import tweepy
import time
import os

CK = os.environ['CK']
CS = os.environ['CS']
AT = os.environ['AT']
AS = os.environ['AS']

# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)

api = tweepy.API(auth)

def checkurl(url):
    # URLにアクセスする htmlが帰ってくる → <html><head><title>経済、株価、ビジネス、政治のニュース:日経電子版</title></head><body....
    try:
        urllib.request.urlopen(url)
        status = 200
        words = "正常"
    except urllib.error.HTTPError as e:
        status = e.code
        words = "ダウン"
    except Exception as e:
        status = None
        words = "ダウン"
    print(status, words)
    return status, words

checker = "正常"

before_moodle = ""
before_campusmate = ""
before_homepege = ""

while True:
    try:
        char = "【九大Webサービス情報】\n\n"
        url = "https://moodle.s.kyushu-u.ac.jp"
        status1, words = checkurl(url)
        char += "moodle  {} {}\n".format(words, status1)

        if status1 == 200:
            txt = GetMoodle()
            if before_moodle != txt and before_moodle != "":
                tmp = "九大Moodleのニュースが更新されました\n\n{}\n\nhttps://moodle.s.kyushu-u.ac.jp/".format(txt)
                api.update_status(status=tmp)
            before_moodle = txt

        url = "https://ku-portal.kyushu-u.ac.jp"
        status2, words = checkurl(url)
        char += "Campusmate  {} {}\n".format(words, status2)

        if status1 == 200:
            # txt = GetCampusmate()
            if before_campusmate != txt and before_campusmate != "":
                tmp = "Campusmateのニュースが更新されました\n\n{}\n\nhttps://ku-portal.kyushu-u.ac.jp/campusweb/login.do".format(txt)
                api.update_status(status=tmp)
            before_campusmate = txt

        url = "https://www.lib.kyushu-u.ac.jp"
        status3, words = checkurl(url)
        char += "図書館ポータル  {} {}\n".format(words, status3)

        url = "https://www.kyushu-u.ac.jp"
        status4, words = checkurl(url)
        char += "ホームページ  {} {}\n\n".format(words, status4)

        if status1 == 200:
            txt, murl = GetHomePage()
            if before_homepege != txt and before_homepege != "":
                tmp = "九大HPのニュースが更新されました\n\n{}\n\n{}".format(txt, murl)
                api.update_status(status=tmp)
            before_homepege = txt

        nowdate = datetime.now()
        nowdate = nowdate + timedelta(hours=9)
        char += nowdate.strftime("%Y/%m/%d %H:%M:%S")
        char += "\n#九大サーバ情報"

        before_checker = checker
        if status1 == status2 == status3 == status4 == 200:
            checker = "正常"
        else:
            checker = "異常"
        if before_checker != checker:
            api.update_status(status=char)
            print("tweeted!")
        else:
            print("Stay")

    except Exception as e:
        print(e)

    time.sleep(30)