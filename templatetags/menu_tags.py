# -*- coding: utf-8 -*-
from django import template
from menus import MenuNode,main_menu
from copy import copy

register = template.Library()

@register.inclusion_tag('menus/menu.html',takes_context=True)
def menu(context):
    curpath = context['request'].path
    pathstart = MenuNode(curpath).pathstart
    context.update({'nodes':(x for x in main_menu.children(pathstart)
                            if x.in_menu)})
    return context

@register.inclusion_tag('menus/node.html',takes_context=True)
def node(context,n,depth=1):
    context = copy(context)
    curpath = context['request'].path
    branch = main_menu.branch(curpath)
    n.open = n.active = n.path in branch
    if not n.open or depth >= main_menu.depth:
        context.update({'children':()})
    else:
        children = tuple(x for x in main_menu.children(n.path) if x.in_menu)
        for c in children:
            n.active &= (c.path not in branch)
        context.update({'children':children})
    context.update({'node':n,'depth':depth+1})
    return context

@register.inclusion_tag('menus/breadcrumbs.html',takes_context=True)
def breadcrumbs(context):
    curpath = context['request'].path
    branchnodes = (main_menu.node(x) or MenuNode(x)
                   for x in main_menu.branch(curpath)[1:])
    context.update({'branch':branchnodes,})
    return context

@register.inclusion_tag('menus/tabbar.html',takes_context=True)
def tabbar(context):
    curpath = context['request'].path
    nodes = tuple(x for x in main_menu.children('/') if x.in_menu)
    pathstart = MenuNode(curpath).pathstart
    for node in nodes:
        node.active = node.path == pathstart
    context.update({'nodes':nodes})
    return context

@register.inclusion_tag('menus/contents.html',takes_context=True)
def contents(context):
    curpath = context['request'].path
    branch = main_menu.branch(curpath)
    for x in reversed(branch):
        node = main_menu.node(x)
        if node and node.show_contents:
            context.update({'rootnode':node,'nodes':main_menu.children(x)})
            break
    return context

