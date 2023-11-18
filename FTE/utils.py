# -*- coding: utf-8 -*-
from time import sleep

from rich.text import Text

from FTE.console import console
from FTE.settings import DEBUG


def print_with_interval(text: str, interval: float, end: str = '\n') -> None:
    for char in text:
        if not DEBUG:
            sleep(interval)
        console.print(char, end='')
    if not DEBUG:
        sleep(interval)
    console.print('', end=end)


def slow_print(text: str, end: str = '\n') -> None:
    print_with_interval(text, 0.1, end)


def slower_print(text: str, end: str = '\n') -> None:
    print_with_interval(text, 0.5, end)


def story(text: str | Text | list[str | Text]) -> None:
    if isinstance(text, list):
        for seg in text:
            console.print(seg)
            if not DEBUG:
                sleep(5.0)
    else:
        console.print(text)
