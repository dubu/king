import re
from bs4 import BeautifulSoup

msg = '''
다.&lt;/span&gt;&lt;/p&gt;&lt;p&gt;&lt;span style=&quot;font-family: Gulim, 굴림, AppleGothic, sans-serif; font-size: 14pt;&quot;&gt;㉢ 동그랑땡을 올려준다.&lt;/span&gt;&lt;/p&gt;&lt;p&gt;&lt;br /&gt;&lt;/p&gt;&lt;p&gt;&lt;br /&gt;&lt;/p&gt;&lt;p style=&quot;text-align: center; clear: none; float: none;&quot;&gt;&lt;br /&gt;&lt;/p&gt;&lt;p&gt;&lt;br /&gt;&lt;/p&gt;&lt;p style=&quot;text-align: center;&quot;&gt;&lt;table cellspacing=&quot;5&quot; cellpadding=&quot;0&quot; border=&quot;0&quot; align=&quot;center&quot;&gt;&lt;tbody&gt;&lt;tr&gt;&lt;td&gt;&lt;span class=&quot;imageblock&quot; style=&quot;display:inline-block;width:242px;;height:auto;max-width:100%&quot;&gt;&lt;img src=&quot;http://cfile26.uf.tistory.com/image/235DE74D56B8A9AF0E12CE&quot; filemime=&quot;image/jpeg&quot; filename=&quot;SAM_7211.jpg&quot; height=&quot;161&quot; width=&quot;242&quot;/&gt;&lt;/span&gt;&lt;/td&gt;&lt;td&gt;&lt;span class=&quot;imageblock&quot; style=&quot;display:inline-block;width:242px;;height:auto;max-width:100%&quot;&gt;&lt;img src=&quot;http://cfile8.uf.tistory.com/image/21440A4D56B8A9B6240783&quot; filemime=&quot;image/jpeg&quot; filename=&quot;SAM_7212.jpg&quot; height=&quot;161&quot; width=&quot;242&quot;/&gt;&lt;/span&gt;&lt;/td&gt;&lt;td&gt;&lt;span class=&quot;imageblock&quot; style=&quot;display:inline-block;width:242px;;height:auto;max-width:100%&quot;&gt;&lt;img src=&quot;http://cfile10.uf.tistory.com/image/243E0B4D56B8A9C029CB4F&quot; filemime=&quot;image/jpeg&quot; filename=&quot;SAM_7213.jpg&quot; height=&quot;161&quot;
'''
# print(msg)

# photo_url = re.search('img src="(.*?)"', item['summary']['content'])
# if photo_url != None:
#     print_format ("\"photoUrl\":\"%s\"," %(photo_url).group(1))

# remove iframe
ifame_url = re.search('&lt;iframe(.*?)/iframe&gt;', msg)
if ifame_url != None:
    print(msg.replace(ifame_url.group(0),""))

# fix width
# photo_url = re.search('img src="(.*?)"', msg)
# if photo_url != None:

json_data=open('demo.xml', encoding='utf-8')

soup = BeautifulSoup(json_data, "lxml")
# print(soup.contents)
# print(soup.findAll("img") )
for img  in soup.findAll("img")  :

    if img.get("src") and re.search("ccl_",img.get("src")) :
        print(str(img))
    else :
        img["width"] = "50%"
        img["height"] = ""
    # print(str(img))
    # print(tmp.text)
# print(soup.contents)

json_data.close()







