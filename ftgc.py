#!/usr/bin/python3
"""SoftDisk Family Tree to Gramps CSV"""

from struct import iter_unpack
from ftgc.format import ft2person

# Test of initial person formatter
ftbuffer = open("test/ft2/SAMPLE.FTD", "rb").read()

for x in iter_unpack(ft2person.fmt, ftbuffer):
    print(x)
