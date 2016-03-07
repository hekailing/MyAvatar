#!/user/bin/python
import hashlib

def _genFileMd5(f):
    '''
    Generate md5sum of a file.  
    Each time read 8096 Bytes from the file, then update md5sum.
    '''
    def read_chunks(fh):
        saved_fp = fh.tell()
        chunk = fh.read(8096)
        while chunk:
            yield chunk
            chunk = fh.read(8096)
        else:
            fh.seek(saved_fp)
    md5obj = hashlib.md5()
    for chunk in read_chunks(f):
        md5obj.update(chunk)
    return md5obj.hexdigest()
        

def genMd5(obj):
    '''
    Generate md5 of an object.  The object can be string or file
    '''
    if isinstance(obj, file):
        return _genFileMd5(obj)
    elif getattr(obj, '__hash__'):
        md5obj = hashlib.md5()
        md5obj.update(obj)
        return md5obj.hexdigest()
    else:
        return None


def genSha256(obj):
    '''
    Generate sha256 of an object.  The object can only be a string
    '''
    if getattr(obj, '__hash__'):
        sha256obj = hashlib.sha256()
        sha256obj.update(obj)
        return sha256obj.hexdigest()
    else:
        return None

if __name__ == '__main__':
    import os
    str = 'hello'
    aList = []
    print 'md5 of "hello" is:', genMd5(str)
    print 'md5 of a list is:', genMd5(aList)
    print 'sha256 of "hello" is:', genSha256(str)
    print 'sha256 of a list is:', genSha256(aList)
    testFileName = '/tmp/genhash.genFileMd5.small'
    with open(testFileName, 'w+') as fw:
        fw.write(str)
    with open(testFileName, 'r') as fr:
        print 'md5 of file(%s) is:' % testFileName, genMd5(fr)
        print 'file(%s) read point is at' % testFileName, fr.tell()
    os.remove(testFileName)
    testFileName = '/tmp/genhash.genFileMd5.big'
    with open(testFileName, 'w+') as fw:
        fw.seek(1024*1024)
        fw.write('hello')
    with open(testFileName, 'r') as fr:
        print 'md5 of file(%s) is:' % testFileName, genMd5(fr)
        print 'file(%s) read point is at' % testFileName, fr.tell()
    os.remove(testFileName)
    
    
