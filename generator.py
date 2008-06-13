# -*- coding: utf-8 -*-
import re
from util.menus import MenuNode

class MenuGenerator:

    def node(self,path):
        return False

    def children(self,path):
        return ()
        
    def parent(self,path):
        return self.node(MenuNode(path).parentpath)

class SimpleMenuGenerator(MenuGenerator):

    def __init__(self):
        self.nodes = {}
        self.offset = 0

    def additem(self,path,name,title=False,in_menu=True,position=0):
        self.nodes[path] = (path,name,title,in_menu,position) 

    def node(self,path):
        if self.nodes.has_key(path):
            n = self.nodes[path]
            return MenuNode(position=n[4]+self.offset,*n[:-1])

    def children(self,path):
        return (MenuNode(position=n[4]+self.offset,*n[:-1])
                     for key,n in self.nodes.iteritems()
                     if re.match(r'^'+path+r'[\w-]+/?$',key))

