# -*- coding: utf-8 -*-
from rich.style import Style
from rich.text import Text


class Location:
    def __init__(
            self,
            name: str,
            *,
            known: bool = True
    ) -> None:
        self.name: str = name
        self.known: bool = known

    @property
    def display_name(self) -> Text:
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
