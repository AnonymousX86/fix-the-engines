# -*- coding: utf-8 -*-
"""
Location is an object, which stores characters. Any NPC character could be in
any location, but player must be only in a single location.
"""
from rich.style import Style
from rich.text import Text


class Location:
    """Represents a location inside the game.

    :param name: The location's name.
    :type name: :obj:`str`
    :param info: What the player should know about the loction.
    :type info: :obj:`str`
    :param known: If location is known to the player.
    :type known: :obj:`bool`
    """
    def __init__(
            self,
            name: str,
            info: str = None,
            *,
            known: bool = True
    ) -> None:
        self.name: str = name
        self.info: str = info or ''
        self.known: bool = known

    @property
    def display_name(self) -> Text:
        """Stylized location's name, or ``"???"`` if location is not known."""
        return Text.assemble(
            self.name if self.known else '???',
            style=Style(
                bold=True,
                color='magenta'
            )
        )

    def __eq__(self, other) -> bool:
        if isinstance(other, Location):
            return self.name == other.name
        return False

    def __ne__(self, other) -> bool:
        if isinstance(other, Location):
            return self.name != other.name
        return True
