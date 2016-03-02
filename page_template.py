#! /usr/bin/python


def readPageTmpl(filename):
    return open('html/' + filename).read()


if __name__ == '__main__':
    print readPageTmpl('login.tmpl')
        
