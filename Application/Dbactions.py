import pymysql
import CryptoFunctions
import sqlite3
import os


class PasswordAccess():
    
    def __init__(self): 
        self.db=pymysql.connect("sql12.freemysqlhosting.net","sql12190405","vlirLU12NN","sql12190405")
        self.cursor=self.db.cursor()

    def GetAll(self,userid):
        self.cursor.execute('SELECT `Site`,`Password` FROM `PasswordAll` WHERE `idUserAccount`=%s;',userid)
        result=self.cursor.fetchall()
        return result
        self.db.close()

    def GetSiteList(self,userid):
        self.cursor.execute('SELECT `Site` FROM `PasswordAll` WHERE `idUserAccount`=%s',userid)
        lis=self.cursor.fetchall()
        returnlist=[]
        for row in lis:
            returnlist.append(row[0])
        return returnlist
        self.db.close()
        
    def InsertSite(self,userid,site,passw):
        sql='INSERT INTO `PasswordAll` VALUES (%s,%s,%s);'
        self.cursor.execute(sql,(userid,site,passw))
        self.db.commit()
        self.db.close()
        
    def UpdateSite(self,uid,site,passw):
        print(uid,site,passw)
        self.cursor.execute('UPDATE `PasswordAll` SET `Password`=%s WHERE `idUserAccount`=%s AND `Site`=%s',(passw,uid,site) )
        self.db.commit()
        self.db.close()
        
class UserAccess():
    def __init__(self):
        self.conn=pymysql.connect("sql12.freemysqlhosting.net","sql12190405","vlirLU12NN","sql12190405")
        self.cursor=self.conn.cursor()
    
    def Login(self,uname,passw):
        data=self.GetAllfromusername(uname)
        try:
            passwh=data[2]
            return CryptoFunctions.checkhass(passw, passwh)
        except TypeError:
            print('ERROR reported lol')
            return False
        self.conn.close()
        
    def GetAllfromusername(self,username):
        #CHanged username to idUserAccounts, may cause damages in Initialogin
        #Used in Initiallogin line no. 70 yet to be managed
        self.cursor.execute('SELECT * FROM `UserAccounts` WHERE `Username`=%s;',username)
        s=self.cursor.fetchone()
        return s  
    
    def getallfromid(self,uid):
        self.cursor.execute('SELECT * FROM `UserAccounts` WHERE `idUserAccounts`=%s;',uid)
        s=self.cursor.fetchone()
        return s
    
      
    def GetId(self,username):
        self.cursor.execute('SELECT `idUserAccounts` FROM `UserAccounts` WHERE `Username`=%s;',username)
        s=self.cursor.fetchone()[0]
        return s
    
    def getKeys(self,userid):
        self.cursor.execute('SELECT `KeyValue`,`IVValue` FROM `KeyValues` WHERE `idUserAccounts`=%s',userid)
        s=self.cursor.fetchone()
        return s
        
    def AddUser(self,username,passw,email):
        print('UPDATED FAGGOT')
        self.cursor.execute("INSERT INTO `UserAccounts` (`Username`, `Passoword`, `Email`) VALUES (%s,%s,%s);",(username,passw,email))
        self.conn.commit()
        self.cursor.execute('SELECT `idUserAccounts` FROM `UserAccounts` WHERE `Username`=%s',username)
        s=self.cursor.fetchone()
        self.conn.close()
        return s[0]
    def UsernameNotAvailabe(self,username):
        self.cursor.execute("SELECT EXISTS(SELECT * FROM `UserAccounts` WHERE `UserName`=%s)",username)
        s=self.cursor.fetchone()[0]
        self.conn.close()
        return s
    def AddKeyEntry(self,uid,key,iv):
        #ALready encrypted key and iv
        self.cursor.execute('INSERT INTO `KeyValues` VALUES (%s,%s,%s)',(uid,key,iv))
        self.conn.commit()
        self.conn.close()
    
class sqlite():
  
    def __init__(self):
        if os.path.exists('Porn.db'):
            self.conn=sqlite3.connect('Porn.db')
            self.cursor=self.conn.cursor()
            self.initialsetup=True
        else:
            self.conn=sqlite3.connect('Porn.db')
            self.cursor=self.conn.cursor()
            self.cursor.execute("""CREATE TABLE `Lonelyboi` (
            `Uid`    INTEGER,
            `Username`    TEXT,
            `Password`    BLOB,
            `Email`    TEXT,
            `Key`    BLOB,
            `IV`     BLOB
            )""")
            self.cursor.execute("""CREATE TABLE `Passwordboi` (
            `Site` TEXT,
            `Password` BLOB,
            `UpdatedOnline` INTEGER,
            PRIMARY KEY(`Site`)
            );""")
            self.conn.commit()
            self.initialsetup=False
        
    def getoffline(self,uid):
        print(uid)
        if not self.initialsetup:
            print('Starting setup')
            self.setup(uid)
        Alldata=PasswordAccess().GetAll(uid)
        print(Alldata)
        for row in Alldata:
            #just worked all of a sudden make sure that no problems with data types being returned.
            if not self.existsintable(row):
                self.cursor.execute('INSERT INTO `Passwordboi`(`Site`,`Password`,`UpdatedOnline`) VALUES (?,?,1)',row)
       
        self.conn.commit()
        
    def updateonline(self,uid):
        self.cursor.execute('SELECT `Site`,`Password` FROM `Passwordboi` WHERE `UpdatedOnline`= 0')
        s=self.cursor.fetchall()
        for row in s:
            PasswordAccess().InsertSite(uid, row[0], row[1])
        self.cursor.execute('UPDATE `Passwordboi` SET `UpdatedOnline`=1 WHERE `UpdatedOnline`=0')
        self.conn.commit()
        
    def existsintable(self,row):
        self.cursor.execute('SELECT `Password` FROM `Passwordboi` WHERE `Site`=?',(row[0],))
        s=self.cursor.fetchall()
        return s
        
    def setup(self,uid):
        data=list(UserAccess().getallfromid(uid))
        keyiv=UserAccess().getKeys(uid)
        for item in keyiv:
            data.append(item)
        
        tdata=tuple(data)
        self.cursor.execute('INSERT INTO `Lonelyboi` VALUES(?,?,?,?,?,?)',tdata)
        
    def login(self,passw):
        try:
            passwh=self.getuserdata()[2]
            return CryptoFunctions.checkhass(passw, passwh)
        except TypeError:
            return False
            print('Password not in db')
            
    def getuserdata(self):
        self.cursor.execute('SELECT * FROM `Lonelyboi`')
        s=self.cursor.fetchone()
        return s
    
    def getpassword(self):
        self.cursor.execute('SELECT `Site`,`Password` FROM `Passwordboi`')
        return self.cursor.fetchall()
    
    def getsitelist(self):
        self.cursor.execute('SELECT `Site` FROM `Passwordboi`')
        lis=self.cursor.fetchall()
        returnlist=[]
        for row in lis:
            returnlist.append(row[0])
        return returnlist
    
    def insertsite(self,site,passw):
        self.cursor.execute('INSERT INTO `Passwordboi` VALUES(?,?,0)',(site,passw))
        self.conn.commit()
        self.conn.close()
        
    def updatesite(self,site,passw):
        self.cursor.execute('UPDATE `Passwordboi` SET `Password`=? WHERE `Site`=?',(passw,site) )
        self.conn.commit()
        self.conn.close()
        
    @staticmethod
    def OfflineCheck():
        return os.path.exists('Porn.db')
        