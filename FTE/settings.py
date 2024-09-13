# -*- coding: utf-8 -*-
"""
Game global settings.

`DEBUG` -- used for skipping game to current working point.
"""
from os import getenv


DEBUG: bool = bool(int(getenv('DEBUG', 0)))
