# -*- coding: utf-8 -*-

def my_import(name):
    """
    This is taken directly from the Python documentation.
    It is a thin wrapper around the buildin __import__
    function that that returns "eggs" instead of "span" when
    importing "spam.eggs"
    """
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

class Menu:
    """
    This class is the high-level interface of the menugen application.
    Is is used in places where the menu should be rendered (by the templatetags).
    It holds a list of references to MenuGenerator instances and its interface methods
    just "merge" the results of the corresponding MenuGenerator method together.
    """
    def __init__(self,depth=1):
        """
        Just initializes self.generators as an empty tuple.
        May take "depth" with is the number of levels of menu hierarchy
        that should be shown when the menu is rendered.
        """
        self.generators = ()
        self.depth = depth

    def addgenerator(self,gen,offset=0):
        """
        Adds a MenuGenerator instance "gen" to the references list.
        If "gen" is a already initialized instance of MenuGenerator, it is
        is added directly.
        If it is a string, the module specified in it is imported and the contained
        instance is added. The module specified should contain such an instance
        just named "generator"
        "offset" is a value that is to be added to the position of every MenuNode
        of the generator before sorting them.
        """
        if type(gen) == str:
            gen = my_import(gen).generator
        gen.offset = offset
        self.generators += (gen,)

    def node(self,path):
        """

        """
        for gen in self.generators:
            n = gen.node(path)
            if n: return n

    def parent(self,path):
        for gen in self.generators:
            n = gen.parent(path)
            if n: return n

    def children(self,path):
        c = []
        for gen in self.generators:
            c += gen.children(path)
        c.sort(lambda x,y:x.position-y.position)
        return c

    def branch(self,path):
        li = tuple(p for p in path.split('/') if p)
        return ('/',)+tuple('/'+'/'.join(li[:c])+'/' for c in range(1,len(li)+1))
