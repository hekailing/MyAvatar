#! /usr/bin/python
import cgi
import cgitb
import re

from  page_template import readPageTmpl as readPageTmpl
import account_info


def usernameCheck(username):
    '''
    Check the username format:
    length is not greater than 20
    only including alphabet, digit and _
    '''
    if len(username) > 20:
        return False
    else if re.match('^\w+$', username):
        return True
    else:
        return False


def emailCheck(email):
    ''' 
    Check the email format    
    length is between 8 and 32
    and the email is like '\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+'
    '''
    emailLen = len(email)
    if emailLen > 32 or emailLen <= 7:
        return False
    else if re.match('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
        return True
    else:
        return False

    
cgitb.enable()
fieldData = cgi.FieldStorage()
print "Content-Type:text/html\n"
createForm = readPageTmpl('createAccount.html')
loginForm = readPageTmpl('login.html')
# with a create form in http request
if 'create' in fieldData:
    username = fieldData.getvalue('username')
    password = fieldData.getvalue('password')
    email = fieldData.getvalue('email')
    if username and password and email:
        if not usernameCheck(username):
            errorMsg = 'username format error'
        else if not emailCheck(email):
            errorMsg = 'email format error'
        else if account_info.usernameExist(username):
            errorMsg = 'username is already used'
        else if account_info.emailExist(email):
            errorMsg = 'email is already used'
        else if account_info.insertAccount(username, password, email):
            errorMsg = ''
        else:
            errorMsg = 'database operation failure'
            errorMsg = 'username or password is wrong'
        if errorMsg:
            print createForm.replace('ErrorMsg', errorMsg)
        else:
            print loginForm.replace('ErrorMsg', '')
    else:
        print createForm.replace('ErrorMsg', 'Please fill in all information')
else:
    print createForm.replace('ErrorMsg', '')
    

