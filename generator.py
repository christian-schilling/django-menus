# -*- coding: utf-8 -*-
import re
from menus import MenuNode

class MenuGenerator:
    """
    This is the interface class every menu generator is
    required to implement.
    For most generators it should be sufficent to implement
    the "node" and "children" methods, as the "parent" implementation
    just depends on "node" and thus should work just automaticly.
    """

    def node(self,path):
        """
        This should return a MenuNode instance corresponding to
        the given path. If no node is found "False" should be returned
        and no exceptions should ever be raised.
        """
        return False

    def children(self,path):
        """
        This should return a tuple containing MenuNode instances
        corresponding to all nodes that could have a parent with "path".
        No checking needs to be done, verifing that a node corresponding to
        "path" itself exists.
        If no children are found an empty tuple should be retured and no exceptions
        should ever be raised.
        """
        return ()
        
    def parent(self,path):
        """
        This should return a MenuNode instance refering to the node
        that would be the parent of a node with the given path, even if the node
        with that given path does not exist.
        The default implementation should do the job in most cases so this
        method will rarly -if ever- be needed to be overwritten.
        """
        return self.node(MenuNode(path).parentpath)

class SimpleMenuGenerator(MenuGenerator):
    """
    This implements the MenuGenerator interface by storing
    the menu in a python dictonary.

    The dict keys are the paths and the values are tuples containing
    data to build MenuNode instances from.
    The MenuNode instances are created on-demand and are not
    permanently stored.
    """
    nodes = []
    offset = 0

    def __init__(self):
        self.nodes_dict = dict([(n.path,n) for n in self.nodes])

    def additem(self,path,name,title=False,in_menu=True,position=0):
        self.nodes_dict[path] = (path,name,title,in_menu,position) 

    def node(self,path):
        if self.nodes_dict.has_key(path):
            n = self.nodes_dict[path]
            if isinstance(n,MenuNode):
                return n
            return MenuNode(position=n[4]+self.offset,*n[:-1])

    def children(self,path):
        return (self.node(key)
                    for key,n in self.nodes_dict.iteritems()
                    if re.match(r'^'+path+r'[\w-]+/?$',key))

