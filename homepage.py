#!/usr/bin/python
import cgi, cgitb
import os
import time

import account_info
import genhash

def loginForm():
    return '''<html>
<head>
    <title>
        Login Form
    </title>
</head>
<body>
    <div id="title">
        <h1>MyAvatar</h1>
    </div>
    <div id="topright">
        Click <a href="homepage.py?createForm=on">Here</a> to Sign In.
    </div>
    <form id="loginForm" class="round" method="post" action="homepage.py">
    <div id="failure">
        ErrorMsg
    </div>
    <div class="field">
        username <input type="text" class="input" name="username" id="user" 
               placeholder="username">
    </div>
    <div class="field">
        password <input type="password" class="input" name="password" id="password" 
               placeholder="password">
    </div>
    <div class="field">
        <input type="checkbox" name="checkbox" id="checkbox">
        <label for="checkbox">Remember me</label>
    </div>
    <div class="field">
        <input type="submit" name="login" class="button" value="Login">
    </div>
    </form>
</body>
</html>'''


def createForm():
    return '''<html>
<head>
    <title>
        Create Form
    </title>
</head>
<body>
    <div id="title">
        <h1>create a new acount</h1>
    </div>
    <form id="createAccountForm" class="round" method="post" action="homepage.py">
    <div id="failure">
        ErrorMsg
    </div>
    <div class="field">
        username <input type="text" class="input" name="user" id="username" 
               placeholder="username">
    </div>
    <div class="field">
        password <input type="password" class="input" name="password" id="password" 
               placeholder="password">
    </div>
    <div class="field">
        email&nbsp&nbsp&nbsp <input type="text" class="input" name="email" id="email" 
               placeholder="email">
    </div>
    <div>
        <input type="submit" name="create" class="button" value="Create Account">
    </div>
    <div id="signIn">
        I Have a Account, Click <a href="homepage.py">Here</a> to Sign In.
    </div>
</body>
</html>'''


def uploadForm():
    return '''<html>
<head>
    <title>
        Upload Form
    </title>
</head>
<body>
    <div id="title">
        <src="PictureUrl">
        <h1>Welcome, AnyBody</h1>
    </div>
    <form id="uploadForm" class="round" method="post" action="homepage.py">
    <div>
        Select a picture: <input type="file" name="filename">
    </div>
    <div>
        <input type="submit" name="upload" class="button" value="Upload">
    </div>
    <div id="failure">
        ErrorMsg
    </div>
</body>
</html>'''


def accountCreater(fieldData):
    username = fieldData['username'] if fieldData.has_key('username') else None
    password = fieldData['password'] if fieldData.has_key('password') else None
    email = fieldData['email'] if fieldData.has_key('email') else None
    if username and password and email:
        pass
    else:
        return createForm().replace('ErrorMsg', 'Please fill in all the information')


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
        return loginForm().replace('ErrorMsg', '')


print "Content-Type:text/html\n"
print makePage()

