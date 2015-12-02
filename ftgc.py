#!/usr/bin/python3
"""SoftDisk Family Tree to Gramps CSV"""

import sys

from struct import iter_unpack
from ftgc.format import ft2person, ft2marriage

if sys.version_info < (3, 4):
    # For struct.iter_unpack
    print('ERROR: this script requires Python 3.4 or greater.')
    sys.exit(1)

# Test of marriage format
ftbuffer = open("test/ft2/SAMPLE.FTM", "rb").read()

for x in iter_unpack(ft2marriage.fmt, ftbuffer):
    print(x)
