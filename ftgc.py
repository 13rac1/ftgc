#!/usr/bin/python3
"""SoftDisk Family Tree to Gramps CSV"""

import sys

from struct import iter_unpack
from ftgc.format import ft2person, ft2marriage
from ftgc.objects import Marriage

if sys.version_info < (3, 4):
    # For struct.iter_unpack
    print('ERROR: this script requires Python 3.4 or greater.')
    sys.exit(1)

marriages = []

# Read marriages
ftbuffer = open("test/ft2/SAMPLE.FTM", "rb").read()

for row in iter_unpack(ft2marriage.fmt, ftbuffer):
    marriage = Marriage(row)
    marriages.append(marriage)