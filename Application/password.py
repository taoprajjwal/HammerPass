from PyQt5 import QtCore, QtGui, QtWidgets
import Dbactions
from PyQt5.Qt import QTableWidgetItem
import CryptoFunctions
import time

#Sanitize Site Input

#Main Program Section
class Ui_MainWindow(object):
    def __init__(self,cred,**kwargs):
        super(Ui_MainWindow,self).__init__(**kwargs)
        self.cred=cred
        print(cred)
        if cred['isoffline']:
            data=Dbactions.sqlite().getuserdata()
            self.encryptedkeys=(data[4],data[5])
        else:
            self.encryptedkeys=Dbactions.UserAccess().getKeys(cred['username'])
        
        self.decryptedkeys=CryptoFunctions.CBCFunctions().CBCdecrypt(self.encryptedkeys[0], self.encryptedkeys[1], cred['password'])
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 801, 541))
        self.tableWidget.setGridStyle(QtCore.Qt.CustomDashLine)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setHorizontalHeaderLabels(['Website','Password'])
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 30))
        self.menubar.setObjectName("menubar")
        self.menuFIle = QtWidgets.QMenu(self.menubar)
        self.menuFIle.setObjectName("menuFIle")
        self.menuDatanase = QtWidgets.QMenu(self.menubar)
        self.menuDatanase.setObjectName("menuDatanase")
        self.menuOfflineFunctions=QtWidgets.QMenu(self.menubar)
        self.menuOfflineFunctions.setObjectName("menuOfflineFunctions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setCheckable(False)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(sys.exit)
        self.actionAdd = QtWidgets.QAction(MainWindow)
        self.actionAdd.setObjectName("actionAdd")
        self.actionAdd.triggered.connect(self.SiteDialog)
        self.actionTest_Database = QtWidgets.QAction(MainWindow)
        self.actionTest_Database.setObjectName("actionTest_Database")
        self.actionTest_Database.triggered.connect(self.UpdateDialog)
        self.actionGetOffline=QtWidgets.QAction(MainWindow)
        self.actionGetOffline.setObjectName("actionGetOffline")
        self.actionUpdateOnline=QtWidgets.QAction(MainWindow)
        self.actionUpdateOnline.setObjectName("actionUpdateOnline")
        if (self.cred['isoffline']):
            self.actionUpdateOnline.triggered.connect(lambda: self.error(MainWindow))
            self.actionGetOffline.triggered.connect(lambda: self.error(MainWindow))
            
        else:
            self.actionUpdateOnline.triggered.connect(lambda: Dbactions.sqlite().updateonline(self.cred['username']))
            self.actionGetOffline.triggered.connect(lambda: Dbactions.sqlite().getoffline(self.cred['username']))
            
        self.menuFIle.addAction(self.actionQuit)
        self.menuDatanase.addAction(self.actionAdd)
        self.menuDatanase.addAction(self.actionTest_Database)
        self.menuOfflineFunctions.addAction(self.actionGetOffline)
        self.menuOfflineFunctions.addAction(self.actionUpdateOnline)
        self.menubar.addAction(self.menuFIle.menuAction())
        self.menubar.addAction(self.menuDatanase.menuAction())
        self.menubar.addAction(self.menuOfflineFunctions.menuAction())
        self.Setuptable()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFIle.setTitle(_translate("MainWindow", "Fi&le"))
        self.menuDatanase.setTitle(_translate("MainWindow", "&Password Functions"))
        self.menuOfflineFunctions.setTitle(_translate("MainWindow","O&nline Functions"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionAdd.setText(_translate("MainWindow", "&Add Password"))
        self.actionGetOffline.setText(_translate("MainWindow","Download Password Database Offline"))
        self.actionUpdateOnline.setText(_translate("MainWindow","U&pdate online database"))
        self.actionTest_Database.setText(_translate("MainWindow", "&Change Password"))
    
    def Setuptable(self):
        if self.cred['isoffline']:
            table=Dbactions.sqlite().getpassword()
        else:    
            table=Dbactions.PasswordAccess().GetAll(self.cred['username'])
        self.tableWidget.setRowCount(len(table))
        for m,row in enumerate(table):
            for n,cell in enumerate(row):
                if n==1:
                    passw=CryptoFunctions.CryptoFunctions(self.decryptedkeys[0],self.decryptedkeys[1]).decrypt(cell)
                    btn=Button(self.tableWidget,passw)
                    self.tableWidget.setCellWidget(m,1,btn)
                else:
                    item=QTableWidgetItem(cell)
                    self.tableWidget.setItem(m,0,item)
    def SiteDialog(self):
        self.site_dialog=CustomAddSiteDialog(self)
        Addsite=Ui_AddSite()
        Addsite.setupUi(self.site_dialog)
        self.site_dialog.show()        
        
    def UpdateDialog(self):
        self.update_dialog=CustomUpdatePasswordDialog(self)
        UpdateSite=Ui_UpdatePassword()
        UpdateSite.setupUi(self.update_dialog)
        self.update_dialog.exec_()
     
    @staticmethod    
    def error(MainInstance):
        print('else')
        QtWidgets.QMessageBox.question(MainInstance,'ERROR','The activities in "Online Functions" are only meant to be used when you are online. So, go online I guess.',QtWidgets.QMessageBox.Ok)

##Dialog UIs
class Ui_AddSite(object):
    def setupUi(self,Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(394, 296)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 361, 140))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.site_label = QtWidgets.QLabel(self.layoutWidget)
        self.site_label.setObjectName("site_label")
        self.horizontalLayout.addWidget(self.site_label)
        self.site_lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.site_lineEdit.setObjectName("site_lineEdit")
        self.horizontalLayout.addWidget(self.site_lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 58, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.Password_label = QtWidgets.QLabel(self.layoutWidget)
        self.Password_label.setObjectName("Password_label")
        self.horizontalLayout_2.addWidget(self.Password_label)
        spacerItem1 = QtWidgets.QSpacerItem(30, 29, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.Password_line = QtWidgets.QLineEdit(self.layoutWidget)
        self.Password_line.setText("")
        self.Password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password_line.setObjectName("Password_line")
        self.horizontalLayout_2.addWidget(self.Password_line)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.password_shown=False
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(227, 160, 141, 34))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.pressed.connect(self.showpass)
        self.GenerateButton = QtWidgets.QPushButton(Dialog)
        self.GenerateButton.setGeometry(QtCore.QRect(10, 160, 111, 34))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.GenerateButton.setFont(font)
        self.GenerateButton.setObjectName("GenerateButton")
        self.GenerateButton.pressed.connect(self.GeneratePass)
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(lambda: Dialog.accept(self.site_lineEdit.text(),self.Password_line.text()))
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self,Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.site_label.setText(_translate("Dialog", "Website Name"))
        self.site_lineEdit.setText(_translate("Dialog", "http://"))
        self.Password_label.setText(_translate("Dialog", "Password"))
        self.pushButton.setText(_translate("Dialog", "Show/Hide Password"))
        self.GenerateButton.setText(_translate("Dialog", "Generate Random"))


    def showpass(self):
        if self.password_shown==False:
            self.Password_line.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.password_shown=True
        else:
            self.Password_line.setEchoMode(QtWidgets.QLineEdit.Password)
            self.password_shown=False
    
    def GeneratePass(self):
        import random
        gen_pass=""
        for i in range(0,16):
            s=random.randint(33,122)
            gen_pass+=chr(s)
    
        self.Password_line.setText(gen_pass)
    
    
class Ui_UpdatePassword(object):
    def setupUi(self, UpdatePassword):
        UpdatePassword.setObjectName("UpdatePassword")
        UpdatePassword.resize(606, 454)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(UpdatePassword.sizePolicy().hasHeightForWidth())
        UpdatePassword.setSizePolicy(sizePolicy)
        UpdatePassword.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        UpdatePassword.setModal(False)
        self.buttonBox = QtWidgets.QDialogButtonBox(UpdatePassword)
        self.buttonBox.setGeometry(QtCore.QRect(380, 410, 211, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(UpdatePassword)
        self.widget.setGeometry(QtCore.QRect(30, 20, 422, 340))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SiteLabel = QtWidgets.QLabel(self.widget)
        self.SiteLabel.setObjectName("SiteLabel")
        self.horizontalLayout.addWidget(self.SiteLabel)
        spacerItem = QtWidgets.QSpacerItem(108, 29, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Sitelist = QtWidgets.QComboBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Sitelist.sizePolicy().hasHeightForWidth())
        self.Sitelist.setSizePolicy(sizePolicy)
        self.Sitelist.setObjectName("Sitelist")
        self.horizontalLayout.addWidget(self.Sitelist)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(17, 68, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.LoginPasswordLabel = QtWidgets.QLabel(self.widget)
        self.LoginPasswordLabel.setWordWrap(True)
        self.LoginPasswordLabel.setObjectName("LoginPasswordLabel")
        self.verticalLayout.addWidget(self.LoginPasswordLabel)
        self.LoginPassEdit = QtWidgets.QLineEdit(self.widget)
        self.LoginPassEdit.setText("")
        self.LoginPassEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LoginPassEdit.setObjectName("LoginPassEdit")
        self.verticalLayout.addWidget(self.LoginPassEdit)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.LoginPassButton = QtWidgets.QPushButton(self.widget)
        self.LoginPassButton.setObjectName("LoginPassButton")
        self.LoginPassButton.pressed.connect(lambda: self.PasswordVisibile(self.LoginPassEdit))
        self.horizontalLayout_3.addWidget(self.LoginPassButton)
        spacerItem2 = QtWidgets.QSpacerItem(298, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem3 = QtWidgets.QSpacerItem(20, 58, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.UpdatedPasswordLabel = QtWidgets.QLabel(self.widget)
        self.UpdatedPasswordLabel.setObjectName("UpdatedPasswordLabel")
        self.horizontalLayout_2.addWidget(self.UpdatedPasswordLabel)
        spacerItem4 = QtWidgets.QSpacerItem(108, 29, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.UpdatedPasswordEdit = QtWidgets.QLineEdit(self.widget)
        self.UpdatedPasswordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.UpdatedPasswordEdit.setObjectName("UpdatedPasswordEdit")
        self.horizontalLayout_2.addWidget(self.UpdatedPasswordEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.widget1 = QtWidgets.QWidget(UpdatePassword)
        self.widget1.setGeometry(QtCore.QRect(30, 360, 420, 36))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.UpdatedPasswordButton = QtWidgets.QPushButton(self.widget1)
        self.UpdatedPasswordButton.setObjectName("UpdatedPasswordButton")
        self.UpdatedPasswordButton.pressed.connect(lambda: self.PasswordVisibile(self.UpdatedPasswordEdit))
        self.horizontalLayout_4.addWidget(self.UpdatedPasswordButton)
        spacerItem5 = QtWidgets.QSpacerItem(298, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.PopulateList(UpdatePassword)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.buttonBox.raise_()
        self.SiteLabel.raise_()
        self.Sitelist.raise_()
        self.LoginPasswordLabel.raise_()
        self.LoginPassEdit.raise_()
        self.LoginPassButton.raise_()
        self.UpdatedPasswordButton.raise_()
        self.UpdatedPasswordButton.raise_()

        self.retranslateUi(UpdatePassword)
        self.buttonBox.accepted.connect(lambda: UpdatePassword.accept(str(self.Sitelist.currentText()),self.LoginPassEdit.text(),self.UpdatedPasswordEdit.text()))
        self.buttonBox.rejected.connect(UpdatePassword.reject)
        QtCore.QMetaObject.connectSlotsByName(UpdatePassword)

    def retranslateUi(self, UpdatePassword):
        _translate = QtCore.QCoreApplication.translate
        UpdatePassword.setWindowTitle(_translate("UpdatePassword", "Update Password"))
        self.SiteLabel.setText(_translate("UpdatePassword", "Site"))
        self.LoginPasswordLabel.setText(_translate("UpdatePassword", "Login Password (This is the pass you use to login into the application"))
        self.LoginPassButton.setText(_translate("UpdatePassword", "Show/Hide Pass"))
        self.UpdatedPasswordLabel.setText(_translate("UpdatePassword", "New Password"))
        self.UpdatedPasswordButton.setText(_translate("UpdatePassword", "Show/Hide Pass"))
        
    def PopulateList(self,Dialog):
        if Dialog.MainInstance.cred['isoffline']:
            self.Sitelist.addItems(Dbactions.sqlite().getsitelist())
        else:
            self.Sitelist.addItems(Dbactions.PasswordAccess().GetSiteList(Dialog.MainInstance.cred['username']))
            
    def PasswordVisibile(self,lineedit):
        if lineedit.echoMode()==QtWidgets.QLineEdit.Password:
            lineedit.setEchoMode(0)
            
        elif lineedit.echoMode()==0:
            lineedit.setEchoMode(2)
                
#Custom Dialog/Button Objects            
class CustomAddSiteDialog(QtWidgets.QDialog):
    
    def __init__(self,MainInstance,**kwargs):
        super(CustomAddSiteDialog,self).__init__(**kwargs)
        self.MainInstance=MainInstance
        
    def accept(self,site,passw, *args, **kwargs):
        site=site.upper()
        encryptedpass=CryptoFunctions.CryptoFunctions(self.MainInstance.decryptedkeys[0],self.MainInstance.decryptedkeys[1]).encrypt(passw)
        if self.MainInstance.cred['isoffline']:
            Dbactions.sqlite().insertsite(site, encryptedpass)
        else:   
            Dbactions.PasswordAccess().InsertSite(self.MainInstance.cred['username'],site,encryptedpass)
        self.MainInstance.Setuptable()
        self.close()

class CustomUpdatePasswordDialog(QtWidgets.QDialog):
    def __init__(self,MainInstance,**kwargs):
        super(CustomUpdatePasswordDialog,self).__init__(**kwargs)
        self.MainInstance=MainInstance
        
    def accept(self,site,loginpass,updatedpass):
        site=site.upper()
        if loginpass==self.MainInstance.cred['password']:
            #Add Encrypted pass
            encryptedpass=CryptoFunctions.CryptoFunctions(self.MainInstance.decryptedkeys[0],self.MainInstance.decryptedkeys[1]).encrypt(updatedpass)
            print(encryptedpass)
            if self.MainInstance.cred['isoffline']:
                Dbactions.sqlite().updatesite(site, encryptedpass)
            else:
                Dbactions.PasswordAccess().UpdateSite(self.MainInstance.cred['username'], site, encryptedpass)
                Dbactions.sqlite().updatesite(site, encryptedpass) #Used because nothing happens if site doens't exist and is more efficient than searching evey row for updated password on each update.
                
        else:
            QtWidgets.QMessageBox.question(self,'FAKE PASSWORD', 'You entered the wrong login password.(Note that login password IS NOT the previous password of the site to be updates. No one gives a fuck about that.) Enter the password that you use while logging in the application.', QtWidgets.QMessageBox.Ok)
        self.MainInstance.Setuptable()
        return self.reject()


class Button(QtWidgets.QPushButton):
    def __init__(self,parent,passw):
        super(Button,self).__init__(parent)
        self.setText("Copy")
        self.word=str(passw)[2:-1]
        self.clicked.connect(self.clip)
        self.maininstance=parent
                
    def clip(self):
        clipboard=QtWidgets.QApplication.clipboard()
        clipboard.setText(self.word,QtGui.QClipboard.Clipboard)
        QtWidgets.QMessageBox.question(self.maininstance, 'LOCKED', 'You just copied the thing and cannot use the application for 30 seconds, copy the password to wherever required, within 30 seconds it will be replaced something awesome.Also please donot click on the copy button after closing this message, it locks the program for another 15 seconds. I am sorry I thought I already fixed it. Guess that is what happens when you program while high on cocaine.' ,QtWidgets.QMessageBox.Ok)
        time.sleep(15)    
        clipboard.setText("You,with your fancy clipboard..You shall not pass.")

    
if __name__ == "__main__":
    import sys
    import InitialLogin
    app = QtWidgets.QApplication(sys.argv)
    cred=InitialLogin.LogIn.getdialog()
    #cred={'username':15,'password':'climacteric2','isoffline':False}
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(cred)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
    

