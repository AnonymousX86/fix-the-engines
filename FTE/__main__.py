# -*- coding: utf-8 -*-
"""
Fix The Engines is a paragraph game written purely in Python with only one library.
"""
from FTE.chapters import chapter_one
from FTE.menus import main_menu
from FTE.settings import DEBUG


if __name__ == '__main__':
    if not DEBUG:
        main_menu()
    chapter_one()
