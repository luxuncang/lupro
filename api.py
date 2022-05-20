'''lupro api'''
import gevent
from .config import HTTP_ENGINE
from .typing import Union, Response
from .hooks import lupros
from .HTTPengine import lupro, analyze, requests
from .publictool import original
from copy import copy

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
def generator(instantiation : lupro, url : list, filenameNo : list = []) -> list:
    '''实例化生成器

    Args:
        `instantiation` : `lupro` lupro模板实例
        `url` : `list` 链接表
        `filenameNo` : `list` filename 序列且此序列会继承 `instantiation.filename` 

    Returns:
        list : lupro实例列表
    '''
    if not filenameNo:
        filenameNo = range(len(url))
    elif len(url) != len(filenameNo):
        raise ValueError('"url" needs to be consistent with "FileNameno"!')
    repr = instantiation.__reprs__()
    return [lupro(**requests_dict(repr,j,filenameNo[i])) for i,j in enumerate(url)]

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
def xpath_Batchanalysis(generator : Union["list[lupro]", "list[Response]"], analytic : dict, auxiliary = original) -> list:
    ''' xpath批量解析器

    Args:
        `generator` : `Union[list[lupro], list[Response]]` lupro实例列表 或 Response实例列表
        `analytic` : `dict` 解析字典
        `auxiliary` : `function` 自定义解析处理
        
    Returns:
        list[dict] : 解析列表
    '''
    if not isinstance(generator[0], lupro):
        return [analyze.xpath(i, analytic, auxiliary) for i in generator]
    a = [gevent.spawn(i.xpath_analysis, analytic, auxiliary) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# json 批量解析
def json_Batchanalysis(generator : Union["list[lupro]", "list[Response]"], analytic : dict, auxiliary = original) -> list:
    '''json批量解析器 <json解析器为 `dtanys`>

    Args:
        `generator` : `Union[list[lupro], list[Response]]` lupro实例列表 或 Response实例列表
        `analytic` : `dict` 解析字典
        `auxiliary` : `function` 自定义解析处理
    
    Returns:
        list[dict] : 解析列表
    '''
    if not isinstance(generator[0], lupro):
        return [analyze.json(i, analytic, auxiliary) for i in generator]
    a = [gevent.spawn(i.json_analysis, analytic, auxiliary) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# 正则 批量解析
def re_Batchanalysis(generator : Union["list[lupro]", "list[Response]"], analytic : dict, auxiliary = original) -> list:
    '''正则解析器

    Args:
        `generator` : `Union[list[lupro], list[Response]]` lupro实例列表 或 Response实例列表
        `analytic` : `dict`{`str`:`function`} 正则解析字典 
        `auxiliary` : `function` 自定义解析处理
    
    Returns:
        list[dict] : 解析列表
    '''
    if not isinstance(generator[0], lupro):
        return [analyze.re(i, analytic, auxiliary) for i in generator]
    a = [gevent.spawn(i.re_analysis, analytic, auxiliary) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])

# 批量解析
def Batchanalysis(mold : str ,generator : Union["list[lupro]", "list[Response]"], analytic : dict, auxiliary = original) -> list:
    '''lupro批量解析

    Args:
        `mold` : `str` 解析方法
        `generator` : `Union[list[lupro], list[Response]]` lupro实例列表 或 Response实例列表
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
def async_lupro(generator : "list[lupros]") -> list:
    '''原生异步`requests`请求

    Args:
        `generator` : `list[lupros]` lupros实例列表
    
    Returns:
        list[Response] : Response列表
    '''

    a = [gevent.spawn(HTTP_ENGINE.request,i[0],*i[1],**i[2]) for i in generator]
    gevent.joinall(a)
    return ([i.value for i in a])
