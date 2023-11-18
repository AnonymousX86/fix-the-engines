# -*- coding: utf-8 -*-
from os import getenv

from FTE.chapters import chapter_one
from FTE.menus import main_menu


if __name__ == '__main__':
    if not bool(getenv('DEBUG', False)):
        main_menu()
    chapter_one()
