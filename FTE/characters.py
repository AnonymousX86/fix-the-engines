# -*- coding: utf-8 -*-
"""
Characters are NPCs, with wich the player can interact.
"""
from enum import IntEnum
from time import sleep

from rich.style import Style
from rich.text import Text

from FTE.console import console
from FTE.locations import Location
from FTE.settings import DEBUG


class Standing(IntEnum):
    """Represents relations between the player and characters."""
    GOOD = 10
    NEUTRAL = 0
    BAD = -10

    def __str__(self) -> str:
        if self >= Standing.GOOD:
            return 'Good'
        if self <= Standing.BAD:
            return 'Bad'
        return 'Neutral'

    @property
    def color(self) -> str:
        """Standing color used in :class:`rich.style.Style`."""
        if self >= Standing.GOOD:
            return 'green4'
        if self <= Standing.BAD:
            return 'red3'
        return 'sky_blue3'

    @property
    def color_text(self) -> Text:
        """Standing name with color applied."""
        return Text.assemble(str(self), style=Style(color=self.color))


class Character:
    def __init__(
        self,
        name: str,
        location: Location,
        *,
        info: str = None,
        poke: str = None,
        standing: Standing = None,
        known: bool = True
    ) -> None:
        """Represetnd a NPC character, with wich the player can interact.

        :param name: Character's name.
        :type name: :obj:`str`
        :param location: Current chracter's location.
        :type location: :class:`FTE.locations.Location`
        :param info: Detailed information baout the player should know, defaults to ``""``.
        :type info: :obj:`str`
        :param poke: What the character says, when the player want to initate dialogue, defaults to ``""``.
        :type poke: :obj:`str`
        :param standing: How character feels towards the player, defaults to `Standing.NEUTRAL`
        :type standing: :class:`FTE.characters.Standing`
        :param known: If the player knows this character.
        :type known: :obj:`bool`
        """
        self.name: str = name
        self.location: Location = location
        self.info: str = info or ''
        self.poke: str = poke or ''
        self.standing: Standing = standing or Standing.NEUTRAL
        self.known: bool = known

    def __eq__(self, other) -> True:
        if isinstance(other, Character):
            return self.name == other.name
        return False

    @property
    def display_name(self) -> Text:
        """Stylized character's name, displays ``"???"`` if character is not known."""
        return Text.assemble(
            self.name if self.known else '???',
            style=Style(
                bold=True,
                color=self.standing.color
            )
        )

    @property
    def pokable(self) -> bool:
        """If character has a poke."""
        return bool(self.poke)

    def monologue(self, text: str | Text) -> None:
        """Character talks towards the player.

        :param text: The text chracter will talk to the player.
        :type text: :obj:`str` or :class:`rich.text.Text`
        """
        console.print(Text.assemble('[ ', self.display_name, ' ] ', '"', text, '"'))
        sleep(0.0 if DEBUG else 1.5)

    def dialogue(self, text: str | Text) -> str:
        """Chracter talks towards the player and awaits a response.

        :param text: The text chracter will talk to the player.
        :type text: :obj:`str` or :class:`rich.text.Text`
        :return: Player's response.
        :rtype: :obj:`str`
        """
        self.monologue(text)
        return console.input('> ').lower()

    def action(self, text: str | Text) -> None:
        """Character interaction towards the player.

        :param text: Action description.
        :type text: :obj:`str` or :class:`rich.text.Text`
        """
        console.print(Text.assemble(
            '[ ', self.display_name, ' ] ',
            Text.assemble('*', text, '*', style=Style(italic=True))
        ))
        sleep(0.0 if DEBUG else 1.5)
