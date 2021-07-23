# lupro 爬虫框架

**lupro是一个完全兼容requests的异步爬虫框架**

## 安装 `Lupro`

### 使用 [PyPi](https://pypi.org/) 安装 Lupro

* `pip` Find, install and publish Python packages with the Python Package Index
* `pip install lupro`

## 开始使用

1. 导入 `from lupro import lupro`

### 兼容requests

```python
from lupro import lupro as requests
```

_这样即可不用修改代码完全替换_ `requests`

### 原生lupro

```python
from lupro import lupro
r = lupro.get('https://www.python.org')
r.status_code
```

### 批量异步任务

```python
from lupro import lupro,lupros,generator,Batchsubmission

# 请求列表
url = ['https://www.python.org','https://www.baidu.com']

# 实例化模板
r = lupro('test',lupros.get(''))

# lupro 生成器
lu = generator(r, url)

# 批量任务
Batchsubmission(lu)
```

## 特性

* [X] 完全继承requests
* [X] 异步特性
* [X] lupro生成器
* [X] 自动编码修正
* [X] 解析器与解析链
* [ ] 选择器与选择链
* [X] 下载器
* [X] 请求头生成器
* [ ] 交互式
* [ ] 微服务

## api 文档

[**lupro api** ](https://luxuncang.github.io/lupro/)
