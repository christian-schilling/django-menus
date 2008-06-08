# -*- coding: utf-8 -*-
import re
from util.menus import MenuNode

class MenuGenerator:
    def node(self,path):
        return False
    def children(self,path):
        return []
    def parent(self,path):
        return self.node(MenuNode(path).parentpath)

class SimpleMenuGenerator(MenuGenerator):
    def __init__(self):
        self.nodes = {}
    def additem(self,path,name,title,in_menu=True):
        self.nodes[path] = MenuNode(path,name,title,in_menu) 

    def node(self,path):
        if self.nodes.has_key(path):
            return self.nodes[path]
    def children(self,path):
        return [node for key,node in self.nodes.iteritems()
                     if re.match(r'^'+path+r'[\w-]+/?$',key)]

