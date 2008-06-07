# -*- coding: utf-8 -*-

class MenuNode():
    def __init__(self,path='',name='',title=''):
        self.pathlist = path.strip('/').split('/')
        self.name = name
        self.title = title
    def __unicode__(self):
        return u'%s - %s' %(self.name,self.path)
    __str__ = __unicode__

    @property
    def path(self):
        path = '/'+'/'.join(self.pathlist)+'/'
        if len(path) == 2:
            path = '/'
        return path

    @property
    def parentpath(self):
        path = '/'+'/'.join(self.pathlist[:-1])+'/'
        if len(path) == 2:
            path = '/'
        return path
