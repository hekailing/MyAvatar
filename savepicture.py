#! /usr/bin/python
import os
import shutil
from os import environ
import string
import cgi
import cgitb

from page_template import readPageTmpl as readPageTmpl
import genhash


def getCookies():
    cookies = { }
    if environ.has_key('HTTP_COOKIE'):
        cookieStrs = string.split(environ['HTTP_COOKIE'], ';')
        for cookie in map(string.strip, cookieStrs):
            key, value = string.split(cookie, '=')
        cookies[key] = value
    return cookies


'''
Save the uploaded picture to /tmp
'''
cgitb.enable()
fieldData = cgi.FieldStorage()
cookies = getCookies()
email = cookies.get('Email')
documentRoot = environ.get('DOCUMENT_ROOT')
server = environ.get('DOCUMENT_ROOT')
documentRoot = environ.get('DOCUMENT_ROOT')
welcomePage = readPageTmpl('welcome.html')
if 'upload' in fieldData:
    fileitem = fieldData['filename']
    if fileitem is not None and fileitem.filename:
        filename = os.sep.join((documentRoot, 'avatar', genhash.genMd5(email)))
        tmpname = '.'.join((filename, 'tmp'))
        with open(tmpname, 'wb') as fh:
            fh.write(fileitem.file.read())
            fh.close()
            shutil.move(tmpname, filename)
        message = 'The file "%s" was uploaded successfully' % fileitem.filename
    else:
        message = 'No file was uploaded'
else:
    message = ''
print "Content-Type:text/html\n"
print welcomePage.replace('ErrorMsg', message)
