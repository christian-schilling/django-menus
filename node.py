# -*- coding: utf-8 -*-

class MenuNode:
    def __init__(self,path='',name='',title='',
                 in_menu=True,in_contents=True,in_index=True,
                 show_contents=False):
        self.pathlist = path.strip('/').split('/')
        self.name = name
        self.title = title
        self.active = self.open = False
        self.in_menu = in_menu
        self.in_index = in_index
        self.in_contents = in_contents
        self.show_contents = show_contents
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

    @property
    def pathstart(self):
        return '/'+self.pathlist[0]+'/'
