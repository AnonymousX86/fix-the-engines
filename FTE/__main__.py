# -*- coding: utf-8 -*-
from FTE.chapters import chapter_one
from FTE.menus import main_menu
from FTE.settings import DEBUG


if __name__ == '__main__':
    if not DEBUG:
        main_menu()
    chapter_one()
