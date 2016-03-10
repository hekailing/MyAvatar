#!/usr/bin/python
import cgi, cgitb
import os
import shutil
from os import environ
import time

import account_info
import genhash
from page_template import readPageTmpl as readPageTmpl
import session


_pictureDir = 'avatar'


def login(sess, fieldData):
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
    serverName = environ.get('SERVER_NAME')
    serverPort = environ.get('SERVER_PORT')
    requestScheme = environ.get('REQUEST_SCHEME')
    serverDomain = '://'.join((requestScheme, ':'.join((serverName, serverPort))))
    filename = os.sep.join((_pictureDir, genhash.genMd5(email)))
    pictureUrl = os.sep.join((serverDomain, filename))
    print readPageTmpl('welcome.html').replace('AnyBody', username) \
                                      .replace('PictureUrl', pictureUrl) \
                                      .replace('ErrorMsg', errorMsg)


def savePicture(sess, fieldData):
    '''
    Save the uploaded picture to /tmp
    '''
    email = sess.data.get('Email', '')
    if email:
        documentRoot = environ.get('DOCUMENT_ROOT')
        fileitem = fieldData['filename']
        if fileitem is not None and fileitem.filename:
            filename = os.sep.join((_pictureDir, genhash.genMd5(email)))
            pathname = os.sep.join((documentRoot, filename))
            tmpname = '.'.join((pathname, 'tmp'))
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

        
def makePage(sess):
    fieldData = cgi.FieldStorage()
    # check whether session is timeout
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
    session_ = session.Session(expires=60*60, cookie_path='/')
    print str(session_.cookie)
    print "Content-Type:text/html\n"
    makePage(session_)
    session_.data['lastvisit'] = repr(time.time())
    session_.close()
