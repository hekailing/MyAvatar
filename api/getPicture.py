#! /usr/bin/python
import urllib
import urllib2
import hashlib
import binascii
import string
import shutil


_serverName = 'http://121.248.48.7'

def getPictureFormat(fh):
    hexheader = string.upper(binascii.b2a_hex(fh.read(32)))
    if hexheader.startswith('FFD8FF'):
        return 'jpg'
    elif hexheader.startswith('89504E47'):
        return 'png'
    elif hexheader.startswith('47494638'):
        return 'gif'
    elif hexheader.startswith('49492A00'):
        return 'tif'
    elif hexheader.startswith('424D'):
        return 'bmp'
    else:
        return ''

# Get your email
email = raw_input('Please imput the email:')

# construct the url
myavatar_url = _serverName + "/avatar/" + hashlib.md5(email.lower()).hexdigest()

# download the picture
pictureBuf = urllib2.urlopen(myavatar_url)
filename = email
with open(email, 'wb') as pictureFile:
    pictureFile.write(pictureBuf.read())
    with open (email, 'r') as fh:
        filename = '.'.join((email, getPictureFormat(fh)))
        print filename
    print 'Saved to "%s"' % filename
if filename != email:
    shutil.move(email, filename)

                                                        
