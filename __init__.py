from menus.menu import *
from menus.node import *
from menus.generator import *

main_menu = Menu(depth=2)
main_generator = SimpleMenuGenerator()
main_menu.addgenerator(main_generator)
main_generator.additem('/','Home','Home')

tmp_generator = main_generator
