# -*- coding: utf-8 -*-

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

class Menu:
    def __init__(self,depth=1):
        self.generators = ()
        self.depth = depth

    def addgenerator(self,gen,offset=0):
        if type(gen) == str:
            gen = my_import(gen).generator
        gen.offset = offset
        self.generators += (gen,)

    def node(self,path):
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
