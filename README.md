# lupro 爬虫框架

**lupro是一个完全兼容requests的异步爬虫框架**

## 安装 `Lupro`

### 使用 [PyPi](https://pypi.org/) 安装 Lupro

* `pip` Find, install and publish Python packages with the Python Package Index
* `pip install lupro`

## 开始使用

1. 导入 `from lupro import lupro`

### 兼容requests或httpx

```python
from lupro import lupro as requests
# or
from lupro import lupro as httpx
```

_这样即可不用修改代码完全替换_ `requests` or `httpx`

### 原生lupro

```python
from lupro import lupro
r = lupro.get('https://www.python.org')
r.status_code
```

### 批量异步任务

```python
from lupro import lupros, async_lupro

# 请求列表
urls = ['https://www.python.org','https://www.baidu.com']
async_lupro([lupros.get(url) for url in urls])
```

### lupro配置

```python
# 工作路径新建 lupro_config.py 即可自定义配置

# 自定义代理
def get_proxies():
    '''获取代理,并将代理已列表返回

    Args:
        None : 无参数

    Returns:
        list : 返回代理列表['xxx.xxx.xxx.xxx:xxxx',...]
    '''
    raise NameError('Please rewrite `get_proxies` function.')


# HTTP引擎
HTTP_ENGINE = httpx

# 对象持久化
PERSISTENCE_ENABLED = False

# 对象持久化存储路径
PERSISTENCE_PATH = 'endurance.db'

# 代理池
PROXIES = []

# 是否验证代理池
VERIFY_PROXIES = False
```

### lupro 实例

```python
'''
lupro 实例参数
Args:
    filename : str 文件路径或请求名称 推荐使用路径命名
    lupros : lupros requests参数字典
    proxie : bool 是否使用代理
    format : str 保存文件格式
    content : int 回调最少字节
    faultolt : int 可重试次数

lupro 实例方法
method:
    task : 请求
    xpath_analysis : xpath解析
    json_analysis : json解析
    re_analysis : re解析
    css_analysis : css解析
    save_file : 下载器
'''

from lupro import lupro, lupros
from pprint import pprint

def cusjoin(text):
    return 'lupro >>> ' + text

task = lupro('python', lupros.get('https://www.python.org/', timeout = 15), content = 200)

pprint(task.xpath_analysis({'News or Events' :'//*[@id="content"]//ul[@class="menu"]//li/a//text()'}, cusjoin))
```

### batch 实例

```python
from lupro import lupro, lupros, batch
from pprint import pprint

url = 'https://www.python.org/doc/versions/'

task = lupro('python docs/', lupros.get(url , timeout = 15), content = 200)

doc_ver = task.xpath_analysis({'documentation url' :'//*[@id="python-documentation-by-version"]/ul//li/a/@href', 'documentation' :'//*[@id="python-documentation-by-version"]/ul//li/a/text()'})
pprint(doc_ver)

savahtml = batch(task, doc_ver['documentation url'], doc_ver['documentation'])

savahtml.BulkDownload()
```

### 任务自省，冷重启

```python
from lupro import batch
from pprint import pprint

# 需要在batch前 设置 PERSISTENCE_ENABLED = True
task_name = 'python docs/'
# 任务冷重启
batch.coldheavy(task_name)
# 任务回调
pprint(batch.callback(task_name))
```

## 特性

* [X] 完全兼容 `requests` or `httpx`
* [X] 异步特性
* [X] lupro生成器
* [X] 自动编码修正
* [X] 解析器与解析链
* [X] 选择器与选择链
* [X] 下载器
* [X] 对象持久化
* [X] 任务自省，冷重启
* [ ] 交互式
* [ ] 微服务

## api 文档

[**lupro api** ](https://luxuncang.github.io/lupro/)
