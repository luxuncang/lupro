'''
lupro HTTP
'''
from gevent import monkey
monkey.patch_all()  # 先引用
import gevent
from .config import HTTP_ENGINE, PROXIES, RUNFILE, VERIFY_PROXIES
from .config import verify_proxies, logging, verify_proxies, get_proxies, get_header
from .hooks import lupros
from .publictool import inherit, original, endurance
from .typing import Response
import os
import random
import requests
import re
from lxml import etree
from dtanys import XDict
from copy import copy
from datetime import datetime

# 'HTTP 引擎'
class engine():
    '''HTTP 引擎'''

    @staticmethod
    def requests(self) -> Response:
        '''`engine.requests` 为 `requests` 请求接口'''

        if self.faultolt <= 0:
            print(f'{self.filename} failed.')
            return None
        print(logging(f"{self.filename} {self.proxie} -----> 开始请求！"))
        try:
            res = requests.request(*self.args, **self.kw)
        except:
            if self.proxie and self.proxie in lupro.Proxies:
                lupro.Proxies.remove(self.proxie)
                self.proxie = random.choice(lupro.Proxies)
                self.kw['proxies'] = {'http': f"//{self.proxie}"}
            self.faultolt -= 1
            print(logging(f"{self.filename} -----> 更新字典中！{self.faultolt}"))
            return engine.requests(self)
        if not res.status_code == 200:
            return engine.requests(self)
        if len(res.content) < self.content:
            return engine.requests(self)
        print(logging(f"{self.filename} {len(res.content)} -----> 请求结束！"))
        return res

# `lupro` 引擎基类
class lupro(metaclass = inherit):
    '''`lupro` 引擎基类'''

    # 兼容 `requests`
    __general__ = HTTP_ENGINE

    # 当前文件夹
    onFile = RUNFILE

    # 代理池
    Proxies = PROXIES

    # 是否验证代理池
    VERIFY_PROXIES = VERIFY_PROXIES

    # 是否已验证代理
    IS_AGENT_VERIFIED = False

    def __init__(self, filename : str, lupros : lupros, proxie : bool = False, format : str = 'html', content : int = 200,faultolt : int = 10):
        ''' 初始化 `lupro` 实例，一个实例代表一个请求或任务.

        Args:
            `filename` : `str` 文件路径或请求名称 推荐使用路径命名
            `lupros` : `lupros` requests参数字典
            `proxie` : `bool` 是否使用代理
            `format` : `str` 保存文件格式
            `content` : `int` 回调最少字节
            `faultolt` : `int` 可重试次数
        
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

        if (not lupro.Proxies) and self.proxie:
            lupro.Proxies = get_proxies()

        assert (not self.proxie) or (self.proxie and lupro.Proxies),'`Proxies` cannot be empty!'

        if not 'headers' in self.kw:
            self.kw['headers'] = {'User-Agent' : get_header()}
        elif not 'User-Agent' in self.kw['headers']:
            self.kw['headers'].update({'User-Agent' : get_header()})
        
        if lupro.VERIFY_PROXIES and self.proxie and (not lupro.IS_AGENT_VERIFIED):
            print(logging('开始验证代理！'))
            t1 = datetime.now()
            self.authentication()
            lupro.IS_AGENT_VERIFIED = True
            print(logging(f'用时{datetime.now() - t1}'))
            print(logging(f"高质量代理：{len(lupro.Proxies)}个！"))

        if (not 'proxies' in self.kw) and self.proxie:
            self.proxie = random.choice(lupro.Proxies)
            self.kw['proxies'] = {'http': f"//{self.proxie}"}
    
    # 验证代理
    def authentication(self) -> None:
        '''`authentication` 为快速代理验证.'''

        auth_proxies = [gevent.spawn(verify_proxies, i) for i in lupro.Proxies]
        gevent.joinall(auth_proxies)
        lupro.Proxies = [i.value for i in auth_proxies if i.value]

    # 请求方法 lupro 所有请求
    @endurance
    def task(self):
        return getattr(engine, lupro.__general__.__name__)(self)
    
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
        if not res:
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
        if not res:
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
        if not res:
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
        if not res:
            return ''
        if os.path.isabs(self.filename):
            path = os.path.split(self.filename)[0]
        else:
            path = os.path.join(self.onFile,os.path.split(self.filename)[0])
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path,os.path.split(self.filename)[1]+f'.{self.format}')
        if res.apparent_encoding == None:
            res.encoding = 'utf-8'
        else:
            res.encoding = res.apparent_encoding
        with open(path,mode='wb') as f:
            f.write(res.content)
        return path

    def __repr__(self) -> str:
        return f"<{__name__}.lupro object {self.filename}>"

    def __reprs__(self) -> dict:
        ''' `__reprs__` 为 `lupro` 实例化参数'''
        return {'filename':self.filename ,'format':self.format , 'proxie':self.proxie, 'faultolt':self.faultolt, 'content' : self.content ,'lupros':self.lupros}

    
    