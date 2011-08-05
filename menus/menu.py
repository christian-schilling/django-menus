# -*- coding: utf-8 -*-

class Menu(object):
    """
    This is the interface class every menu is
    required to implement.
    For most menus it should be sufficent to implement
    the "node" and "children" methods, as the "parent" implementation
    just depends on "node" and thus should work just automaticly.
    """

    def node(self,path):
        """
        This should return a Node instance corresponding to
        the given path. If no node is found "False" should be returned
        and no exceptions should ever be raised.
        """
        return False

    def children(self,path):
        """
        This should return a tuple containing Node instances
        corresponding to all nodes that could have a parent with "path".
        No checking needs to be done, verifing that a node corresponding to
        "path" itself exists.
        If no children are found an empty tuple should be retured and no exceptions
        should ever be raised.
        """
        return ()

    def parent(self,path):
        """
        This should return a Node instance refering to the node
        that would be the parent of a node with the given path, even if the node
        with that given path does not exist.
        The default implementation should do the job in most cases so this
        method will rarly -if ever- be needed to be overwritten.
        """
        if path == "/": return None
        return self.node(path.rstrip("/").rsplit("/",1)[0] + "/")

class SimpleMenu(Menu):
    """
    This implements the Menu interface by storing
    the menu in a python dictonary.

    The dict keys are the paths and the values are tuples containing
    data to build Node instances from.
    The Node instances are created on-demand and are not
    permanently stored.
    """
    nodes = []

    def __init__(self):
        self.nodes_dict = dict([(n.path,n) for n in self.nodes])

    def addnode(self,node):
        self.nodes_dict[node.path] = node

    def node(self,path):
        if self.nodes_dict.has_key(path):
            return self.nodes_dict[path]

    def children(self,path):
        return (n for n in self.nodes_dict.values() if n.parentpath == path)
