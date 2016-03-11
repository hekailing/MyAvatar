#! /usr/bin/python
import cgi
import cgitb
import re
import string

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
    elif re.match('^\w+$', username):
        return True
    else:
        return False


def passwordCheck(password):
    # password' length must between 6 and 32
    pwlen = len(password)
    return pwlen >= 6 and pwlen <= 32
    
def emailCheck(email):
    ''' 
    Check the email format    
    length is between 8 and 32
    and the email is like '\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+'
    '''
    emailLen = len(email)
    if emailLen > 32 or emailLen <= 7:
        return False
    elif re.match('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email):
        return True
    else:
        return False


def createAccount():
    '''
    Create account with username, password and email.
1. Get username, password and email from FieldData
2. Check username, password and email value
3. Check username already used
4. Check email already used
5. Insert the account info into database
6. Jump to login page if succeess
    '''
    fieldData = cgi.FieldStorage()
    print "Content-Type:text/html\n"
    createForm = readPageTmpl('createAccount.html')
    loginForm = readPageTmpl('login.html')
    # with a create form in http request
    if 'create' in fieldData:
        username = fieldData.getvalue('username')
        password = fieldData.getvalue('password')
        email = string.lower(fieldData.getvalue('email'))
        if username and password and email:
            if not usernameCheck(username):
                errorMsg = 'username format error'
            elif not passwordCheck(password):
                errorMsg = 'password invalid'
            elif not emailCheck(email):
                errorMsg = 'email format error'
            elif account_info.usernameExist(username):
                errorMsg = 'username is already used'
            elif account_info.emailExist(email):
                errorMsg = 'email is already used'
            elif account_info.insertAccount(username, password, email):
                errorMsg = ''
            else:
                errorMsg = 'database operation failure'
            if errorMsg:
                print createForm.replace('ErrorMsg', errorMsg)
            else:
                print loginForm.replace('ErrorMsg', '')
        else:
            print createForm.replace('ErrorMsg', 'Please fill in all information')
    else:
        print createForm.replace('ErrorMsg', '')
    

if __name__ == '__main__':
    cgitb.enable()
    createAccount()
