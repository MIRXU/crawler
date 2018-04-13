#coding=utf-8
import requests
import xlwt
import re
import json
import time
from hashlib import md5
DATA=[]
find_keyword='python'
t=time.localtime()
find_arg={
    'q':find_keyword,
    'initiative_id':'staobaoz_%s%02d%02d' %(t[0],t[1],t[2])
}
first_url='https://s.taobao.com/search?imgfile=&js=1&stats_click=search_radio_all%3A1&ie=utf8'

r=requests.get(first_url,params=find_arg)
html=r.text

content=re.findall(r'g_page_config = (.*?)g_srp_loadCss()',html,re.S)[0][0][:-6]
content=json.loads(content)
data_list=content['mods']['itemlist']['data']['auctions']
for item in data_list:
    temp={
        'title':item['title'],
        'view_price':item['view_price'],
        'view_sales':item['view_sales'],
        'view_fee':'否'if float(item['view_fee']) else '是',
        'isTmall':'是' if item['shopcard']['isTmall'] else '否',
        'area':item['item_loc'],
        'name':item['nick'],
        'detail_url':item['detail_url'],
    }
    DATA.append(temp)
cookie_=r.cookies

#获取时间戳
ksts=str(int(time.time()*1000))
second_url='https://s.taobao.com/api?_ksTS={}&callback=jsonp239&ajax=true&m=customized&stats_click=search_radio_all:1&q=python&s=36&imgfile=&initiative_id=staobaoz_20180209&bcoffset=0&js=1&ie=utf8&rn={}'.format(ksts,md5(ksts.encode()).hexdigest())
r2=requests.get(second_url,params=find_arg,cookies=cookie_)
html=r2.text

data_list=json.loads(re.findall(r'{.*}',html)[0])['API.CustomizedApi']['itemlist']['auctions']


for item in data_list:
    temp={
        'title':item['title'],
        'view_price':item['view_price'],
        'view_sales':item['view_sales'],
        'view_fee':'否'if float(item['view_fee']) else '是',
        'isTmall':'是' if item['shopcard']['isTmall'] else '否',
        'area':item['item_loc'],
        'name':item['nick'],
        'detail_url':item['detail_url'],
    }
    DATA.append(temp)
cookie_=r2.cookies
for i in xrange(1,10):
    ksts=time.time()
    find_arg['_ksTS']='%s_%s' %(int(ksts*1000),str(ksts)[-3:])
    find_arg['callback']='jsonp%d' %(int(str(ksts)[-2:]) + 1)
    find_arg['data-value']=44*i
    url='https://s.taobao.com/search?data-key=s&data-value=132&ajax=true&imgfile=&js=1&stats_click=search_radio_all%3A1&ie=utf8&bcoffset=4&ntoffset=4&p4ppushleft=1%2C48'.format(time.time())
    if i>1:
        find_arg['s']=44*(i-1)
    r3=requests.get(url,params=find_arg,cookies=cookie_)
    html=r3.text
    content2=re.findall(r'{.*}', html)[0]
    content2=json.loads(content2)
    data_list=content2['mods']['itemlist']['data']['auctions']
    for item in data_list:
        temp = {
            'title': item['title'],
            'view_price': item['view_price'],
            'view_sales': item['view_sales'],
            'view_fee': '否' if float(item['view_fee']) else '是',
            'isTmall': '是' if item['shopcard']['isTmall'] else '否',
            'area': item['item_loc'],
            'name': item['nick'],
            'detail_url': item['detail_url'],
        }
        DATA.append(temp)
    cookie_ = r.cookies

f=xlwt.Workbook(encoding='utf-8')
sheet01=f.add_sheet(u'sheet1',cell_overwrite_ok=True)

sheet01.write(0,0,'标题')
sheet01.write(0,1,'标价')
sheet01.write(0,2,'购买人数')
sheet01.write(0,3,'是否包邮')
sheet01.write(0,4,'是否天猫')
sheet01.write(0,5,'地区')
sheet01.write(0,6,'店名')
sheet01.write(0,7,'url')
for i in range(len(DATA)):
    sheet01.write(i+1, 0,DATA[i]['title'])
    sheet01.write(i+1, 1, DATA[i]['view_price'])
    sheet01.write(i+1, 2, DATA[i]['view_sales'])
    sheet01.write(i+1, 3, DATA[i]['view_fee'])
    sheet01.write(i+1, 4, DATA[i]['isTmall'])
    sheet01.write(i+1, 5, DATA[i]['area'])
    sheet01.write(i+1, 6, DATA[i]['name'])
    sheet01.write(i+1, 7, DATA[i]['detail_url'])

f.save(u'搜索%s的结果.xls' % find_keyword)




