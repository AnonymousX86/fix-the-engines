# -*- coding: utf-8 -*-
from enum import IntEnum
from time import sleep

from rich.style import Style
from rich.text import Text

from FTE.console import console
from FTE.locations import Location
from FTE.settings import DEBUG


class Standing(IntEnum):
    GOOD = 10
    NEUTRAL = 0
    BAD = -10


class Character:
    def __init__(
        self,
        name: str,
        location: Location,
        *,
        poke: str = None,
        standing: Standing = None,
        known: bool = True
    ) -> None:
        self.name: str = name
        self.location: Location = location
        self.poke: str = poke or ''
        self.standing: Standing = standing or Standing.NEUTRAL
        self.known: bool = known

    def __eq__(self, other) -> True:
        if isinstance(other, Character):
            return self.name == other.name
        return False

    @property
    def display_name(self) -> Text:
        return Text.assemble(
            self.name if self.known else '???',
            style=Style(
                bold=True,
                color=standing_color(self.standing)
            )
        )

    @property
    def pokable(self) -> bool:
        return bool(self.poke)

    def monologue(self, text: str | Text) -> None:
        console.print(Text.assemble('[ ', self.display_name, ' ] ', '"', text, '"'))
        sleep(0.0 if DEBUG else 1.5)

    def dialogue(self, text: str | Text) -> str:
        self.monologue(text)
        return console.input('> ').lower()

    def action(self, text: str | Text) -> None:
        console.print(Text.assemble(
            '[ ', self.display_name, ' ] ',
            Text.assemble('*', text, '*', style=Style(italic=True))
        ))
        sleep(0.0 if DEBUG else 1.5)


def standing_color(standing: Standing) -> str:
    if standing >= Standing.GOOD:
        return 'green4'
    if standing <= Standing.BAD:
        return 'red3'
    return 'sky_blue3'
