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
        return {i: [auxiliary(r) for r in html.xpath(j)] for i, j in analytic.items()}

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
        response.encoding = (
            'utf-8'
            if response.apparent_encoding is None
            else response.apparent_encoding
        )

        return {
            i: auxiliary(XDict(response.json(), j).edict())
            for i, j in analytic.items()
        }

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
        res = {i: [auxiliary(r) for r in j(html)] for i, j in analytic.items()}
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
        res = {
            i: [auxiliary(r) for r in html.css(j).extract()]
            for i, j in analytic.items()
        }

        return res        