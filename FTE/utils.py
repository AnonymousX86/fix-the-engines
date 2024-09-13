# -*- coding: utf-8 -*-
"""
Comonnly used functions between classes and chapters.
"""
from time import sleep

from rich.text import Text

from FTE.console import console
from FTE.settings import DEBUG


def print_with_interval(text: str, interval: float, end: str = '\n') -> None:
    """Displays text character by character with desired interval.

    :param text: Text to be displayed.
    :type text: :obj:`str`
    :param interval: Time between each character to be displayed.
    :type interval: :obj:`float`
    :param end: Overrides ending caracter, defaults to ``"\\n"``.
    :type end: :obj:`str`
    """
    for char in text:
        if not DEBUG:
            sleep(interval)
        console.print(char, end='')
    if not DEBUG:
        sleep(interval)
    console.print('', end=end)


def slow_print(text: str, end: str = '\n') -> None:
    """Slowly displays text character by character.

    :param text: Text to be displayed.
    :type text: :obj:`str`
    :param end: Overrides ending caracter, defaults to ``"\\n"``.
    :type end: :obj:`str`
    """
    print_with_interval(text, 0.1, end)


def slower_print(text: str, end: str = '\n') -> None:
    """Very slowly displays text character by character.

    :param text: Text to be displayed.
    :type text: :obj:`str`
    :param end: Overrides ending caracter, defaults to ``"\\n"``.
    :type end: :obj:`str`
    """
    print_with_interval(text, 0.5, end)


def story(text: list[str | Text]) -> None:
    """Displays a bunch of text in easy readible form for player.

    :param text: A text to be displayed. Could be a single text or
    :type text: :obj:`list` of :obj:`str` or :class:`rich.text.Text`
    """
    if isinstance(text, list):
        for seg in text:
            console.print(seg)
            if not DEBUG:
                sleep(5.0)
    else:
        console.print(text)
