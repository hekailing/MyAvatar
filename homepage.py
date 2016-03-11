#!/usr/bin/python
import cgi, cgitb
import os
import shutil
from os import environ
import time
import string

import account_info
import genhash
from page_template import readPageTmpl as readPageTmpl
import session
import getpicture


def login(sess, fieldData):
    '''
    Get username and password from the fieldData.  Check the account info.  
    If the checking success, write username an email into session file and 
    then jump to the welcome page.  Otherwise show login page with error 
    message.
    '''
    username = fieldData.getvalue('username', '')
    password = fieldData.getvalue('password', '')
    if account_info.accountCheck(username, password):
        sess.data['Username'] = username
        sess.data['Email'] = account_info.getEmailFromUserName(username)
        welcome(sess)
        return True
    else:
        print readPageTmpl('login.html') \
            .replace('ErrorMsg', 'username or password incorrect!!')
        return False


def logout(sess):
    # clear session data
    sess.data.pop('Username')
    sess.data.pop('Email')
    # Back to the login
    print readPageTmpl('login.html').replace('ErrorMsg', '')


def welcome(sess, errorMsg=''):
    '''
    Print the welcome html.  Replace username, pictureUrl and errorMsg pattern.  
    '''
    username = sess.data['Username']
    email = sess.data['Email']
    pictureUrl = getpicture.getUrlFromEmail(email)
    print readPageTmpl('welcome.html').replace('AnyBody', username) \
                                      .replace('PictureUrl', pictureUrl) \
                                      .replace('ErrorMsg', errorMsg)


def savePicture(sess, fieldData):
    '''
    Save the uploaded picture to DOCUMENT_ROOT/avatar/xxxx.
    And then generate the welcome page with error message.
    '''
    email = sess.data.get('Email', '')
    if email:
        documentRoot = environ.get('DOCUMENT_ROOT')
        fileitem = fieldData['filename']
        if fileitem is not None and fileitem.filename:
            filename = os.sep.join((getpicture.pictureDir,
                                    genhash.genMd5(string.lower(email))))
            pathname = os.sep.join((documentRoot, filename))
            tmpname = '.'.join((pathname, 'tmp'))
            message = 'The file "%s" was uploaded failed' % fileitem.filename
            with open(tmpname, 'wb') as fh:
                fh.write(fileitem.file.read())
                fh.close()
                shutil.move(tmpname, pathname)
                message = 'The file "%s" was uploaded successfully' % fileitem.filename
        else:
            message = 'No file was uploaded'
    else:
        message = 'Email lost!!'
    welcome(sess, message)


def showPicture(url):
    '''
    For the API to get picture.  
    Just show the picture of provided url in browser
    '''
    print '''
<html>
  <head>
    <title>Get Picture</title>
  </head>
  <body>
    <img src="%s">
  </body>
</html>''' % url

        
def makePage(sess, fieldData):
    if sess.isTimeout():
        # Session is timeout.  Login again.
        print readPageTmpl('login.html').replace('ErrorMsg',
                                                 'Timeout! Please login again.')
    elif sess.data.has_key('Username') and sess.data.has_key('Email'):
        if 'upload' in fieldData:
            savePicture(sess, fieldData)
        elif 'logout' in fieldData:
            logout(sess)
        else:
            welcome(sess, '')
    else:
        # Session data lost.  Maybe the session is created just right now.
        if 'login' in fieldData:
            login(sess, fieldData)
        else:
            print readPageTmpl('login.html').replace('ErrorMsg', '')
        


if __name__ == '__main__':
    cgitb.enable()
    fieldData = cgi.FieldStorage()
    # This is for getpicture api
    if 'u' in fieldData:
        url = getpicture.getUrlFromUserName(fieldData.getvalue('u', ''))
        print "Content-Type:text/html\n"
        showPicture(url)
    # This is also for getpicture api
    elif 'e' in fieldData:
        url = getpicture.getUrlFromEmail(fieldData.getvalue('e', ''))
        print "Content-Type:text/html\n"
        showPicture(url)
    # This is for user to login, logout and upload picture
    else:
        # Open or create the session according to the cookie "sid"
        session_ = session.Session(expires=7*24*60*60, cookie_path='/')
        print str(session_.cookie)
        print "Content-Type:text/html\n"
        # Generate the page
        makePage(session_, fieldData)
        session_.data['lastvisit'] = repr(time.time())
        # write session data to file
        session_.close()
