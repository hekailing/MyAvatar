import sha
import shelve
import time
import Cookie
import os
import string


'''
This source code is from http://cgi.tutorial.codepoint.net/a-session-class.  
I modify a few lines of the initial code.
'''


class Session(object):

    def __init__(self, expires=None, cookie_path=None):
        '''
        When the session object is constructed, something is done as follows:
        1. Get the cookie and check whether 'sid' existed.  If 'sid' is missing,
        generate a new sid according to the system time.
        2. Open session file.  If the file don't exist, create it
        3. Set cookie expires
        '''
        string_cookie = os.environ.get('HTTP_COOKIE', '')
        self.cookie = Cookie.SimpleCookie()
        self.cookie.load(string_cookie)

        if self.cookie.get('sid'):
            sid = self.cookie['sid'].value
            # Clear session cookie from other cookies
            self.cookie.clear()
        else:
            self.cookie.clear()
            sid = sha.new(repr(time.time())).hexdigest()

        self.cookie['sid'] = sid

        if cookie_path:
            self.cookie['sid']['path'] = cookie_path

        session_dir = os.environ['DOCUMENT_ROOT'] + '/avatar/session'
        if not os.path.exists(session_dir):
            try:
                os.mkdir(session_dir, 02770)
                # If the apache user can't create it do it manualy
            except OSError, e:
                errmsg =  """
                %s when trying to create the session directory.
                Create it as '%s'
                """ % (e.strerror, session_dir)
                raise OSError, errmsg
        self.data = shelve.open(
            '%s/sess_%s' % (session_dir, sid),
            writeback=True
        )
        os.chmod('%s/sess_%s' % (session_dir, sid), 0660)
        # Initializes the expires data
        if not self.data.get('cookie'):
            self.data['cookie'] = {'expires':''}
        self.set_expires(expires)

    def close(self):
        self.data.close()

    def set_expires(self, expires=None):
        if expires == '':
            self.data['cookie']['expires'] = ''
        elif isinstance(expires, int):
            self.data['cookie']['expires'] = expires
        self.cookie['sid']['expires'] = self.data['cookie']['expires']

    def isTimeout(self):
        '''
        Check whether session is timeout.
        '''
        return self.data.has_key('lastvisit') \
            and time.time() - float(self.data['lastvisit']) >= 7*24*60*60
            
