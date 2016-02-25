# encoding: utf-8
'''
Created on 2016年2月22日

@author: ZhongPing
'''
import os.path
from whoosh.index import create_in
from whoosh.fields import *

def main():
    indexpath = "D:/tmp/indexdir"
    if not os.path.exists(indexpath):
        os.mkdir(indexpath)
    schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT)
    ix = create_in(indexpath, schema)
    writer = ix.writer()
    writer.add_document(title=u"First document", path=u"/a",
                        content=u"This is the first document we've added!")
    writer.add_document(title=u"Second document", path=u"/b",
                        content=u"The second one is even more interesting!")
    writer.commit()
    from whoosh.qparser import QueryParser
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse("one")
        results = searcher.search(query)
        print results[0]

if __name__ == '__main__':
    main()
    pass