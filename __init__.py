from util.menus.menu import *
from util.menus.node import *
from util.menus.generator import *

main_menu = Menu(depth=2)
main_generator = SimpleMenuGenerator()
main_menu.addgenerator(main_generator)
main_generator.additem('/','Home','Home')
