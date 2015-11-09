# -*- coding: utf-8 -*-
'''
Created on 2015年11月8日

@author: ZhongPing
'''

import rsa,base64

def genkey():
    (pubkey, privkey) = rsa.newkeys(4096)

    pub = pubkey.save_pkcs1()
    pubfile = open('public.pem','w+')
    pubfile.write(pub)
    pubfile.close()
    
    pri = privkey.save_pkcs1()
    prifile = open('private.pem','w+')
    prifile.write(pri)
    prifile.close()
    


def test():
    message = 'hello'
    with open('public.key') as publickfile:
        p = publickfile.read()
        #print p
        pubkey = rsa.PublicKey.load_pkcs1(p)
    
    with open('private.key') as privatefile:
        p = privatefile.read()
        #print p
        privkey = rsa.PrivateKey.load_pkcs1(p)
        
    crypto = base64.encodestring(rsa.encrypt(message, pubkey))
    print len(base64.encodestring(rsa.encrypt('20161230', pubkey)))
    print len(rsa.encrypt('abcd123123123123123123123123123123', pubkey))

    message = rsa.decrypt(base64.decodestring(crypto), privkey)
    print message
    
    #signature = rsa.sign(message, privkey, 'SHA-1')
    #rsa.verify('hello', signature, pubkey)

if __name__ == '__main__':
    #genkey()
    test()