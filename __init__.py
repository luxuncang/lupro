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

from .hooks import lupros
from .controller import persistence, batch
from .publictool import original, abnormal
from .HTTPengine import lupro
from .api import generator, Batchsubmission, BulkDownload, xpath_Batchanalysis, json_Batchanalysis, re_Batchanalysis, Batchanalysis, async_lupro
from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__


'''
v1.0.4
* 完全兼容 `requests` 一切操作，只需 `from lupro import lupro as requests` 即可不更改一行代码
* 新增原生异步 `requests`请求 只需 `async_lupro([lupros.get('https://www.python.org')]*10)`
* 标准化函数描述

v1.0.5
* 修复了 `lupro.lupro` 解析方法判断的失误
* 修复了 移除无效代理的方式

v1.0.6
* 修复了不启用代理且请求错误时的，更新字典的方式
* 文件结构优化
* 新增对象持久化
* 新增批量任务自省，冷重启
'''

