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
    ),
    info = Command(
        'info',
        'Get information about a character or a place.',
        'Pass character or location name to get information about what' +
        'do you know about the subject.'
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
        self._fails = 0

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

    def _show_location_characters(self) -> None:
        self._prefix()
        if (l := len(self.characters)) == 0:
            console.print('There are no characters in this location.')
            return
        if l == 1:
            console.print('There is 1 character in this location: ', end='')
        else:
            console.print(f'There are {l} characters in this location: ', end='')
        location_characters: list[str | Text] = []
        for char in self.characters:
            location_characters.append(char.display_name)
            location_characters.append(', ')
        location_characters = location_characters[:-1]
        console.print(*location_characters, '.', sep='')

    def _show_all_locations(self) -> None:
        self._prefix()
        other_locations = tuple(filter(lambda l: l != self.location, self._all_locations))
        if (l := len(other_locations)) == 0:
            console.print('There are no other locations you can go to.')
            return
        if l == 1:
            console.print('There is 1 other location you can go to: ', end='')
        else:
            console.print(f'There are {l} other locations you can go to: ', end='')
        locations: list[str | Text] = []
        for loc in self._all_locations:
            locations.append(loc.display_name)
            locations.append(', ')
        locations = locations[:-1]
        console.print(*locations, '.', sep='')

    def go_to(
            self,
            location: Location,
    ) -> bool:
        """Tries to go specifiec `Location`.
           If location didn't change it returns `False`, otherwise `True`.
        """
        if self._location == location:
            console.print('You\'re currently here.')
            return False
        self._location = location
        self._prefix()
        console.print(Text.assemble('You\'re now in ', self.location.display_name, '.'))
        self._show_location_characters()
        return True

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
        query = ''
        while not query:
            try:
                self._prefix()
                query = console.input('')
            except KeyboardInterrupt:
                console.print(Text.assemble(
                    ' Retry...',
                    style=Style(
                        color='yellow',
                        italic=True
                )))
                continue
        try:
            query.index(' ')
        except ValueError:
            command, argument = query, None
        else:
            [command, argument] = query.split(' ', 1)
        command = commands.get(command)
        if not command:
            self._fails += 1
            self._prefix()
            if self._fails >= 3:
                console.print('Psst, you can use `help`.')
            else:
                console.print('I\'m not sure what do you mean.')
            return None
        self._fails = 0
        match command.name:
            case 'exit':
                self._prefix()
                console.print('Goodbye!')
                exit()
            case 'help':
                self._prefix()
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
                if not self.go_to(loc):
                    return None
                return self._location
            case 'info':
                if not argument:
                    self._show_location_characters()
                    self._show_all_locations()
                    return None
                if (char := self.find_character(argument)):
                    self._prefix()
                    console.print(Text.assemble(
                        char.display_name,
                        'has',
                        char.standing.color_text,
                        'standing towards you.'
                    ))
                    if (i := char.info):
                        self._prefix()
                        console.print(Text.assemble(char.display_name, '-', i))
                    return None
                if (loc := self.find_location(argument)):
                    self._prefix()
                    if (i := loc.info):
                        console.print(i)
                    else:
                        console.print('You don\'t know anything about tat location.')
                    return None
                self._prefix()
                console.print('I don\'t know what do you mean.')
