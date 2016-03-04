# encoding: utf-8
'''
Created on 2016年3月4日

@author: ZhongPing
'''
import os.path
from whoosh.index import create_in
import whoosh.index as index
from whoosh.fields import *
from whoosh import writing

class Indexer(object):
    def __init__(self,Title):
        self.indexpath = "D:/tmp/"+Title+"index"
        self.schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)        
        if not os.path.exists(self.indexpath):
            os.mkdir(self.indexpath)
            self.ix = create_in(self.indexpath, self.schema)  
        else:
            self.ix = index.open_dir(self.indexpath)
        self.writer = self.ix.writer()
    
    def clean(self):
        #self.writer.commit(mergetype=writing.CLEAR)
        self.ix = create_in(self.indexpath, self.schema)
        
    def merge(self):
        self.writer.commit(optimize=True)
        
    def adddocs(self,docs):
        for doc in docs:
            self.writer.add_document()
        self.writer.commit(merge=False)
          

if __name__ == '__main__':
    pass