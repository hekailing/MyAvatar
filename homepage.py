#!/usr/bin/python
import cgi, cgitb
import os
import time

import account_info
import genhash
from page_template import readPageTmpl as readPageTmpl


def login(fieldData):
    username = fieldData.getvalue('username')
    password = fieldData.getvalue('password')
    if account_info.accountCheck(username, password):
        return uploadForm().replace('AnyBody', str(username)). \
            replace('PictureUrl', '').replace('ErrorMsg', '')
    else:
        return loginForm().replace('ErrorMsg', 'username or password incorrect!!')


def logout():
    pass


def savePicture(fieldData):
    '''
    Save the uploaded picture to /tmp
    '''
    fileitem = fieldData.getvalue('filename')
    if fileitem and fileitem.filename:
        filename = os.path.basename(fileitem.filename)
        open('/tmp' + filename, 'wb').write(fileitem.file.read())
        message = 'The file "' + filename + '" was uploaded successfully'
    else:
        message = 'No file was uploaded'
    return uploadForm().replace('ErrorMsg', message)
        
        
def makePage():
    cgitb.enable()
    fieldData = cgi.FieldStorage()    
    if 'createForm' in fieldData:
        return createForm().replace('ErrorMsg', '')
    elif 'create' in fieldData:
        return accountCreater(fieldData)
    elif 'logout' in fieldData:
        logout()
        return loginForm().replace('ErrorMsg', '')
    elif 'login' in fieldData:
        return login(fieldData)
    else:
        return readPageTmpl('login.html').replace('ErrorMsg', '')


print "Content-Type:text/html\n"
print readPageTmpl('login.html').replace('ErrorMsg', '')

