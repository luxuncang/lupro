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

from typing import Any
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
from dtanys import XDict
from copy import copy

__author__ = 'ShengXin Lu'
__version__ = '1.0.4'

# UA池
ua_list = [ 
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
     "Opera/8.0 (Windows NT 5.1; U; en)",
     "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
     "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
     "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
     "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
     "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
     "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
     "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 ",
     "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
     "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
     "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
     "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
     "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
     "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
     "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
     "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
     "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
     "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
     "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
     "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
     "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
     "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
     "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
     "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
     "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
     "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
     "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
     "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
     "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
     "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
     "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

# 自定义请求头
def get_header() -> str:
    '''`get_header` 生成一个UA头.

    Args:
        None : 无参数

    Returns:
        str : 返回一个UA头字符串即可
    '''
    return random.choice(ua_list)

# 自定义代理池
def get_proxies():
    '''获取代理,并将代理赋值到 `lupro.Proxies`.

    Args:
        None : 无参数

    Returns:
        bool : 返回Ture
    '''
    raise NameError('Please rewrite `get_proxies` function.')

# 自定义代理验证
def verify_proxies(proxies : str) -> str:
    ''' 自定义代理验证 `verify_proxies` 可以重写,如果可用返回 `proxies` 否则返回 `False`.

    Args:
        `proxies` : str 代理
    
    Returns:
        str | bool : 如果可用返回 `proxies` 否则返回 `False`
    '''
    try:
        requests.get(url='http://www.baidu.com/', headers={"User-Agent": get_header()},proxies={'http': f"//{proxies}"},timeout=10)
    except:
        return False
    return proxies

# 自定义日志打印
def logging(text) -> str:
    '''自定义日志打印  `logging` 可以重写,返回带 `text` 的字符串即可.

    Args:
        `text` : str 日志
    
    Returns:
        str : 返回处理后的打印日志
    '''
    return "%s INFO %s"  % (datetime.now(), text)

# 辅助函数
def original(f) -> Any:
    '''  默认解析处理函数.

    Args:
        `f` : function 自定义解析处理函数
    
    Retuens:
        function : 自定义解析处理函数
    '''
    return f

# 泛属性元类
class inherit(type):
    '''类泛属性'''

    def __getattr__(cls, name):
        if not '__general__' in dir(cls):
            raise NameError("name '__general__' is not defined")
        if hasattr(cls.__general__, name):
            return getattr(cls.__general__, name)
        return getattr(object.__getattr__, name)

# `requests` 字典
class lupros():
    '''`requests` 辅助字典生成器'''

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
    
# `lupro` 引擎基类
class lupro(metaclass=inherit):
    '''`lupro` 引擎基类'''

    # 兼容 `requests`
    __general__ = requests

    # 当前文件夹
    onFile = os.path.split(sys.argv[0])[0]

    # 代理池
    Proxies = []

    # 是否验证代理池
    VERIFY_PROXIES = False

    # 是否已验证代理
    IS_AGENT_VERIFIED = False

    def __init__(self, filename : str, lupros : lupros, proxie : bool = False, format : str = 'html', content : int = 200,faultolt : int = 10):
        ''' 初始化 `lupro` 实例，一个实例代表一个请求或任务.

        Args:
            `filename` : `str` 文件路径或请求名称 推荐使用路径命名
            `lupros` : `lupros` requests参数字典
            `proxie` : `bool` 是否使用代理
            `format` : `str` 保存文件格式
            `content` : `str` 回调最少字节
            `faultolt` : `str` 可重试次数
        
        Returns:
            None
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
        '''`authentication` 为快速代理验证.'''

        auth_proxies = [gevent.spawn(verify_proxies,i) for i in lupro.Proxies]
        gevent.joinall(auth_proxies)
        lupro.Proxies = [i.value for i in auth_proxies if i.value]

    # 请求方法 lupro 所有请求
    def task(self) -> requests:
        '''`task` 为 `lupro` 实例所有请求接口'''

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
    def xpath_analysis(self, analytic : dict, auxiliary = original) -> dict:
        '''实例 xpath 解析方法.

        Args:
            `analytic` : `dict[str:str]` xpath解析字典
            `auxiliary` : `function` 自定义解析处理
        
        Returns:
            dict : 解析字典
        '''
        res = self.task()
        if res:
            return {}
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
    def json_analysis(self, analytic : dict, auxiliary = original) -> dict:
        '''实例 json 解析方法.

        Args:
            `analytic` : `dict[str:str]` xpath解析字典
            `auxiliary` : `function` 自定义解析处理
        
        Returns:
            dict : 解析字典
        '''
        res = self.task()
        if res:
            return {}
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
        '''实例 正则 解析方法.

        Args:
            `analytic` : `dict`{`str`:`function`} 正则解析字典 
            `auxiliary` : `function` 自定义解析处理
        
        Returns:
            dict : 解析字典
        '''
        res = self.task()
        if res:
            return {}
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
        '''保存文件方法，如果 `filename` 不为绝对路径,则保存文件的路径为当前目录'''

        res = self.task()
        if res:
            return ''
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
        ''' `__repr__` 为 `lupro` 实例化参数'''
        return {'filename':self.filename ,'format':self.format , 'proxie':self.proxie, 'faultolt':self.faultolt, 'content' : self.content ,'lupros':self.lupros}


# 实例化参数字典
def requests_dict(luprodir,url,no) -> dict:
    '''实例化参数字典.

    Args:
        `luprodir` : `dict` lupro构造参数
        `url` : `str` 链接
        `no` : `str` filename 序列
    
    Returns:
        dict : lupro参数字典
    '''
    luprodict = copy(luprodir)
    if luprodict['lupros'][1]:
        luprodict['lupros'] = (luprodict['lupros'][0], (url,*luprodict['lupros'][1][1:]),luprodict['lupros'][2])
    else:
        luprodict['lupros'][2]['url'] = url
    luprodict['filename'] += str(no)
    return luprodict

# 实例化生成器
def generator(instantiation : lupro, url : list, filenameNo = []) -> list:
    '''实例化生成器

    Args:
        `instantiation` : `lupro` lupro模板实例
        `url` : `list` 链接表
        `filenameNo` : `list` filename 序列

    Returns:
        list : lupro实例列表
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
    '''通过实例列表的批量请求
    
    Args：

        `generator` : `list[lupro]` lupro实例列表
    
    Returns:
        list : Response列表
    '''
    a = [gevent.spawn(i.task,) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# 批量下载
def BulkDownload(generator) -> list:
    '''通过实例列表的批量下载
    
    Args：

        `generator` : `list[lupro]` lupro实例列表
    
    Returns:
        list : path 列表
    '''
    a = [gevent.spawn(i.save_file,) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# xpath 批量解析
def xpath_Batchanalysis(generator, analytic, auxiliary = original) -> list:
    ''' xpath批量解析器

    Args:
        `generator` : `list[lupro]` lupro实例列表
        `analytic` : `dict` 解析字典
        `auxiliary` : `function` 自定义解析处理
        
    Returns:
        list[dict] : 解析列表
    '''
    a = [gevent.spawn(i.xpath_analysis, analytic, auxiliary) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# json 批量解析
def json_Batchanalysis(generator, analytic, auxiliary = original) -> list:
    '''json批量解析器 <json解析器为 `dtanys`>

    Args:
        `generator` : `list[lupro]` lupro实例列表
        `analytic` : `dict` 解析字典
        `auxiliary` : `function` 自定义解析处理
    
    Returns:
        list[dict] : 解析列表
    '''
    a = [gevent.spawn(i.json_analysis, analytic, auxiliary) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# 正则 批量解析
def re_Batchanalysis(generator, analytic, auxiliary = original) -> list:
    '''正则解析器

    Args:
        `generator` : `list[lupro]` lupro实例列表
        `analytic` : `dict`{`str`:`function`} 正则解析字典 
        `auxiliary` : `function` 自定义解析处理
    
    Returns:
        list[dict] : 解析列表
    '''
    a = [gevent.spawn(i.re_analysis, analytic, auxiliary) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# 批量解析
def Batchanalysis(mold : str ,generator : list, analytic : dict, auxiliary = original) -> list:
    '''lupro批量解析

    Args:
        `mold` : `str` 解析方法
        `generator` : `list[lupro]` lupro实例列表
        `analytic` : `dict` 解析字典
        `auxiliary` : `function` 自定义解析处理

    Returns:
        list[dict] : 解析列表
    '''
    if mold == 'xpath':
        return xpath_Batchanalysis(generator, analytic, auxiliary)
    elif mold == 'json':
        return json_Batchanalysis(generator, analytic, auxiliary)
    elif mold == 're':
        return re_Batchanalysis(generator, analytic, auxiliary)
    else:
        raise TypeError('No corresponding parsing method!')

# 批量异步请求
def async_lupro(generator):
    '''原生异步`requests`请求

    Args:
        `generator` : `list[lupros]` lupros实例列表
    
    Returns:
        list[Response] : Response列表
    '''

    a = [gevent.spawn(requests.request,i[0],*i[1],**i[2]) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# Update log
'''
v1.0.4
* 完全兼容 `requests` 一切操作，只需 `from lupro import lupro as requests` 即可不更改一行代码
* 新增原生异步 `requests`请求 只需 `async_lupro([lupros.get('https://www.python.org')]*10)`
* 标准化函数描述
'''
