#! /usr/bin/python
import os
import cgi
import cgitb

from page_template import readPageTmpl as readPageTmpl


'''
Save the uploaded picture to /tmp
'''
cgitb.enable()
fieldData = cgi.FieldStorage()    
welcomePage = readPageTmpl('welcome.html')
if 'upload' in fieldData:
    fileitem = fieldData['filename']
    if fileitem is not None and fileitem.filename:
        filename = os.path.basename(fileitem.filename)
        open('/tmp/' + filename, 'wb').write(fileitem.file.read())
        message = 'The file "' + filename + '" was uploaded successfully'
    else:
        message = 'No file was uploaded'
else:
    message = ''
print "Content-Type:text/html\n"
print welcomePage.replace('ErrorMsg', message)
