# -*- coding: UTF8 -*-
'''
Created on 2015年12月1日

@author: ZhongPing
'''
from ctypes import *
dll = CDLL( 'E:/test/gtmanager/DiskID32.dll' )
#dll.DiskID32.argtypes=[c_char *32,c_char *32]
dll.DiskID32.argtypes=[c_char_p,c_char_p]
#model = c_char() * 31
#id = c_char() * 31
'''
for i in range(0,32):
    c = c_char()
    c.value = '0'
    id.append(c)
    model.append(c)
'''
#succ = dll.DiskID32(byref(model),byref(id))
model = (c_char *32)()
id = (c_char *32)()
#model = create_string_buffer('\000' * 31)
#id = create_string_buffer('\000' * 31)
model = create_string_buffer("Hello, World",32)
id = create_string_buffer("Hello, World",32)
succ = dll.DiskID32(model,id)
print model
print id