# -*- coding: utf-8 -*-
"""
Game global settings.

Settings are set by environemnt variables. None is required.

`DEBUG` -- used for skipping game to current working point.
"""
from os import getenv


DEBUG: bool = bool(int(getenv('DEBUG', 0)))
