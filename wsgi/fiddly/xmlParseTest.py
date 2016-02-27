# -*- encoding: utf-8 -*-
body = '''
<ul class="list_imgtxt #news">
<li class="default_img #img">
<a href="http://media.daum.net/photo/2815#20160228053246570" class="link_img @1-1">
<img src="http://t1.daumcdn.net/alvolo/_thumbnails_cutter/media_pc/20160227GMT/20160227_221647GMT_fvhphPVBo0zQjQ5GG3V7" width="113" height="68" class="img_init" alt="">
<span class="frame_g"></span>
<span class="txt_cont">새끼 잡아먹는 아빠 북극곰 포착<br></span>
<em class="img_daum ico_photo"></em>
</a>
</li>
<li class="fst_txt #txt">
<a href="http://v.media.daum.net/v/20160228070309075" class="ellipsis_g @1-1">대출심사 강화 통했나? 주택대출 증가세 꺾여</a>
</li>
<li class=" #txt">
<a href="http://v.media.daum.net/v/20160228004932646" class="ellipsis_g @1-2">안보리 대북결의 채택 왜 늦어지나..푸틴 딴지?</a>
</li>
<li class=" #txt">
<a href="http://v.media.daum.net/v/20160228060105723" class="ellipsis_g @1-3">중기청, 융복합 우수 아이디어 개발에 546억 지원</a>
</li>
<li class=" #txt">
<a href="http://v.media.daum.net/v/20160228053247571" class="ellipsis_g @1-4">제네바모터쇼 3월1일 개막..친환경차 각축전</a>
</li>
<li class=" #txt">
<a href="http://v.media.daum.net/v/20160228022706066" class="ellipsis_g @1-5">런던서 핵잠수함 현대화 반대 대규모 집회</a>
</li>
<li class="default_img #img">
<a href="http://media.daum.net/entertain/photo/gallery/?gid=110149#20160227220826265" class="link_img @1-2">
<img src="http://t1.daumcdn.net/alvolo/_thumbnails_cutter/media_pc/20160227GMT/20160227_133706GMT_1aERRVaPUfwFDpPjMvtv" width="113" height="68" class="img_init" alt="">
<span class="frame_g"></span>
<span class="txt_cont">'SNL' 예원 등장..욕설 사건 패러디<br></span>
<em class="img_daum ico_photo"></em>
</a>
</li>
<li class="fst_txt #txt">
<a href="http://v.media.daum.net/v/20160228070903123" class="ellipsis_g @1-6">세계 외환보유액 1년간 7천억달러 사라졌다</a>
</li>
<li class=" #txt">
<a href="http://v.media.daum.net/v/20160228070304073" class="ellipsis_g @1-7">승용차에 2천만원 여행권까지..ISA 경품만 17억원</a>
</li>
<li class=" #txt">
<a href="http://v.media.daum.net/v/20160228060208742" class="ellipsis_g @1-8">이복남매 협박해 수천만원 뜯어낸 주부 실형</a>
</li>
<li class=" #txt">
<a href="http://v.media.daum.net/v/20160228070302071" class="ellipsis_g @1-9">계좌이동제 이어 ISA..은행권 총성없는 전쟁 돌입</a>
</li>
<li class=" #txt">
<a href="http://v.media.daum.net/v/20160228055008647" class="ellipsis_g @1-10">'쿡방 열풍' 반려동물 먹거리도 바꿨다</a>
</li>
</ul>
'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(body, "lxml")
# print(str(soup))
lastAHrefLink = soup.findAll("a")[-1]["href"]
for aTagList  in soup.findAll("a")  :
    aTagList["href"] = lastAHrefLink
print(str(soup))