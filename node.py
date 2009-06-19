# -*- coding: utf-8 -*-

from menus import helpers

class Node:
    def __init__(self,path,name,position=0,**kwargs):
        self.path = path

        if path == "/":
            self.parentpath = None
        else:
            self.parentpath = path.rstrip("/").rsplit("/",1)[0] + "/"

        self.position = position
        self.name = name
        self.options = kwargs
        self.branch = helpers.branch(path)
