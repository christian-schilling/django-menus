from django.test import TestCase

from menus.menu import SimpleMenu
from menus.node import Node
import menus

class TestMenu(SimpleMenu):
    nodes = [
        Node("/","Rootnode",position=0,some="additional",options=1),
        Node("/first1/","First1"),
        Node("/first2/","First2"),
        Node("/first3/","First3"),
        Node("/first1/second1/","First1Second1"),
        Node("/first1/second2/","First1Second2"),
        Node("/first1/second1/third1/","First1Second1Third1"),
    ]

class MenuTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_node(self):

        n = Node("/","Rootnode",position=0,some="additional",options=1)
        self.assertEqual(n.path,"/")
        self.assertEqual(n.parentpath,None)
        self.assertEqual(n.name,"Rootnode")
        self.assertEqual(n.branch,("/",))
        self.assertEqual(n.position,0)
        self.assertEqual(n.options,{
            "some":"additional",
            "options":1,
        })

        n = Node("/first/","First")
        self.assertEqual(n.path,"/first/")
        self.assertEqual(n.parentpath,"/")
        self.assertEqual(n.branch,("/","/first/"))

        n = Node("/first/second/","Second")
        self.assertEqual(n.path,"/first/second/")
        self.assertEqual(n.parentpath,"/first/")
        self.assertEqual(n.branch,("/","/first/","/first/second/"))

        n = Node("/first/second/third/","Third")
        self.assertEqual(n.path,"/first/second/third/")
        self.assertEqual(n.parentpath,"/first/second/")
        self.assertEqual(n.branch,("/","/first/","/first/second/","/first/second/third/"))

    def test_simple_menu(self):
        from menus.node import Node

        test_menu = TestMenu()
        self.assertEqual(test_menu.node("/").name,"Rootnode")
        self.assertEqual(test_menu.node("/first1/").name,"First1")
        self.assertEqual(test_menu.node("/first2/").name,"First2")
        self.assertEqual(test_menu.node("/first3/").name,"First3")
        self.assertEqual(test_menu.node("/first1/second1/").name,"First1Second1")
        self.assertEqual(test_menu.node("/first1/second2/").name,"First1Second2")
        self.assertEqual(test_menu.node("/first1/second1/third1/").name,"First1Second1Third1")

        self.assertEqual(test_menu.parent("/"),None)
        self.assertEqual(test_menu.parent("/first1/").name,"Rootnode")
        self.assertEqual(test_menu.parent("/first2/").name,"Rootnode")
        self.assertEqual(test_menu.parent("/first3/").name,"Rootnode")
        self.assertEqual(test_menu.parent("/first1/second1/").name,"First1")
        self.assertEqual(test_menu.parent("/first1/second2/").name,"First1")
        self.assertEqual(test_menu.parent("/first1/second1/third1/").name,"First1Second1")

        self.assertEqual(set(x.name for x in test_menu.children("/")),
            set(("First1","First2","First3"))
        )
        self.assertEqual(set(x.name for x in test_menu.children("/first1/")),
            set(("First1Second1","First1Second2"))
        )
        self.assertEqual(tuple(x.name for x in test_menu.children("/first2/")),())
        self.assertEqual(set(x.name for x in test_menu.children("/first3/")), set(()))
        self.assertEqual(set(x.name for x in test_menu.children("/first1/second1/")),
            set(["First1Second1Third1"])
        )
        self.assertEqual(tuple(x.name for x in test_menu.children("/first1/second2/")),())
        self.assertEqual(tuple(x.name for x in test_menu.children("/first1/second1/third1")),())

    def test_site(self):
        from menus.menu import SimpleMenu
        from menus.node import Node
        from menus.site import MenuSite
        site = MenuSite()
        site.register(TestMenu)
        self.assertEqual(site.menus[0][1],0)
        site.setoffset(TestMenu,1)
        self.assertEqual(site.menus[0][1],1)

        self.assertEqual(site.node("/").name,"Rootnode")
        self.assertEqual(site.node("/first1/").name,"First1")
        self.assertEqual(site.node("/first2/").name,"First2")
        self.assertEqual(site.node("/first3/").name,"First3")
        self.assertEqual(site.node("/first1/second1/").name,"First1Second1")
        self.assertEqual(site.node("/first1/second2/").name,"First1Second2")
        self.assertEqual(site.node("/first1/second1/third1/").name,"First1Second1Third1")

        self.assertEqual(site.parent("/"),None)
        self.assertEqual(site.parent("/first1/").name,"Rootnode")
        self.assertEqual(site.parent("/first2/").name,"Rootnode")
        self.assertEqual(site.parent("/first3/").name,"Rootnode")
        self.assertEqual(site.parent("/first1/second1/").name,"First1")
        self.assertEqual(site.parent("/first1/second2/").name,"First1")
        self.assertEqual(site.parent("/first1/second1/third1/").name,"First1Second1")

        self.assertEqual(tuple(x.name for x in site.children("/")),
            ("First1","First2","First3")
        )
        self.assertEqual(tuple(x.name for x in site.children("/first1/")),
            ("First1Second1","First1Second2")
        )
        self.assertEqual(tuple(x.name for x in site.children("/first2/")),())
        self.assertEqual(tuple(x.name for x in site.children("/first3/")), ())
        self.assertEqual(tuple(x.name for x in site.children("/first1/second1/")),
            ("First1Second1Third1",)
        )
        self.assertEqual(tuple(x.name for x in site.children("/first1/second2/")),())
        self.assertEqual(tuple(x.name for x in site.children("/first1/second1/third1")),())

from django.template import Template, Context, add_to_builtins
add_to_builtins('menus.templatetags.menu_tags')

class MockRequest(object):
    def __init__(self,path):
        self.path = path

class Templates(TestCase):
    def setUp(self):
        self.orig_site = menus.site
        menus.site = menus.MenuSite()
        menus.site.register(TestMenu)

    def tearDown(self):
        menus.site = self.orig_site

    def test_full_menu(self):
        self.assertEqual(
            Template("{% menu %}").render(Context({'request':MockRequest("/")})),
            u'<li class="open active"><a href="/">Rootnode</a><ul><li class=""><a href="/first1/">First1</a><ul><li class=""><a href="/first1/second1/">First1Second1</a><ul><li class=""><a href="/first1/second1/third1/">First1Second1Third1</a></li></ul></li><li class=""><a href="/first1/second2/">First1Second2</a></li></ul></li><li class=""><a href="/first2/">First2</a></li><li class=""><a href="/first3/">First3</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu from '/first1/' %}").render(Context({'request':MockRequest("/first1/")})),
            u'<li class="open active"><a href="/first1/">First1</a><ul><li class=""><a href="/first1/second1/">First1Second1</a><ul><li class=""><a href="/first1/second1/third1/">First1Second1Third1</a></li></ul></li><li class=""><a href="/first1/second2/">First1Second2</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu from '/first2/' %}").render(Context({'request':MockRequest("/first1/")})),
            u'<li class=""><a href="/first2/">First2</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu from 1 %}").render(Context({'request':MockRequest("/first2/")})),
            u'<li class="open active"><a href="/first2/">First2</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu from 1 %}").render(Context({'request':MockRequest("/first1/second1/third1/")})),
            u'<li class="open"><a href="/first1/">First1</a><ul><li class="open"><a href="/first1/second1/">First1Second1</a><ul><li class="open active"><a href="/first1/second1/third1/">First1Second1Third1</a></li></ul></li><li class=""><a href="/first1/second2/">First1Second2</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu limit 2 %}").render(Context({'request':MockRequest("/")})),
            u'<li class="open active"><a href="/">Rootnode</a><ul><li class=""><a href="/first1/">First1</a><ul><li class=""><a href="/first1/second1/">First1Second1</a></li><li class=""><a href="/first1/second2/">First1Second2</a></li></ul></li><li class=""><a href="/first2/">First2</a></li><li class=""><a href="/first3/">First3</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu from 0 limit 2 %}").render(Context({'request':MockRequest("/first1/second1/third1/")})),
            u'<li class="open"><a href="/">Rootnode</a><ul><li class="open"><a href="/first1/">First1</a><ul><li class="open active"><a href="/first1/second1/">First1Second1</a></li><li class=""><a href="/first1/second2/">First1Second2</a></li></ul></li><li class=""><a href="/first2/">First2</a></li><li class=""><a href="/first3/">First3</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu limit 2 from '/first1/' %}").render(Context({'request':MockRequest("/first1/")})),
            u'<li class="open active"><a href="/first1/">First1</a><ul><li class=""><a href="/first1/second1/">First1Second1</a><ul><li class=""><a href="/first1/second1/third1/">First1Second1Third1</a></li></ul></li><li class=""><a href="/first1/second2/">First1Second2</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu limit 2 from '/first2/' %}").render(Context({'request':MockRequest("/first1/")})),
            u'<li class=""><a href="/first2/">First2</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu limit 2 from 1 %}").render(Context({'request':MockRequest("/first2/")})),
            u'<li class="open active"><a href="/first2/">First2</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu limit 2 from 1 %}").render(Context({'request':MockRequest("/first1/second1/third1/")})),
            u'<li class="open"><a href="/first1/">First1</a><ul><li class="open"><a href="/first1/second1/">First1Second1</a><ul><li class="open active"><a href="/first1/second1/third1/">First1Second1Third1</a></li></ul></li><li class=""><a href="/first1/second2/">First1Second2</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu limit 0 %}").render(Context({'request':MockRequest("/")})),
            u'<li class="open active"><a href="/">Rootnode</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu limit 1 %}").render(Context({'request':MockRequest("/")})),
            u'<li class="open active"><a href="/">Rootnode</a><ul><li class=""><a href="/first1/">First1</a></li><li class=""><a href="/first2/">First2</a></li><li class=""><a href="/first3/">First3</a></li></ul></li>\n'
        )

    def test_dynamic_menu(self):
        self.assertEqual(
            Template("{% menu template 'menus/dynamic.html' %}").render(Context({'request':MockRequest("/")})),
            u'<li class="open active"><a href="/">Rootnode</a><ul><li class=""><a href="/first1/">First1</a></li><li class=""><a href="/first2/">First2</a></li><li class=""><a href="/first3/">First3</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/dynamic.html' from '/first1/' %}").render(Context({'request':MockRequest("/first1/")})),
            u'<li class="open active"><a href="/first1/">First1</a><ul><li class=""><a href="/first1/second1/">First1Second1</a></li><li class=""><a href="/first1/second2/">First1Second2</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/dynamic.html' from '/first2/' %}").render(Context({'request':MockRequest("/first1/")})),
            u'<li class=""><a href="/first2/">First2</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/dynamic.html' from 1 %}").render(Context({'request':MockRequest("/first2/")})),
            u'<li class="open active"><a href="/first2/">First2</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/dynamic.html' from 1 %}").render(Context({'request':MockRequest("/first1/second1/third1/")})),
            u'<li class="open"><a href="/first1/">First1</a><ul><li class="open"><a href="/first1/second1/">First1Second1</a><ul><li class="open active"><a href="/first1/second1/third1/">First1Second1Third1</a></li></ul></li><li class=""><a href="/first1/second2/">First1Second2</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/dynamic.html' limit 2 %}").render(Context({'request':MockRequest("/")})),
            u'<li class="open active"><a href="/">Rootnode</a><ul><li class=""><a href="/first1/">First1</a></li><li class=""><a href="/first2/">First2</a></li><li class=""><a href="/first3/">First3</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/dynamic.html' limit 2 from '/first1/' %}").render(Context({'request':MockRequest("/first1/")})),
            u'<li class="open active"><a href="/first1/">First1</a><ul><li class=""><a href="/first1/second1/">First1Second1</a></li><li class=""><a href="/first1/second2/">First1Second2</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/dynamic.html' limit 2 from '/first2/' %}").render(Context({'request':MockRequest("/first1/")})),
            u'<li class=""><a href="/first2/">First2</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/dynamic.html' limit 2 from 1 %}").render(Context({'request':MockRequest("/first2/")})),
            u'<li class="open active"><a href="/first2/">First2</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/dynamic.html' limit 2 from 1 %}").render(Context({'request':MockRequest("/first1/second1/third1/")})),
            u'<li class="open"><a href="/first1/">First1</a><ul><li class="open"><a href="/first1/second1/">First1Second1</a><ul><li class="open active"><a href="/first1/second1/third1/">First1Second1Third1</a></li></ul></li><li class=""><a href="/first1/second2/">First1Second2</a></li></ul></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/dynamic.html' limit 0 %}").render(Context({'request':MockRequest("/")})),
            u'<li class="open active"><a href="/">Rootnode</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/dynamic.html' limit 1 %}").render(Context({'request':MockRequest("/")})),
            u'<li class="open active"><a href="/">Rootnode</a><ul><li class=""><a href="/first1/">First1</a></li><li class=""><a href="/first2/">First2</a></li><li class=""><a href="/first3/">First3</a></li></ul></li>\n'
        )

    def test_breadcrumbs(self):
        self.assertEqual(
            Template("{% menu template 'menus/breadcrumbs.html' %}").render(Context({'request':MockRequest("/")})),
            u'<li class="open active"><a href="/">Rootnode</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/breadcrumbs.html' %}").render(Context({'request':MockRequest("/first1/")})),
            u'<li class="open"><a href="/">Rootnode</a></li><li class="open active"><a href="/first1/">First1</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu template 'menus/breadcrumbs.html' %}").render(Context({'request':MockRequest("/first1/second1/third1/")})),
            u'<li class="open"><a href="/">Rootnode</a></li><li class="open"><a href="/first1/">First1</a></li><li class="open"><a href="/first1/second1/">First1Second1</a></li><li class="open active"><a href="/first1/second1/third1/">First1Second1Third1</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu from 1 template 'menus/breadcrumbs.html' %}").render(Context({'request':MockRequest("/first1/second1/third1/")})),
            u'<li class="open"><a href="/first1/">First1</a></li><li class="open"><a href="/first1/second1/">First1Second1</a></li><li class="open active"><a href="/first1/second1/third1/">First1Second1Third1</a></li>\n'
        )
        self.assertEqual(
            Template("{% menu limit 2 template 'menus/breadcrumbs.html' %}").render(Context({'request':MockRequest("/first1/second1/third1/")})),
            u'<li class="open"><a href="/">Rootnode</a></li><li class="open"><a href="/first1/">First1</a></li><li class="open active"><a href="/first1/second1/">First1Second1</a></li>\n'
        )
