'''
Lupro Library
~~~~~~~~~~~~~~~~~~~~~

Lupro is an Asynchronous HTTP library, written in Python, It is fully compatible with `requests`.
usage:

* `兼容requests`

   >>> from lupro import lupro
   >>> r = lupro.get('https://www.python.org')
   >>> r.status_code
   200

其它 `lupro.api` 请参考 <https://github.com/luxuncang/lupro>.

:copyright: (c) 2021 by ShengXin Lu.
'''

from gevent import monkey
monkey.patch_all()  # 先引用
import gevent
import requests
import os
import sys
import random
import re
from datetime import datetime
from lxml import etree
from fake_useragent import UserAgent
from dtanys import XDict
from copy import copy

# 自定义请求头
def get_header() -> str:
    '''
    `get_header` 可以重写，返回一个UA头字符串即可
    '''
    location = os.getcwd() + '/fake_useragent.json'
    ua = UserAgent(path=location)
    return ua.random

# 自定义代理池
def get_proxies():
    '''
    * 将代理赋值到 `lupro.Proxies` 
    '''
    assert False,'Please rewrite `get_proxies` function.'

# 自定义代理验证
def verify_proxies(proxies):
    '''
    `proxies` : str 代理
    `verify_proxies` 可以重写,如果可用返回 `proxies` 否则返回 `False`
    '''
    try:
        requests.get(url='http://www.baidu.com/', headers={"User-Agent": get_header()},proxies={'http': f"//{proxies}"},timeout=10)
    except:
        return False
    return proxies

# 自定义日志打印
def logging(text):
    '''
    `text` : str 日志
    `logging` 可以重写,返回带 `text` 的字符串即可
    '''
    return "%s INFO %s"  % (datetime.now(), text)

# 辅助函数
def original(f):
    '''
    `original` 为默认解析处理函数
    '''
    return f

class lupros():
    '''
    #### requests 辅助字典生成器
    '''

    @classmethod
    def request(self, *args, **kw):
        return (args, kw)

    @classmethod
    def get(self, *args, **kw):
        return ('get', args, kw)

    @classmethod
    def post(self, *args, **kw):
        return ('post', args, kw)

    @classmethod
    def options(self, *args, **kw):
        return ('options', args, kw)

    @classmethod
    def head(self, *args, **kw):
        self.args = ('get', *args)
        self.kw = kw
        return ('head', args, kw)

    @classmethod
    def put(self, *args, **kw):
        return ('put', args, kw)

    @classmethod
    def patch(self, *args, **kw):
        return ('patch', args, kw)

    @classmethod
    def delete(self, *args, **kw):
        return ('delete', args, kw)

class lupro():
    '''
    * 完全兼容 `requests`
    '''

    # 当前文件夹
    onFile = os.path.split(sys.argv[0])[0]

    # 代理池
    Proxies = []

    # 是否验证代理池
    VERIFY_PROXIES = False

    # 是否已验证代理
    IS_AGENT_VERIFIED = False

    def __init__(self, filename : str, lupros : lupros, proxie : bool = False, format : str = 'html', content : int = 200,faultolt : int = 10):
        '''
        `filename` : `str` 文件路径或请求名称 推荐使用路径命名
        `lupros` : `lupros` requests参数字典
        `proxie` : `bool` 是否使用代理
        `format` : `str` 保存文件格式
        `content` : `str` 回调最少字节
        `faultolt` : `str` 可重试次数
        '''
        self.filename = filename    # 文件路径或请求名称 推荐使用路径命名
        self.format = format        # 保存文件格式
        self.faultolt = faultolt    # 可重试次数
        self.proxie = proxie        # 是否使用代理
        self.content = content      # 回调最少字节
        self.lupros = lupros
        self.args = (lupros[0],*lupros[1])
        self.kw = copy(lupros[2])

        if (not lupro.Proxies) and proxie:
            get_proxies()

        assert (not self.proxie) or (self.proxie and lupro.Proxies),'`Proxies` cannot be empty!'

        if not 'headers' in self.kw:
            self.kw['headers'] = {'User-Agent' : get_header()}
        
        if lupro.VERIFY_PROXIES and self.proxie and (not lupro.IS_AGENT_VERIFIED):
            print(logging('开始验证代理！'))
            t1 = datetime.now()
            self.authentication()
            lupro.IS_AGENT_VERIFIED = True
            print(logging(f'用时{datetime.now()-t1}'))
            print(logging(f"高质量代理：{len(lupro.Proxies)}个！"))
        if (not 'proxies' in self.kw) and self.proxie:
            self.proxie = random.choice(lupro.Proxies)
            self.kw['proxies'] = {'http': f"//{self.proxie}"}
    
    # 验证代理
    def authentication(self) -> None:
        '''
        `authentication` 为快速代理验证
        '''
        auth_proxies = [gevent.spawn(verify_proxies,i) for i in lupro.Proxies]
        gevent.joinall(auth_proxies)
        lupro.Proxies = [i.value for i in auth_proxies if i.value]

    # 请求方法 lupro 所有请求
    def task(self) -> requests:
        '''
        `task` 为 `lupro` 实例所有请求接口
        '''
        if self.faultolt<=0:
            print(f'{self.filename} failed.')
            return False
        print(logging(f"{self.filename} {self.proxie} ----->开始请求！"))
        try:
            res = requests.request(*self.args, **self.kw)
        except:
            if self.proxie in lupro.Proxies:
                lupro.Proxies.remove(self.proxies)
            self.faultolt-=1
            self.proxies = random.choice(lupro.Proxies)
            self.kw['proxies'] = {'http': f"//{self.proxies}"}
            print(logging(f"{self.filename}----->更新字典中！"))
            return self.task()
        if not res.status_code==200:
            return self.task()
        if len(res.content)<self.content:
            return self.task()
        print(logging(f"{self.filename} {len(res.content)} ----->请求结束！"))
        return res
    
    # xpath 解析
    def xpath_analysis(self, analytic : dict, auxiliary = original):
        '''
        `analytic` : `dict` xpath解析字典
        `auxiliary` : `function` 自定义解析处理
        `xpath_analysis` 为实例xpath解析方法
        '''
        res = self.task()
        if res.apparent_encoding == None:
            res.encoding = 'utf-8'
            html = etree.HTML(res.content.decode('utf-8'))
        else:
            res.encoding = res.apparent_encoding
            html = etree.HTML(res.content.decode(res.encoding, 'ignore'))
        res = {}
        for i, j in analytic.items():
            res[i] = [auxiliary(r) for r in html.xpath(j)]
        return res

    # json 解析
    def json_analysis(self, analytic : dict, auxiliary = original):
        '''
        `analytic` : `dict` json解析字典
        `auxiliary` : `function` 自定义解析处理
        `json_analysis` 为实例json解析方法
        '''
        res = self.task()
        if res.apparent_encoding == None:
            res.encoding = 'utf-8'
        else:
            res.encoding = res.apparent_encoding
        reDict = {}
        for i,j in analytic.items():
            reDict[i] = auxiliary(XDict(res.json(),j).edict())
        return reDict

    # 正则 解析
    def re_analysis(self, analytic, auxiliary = original):
        '''
        `analytic` : `dict`{`str`:`function`} 正则解析字典 
        `auxiliary` : `function` 自定义解析处理
        `re_analysis` 为实例json解析方法
        '''
        res = self.task()
        if res.apparent_encoding == None:
            res.encoding = 'utf-8'
            html = etree.HTML(res.content.decode('utf-8'))
        else:
            res.encoding = res.apparent_encoding
            html = etree.HTML(res.content.decode(res.encoding, 'ignore'))
        res = {}
        for i, j in analytic.items():
            res[i]=[auxiliary(r) for r in j(html)]
        return res

    # 保存文件路径
    def save_file(self) -> str:
        '''
        * 如果 `filename` 不为绝对路径,则保存文件的路径为当前目录
        '''
        res = self.task()
        if os.path.isabs(self.filename):
            path = os.path.split(self.filename)[0]
        else:
            path = os.path.join(self.onFile,os.path.split(self.filename)[0])
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path,os.path.split(self.filename)[1]+f'.{self.format}')
        with open(path,mode='wb') as f:
            f.write(res.content)
        return path

    def __repr__(self) -> dict:
        '''
        `__repr__` 为 `lupro` 实例化参数
        '''
        return {'filename':self.filename ,'format':self.format , 'proxie':self.proxie, 'faultolt':self.faultolt, 'content' : self.content ,'lupros':self.lupros}

    @classmethod
    def request(self, *args, **kw):
        return requests.request(*args, **kw)

    @classmethod
    def get(self, *args, **kw):
        return self.request('get', *args, **kw)

    @classmethod
    def post(self, *args, **kw):
        return self.request('post', *args, **kw)

    @classmethod
    def options(self, *args, **kw):
        return self.request('options', *args, **kw)

    @classmethod
    def head(self, *args, **kw):
        return self.request('head', *args, **kw)

    @classmethod
    def put(self, *args, **kw):
        return self.request('put', *args, **kw)

    @classmethod
    def patch(self, *args, **kw):
        return self.request('patch', *args, **kw)

    @classmethod
    def delete(self, *args, **kw):
        return self.request('delete', *args, **kw)

    @classmethod
    def Session(self):
        return requests.Session()


# 实例化参数字典
def requests_dict(luprodir,url,no) -> dict:
    '''
    `luprodir` : `dict` lupro构造参数
    `url` : `str` 链接
    `no` : `str` filename 序列
    '''
    luprodict = copy(luprodir)
    if luprodict['lupros'][1]:
        luprodict['lupros'] = (luprodict['lupros'][0], (url,*luprodict['lupros'][1][1:]),luprodict['lupros'][2])
    else:
        luprodict['lupros'][2]['url'] = url
    luprodict['filename'] += str(no)
    return luprodict

# 实例化生成器
def generator(instantiation, url, filenameNo = []) -> list:
    '''
    `instantiation` : `lupro` lupro模板实例
    `url` : `list` 链接表
    `filenameNo` : `list` filename 序列
    '''
    if not filenameNo:
        filenameNo = range(len(url))
    repr = instantiation.__repr__()
    res = []
    for i,j in enumerate(url):
        res.append(lupro(**requests_dict(repr,j,filenameNo[i])))
    return res

# 批量请求
def Batchsubmission(generator) -> list:
    '''
    `generator` : `list[lupro]` lupro实例列表
    `Batchsubmission` 为通过实例列表的批量请求
    '''
    a = [gevent.spawn(i.task,) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# 批量下载
def BulkDownload(generator) -> list:
    '''
    `generator` : `list[lupro]` lupro实例列表
    `BulkDownload` 为通过实例列表的批量下载
    '''
    a = gevent.joinall([gevent.spawn(i.save_file,) for i in generator])
    return ([i.value for i in a])

# xpath 批量解析
def xpath_Batchanalysis(generator, analytic, auxiliary = original) -> list:
    '''
    `generator` : `list[lupro]` lupro实例列表
    `analytic` : `dict` 解析字典
    `auxiliary` : `function` 自定义解析处理
    `xpath_Batchanalysis` 为xpath解析器
    '''
    a = [gevent.spawn(i.xpath_analysis, analytic, auxiliary) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# json 批量解析
def json_Batchanalysis(generator, analytic, auxiliary = original):
    '''
    `generator` : `list[lupro]` lupro实例列表
    `analytic` : `dict` 解析字典
    `auxiliary` : `function` 自定义解析处理
    `json_Batchanalysis` 为json解析器 <json解析器为 `dtanys`>
    '''
    a = [gevent.spawn(i.json_analysis, analytic, auxiliary) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# 正则 批量解析
def re_Batchanalysis(generator, analytic, auxiliary = original):
    '''
    `generator` : `list[lupro]` lupro实例列表
    `analytic` : `dict`{`str`:`function`} 正则解析字典 
    `auxiliary` : `function` 自定义解析处理
    `re_Batchanalysis` 为正则解析器
    '''
    a = [gevent.spawn(i.re_analysis, analytic, auxiliary) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# 批量解析
def Batchanalysis(mold : str ,generator : list, analytic : dict, auxiliary = original) -> list:
    '''
    `mold` : `str` 解析方法
    `generator` : `list[lupro]` lupro实例列表
    `analytic` : `dict` 解析字典
    `auxiliary` : `function` 自定义解析处理
    `Batchanalysis` 为解析链
    '''
    if mold == 'xpath':
        return xpath_Batchanalysis(generator, analytic, auxiliary)
    elif mold == 'json':
        return json_Batchanalysis(generator, analytic, auxiliary)
    elif mold == 're':
        return re_Batchanalysis(generator, analytic, auxiliary)
    else:
        assert False,'No corresponding parsing method!'