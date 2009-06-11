from menus.menu import *
from menus.node import *
from menus.generator import *

site_menu = Menu()
tmp_generator = SimpleMenuGenerator()
site_menu.addgenerator(tmp_generator)

def autodiscover():
    import imp
    from django.conf import settings
    from django.utils.importlib import import_module

    for app in settings.INSTALLED_APPS:
        try:
            app_path = import_module(app).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('menu', app_path)
        except ImportError:
            continue

        import_module("%s.menu" % app)
