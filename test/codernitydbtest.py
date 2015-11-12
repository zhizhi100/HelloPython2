# encoding: utf-8
'''
Created on 2015年11月12日

@author: ZhongPing
'''

from CodernityDB.database import Database
from CodernityDB.tree_index import TreeBasedIndex

class WithXIndex(TreeBasedIndex):

    def __init__(self, *args, **kwargs):
        kwargs['node_capacity'] = 10
        kwargs['key_format'] = 'I'
        super(WithXIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        t_val = data.get('x')
        if t_val is not None:
            return t_val, None
        return None

    def make_key(self, key):
        return key


def main():
    db = Database('/tmp/tut4')
    db.open()
    #db.create()
    #x_ind = WithXIndex(db.path, 'x')
    #db.add_index(x_ind)
    '''
    for x in xrange(100):
        db.insert(dict(x=x))

    for y in xrange(100):
        db.insert(dict(y=y))
    '''
    print db.get('x', 10, with_doc=True)

    for curr in db.get_many('x', start=15, end=25, limit=-1, with_doc=False):
        print curr


if __name__ == '__main__':
    main()