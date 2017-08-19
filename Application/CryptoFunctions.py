from Crypto.Cipher import AES
from passlib.hash import sha256_crypt
import os

class CryptoFunctions():
    
    def __init__(self,key,iv):
        self.key=key
        self.iv=iv
        
    def encrypt(self,msg):
        enc=AES.new(self.key,AES.MODE_CFB,self.iv)
        return enc.encrypt(msg)
        
    def decrypt(self,cipher):
        dec=AES.new(self.key,AES.MODE_CFB,self.iv)
        return dec.decrypt(cipher)

class CBCFunctions():
    def CBCencrypt(self,password):
        password=self.pad(password)
        key=os.urandom(16)
        iv=os.urandom(16)
        enc=AES.new(password)
        return (enc.encrypt(key),enc.encrypt(iv))
    
    def CBCdecrypt(self,key,iv,passw):
        passw=self.pad(passw)
        dec=AES.new(passw)
        return(dec.decrypt(key),dec.decrypt(iv))
    
    
    def pad(self,key):
        BLOCK_SIZE=16
        PADCHARACTER="~"
        if len(key)>BLOCK_SIZE:
            return key[:16]
        else:
            while len(key)<16:
                key+=PADCHARACTER
            return  key

def hashpassw(passw):
    has=sha256_crypt.encrypt(passw)
    return(has)

def checkhass(passw,has):
    return sha256_crypt.verify(passw, has)
