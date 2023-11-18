# -*- coding: utf-8 -*-
from os import getenv


DEBUG: bool = bool(getenv('DEBUG', False))
