#!/usr/bin/python
# encoding=utf-8
import os
import string
import random
# ensure import MySQLdb success
os.environ.setdefault("PYTHON_EGG_CACHE", "/tmp/.python-eggs")
import MySQLdb

import genhash


_mysqlAddr = 'localhost'
_mysqlUser = 'root'
_rootPassword = '123456789'
_avatardb = 'avatar_test'


def execQuery(query, param=None, fetch=False):
    '''
    Open MySQLdb and execute the query.  Fetch result if necessary.  
    Close cursor and database at last.  
    Return False if execution failed, otherwise True or fetchdata.
    This function only tested with 'select', 'insert', 'update'
    '''
    db = MySQLdb.connect(_mysqlAddr, _mysqlUser, _rootPassword, _avatardb, charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute(query, param)
    except MySQLdb.IntegrityError:
        data = False
    else:
        data = cursor.fetchone() if fetch else db.commit() is None
    cursor.close()
    db.close()
    return data


def accountCheck(username, password):
    '''
    Check user authority
    return: error message.
    '''
    if username and password:
        sql = 'SELECT password, salt FROM user_info WHERE username=%s'
        ret = execQuery(sql, (username,), True)
        if isinstance(ret, tuple):
            saltedPassword, salt = ret
            return saltedPassword == genhash.genSha256(salt+password)
        else:
            return False
    else:
        return False


def usernameExist(username):
    if username:
        sql = 'SELECT * FROM user_info WHERE username=%s'
        return execQuery(sql, (username,), True) is not None
    else:
        return False


def emailExist(email):
    if email:
        sql = 'SELECT * FROM email2user WHERE email=%s'
        return execQuery(sql, (email,), True) is not None
    else:
        return False


def getEmailFromUserName(username):
    if username:
        sql = 'SELECT email FROM user_info WHERE username=%s'
        results = execQuery(sql, (username,), True)
        return results[0] if results else None


def insertAccount(username, password, email):
    '''
    Insert an account into database.  The function includes two steps:
    1. insert a record into user_info(username, password, salt, email)
    2. insert a record into email2user(email, username)
    These two step should in a transaction, so DO NOT call execQuery seperatedly
    '''
    digitalpha = string.digits + string.lowercase
    salt = ''.join([random.choice(digitalpha) for i in range(64)])
    saltedPassword = genhash.genSha256(salt+password)
    db = MySQLdb.connect('localhost', 'root', _rootPassword, _avatardb, charset='utf8')
    cursor = db.cursor()
    insertUserSql = ('INSERT INTO user_info (username, password, salt, email) '
                     'VALUES (%s, %s, %s, %s)')
    insertEmailSql = 'INSERT INTO email2user (email, username) VALUES (%s, %s)'
    try:
        cursor.execute(insertUserSql, (username, saltedPassword, salt, email))
        cursor.execute(insertEmailSql, (email, username))
    except MySQLdb.IntegrityError:
        ret = False
    else:
         db.commit()
         ret = True
    cursor.close()
    db.close()
    return ret

        
def main():
    # userinfo
    username = 'hekai'
    password = '123456'
    email = 'hekai@163.com'
    # clear the user_info
    execQuery('DELETE FROM user_info')
    execQuery('DELETE FROM email2user')
    insertAccount(username, password, email)
    if usernameExist(username):
        print '[OK] username(%s) exist' % username
    else:
        print '[FAILED] username(%s) not exist' % username
    if not usernameExist('unexistedUsername'):
        print '[OK] username(unexistedUsername) not exist'
    else:
        print '[FAILED] username(unexistedUsername) exist'
    if emailExist(email):
        print '[OK] email(%s) exist' % email
    else:
        print '[FAILED] email(%s) not exist' % email
    if not emailExist('unexistedEmail@163.com'):
        print '[OK] email(unexistedEmail@163.com) not exist'
    else:
        print '[FAILED] email(unexistedEmail@163.com) exist'
    if accountCheck(username, password):
        print '[OK] accountCheck success'
    else:
        print '[FAILED] accountCheck failure'
    if not accountCheck(username, 'wrong password'):
        print '[OK] wrong password failure'
    else:
        print '[FAILED] wrong password passed'
    if not accountCheck('unexistUsername', password):
        print '[OK] unexistUsername failure'
    else:
        print '[FAILED] unexistUsername passed'


if __name__ == '__main__':
    main()
