# -*- coding: utf-8 -*-
from time import sleep

from rich.text import Text

from FTE.characters import Character, Standing
from FTE.console import console
from FTE.locations import Location
from FTE.settings import DEBUG
from FTE.utils import slow_print, slower_print, story
from FTE.world import World

def chapter_one() -> None:
    bridge = Location('Bridge')
    capsules = Location('Capsules')
    engine_deck = Location('Engine Deck')
    quarters = Location('Quarters')

    roommate = Character('Hevy', quarters, poke='Good to see you.', standing=Standing.GOOD)
    capitan = Character('Rex', bridge, poke='Yes sergant? Oh, wait.')
    pilot = Character('Mixiu', bridge, poke='What the fuck do you want?')
    engineer = Character('Tech', engine_deck, poke='We should invest in twin ion engines.')

    world = World(
        all_locations=(bridge, capsules, engine_deck, quarters),
        all_characters=(roommate, capitan, pilot, engineer),
        starting_location=quarters
    )

    console.clear()
    console.rule('Chapter I')
    console.print(3 * '\n')
    for line in [
        'Year:      3015',
        'Ship:      Epsilon IV',
        'Mission:   Who cares?'
    ]:
        slow_print(line, end='')
        slower_print('...')
    sleep(1.0 if DEBUG else 3.0)

    console.clear()
    console.rule('Chapter I')
    story([
        'You wake up in your bed, someone is trying to talk to you, '
        'but you\'re too sleepy to understand.',
        Text.assemble('You recognize them. I\'s your roommate - ', roommate.display_name, '.'),
        'He\'s shaking you and after a while you can finally understand him...'
    ])
    expect = ('no', 'yes')
    res = roommate.dialogue('Hey! Man! Are you dead already?')
    while res not in expect:
        res = roommate.dialogue('...')
    char_res = 'Unfortunately no' if res == 'yes' else 'That\'s great'
    roommate.monologue(f'{char_res}, now wake up and get a move on, of we\'re screwed.')
    roommate.action('Throws you your clothes.')
    roommate.monologue('Aight, you ready?')
    roommate.action('Claps to you.')
    roommate.monologue(Text.assemble(
        'We either go to ',
        capsules.display_name,
        ' or to ',
        engine_deck.display_name,
        ', I don\'t trust our engineers tho.'
    ))
    expect = (capsules, engine_deck)
    roommate.poke = 'There\'s no time, let\'s go!'
    while res != capsules and res != engine_deck:
        res = None
        while res is None:
            res = world.interaction()
    if res == capsules:
        world.character_enters(roommate)
        roommate.monologue('This ship sucks either way...')
    else:
        engineer.monologue('Hey! What are you doing here?')
        world.character_enters(roommate)
        roommate.monologue('Don\'t worry, we\'re here to help.')

    story('...more coming soon!')
