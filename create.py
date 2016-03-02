#! /usr/bin/python
import cgi
import cgitb

from  page_template import readPageTmpl as readPageTmpl
import account_info


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
        print loginForm.replace('ErrorMsg', '')
    else:
        print createForm.replace('ErrorMsg', 'Please fill in all information')
else:
    print createForm.replace('ErrorMsg', '')
    

