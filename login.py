#! /usr/bin/python
import cgi
import cgitb

import account_info
from page_template import readPageTmpl as readPageTmpl


cgitb.enable()
fieldData = cgi.FieldStorage()    
print "Content-Type:text/html\n"
if 'login' in fieldData:
    username = fieldData.getvalue('username')
    password = fieldData.getvalue('password')
    if account_info.accountCheck(username, password):
        print readPageTmpl('welcome.html') \
            .replace('AnyBody', str(username)) \
            .replace('PictureUrl', '').replace('ErrorMsg', '')
    else:
        print readPageTmpl('login.html') \
            .replace('ErrorMsg', 'username or password incorrect!!')
else:
    raise Exception("cannot run here")
