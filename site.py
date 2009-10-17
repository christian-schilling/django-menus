# -*- coding: utf-8 -*-

class MenuSite(object):
    """
    This class is the high-level interface of the menus application.
    Is is used in places where the menu should be rendered (by the templatetags).
    It holds a list of references to Menu instances and its interface methods
    just "merge" the results of the corresponding Menu method together.
    """
    menus = []
    def __init__(self):
        """
        Just initializes self.menus as an empty tuple.
        """
        tmp = self.menus
        self.menus = []
        for menu in tmp:
            if isinstance(menu,tuple):
                self.register(*menu)
            else:
                self.register(menu)

    def register(self,menuclass,offset=0):
        """
        Adds a Menu instance "menu" to the references list.
        "offset" is a value that is to be added to the position of every Node
        of the menu before sorting them.
        """
        self.menus.append((menuclass(),offset))

    def setoffset(self,menuclass,newoffset):
        self.menus = [(obj,offset) if not isinstance(obj,menuclass) else (obj,newoffset)
                        for (obj,offset) in self.menus]

    def node(self,path):
        """
        Finds the Node for a given path by asking all
        Menu instances.
        If multiple menus have a node for the given path the
        fist match is returned.
        """
        for menu,offset in self.menus:
            n = menu.node(path)
            if n: return n

    def parent(self,path):
        """
        Finds the Node beeing the parent of the node
        at the given path.
        This succedes even if no node exists with the given path, as
        long as a node could be the parent of the (nonexistent) node.
        If multiple menus have a node for the given path the
        fist match is returned.
        """
        for menu,offset in self.menus:
            n = menu.parent(path)
            if n: return n

    def children(self,path):
        """
        Builds a list of all Node instances having a parent with the given path.
        The list is build by gathering the nodes from all menus and
        sorting them by position afterwards.
        """
        c = []
        for menu,offset in self.menus:
            c += [(node,node.position+offset) for node in menu.children(path)]
        c.sort(lambda x,y:-1 if x[0].path < y[0].path else 1)
        c.sort(lambda x,y:x[1]-y[1])
        return [x[0] for x in c]

