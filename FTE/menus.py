# -*- coding: utf-8 -*-
"""
Displays menu's. Currently only main menu to start or exit the game.
"""
from rich.style import Style

from time import sleep

from FTE.console import console


def main_menu() -> None:
    """Displays main menu."""
    while True:
        console.clear()
        console.rule('Main menu')
        console.print('''
\u00a0_____  ____  __ __      ______  __ __    ___        ___  ____    ____  ____  ____     ___  _____
|     ||    ||  |  |    |      ||  |  |  /  _]      /  _]|    \  /    ||    ||    \   /  _]/ ___/
|   __| |  | |  |  |    |      ||  |  | /  [_      /  [_ |  _  ||   __| |  | |  _  | /  [_(   \_
|  |_   |  | |_   _|    |_|  |_||  _  ||    _]    |    _]|  |  ||  |  | |  | |  |  ||    _]\__  |
|   _]  |  | |     |      |  |  |  |  ||   [_     |   [_ |  |  ||  |_ | |  | |  |  ||   [_ /  \ |
|  |    |  | |  |  |      |  |  |  |  ||     |    |     ||  |  ||     | |  | |  |  ||     |\    |
|__|   |____||__|__|      |__|  |__|__||_____|    |_____||__|__||___,_||____||__|__||_____| \___|
''',
            justify='center',
            style=Style(
                bold=True
        ))
        console.print('1. Let\'s fix them!')
        console.print('2. Maybe later...')
        console.print('')
        choice = console.input('Your choice? ')
        if choice == '1':
            break
        elif choice == '2':
            console.print(':wave: Goodbye!')
            sleep(3.0)
            exit()
