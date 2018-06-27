# coding=utf-8
import requests
import json
import re
import gevent
from gevent import monkey,pool
monkey.patch_socket()
import os

def xz(url,data):
    re_=re.compile('"HistoryGuid" : "(.*?)",',re.S)
    res=requests.post(url,headers=header,data=data)
    res.encoding='gb2312'
    js=res.json()
    for historyguid in re.findall(re_,js):
        ar.append(historyguid)
    res.close()

def get_detail(data):
    print data
    url_detail = 'http://www.xz.gov.cn/BaseSv/Base.asmx/GetConHandDetail'
    gevent.sleep(1)
    res=requests.post(url_detail,headers=header_detail,data=data)
    res.encoding='gb2312'
    js=res.json()
    for txt in re.findall(re_,js):
        for t in txt:
            f.write(t.replace('&nbsp;','').replace('</br>','\n').encode('utf-8')+'\n')
    res.close()

if __name__=='__main__':
    re_=re.compile('"PostDate" : "(.*?)",.*?"Subject" : "(.*?)","Content" : "(.*?)",.*?"ReplyOpinion" : "(.*?)",',re.S)
    f=open('xz.txt','a')
    ar=[]
    url = 'http://www.xz.gov.cn/BaseSv/Base.asmx/GetconHandPageList'
    header = {'Accept':'application/json, text/javascript, */*',
        'Origin':'http://www.xz.gov.cn',
        'X-Requested-With':'XMLHttpRequest',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'Content-Type':'application/json; charset=UTF-8',
        'Referer':'http://www.xz.gov.cn/zgxz/Template/Default/gzcy/conhandlist.htm',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9'}
    for i in range(1,104): #104
        data={'pageIndex':i,'pageSize':'20','boxguid':'','IsHot':'undefined','isDept':'undefined'}
        data=json.dumps(data)
        xz(url,data)

    #url_detail = 'http://www.xz.gov.cn/BaseSv/Base.asmx/GetConHandDetail'
    header_detail={'Accept':'application/json, text/javascript, */*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':'52',
        'Content-Type':'application/json; charset=UTF-8',
        'Host':'www.xz.gov.cn',
        'Origin':'http://www.xz.gov.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'}
    p=pool.Pool(20)
    th=[]
    for a in ar:
        data={}
        data['HistoryGuid']=a
        data=json.dumps(data)
        th.append(p.spawn(get_detail,data))
    gevent.joinall(th)
    f.close()

'''
def xz(url,data):
    res=requests.post(url,headers=header,data=data)
    res.encoding='gb2312'
    js=res.json()
    print js
    res.close()

if __name__=='__main__':
    url = 'http://www.xz.gov.cn/BaseSv/Base.asmx/GetConHandDetail'
    header={'Accept':'application/json, text/javascript, */*',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Content-Length':'52',
        'Content-Type':'application/json; charset=UTF-8',
        'Host':'www.xz.gov.cn',
        'Origin':'http://www.xz.gov.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'}

    for i in range(1,2):
        str='8e5f4ed7-d22a-4104-a6c8-7826c5a0abfc'
        data={}
        data['HistoryGuid']=str
        data=json.dumps(data)
        xz(url,data)
'''