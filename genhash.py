#!/user/bin/python
import hashlib

def genMd5(obj):
    if getattr(obj, '__hash__'):
        md5obj = hashlib.md5()
        md5obj.update(obj)
        return md5obj.hexdigest()
    else:
        return None


def genSha256(obj):
    if getattr(obj, '__hash__'):
        sha256obj = hashlib.sha256()
        sha256obj.update(obj)
        return sha256obj.hexdigest()
    else:
        return None

if __name__ == '__main__':
    str = 'hello'
    aList = []
    print 'md5 of "hello" is:', genMd5(str)
    print 'md5 of a list is:', genMd5(aList)
    print 'sha256 of "hello" is:', genSha256(str)
    print 'sha256 of a list is:', genSha256(aList)
