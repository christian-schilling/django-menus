# -*- coding: utf-8 -*-

class Menu:
    def __init__(self):
        self.generators = []

    def addgenerator(self,gen):
        self.generators += [gen]

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
        return c

    def branch(self,path):
        li = [p for p in path.split('/') if p]
        return ['/']+['/'+'/'.join(li[:c])+'/' for c in range(1,len(li)+1)]
