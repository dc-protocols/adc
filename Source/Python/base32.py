1.#!/usr/bin/python
2. 
3.import base64
4. 
5.def toBase32(s):
6.        return base64.b32encode(s).strip('=')
7.        
8.def fromBase32(base32):
9.        base32+= (8-len(base32) %8)*'='
10.        return base64.b32decode(base32)
