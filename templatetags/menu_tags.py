# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
import menus

register = template.Library()

def parse_ttag(token):
    """
    allows for easy parsing of templatetag options.
    see: http://ericholscher.com/blog/2008/nov/8/problem-django-template-tags/
    """
    bits = token.split_contents()
    tags = {}
    possible_tags = ['from', 'limit', 'template',]
    for index, bit in enumerate(bits):
        if bit.strip() in possible_tags:
            tags[bit.strip()] = bits[index+1]
    return tags

def render_menu_node(path,branch,limit,template_name,nodecontext):
    children = menus.site.children(path)
    nodecontext.update({
        'node':menus.site.node(path),
        'classes':'open active' if path in branch[-1:] else 'open' if path in branch else '',
        'children':{
            'all':
                (render_menu_node(n.path,branch,limit-1,template_name,nodecontext) for n in children)
                    if children and limit > 0 else [],
            'all_of_current':
                (render_menu_node(n.path,branch,limit-1,template_name,nodecontext) for n in children)
                    if children and limit > 0 and path in branch else [],
            'only_current':
                (render_menu_node(n.path,branch,limit-1,template_name,nodecontext) for n in children
                    if children and n.path in branch) if limit > 0 else [],
            'nodes': children if limit > 0 else [],
        }
    })
    return template.loader.render_to_string(template_name,nodecontext)

class MenuTagNode(template.Node):
    def __init__(self,options):
        self.start_path = template.Variable(options.pop('from','0'))
        self.limit = template.Variable(options.pop('limit','9999'))
        self.template = template.Variable(options.pop('template','"menus/full.html"'))

    def render(self,context):
        branch = menus.helpers.branch(context['request'].path)

        start_path = self.start_path.resolve(context)
        if isinstance(start_path,int):
            start_index = start_path
            start_path = branch[start_path]
        else:
            start_index = len(menus.helpers.branch(start_path))-1

        limit = self.limit.resolve(context)
        template = self.template.resolve(context)

        return render_menu_node(start_path,branch[start_index:start_index+limit+1],limit,template,context)

@register.tag('menu')
def do_menu_node(parser,token):
    return MenuTagNode(parse_ttag(token))

