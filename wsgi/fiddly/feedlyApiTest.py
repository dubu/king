#/usr/bin/env python3
# -*- encoding: utf-8 -*-

import json
import requests
import re
import os
import cgi
import dateutil.parser
from datetime import *
from dateutil.parser import *
from bs4 import BeautifulSoup

from feedly import FeedlyClient

def json_fetch(url, method, params={}, data={}, headers={}):
    response = requests.request(
            method, url, params=params, data=json.dumps(data), headers=headers)
    return response.json()

FEEDLY_REDIRECT_URI = "http://fabreadly.com/auth_callback"
FEEDLY_CLIENT_ID="sandbox"
FEEDLY_CLIENT_SECRET="JSSBD6FZT72058P51XEG"
# a = FeedlyClient(client_id=FEEDLY_CLIENT_ID,client_secret=FEEDLY_CLIENT_SECRET,sandbox=True)

def get_feedly_client(token=None):
    if token:
        return FeedlyClient(token=token, sandbox=False)
    else:
        return FeedlyClient(
                client_id=FEEDLY_CLIENT_ID,
                client_secret=FEEDLY_CLIENT_SECRET,
                sanbox=False
        )

json_data=open('settings.json')
data=json.load(json_data)
access_token=data['access_token']
cates=data['category']
client = get_feedly_client(access_token)

categoryList = client.get_user_categories(access_token)
print(categoryList)


# item = client.get_feed_content(access_token,'feed/http://lucy7599.tistory.com/rss')
# print(item)

def makeFile(name ,seq ,category):

    def getFileName(name, seq):
        if os.path.isfile(name + str(seq) + ".json"):
            return getFileName(name, seq+1)
        else:
            return name + str(seq) + ".json";

    content = client.get_feed_content(access_token,category,unreadOnly=True)
    # print(content)

    fname = getFileName(name, seq)
    print(fname)
    f= open(fname, 'w', encoding='utf-8')

    def print_format(str):
        # print(str)
        f.write(str + "\n")

    cnt = 0
    print_format ("{\"sessions\": [")
    for item in content['items']:
        print_format ("{")
        print_format ("\"id\":\"%s\"," %(item['originId']))
        print_format ("\"url\":\"%s\"," %(item['alternate'][0]['href']))
        print_format ("\"title\":\"%s\"," %(item['title'].replace("\"","\\\"")))

        description = cgi.escape(item['summary']['content'], True).replace("\n","\\n")
        print_format ("\"description\":\"%s\"," %(description))

        startTimestamp = dateutil.parser.parse("02-02-2016").strftime('%Y-%m-%dT%H:%M:%SZ')
        endTimestamp = dateutil.parser.parse("02-02-2016").strftime('%Y-%m-%dT%H:%M:%SZ')
        print_format ("\"startTimestamp\":\"%s\"," %(startTimestamp))
        print_format ("\"endTimestamp\":\"%s\"," %(endTimestamp))

        print_format ("\"isFeatured\":%s," %("false"))

        soup = BeautifulSoup(item['summary']['content'], "lxml")
        # page_images = [image["src"] for image in soup.findAll("img")]
        # img =  soup.findAll("img")[0]

        if(soup.findAll("img")):
            print_format ("\"photoUrl\":\"%s\"," %(soup.findAll("img")[0]["src"]))
        else:
            print_format ("\"photoUrl\":\"%s\"," %(""))

        # photo_url = re.search('img src="(.*?)"', item['summary']['content'])
        # if photo_url != None:
        #     print_format ("\"photoUrl\":\"%s\"," %(photo_url).group(1))
        # else:
        #     print_format ("\"photoUrl\":\"%s\"," %(""))

        print_format ("\"isLivestream\":%s," %("true"))
        print_format ("\"youtubeUrl\":\"%s\"," %(""))
        print_format ("\"tags\": [\"THEME_%s\",\"THEME_Tistory\"]," %(item['categories'][0]['label'].upper()))
        print_format ("\"mainTag\":\"THEME_%s\"," %(item['categories'][0]['label'].upper()))
        print_format ("\"hashtag\":\"%s\"," %("uuu"))
        print_format ("\"color\":\"%s\"," %("#ffffff"))
        # author = item['author'];
        # if author != None:
        #     print_format ("\"speakers\":[\"%s\"]," %(item['author']))
        # else:
        #     print_format ("\"speakers\":[\"%s\"]," %(""))

        print_format ("\"speakers\":[\"%s\"]," %("dubu"))

        print_format ("\"room\":\"%s\"," %(""))
        print_format ("\"captionsUrl\":\"%s\"" %(""))

        if cnt < len(content['items']) - 1:
            print_format("},")
        else:
            print_format("}")
        cnt += 1

    print_format ("]")
    print_format(", \"tags\":[ { \"category\":\"THEME\", \"tag\":\"THEME_%s\", \"name\":\"%s\", \"original_id\":\"tag_theme_blog\", \"abstract\":\"\", \"order_in_category\":4 } ] }" %(item['categories'][0]['label'].upper() ,item['categories'][0]['label'].upper()) )
    f.close()

makeFile("../static/it_v",1, cates[0])
makeFile("../static/media_v",1,cates[1])
makeFile("../static/life_v",1,cates[2])
makeFile("../static/enter_v",1,cates[3])

