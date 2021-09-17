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
from .hooks import lupros
from .controller import persistence, batch
from .HTTPengine import lupro, analyze
from .api import generator, Batchsubmission, BulkDownload, xpath_Batchanalysis, json_Batchanalysis, re_Batchanalysis, Batchanalysis, async_lupro
from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__

__all__ = [
   'lupro',    # lupro 控制台 兼容HTTP客服端
   'lupros',   # lupros 请求参数
   'batch',    # 批量任务控制器
   'analyze',  # 解析器
   'persistence', # 对象持久化控制器
   'generator', 
   'Batchsubmission', 
   'BulkDownload', 
   'xpath_Batchanalysis', 
   'json_Batchanalysis', 
   're_Batchanalysis', 
   'Batchanalysis', 
   'async_lupro' # 极简批量请求
]

'''
v1.0.4
* 完全兼容 `requests` 一切操作，只需 `from lupro import lupro as requests` 即可不更改一行代码
* 新增原生异步 `requests`请求 只需 `async_lupro([lupros.get('https://www.python.org')]*10)`
* 标准化函数描述

v1.0.5
* 修复了 `lupro.lupro` 解析方法判断的失误
* 修复了 移除无效代理的方式

v1.0.6 v1.0.7
* 修复了不启用代理且请求错误时的，更新字典的方式
* 文件结构优化
* 新增对象持久化(shelve)
* 新增批量任务自省，冷重启(atexit)

v1.0.8
* 改变了 response.encoding 为空时的编码推测(chardet)
* 优化了html解析器的接口，`response` 类型可直接通过 `class analyze` 和 `class batch` 进行解析
* 新增 css解析器(parsel)
* 新增 httpx 客服端(httpx)
'''

