# -*- coding: utf-8 -*-
"""
Main game component, everything about user interactions. "Glues" together all components.
"""
from time import sleep

from rich.style import Style
from rich.table import Table
from rich.text import Text

from FTE.console import console
from FTE.characters import Character
from FTE.locations import Location
from FTE.settings import DEBUG


class UnknownCommand(BaseException):
    """Command doesn't exist."""


class UnknownLocation(BaseException):
    """Location doesn't exist."""


class UnknownCharacter(BaseException):
    """Character doesn't exist."""


class Command:
    """How player can interact with the game. Represents player's action.

    :param name: Which word invokes the command.
    :type name: :obj:`str`
    :param description: Detailed and complete information how to use the command.
    :type description: :obj:`str`
    :param usage: Example usage of a command with expected types.
    :type usage: :obj:`str`
    """
    def __init__(
            self,
            name: str,
            description: str = None,
            *,
            usage: str = None
    ) -> None:
        self.name: str = name
        self.description: str = description
        self._usage: str = usage or ''

    @property
    def usage(self) -> str:
        """Example usage of a command with expected types, defaults to :attr:`FTE.world.Command.name`."""
        if not self._usage:
            return self.name
        return f'{self.name} {self._usage}'


COMMANDS: dict[str, Command] = dict(  # All available commands
    exit = Command(
        'exit',
        'Exits the game.'
    ),
    help = Command(
        'help',
        'Shows help. Optionally only "commands" or "arguments".',
        usage='("commands" | "arguments")'
    ),
    talk = Command(
        'talk',
        'Talk to someone.' +
        ' Pass character name to start conversation with them.' +
        ' You can talk only to characters in your location.',
        usage='<character name>'
    ),
    go = Command(
        'go',
        'Go somewhere.' +
        ' Pass location name to go there.',
        usage='<location name>'
    ),
    info = Command(
        'info',
        'Get information about a character or a location.' +
        ' Do not pass anything to show info about current location.',
        usage='(charcter name | location name)'
    )
)


class World:
    """Represents the game environment, the player, locations, characters, and matches of those.

    :param all_locations: Available (used) locations.
    :type all_locations: :obj:`tuple` of :class:`FTE.locations.Location`
    :param all_characters: Availabel (used) characters.
    :type all_characters: :obj:`tuple` of :class:`FTE.characters.Character`
    :param starting_location: Where player starts the game.
    :type starting_location: :class:`FTE.locations.Location`
    :param first_interaction: If this session is player's first interaction, e.g. first chapter.
    :type first_interaction: :obj:`bool`
    :param assistant: If game assistant should be enabled.
    :type assistant: :obj:`bool`
    """
    def __init__(
            self,
            all_locations: tuple[Location],
            all_characters: tuple[Character],
            starting_location: Location,
            first_interaction: bool = False,
            assistant: bool = False
    ) -> None:
        self._all_locations: tuple[Location] = all_locations
        self._all_characters: tuple[Character] = all_characters
        self._location: Location = starting_location
        self._fails = 0
        self._first_interaction = first_interaction
        self._assistant: bool = assistant

    @property
    def location(self) -> Location:
        """Player's current location. Displays ``"???"`` if location is not known by the player."""
        if self._location not in self._all_locations:
            return Location('???')
        return self._location

    @property
    def characters(self) -> tuple[Character]:
        """All characters in player's current location."""
        return tuple(c for c in self._all_characters if c.location.name == self._location.name)

    def _prefix(self) -> None:
        """Displays before game console's input field with current location's name."""
        console.print(Text.assemble('[ ', self.location.display_name, ' ] '), end='')

    def _prefix_help(self) -> None:
        """Displays before game console's input field inside help menu/mode."""
        console.print('[', Text.assemble( 'Help', style=Style(color='blue') ), ']', end=' ')

    def find_location(self, name: str) -> Location | None:
        """Tries to find a location in all locations by its' name.

        :param name: The location's name to be found.
        :type name: :obj:`str`
        :return: The location if it's found, `None` otherwise.
        :rtype: :class:`FTE.locations.Location` or `None`
        """
        try:
            location = tuple(filter(
                lambda l: l.name.lower() == name.lower() and l.known,
                self._all_locations
            ))[0]
        except IndexError:
            return None
        else:
            return location

    def find_character(self, name: str) -> Character | None:
        """Tries to find a character in all characters by it's name.

        :param name: The character's name to be found.
        :type name: :obj:`str`
        :return: The character if it's found, `None` otherwise.
        :rtype: :class:`FTE.characters.Character` or `None`
        """
        return next((c for c in self._all_characters if c.name.lower() == name.lower()), None)

    def _character_in(self, name: str, scope: tuple[Character] | list[Character]) -> bool:
        """Checks if character is in a location.

        :param name: Character's name to be checked.
        :type name: :obj:`str`
        :param scope: List of characters to search in.
        :type scope: :obj:`tuple` of :class:`FTE.characters.Character` or :obj:`list` of :class:`FTE.characters.Character`
        :return: `True` if character is in a location, `False` otherwise.
        :rtype: :obj:`bool`
        """
        return any(c.name.lower() == name.lower() and c.known for c in scope)

    def character_in_global(self, name: str) -> bool:
        """Checks if character exists.

        :param name: Target character's name.
        :type name: :obj:`str`
        :return: `True` if character exists, `False` otherwise.
        :rtype: :obj:`bool`
        """
        return self._character_in(name, self._all_characters)

    def character_in_location(self, name: str) -> bool:
        """Checks if character is in the same location.

        :param name: Target character's name.
        :type name: :obj:`str`
        :return: `True` if character is in the same location as the player, `False` otherwise.
        :rtype: :obj:`bool`
        """
        return self._character_in(name, self.characters)

    def character_enters(
            self,
            character: Character,
            *,
            silently: bool = False
    ) -> None:
        """Moves a character to player's current location.

        :param character: The character to move.
        :type character: :class:`FTE.characters.Character`
        :param silently: If player should know about the character's entrance.
        :type silently: :obj:`bool`
        """
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
        """Moves a character to another location.

        :param character: The character to move.
        :type character: :class:`FTE.characters.Character`
        :param goes_to: Where the character will move.
        :type goes_to: :class:`FTE.locations.Location`
        :param silently: If player should know about the character's leave.
        :type silently: :obj:`bool` or `None`
        """
        if self.character_in_location(character.name):
            character.location = goes_to
            if not silently:
                character.action('Walks out.')

    def _show_location_characters(self) -> None:
        """Displays characters count and list in player's location."""
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

    def _show_other_locations(self) -> None:
        """Displays count and list of available locations."""
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
        for loc in other_locations:
            locations.append(loc.display_name)
            locations.append(', ')
        locations = locations[:-1]
        console.print(*locations, '.', sep='')

    def _do_first_interaction(self) -> None:
        """Displays basic information how to play and asks if player needs additional help."""
        self._prefix_help()
        console.print(
            'This is your first interaction with the World.',
            'Would you like to enable assitant?'
        )
        expect = ('yes', 'no')
        self._prefix_help()
        query = console.input('')
        while query.lower() not in expect:
            self._prefix_help()
            query = console.input('"yes" or "no"? ')
        self._first_interaction = False
        if query == 'no':
            self._prefix_help()
            console.print('OK! I won\'t ask you again. Have fun!')
            return
        for line in (
            Text.assemble(
                Text.assemble('Fix The Engines', style=Style(bold=True)),
                ' is text-based, paragraph game. There is no mouse control,',
                ' you operate only with commands.'
            ),
            'You can show them by typing "help" during interaction' +
            ' with the World.',
            'All commands are single words. For example "help" or' +
            ' "go" insted of "go to".',
            'Have fun! :smile:'
        ):
            self._prefix_help()
            console.print(line)
            if not DEBUG:
                sleep(2.0)
        self._assistant = True

    def _command_exit(self) -> None:
        """Exits the game."""
        self._prefix()
        console.print('Goodbye!')
        exit()

    def _command_help(self, menu: str = None) -> None:
        """Displays help menu."""
        show_commands, show_arguments = False, False
        if menu == 'commands':
            show_commands = True
        elif menu == 'arguments':
            show_arguments = True
        else:
            show_commands, show_arguments = True, True
        if show_commands:
            commands_table = Table(
                title='Available commands',
                show_lines=True
            )
            commands_table.add_column('Command')
            commands_table.add_column('Description')
            commands_table.add_column('Usage')
            for cmd in COMMANDS.values():
                commands_table.add_row(cmd.name, cmd.description, cmd.usage)
            console.print(commands_table)
        if show_arguments:
            arguments_table = Table(title='Arguments description')
            arguments_table.add_column('Representation')
            arguments_table.add_column('Description')
            for line in (
                ('< ... >', 'Required argument.'),
                ('( ... )', 'Optional argument.'),
                ('( a | b )', 'Optional argument, but only "a" or "b".')
            ):
                arguments_table.add_row(*line)
            console.print(arguments_table)

    def _command_talk(self, character_name: str) -> Character | None:
        """
        Tries to talk to a :class:`FTE.characters.Character`.
        The character must:

        - exist,
        - be in the player's location,
        - be pokable.

        If no name is specified, nothing happens.

        :param character_name: The character's name to which player is trying to talk.
        :type character_name: :obj:`str`
        :return: The character player is trying to talk. `None` if the character doesn't meet above requirements.
        :rtype: :class:`FTE.characters.Character` or `None`
        """
        if not character_name:
            self._prefix()
            console.print('You speak to everyone, but no one hears you.')
            return None
        if not self.character_in_global(character_name):
            self._prefix()
            console.print('You don\'t know this character.')
            return None
        if not self.character_in_location(character_name):
            self._prefix()
            console.print('This chracter is not here.')
            return None
        char = self.find_character(character_name)
        if not char.pokable:
            self._prefix()
            console.print(Text.assemble(char.display_name, ' does not want to talk with you.'))
            return None
        char.monologue(char.poke)
        return char

    def _command_go(
            self,
            location_name: str = None,
    ) -> Location | None:
        """Tries to go to a location.

        :param location_name: The location's name to which player is trying to go to. If no name is specified, nothing happens.
        :type location_name: :obj:`str`
        :return: The location player is trying to go. `None` if the location doesn't exist or player is already in wanted location.
        :rtype: :class:`FTE.locations.Location` or `None`
        """
        if not location_name:
            self._prefix()
            console.print('After running in circle for a while you find it worthless.')
            return None
        if not (location := self.find_location(location_name)):
            self._prefix()
            console.print('You don\'t know this location.')
            return None
        if self._location == location:
            console.print('You\'re currently here.')
            return None
        self._location = location
        self._prefix()
        console.print(Text.assemble('You\'re now in ', self.location.display_name, '.'))
        self._show_location_characters()
        return location

    def _command_info(self, name: str = None) -> None:
        """Displays informaiom about a character or location.

        :param name: Character or location name the player wants information baout, defaults to current location.
        :type name: :obj:`str`
        """
        if not name:
            name = self._location.name
        if (loc := self.find_location(name)):
            self._prefix()
            if (i := loc.info):
                console.print(i)
            else:
                console.print('You don\'t know anything about this location.')
            if loc == self._location:
                self._show_location_characters()
                self._show_other_locations()
        elif (char := self.find_character(name)):
            self._prefix()
            console.print(Text.assemble(
                char.display_name,
                ' has ',
                char.standing.color_text,
                ' standing towards you.'
            ))
            if (i := char.info):
                self._prefix()
                console.print(Text.assemble(char.display_name, '-', i))
        else:
            self._prefix()
            console.print('I don\'t know what do you mean.')

    def assistant(self, text: str | Text) -> None:
        """Displays additional help if the player requested it during the first :meth:`FTE.world.World.interaction`.

        :param text: The text to display.
        :type text: :obj:`str` or :class:`rich.text.Text`
        """
        if self._assistant:
            console.print(text)

    def interaction(self) -> Character | Location | None:
        """
        The main game logic. Controls interactions between the player and world.
        For example talking to characters and going to locations.
        At first time game asks player if they want to enable assistant (:meth:`FTE.world.World.assistant`).

        :return: The object with wich player got with interaction. `None` if doesn't apply.
        :rtype: :class:`FTE.characters.Character`, :class:`FTE.locations.Location`, or `None`
        """
        if self._first_interaction:
            self._do_first_interaction()
            return None
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
        command = COMMANDS.get(command)
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
                self._command_exit()
            case 'help':
                self._command_help(argument)
                return None
            case 'talk':
                return self._command_talk(argument)
            case 'go':
                return self._command_go(argument)
            case 'info':
                self._command_info(argument)
                return None
