'''
HTTP 请求钩子
'''

from .config import HTTP_ENGINE

# 类泛属性
class inherit(type):
    '''类泛属性'''

    def __getattr__(cls, name):
        if not '__general__' in dir(cls):
            raise NameError("name '__general__' is not defined")
        if hasattr(cls.__general__, name):
            return getattr(cls.__general__, name)
        raise AttributeError(f"method '{name}' is not defined in {cls.__general__}")

# 类方法描述
class repr(type):
    '''类方法描述'''

    def __repr__(cls) -> str:
        return f"<lupros.{cls.__name__} object>"

# requests参数引擎
class requests(metaclass = repr):
    '''`requests参数引擎` 辅助字典生成器'''

    @classmethod
    def request(cls, *args, **kw):
        return (args, kw)

    @classmethod
    def get(cls, *args, **kw):
        return ('get', args, kw)

    @classmethod
    def post(cls, *args, **kw):
        return ('post', args, kw)

    @classmethod
    def options(cls, *args, **kw):
        return ('options', args, kw)

    @classmethod
    def head(cls, *args, **kw):
        return ('head', args, kw)

    @classmethod
    def put(cls, *args, **kw):
        return ('put', args, kw)

    @classmethod
    def patch(cls, *args, **kw):
        return ('patch', args, kw)

    @classmethod
    def delete(cls, *args, **kw):
        return ('delete', args, kw)

    def __repr__(self) -> str:
        return "<lupros.requests object >"

# httpx参数引擎
class httpx(metaclass = repr):
    '''`httpx参数引擎` 辅助字典生成器'''

    @classmethod
    def request(cls, *args, **kw):
        return (args, kw)

    @classmethod
    def get(cls, *args, **kw):
        return ('GET', args, kw)

    @classmethod
    def post(cls, *args, **kw):
        return ('POST', args, kw)

    @classmethod
    def options(cls, *args, **kw):
        return ('OPTIONS', args, kw)

    @classmethod
    def head(cls, *args, **kw):
        return ('HEAD', args, kw)

    @classmethod
    def put(cls, *args, **kw):
        return ('PUT', args, kw)

    @classmethod
    def patch(cls, *args, **kw):
        return ('PATCH', args, kw)

    @classmethod
    def delete(cls, *args, **kw):
        return ('DELETE', args, kw)

    def __repr__(self) -> str:
        return "<lupros.httpx object >"

# `HTTP参数引擎` 
class lupros(metaclass = inherit):
    '''`HTTP参数引擎` 辅助字典生成器'''

    kernel = {'requests': requests, 'httpx' : httpx}

    __general__ = kernel[HTTP_ENGINE.__name__]


