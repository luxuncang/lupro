'''response解析器'''
import re
from lxml import etree
from dtanys import XDict
import parsel
from .publictool import original, responsecoding

# `response` 解析控制器
class analyze():
    '''`response` 解析控制器'''

    @staticmethod
    def xpath(response, analytic : dict, auxiliary = original):
        ''' xpath 解析方法.

        Args:
            `response` : `response` response响应
            `analytic` : `dict[str:str]` xpath解析字典
            `auxiliary` : `function` 自定义解析处理
        
        Returns:
            dict : 解析字典
        '''
        html = etree.HTML(responsecoding(response))
        res = {}
        for i, j in analytic.items():
            res[i] = [auxiliary(r) for r in html.xpath(j)]
        return res

    @staticmethod
    def json(response, analytic : dict, auxiliary = original):
        ''' json 解析方法.

        Args:
            `response` : `response` response响应
            `analytic` : `dict[str:str]` json解析字典
            `auxiliary` : `function` 自定义解析处理
        
        Returns:
            dict : 解析字典
        '''
        if response.apparent_encoding == None:
            response.encoding = 'utf-8'
        else:
            response.encoding = response.apparent_encoding
        reDict = {}
        for i,j in analytic.items():
            reDict[i] = auxiliary(XDict(response.json(),j).edict())
        return reDict

    @staticmethod
    def re(response, analytic : dict, auxiliary = original):
        ''' re 解析方法.

        Args:
            `response` : `response` response响应
            `analytic` : `dict[str:str]` re解析字典
            `auxiliary` : `function` 自定义解析处理
        
        Returns:
            dict : 解析字典
        '''
        res = []
        html = etree.HTML(responsecoding(response))
        res = {}
        for i, j in analytic.items():
            res[i]=[auxiliary(r) for r in j(html)]
        return res

    @staticmethod
    def css(response, analytic : dict, auxiliary = original):
        ''' css 解析方法.

        Args:
            `response` : `response` response响应
            `analytic` : `dict[str:str]` css解析字典
            `auxiliary` : `function` 自定义解析处理
        
        Returns:
            dict : 解析字典
        '''
        res = []
        html = parsel.Selector(responsecoding(response))
        res = {}
        for i, j in analytic.items():
            res[i] = [auxiliary(r) for r in html.css(j).extract()]
        return res        