from urllib import request, parse
from lxml import html
import os
import base64
import json

CCL_ID = os.environ["CCL_ID"]
CCL_PASSWORD = os.environ["CCL_PASSWORD"]
CCL_URL = os.environ["CCL_URL"]
LINE_TOKEN = os.environ["LINE_TOKEN"]
LINE_ID = os.environ["LINE_ID"]

if not os.path.exists("./backup.db"):
    with open("backup.db", mode="w", encoding="utf-8") as f:
        f.write("")


def ccl_scraping():
    # Basic認証用の文字列を作成.
    basic_user_and_pasword = base64.b64encode('{}:{}'.format(CCL_ID, CCL_PASSWORD).encode('utf-8'))

    req = request.Request(CCL_URL, headers={"Authorization": "Basic " + basic_user_and_pasword.decode('utf-8')})
    data = request.urlopen(req)
    raw_html = data.read().decode("utf-8")
    # print(raw_html)
    res_html = html.fromstring(str(raw_html))
    # print(res_html)
    tr_data = res_html.xpath("//table[1]//tr")
    tr_data = tr_data[2:-9]

    # parse
    for tr in tr_data:
        gakusei_id = tr.xpath('td//text()')[0]
        gakusei_name = tr.xpath('td//text()')[1]
        kadais = tr.xpath('td')
        kadais = [x.xpath('span') for x in kadais][2:7]
        # print(kadais)
        for i, kadai in enumerate(kadais):
            if len(kadai) == 1:
                # print(kadai[0].text)
                if "提出" in kadai[0].text:
                    index = i + 1
                    res_str = f"{gakusei_id}/{gakusei_name} さんが 課題{index} を提出しました"
                    with open("backup.db", mode="r", encoding="utf-8") as f:
                        db_list = f.readlines()
                    if res_str not in db_list:
                        # LINE通知を送る
                        db_list.append(res_str)
                        with open("backup.db", mode="w", encoding="utf-8") as f:
                            f.writelines(db_list)
                        print(res_str)

                        res_dict = {
                            "to": LINE_ID,
                            "messages":[{"type":"text", "text":res_str}]
                        }
                        post_headers = {
                            'Content-Type': 'application/json',
                            'Authorization': f'Bearer {LINE_TOKEN}'
                        }
                        post_req = request.Request('https://api.line.me/v2/bot/message/push',
                            data=json.dumps(res_dict).encode(), headers=post_headers, method='POST')
                        req = request.urlopen(post_req)
                    else:
                        # なにもしない
                        pass



if __name__ == '__main__':
    ccl_scraping()
