'''
lupro 内部控制器
'''

from .typing import Any
from .api import generator, Batchsubmission, BulkDownload, Batchanalysis, xpath_Batchanalysis, json_Batchanalysis, re_Batchanalysis
from .publictool import reconfig, abnormal, original, persistence
import atexit

# 批量任务控制器
class batch():
    '''批量任务控制器'''

    def __init__(self, instantiation, url : list, filenameNo : list = []) -> list:
        '''实例化生成器

        Args:
            `instantiation` : `lupro` lupro模板实例
            `url` : `list` 链接表
            `filenameNo` : `list` filename 序列且此序列会继承 `instantiation.filename` 

        Returns:
            None
        '''
        self.name = instantiation.filename
        self.generator = generator(instantiation, url, filenameNo)
        self.filenameNo = [i.filename for i in self.generator]
        persistence.shelve.add(self.name, {})
    
    # 任务自省
    @reconfig(config = persistence.ENABLED)
    def province(self):
        '''任务自省'''
        fail, success, task = [], [], []
        dbdict = persistence.shelve.put()
        for i,j in enumerate(self.filenameNo):
            if not j in dbdict:
                fail.append(j)
                task.append(self.generator[i])
                success.append('-') # not perfect
            else:
                success.append(dbdict[j])
        persistence.shelve.add(self.name, {'success' : success, 'task' : task, 'filenameNo' : self.filenameNo})

        print(f"批量任务 {self.name} >> 一共有 {len(self.filenameNo)} 次请求", f"失败了 {len(fail)} 次" ,sep = '\n')
        if not len(fail)==0:
            res = '\n' + '\n'.join(fail)
            print(f"分别是: {res}")

    # 冷重启
    @staticmethod
    def coldheavy(filename) -> None:
        '''冷重启

        Args：
            `filename` : `str` 冷重启对象的 `self.name`
            
        Returns:
            None
        '''
        Batchsubmission(persistence.shelve.put()[filename]['task'])

    # 任务回调
    @staticmethod
    def callback(filename) -> list:
        '''任务反持久化

        Args：
            `filename` : `str` 冷重启对象的 `self.name`
            
        Returns:
            None
        '''
        container = persistence.shelve.put()
        return [container.get(i) for i in container[filename]['filenameNo']]
        
    # 批量请求
    @abnormal
    def Batchsubmission(self) -> list:
        '''批量请求'''
        atexit.register(batch.province, self)
        return Batchsubmission(self.generator)
    
    # 批量下载
    @abnormal
    def BulkDownload(self) -> list:
        '''批量下载'''
        atexit.register(batch.province, self)
        return BulkDownload(self.generator)
    
    # 批量解析
    @abnormal
    def Batchanalysis(self, mold : str , analytic : dict, auxiliary = original) -> list:
        '''批量解析'''
        atexit.register(batch.province, self)
        return Batchanalysis(mold, self.generator, analytic, auxiliary)
    
    # xpath 批量解析
    @abnormal
    def xpath_Batchanalysis(self, analytic, auxiliary = original) -> list:
        '''xpath 批量解析'''
        atexit.register(batch.province, self)
        return xpath_Batchanalysis(self.generator, analytic, auxiliary)
    
    # json 批量解析
    @abnormal
    def json_Batchanalysis(self, analytic, auxiliary = original) -> list:
        '''json 批量解析'''
        atexit.register(batch.province, self)
        return json_Batchanalysis(self, analytic, auxiliary)    
    
    # 正则 批量解析
    @abnormal
    def re_Batchanalysis(self, analytic, auxiliary = original) -> list:
        '''正则 批量解析'''
        atexit.register(batch.province, self)
        return re_Batchanalysis(self.generator, analytic, auxiliary)

