'''lupro 工具箱'''

from .typing import Any , Response
from .config import PERSISTENCE_ENABLED, PERSISTENCE_PATH
from decorator import decorator
import shelve
import chardet

# 泛属性元类
class inherit(type):
    '''类泛属性'''

    def __getattr__(cls, name):
        if not '__general__' in dir(cls):
            raise NameError("name '__general__' is not defined")
        if hasattr(cls.__general__, name):
            return getattr(cls.__general__, name)
        return getattr(object.__getattr__, name)

# 对象持久化控制器
class persistence():
    '''对象持久化控制器'''

    '''是否启用对象持久化'''
    ENABLED = PERSISTENCE_ENABLED

    # 对象持久化元类
    class kernelk(type):
        '''对象持久化元类'''
        pass

    # shelve内核
    class shelve():
        '''shelve内核'''

        '''对象持久化存储路径'''
        dbfile = PERSISTENCE_PATH

        @classmethod
        def add(cls, key : str, value : Any) -> bool:
            '''持久化一个新对象

            Args：
                `cls` : `persistence.shelve` 类对象
                `key` : `str` 新增对象的键
                `value` : `Any` 新增对象的值
            
            Returns:
                `bool` : True
            '''

            with shelve.open(persistence.shelve.dbfile) as f:
                f[key] = value
            return True
        
        @classmethod
        def put(cls):
            '''持久化一个新对象

            Args：
                `cls` : `persistence.shelve` 类对象
            
            Returns:
                `shelve` : 当前路径shelve对象字典
            '''

            with shelve.open(persistence.shelve.dbfile) as f:
                res = {i:j for i,j in f.items()}
            return res

    # ZODB内核
    class ZODB():
        '''ZODB内核'''

        pass  

# 辅助函数
def original(f) -> Any:
    '''  默认解析处理函数.

    Args:
        `f` : function 自定义解析处理函数
    
    Retuens:
        function : 自定义解析处理函数
    '''
    return f

# 函数功能启停装饰器
@decorator
def reconfig(func, config = True, *args, **kwargs):
    '''函数功能启停装饰器'''
    if config:
        return func(*args , **kwargs)
    else:
        return None

# 对象持久化装饰器
@decorator
def endurance(func, *args, **kwargs):
    '''对象持久化装饰器'''
    res = func(*args, **kwargs)
    if persistence.ENABLED:
        persistence.shelve.add(args[0].filename, res)
    return res

# 异常处理装饰器
@decorator
def abnormal(func, *args, **kwargs):
    '''异常处理装饰器'''
    try:
        return func(*args, **kwargs)
    except KeyboardInterrupt:
        pass

# 回调空键默认值
def putdefault(value, default) -> Any:
    '''与dict.setdefault相识，但是不赋值.
    
    Args：
        `value` : `Any` 字典键值
        `default` : `Any` 返回的默认值
    
    Returns:
        `Any` : 默认值`default`
    '''
    if value:
        return value
    else:
        return default

# bytes编码解析
def bytescoding(response : bytes) -> str:
    '''bytes编码解析'''
    dend = chardet.detect(response)
    return response.decode(encoding = dend['encoding'])

# response编码解析
def responsecoding(response : Response) -> str:
    '''response编码解析'''
    if response.apparent_encoding == None:
        return bytescoding(response.content)
    else:
        response.encoding = response.apparent_encoding
        return response.content.decode(response.encoding, 'ignore')