'''
lurpo 全局配置
'''

from .useragent import ua_list
import random
from datetime import datetime
import requests
import os
import sys


__all__ = [
    'RUNFILE',
    'HTTP_ENGINE',
    'PERSISTENCE_ENABLED',
    'PERSISTENCE_PATH',
    'PROXIES',
    'VERIFY_PROXIES',
    'VERIFY_PROXIES',
    'get_header',
    'get_proxies',
    'logging',
    'verify_proxies'
]

# runfile
RUNFILE = os.path.split(sys.argv[0])[0]

# HTTP引擎
HTTP_ENGINE = requests

# 对象持久化
PERSISTENCE_ENABLED = False

# 对象持久化存储路径
PERSISTENCE_PATH = 'endurance.db'

# 代理池
PROXIES = []

# 是否验证代理池
VERIFY_PROXIES = False

# 自定义请求头
def get_header(ualist = ua_list) -> str:
    '''`get_header` 生成一个UA头.

    Args:
        None : 无参数

    Returns:
        str : 返回一个UA头字符串即可
    '''
    return random.choice(ualist)

# 自定义代理池
def get_proxies():
    '''获取代理,并将代理赋值到 `lupro.config.PROXIES`.

    Args:
        None : 无参数

    Returns:
        bool : 返回Ture
    '''
    raise NameError('Please rewrite `get_proxies` function.')

# 自定义日志打印
def logging(text) -> str:
    '''自定义日志打印  `logging` 可以重写,返回带 `text` 的字符串即可.

    Args:
        `text` : str 日志
    
    Returns:
        str : 返回处理后的打印日志
    '''
    return "%s INFO %s"  % (datetime.now(), text)

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

# 载入配置
try:
    import lupro_config
    for i in __all__:
        if hasattr(lupro_config, i):
            locals()[i] = getattr(lupro_config, i)
except ModuleNotFoundError:
    pass
