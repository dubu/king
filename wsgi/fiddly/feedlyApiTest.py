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
import datetime
import copy
import pytz

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
            global g_seq
            g_seq = 1
            g_seq = seq
            return name + str(seq) + ".json";

    content = client.get_feed_content(access_token,category,unreadOnly=True)
    if content.get("errorCode") == 503 :
        exit();

    # print(content)

    fname = getFileName(name, seq)
    print(fname)
    f= open(fname, 'w', encoding='utf-8')

    def print_format(str):
        # print(str)
        f.write(str + "\n")

    cnt = 0
    print_format ("{\"sessions\": [")

    roomList = []
    for item in content['items']:

        room = {}
        room["id"] = item['originId']
        if(item.get('author')) :
            room["name"] = item['author']
        else:
            room["name"] = ""
        roomList.append(room)

        print_format ("{")
        print_format ("\"id\":\"%s\"," %(item['originId']))
        print_format ("\"url\":\"%s\"," %(item['alternate'][0]['href']))
        if item.get('title') :
            print_format ("\"title\":\"%s\"," %(item['title'].replace("\"","\\\"")))
        else :
            print_format ("\"title\":\"%s\"," %(""))

        # fix image width

        if item.get('summary') :
            soup = BeautifulSoup(item['summary']['content'], "lxml")
        elif item.get('content') :
            soup = BeautifulSoup(item['content']['content'], "lxml")
        else :
            soup = BeautifulSoup(item['title'], "lxml")

        for img  in soup.findAll("img")  :
            if img.get("src") and re.search("ccl_|creativecommons",img.get("src")) :
                print("except ccl mark")
            else :
                img["width"] = "100%"
                img["height"] = ""

        description = str(soup)
        description = cgi.escape(description , True).replace("\n","\\n")

        # remove iframe
        ifame_url = re.search('&lt;iframe(.*?)/iframe&gt;', description)
        if ifame_url != None:
            description  = description.replace(ifame_url.group(0),"")

        # news aHref 보정

        # if item['categories'][0]['label'].upper() == "NEWS":
        #     for aTagList  in soup.findAll("a")  :
        #         ## aTagList = BeautifulSoup(str(aTagList), "lxml").body.contents[0]
        #         aTagLastTmp =  aTagList[-1]
        #         for aTag in  aTagList :
        #             aTag = aTag["text"]
        #         aTagList[-1] = aTagLastTmp

        # fix image width
        # soup = BeautifulSoup(item['summary']['content'], "lxml")

        # if item.get('summary') :
        #     soup = BeautifulSoup(item['summary']['content'], "lxml")
        # else :
        #     soup = BeautifulSoup(item['content']['content'], "lxml")

        for img  in soup.findAll("img")  :
            img = BeautifulSoup(str(img), "lxml").body.contents[0]
            img["width"] = "50%"
            img["height"] = ""

        print_format ("\"description\":\"%s\"," %(description))

        # startTimestamp = dateutil.parser.parse("02-02-2016").strftime('%Y-%m-%dT%H:%M:%SZ')
        # startTimestamp = datetime.datetime.fromtimestamp(item['crawled'][:3]).strftime('%Y-%m-%dT%H:%M:%SZ')
        tmpTimestamp =  str(item['crawled'])[:-3]
        # print(tmpTimestamp)
        #cwTimestamp =datetime.datetime.fromtimestamp(int(tmpTimestamp)).strftime('%Y-%m-%dT%H:%M:%SZ')
        #cwTimestamp = dateutil.parser.parse("02-02-2016").strftime('%Y-%m-%dT%H:%M:%SZ')

        local = pytz.timezone ("Asia/Seoul")
        naive = datetime.datetime.fromtimestamp(int(tmpTimestamp))
        local_dt = local.localize(naive, is_dst=None)
        utc_dt = local_dt.astimezone (pytz.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        print_format ("\"startTimestamp\":\"%s\"," %(utc_dt))
        print_format ("\"endTimestamp\":\"%s\"," %(utc_dt))

        print_format ("\"isFeatured\":%s," %("false"))

        # soup = BeautifulSoup(item['summary']['content'], "lxml")

        # if item.get('summary') :
        #     soup = BeautifulSoup(item['summary']['content'], "lxml")
        # else :
        #     soup = BeautifulSoup(item['content']['content'], "lxml")

        # page_images = [image["src"] for image in soup.findAll("img")]
        # img =  soup.findAll("img")[0]

        if item['categories'][0]['label'].upper() == "MOVIE":
            vid = item['originId'].split(":")[-1]
            print_format ("\"photoUrl\":\"http://i.ytimg.com/vi/%s/mqdefault.jpg\"," %(vid))
        else :
            if(soup.findAll("img") and soup.findAll("img")[0].get("src")):
                if not re.search("ccl_",soup.findAll("img")[0]["src"]):
                    if re.search("uf.tistory.com",soup.findAll("img")[0]["src"]) :
                        print_format ("\"photoUrl\":\"%s\"," %(soup.findAll("img")[0]["src"].replace("/image/","/T250x250/")))
                    else:
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

        # session is tagged by TOPIC, THEME and TYPE
        topicCatetory = ["SHORT","NEWS", "MOVIE"]
        if item['categories'][0]['label'].upper() in topicCatetory:
            print_format ("\"tags\": [\"TOPIC_%s\",\"TOPIC_ALL\"]," %(item['categories'][0]['label'].upper()))
            print_format ("\"mainTag\":\"TOPIC_%s\"," %(item['categories'][0]['label'].upper()))
        else:
            print_format ("\"tags\": [\"THEME_%s\",\"THEME_ALL\"]," %(item['categories'][0]['label'].upper()))
            print_format ("\"mainTag\":\"THEME_%s\"," %(item['categories'][0]['label'].upper()))

        print_format ("\"hashtag\":\"%s\"," %("uuu"))
        print_format ("\"color\":\"%s\"," %("#ffffff"))
        # author = item['author'];
        # if author != None:
        #     print_format ("\"speakers\":[\"%s\"]," %(item['author']))
        # else:
        #     print_format ("\"speakers\":[\"%s\"]," %(""))

        print_format ("\"speakers\":[\"%s\"]," %(""))
        print_format ("\"room\":\"%s\"," %(item['originId']))
        print_format ("\"captionsUrl\":\"%s\"" %(""))

        if cnt < len(content['items']) - 1:
            print_format("},")
        else:
            print_format("}")
        cnt += 1

    print_format ("]")

    if item['categories'][0]['label'].upper() in topicCatetory:
        print_format(", \"tags\":[ { \"category\":\"TOPIC\", \"tag\":\"TOPIC_%s\", \"name\":\"%s\", \"original_id\":\"tag_topic_blog\", \"abstract\":\"\", \"order_in_category\":4 } , { \"category\":\"TOPIC\", \"tag\":\"TOPIC_ALL\", \"name\":\"ETC_ALL\", \"original_id\":\"tag_topic_all\", \"abstract\":\"\", \"order_in_category\":3 }]" %(item['categories'][0]['label'].upper() ,item['categories'][0]['label'].upper()) )
    else :
        print_format(", \"tags\":[ { \"category\":\"THEME\", \"tag\":\"THEME_%s\", \"name\":\"%s\", \"original_id\":\"tag_theme_blog\", \"abstract\":\"\", \"order_in_category\":2 } , { \"category\":\"THEME\", \"tag\":\"THEME_ALL\", \"name\":\"ALL\", \"original_id\":\"tag_theme_all\", \"abstract\":\"\", \"order_in_category\":1 }]" %(item['categories'][0]['label'].upper() ,item['categories'][0]['label'].upper()) )

    print_format(",\"rooms\": [")
    cnt = 0
    for r in roomList :
        print_format("{")
        tmplet  ='''
            "id": "%s",
            "name": "%s",
            "original_id": "%s"
        '''
        print_format(tmplet %(r.get("id") ,r.get("name").replace("\"","\\\""),r.get("id") ))
        if cnt < len(roomList) - 1:
            print_format("},")
        else:
            print_format("}")
        cnt += 1
    print_format("]}")
    f.close()

makeFile("../static/it_v",1, cates[0])
makeFile("../static/media_v",1,cates[1])
makeFile("../static/life_v",1,cates[2])
makeFile("../static/enter_v",1,cates[3])
makeFile("../static/short_v",1,cates[4])
makeFile("../static/fun_v",1,cates[5])
makeFile("../static/alram_v",1,cates[6])
makeFile("../static/movie_v",1,cates[7])

ff= open("../static/manifest_v1.json", 'w', encoding='utf-8')
ff.write("{\"format\":\"iosched-json-v1\",\"data_files\":[\"enter_v%d.json\",\"it_v%d.json\",\"life_v%d.json\",\"media_v%d.json\",\"short_v%d.json\",\"fun_v%d.json\",\"alram_v%d.json\",\"movie_v%d.json\"]}" %(g_seq,g_seq,g_seq,g_seq,g_seq,g_seq,g_seq,g_seq))
ff.close()