from PyQt5 import QtCore, QtGui, QtWidgets
import re
import Dbactions
import CryptoFunctions



class LogIn(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(521, 341)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(170, 290, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 110, 471, 34))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.PassLabe = QtWidgets.QLabel(self.layoutWidget)
        self.PassLabe.setObjectName("PassLabe")
        self.horizontalLayout_2.addWidget(self.PassLabe)
        spacerItem = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.PassLine = QtWidgets.QLineEdit(self.layoutWidget)
        self.PassLine.setText("")
        self.PassLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PassLine.setObjectName("PassLine")
        self.horizontalLayout_2.addWidget(self.PassLine)
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(10, 190, 191, 22))
        self.checkBox.setObjectName("checkBox")
        self.layoutWidget1 = QtWidgets.QWidget(Dialog)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 10, 461, 34))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.UserLabe = QtWidgets.QLabel(self.layoutWidget1)
        self.UserLabe.setObjectName("UserLabe")
        self.horizontalLayout.addWidget(self.UserLabe)
        spacerItem1 = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.UserEdit = QtWidgets.QLineEdit(self.layoutWidget1)
        self.UserEdit.setText("")
        self.UserEdit.setObjectName("UserEdit")
        self.horizontalLayout.addWidget(self.UserEdit)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(370, 180, 111, 34))
        self.pushButton.setObjectName("pushButton")
        Dialog.accept=self.accept
        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(lambda: self.accept(Dialog,self.UserEdit.text(),self.PassLine.text(),self.checkBox.isChecked()))
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.pushButton.clicked.connect(self.signup)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.PassLabe.setText(_translate("Dialog", "Password"))
        self.checkBox.setText(_translate("Dialog", "Work Offline"))
        self.UserLabe.setText(_translate("Dialog", "Username"))
        self.pushButton.setText(_translate("Dialog", "Create Account"))

    def accept(self,Dialog,user,passw,isoffline):
        if isoffline:
            if Dbactions.sqlite.OfflineCheck():
                print('Yeahabove')
                if Dbactions.sqlite().login(passw):
                    print('YEAH')
                    self.info={'username':None,'password':passw,'isoffline':True}
                    return Dialog.reject()
                else:
                    print('Yeahbelovw')
                    self.errormsg(Dialog)
            else:
                self.errormsg(Dialog, 'Hey so you gotta go online and download the database first.Log in in online mode and Download from menu.')    
                
                
        else:
            if Dbactions.UserAccess().Login(user,passw):
                userid=Dbactions.UserAccess().GetId(user)
                self.info={'username':userid,'password':passw,'isoffline':False}
                return Dialog.reject()
            else:
                self.errormsg(Dialog)
                

    def errormsg(self,Dialog,msg='Unfortunately, you seem to have entered the wrong password. No worries tho, most people eventually figure it out sooner or later. We have a eight character minimum on password FYI'
):
        QtWidgets.QMessageBox.question(Dialog, 'ERROR', msg, QtWidgets.QMessageBox.Ok)
    
    def signup(self):
        details=SignUp.getdetails()
        self.UserEdit.setText(details[0])
        self.PassLine.setText(details[1])
        
    @staticmethod
    def getdialog():
        Logindialog=QtWidgets.QDialog()
        s=LogIn()
        s.setupUi(Logindialog)
        Logindialog.exec_()
        return s.info
    
class Ui_SingUp(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(511, 395)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(160, 330, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 471, 271))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.UserLabe = QtWidgets.QLabel(self.layoutWidget)
        self.UserLabe.setObjectName("UserLabe")
        self.horizontalLayout.addWidget(self.UserLabe)
        spacerItem = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.UserEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.UserEdit.setText("")
        self.UserEdit.setObjectName("UserEdit")
        self.horizontalLayout.addWidget(self.UserEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.PassLabe = QtWidgets.QLabel(self.layoutWidget)
        self.PassLabe.setObjectName("PassLabe")
        self.horizontalLayout_2.addWidget(self.PassLabe)
        spacerItem1 = QtWidgets.QSpacerItem(68, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.PassLine = QtWidgets.QLineEdit(self.layoutWidget)
        self.PassLine.setText("")
        self.PassLine.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PassLine.setObjectName("PassLine")
        self.horizontalLayout_2.addWidget(self.PassLine)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.UserLabe_2 = QtWidgets.QLabel(self.layoutWidget)
        self.UserLabe_2.setObjectName("UserLabe_2")
        self.horizontalLayout_3.addWidget(self.UserLabe_2)
        spacerItem2 = QtWidgets.QSpacerItem(222, 29, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.UserEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.UserEdit_2.setText("")
        self.UserEdit_2.setObjectName("UserEdit_2")
        self.horizontalLayout_3.addWidget(self.UserEdit_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.errorcount=0

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.UserLabe.setText(_translate("Dialog", "Username"))
        self.PassLabe.setText(_translate("Dialog", "Password"))
        self.UserLabe_2.setText(_translate("Dialog", "Email"))

class SignUp(QtWidgets.QDialog):
    def __init__(self,parent=None,**kwargs):
        super(SignUp,self).__init__(parent,**kwargs)
        self.UiInstance=Ui_SingUp() 
        self.UiInstance.setupUi(self)
        
    @staticmethod
    def getdetails(parent=None):
        Signd=SignUp(parent)
        Signd.exec_()
        result=(Signd.UiInstance.UserEdit.text(),Signd.UiInstance.PassLine.text())
        return result

    def accept(self, *args, **kwargs):
        username=self.UiInstance.UserEdit.text()
        password=self.UiInstance.PassLine.text()
        email=self.UiInstance.UserEdit_2.text()
        
        if self.validate(username, password, email):
            passwordhashed=CryptoFunctions.hashpassw(password)
            uid=Dbactions.UserAccess().AddUser(username, passwordhashed, email)
            keyiv=CryptoFunctions.CBCFunctions().CBCencrypt(password)
            Dbactions.UserAccess().AddKeyEntry(uid, keyiv[0],keyiv[1])
            self.reject()
        
    def error(self,typ='password'):
        msg='Error in password: Must be atleast eight characters.Come on you just have to remember this one, make it a little secure allright'
        if typ=='email':
            msg='Give a valid email you fraud.'
        if typ=='username':
            msg='Hey, dipshit you already have an account.'
            
        QtWidgets.QMessageBox.question(self, 'ERROR', msg, QtWidgets.QMessageBox.Ok)

    def validate(self,username,password,email):
        if len(password)<8:
            self.error()
            return False
            
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)==None:
            self.error('email')
            return False
            
        if Dbactions.UserAccess().UsernameNotAvailabe(username)==1:
            self.error('username')
            return  False
        return True
