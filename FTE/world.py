# -*- coding: utf-8 -*-
from rich.style import Style
from rich.text import Text

from FTE.console import console
from FTE.characters import Character
from FTE.locations import Location


class UnknownCommand(BaseException):
    pass


class UnknownLocation(BaseException):
    pass


class UnknownCharacter(BaseException):
    pass


class Command:
    def __init__(
            self,
            name: str,
            brief: str,
            description: str = None
    ) -> None:
        self.name: str = name
        self.brief: str = brief
        self._description: str = description

    @property
    def description(self) -> str:
        return self._description or self._brief


commands: dict[str, Command] = dict(
    exit = Command(
        'exit',
        'Exits the game.'
    ),
    help = Command(
        'help',
        'Shows help.',
        'Shows how to use specific command. What more did you expect?'
    ),
    talk = Command(
        'talk',
        'Talk to someone.',
        'Pass character name to start conversation with them.' +
        ' You can talk only to characters in your location.'
    ),
    go = Command(
        'go',
        'Go somewhere.',
        'Pass location name to go there.'
    )
)


class World:
    def __init__(
            self,
            all_locations: tuple[Location],
            all_characters: tuple[Character],
            starting_location: Location
    ) -> None:
        self._all_locations: tuple[Location] = all_locations
        self._all_characters: tuple[Character] = all_characters
        self._location: Location = starting_location

    @property
    def location(self) -> Location:
        if self._location not in self._all_locations:
            return Location('???')
        return self._location

    @property
    def characters(self) -> tuple[Character]:
        return tuple(c for c in self._all_characters if c.location.name == self._location.name)

    def _prefix(self) -> None:
        console.print(Text.assemble('[ ', self.location.display_name, ' ] '), end='')

    def find_location(self, name: str) -> Location | None:
        try:
            location = tuple(filter(
                lambda l: l.name.lower() == name.lower() and l.known,
                self._all_locations
            ))[0]
        except IndexError:
            return None
        else:
            return location

    def find_character(self, name: str) -> Character:
        return next((c for c in self._all_characters if c.name.lower() == name.lower()), None)

    def _character_in(self, name: str, scope: tuple[Character] | list[Character]) -> bool:
        return any(c.name.lower() == name.lower() and c.known for c in scope)

    def character_in_global(self, name: str) -> bool:
        return self._character_in(name, self._all_characters)

    def character_in_location(self, name: str) -> bool:
        return self._character_in(name, self.characters)

    def character_enters(
            self,
            character: Character,
            *,
            silently: bool = False
    ) -> None:
        if not self.character_in_location(character.name):
            character.location = self._location
            if not silently:
                character.action('Walks in.')

    def character_leaves(
            self,
            character: Character,
            goes_to: Location,
            *,
            silently: bool = False
    ) -> None:
        if self.character_in_location(character.name):
            character.location = goes_to
            if not silently:
                character.action('Walks out.')

    def go_to(
            self,
            location: Location,
    ) -> tuple[bool, Text]:
        """Tries to go specifiec `Location`.
           If location didn't change it returns `False`, otherwise `True`.
        """
        if self._location == location:
            return (False, Text('You\'re currently here.'))
        self._location = location
        return (True, Text.assemble('You\'re now in ', self.location.display_name, '.'))

    # def talk_to(
    #         self,
    #         character: Character
    # ) -> tuple(bool, str):
    #     """Checks if you can talk to the character."""
    #     if character not in self._characters:
    #         return (False, 'You can\'t talk to this character.')
    #     if not character.hookable:
    #         return (False, 'This character does not want to talk with you.')
    #     return (True, character.hook)

    def interaction(self) -> Character | Location | None:
        fails = 0
        query = ''
        while not query:
            try:
                self._prefix()
                query = console.input('')
            except KeyboardInterrupt:
                continue
        try:
            query.index(' ')
        except ValueError:
            command, argument = query, None
        else:
            [command, argument] = query.split(' ', 1)
        command = commands.get(command)
        if not command:
            self._prefix()
            if fails > 3:
                console.print('Psst, you can use `help`')
            else:
                console.print('I\'m not sure what do you mean')
                fails += 1
            return None
        match command.name:
            case 'exit':
                console.print('Goodbye!')
                exit()
            case 'help':
                if not argument:
                    console.print(Text.assemble(
                        'Available commands',
                        style=Style(bold=True)
                    ))
                    for cmd in commands.keys():
                        console.print(
                            '{0.name} - {0.brief}'.format(commands[cmd])
                        )
                else:
                    if not (cmd := commands.get(argument)):
                        console.print(f'Command `{argument}` does not exist.')
                    else:
                        console.print('{0.name}: {0.description}'.format(cmd))
            case 'talk':
                if not argument:
                    self._prefix()
                    console.print('You speak to everyone, but no one hears you.')
                    return None
                if not self.character_in_global(argument):
                    self._prefix()
                    console.print('You don\'t know this character.')
                    return None
                if not self.character_in_location(argument):
                    self._prefix()
                    console.print('This chracter is not here.')
                    return None
                char = self.find_character(argument)
                if not char.pokable:
                    self._prefix()
                    console.print(Text.assemble(char.display_name, ' does not want to talk with you.'))
                    return None
                char.monologue(char.poke)
                return char
            case 'go':
                if not argument:
                    self._prefix()
                    console.print('After running in circle for a while you find it worthless.')
                    return None
                if not (loc := self.find_location(argument)):
                    self._prefix()
                    console.print('You don\'t know this location.')
                    return None
                (success, response) = self.go_to(loc)
                self._prefix()
                console.print(response)
                return loc if success else None
