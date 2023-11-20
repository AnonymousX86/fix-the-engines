# -*- coding: utf-8 -*-
from os import getenv


DEBUG: bool = bool(int(getenv('DEBUG', 0)))
