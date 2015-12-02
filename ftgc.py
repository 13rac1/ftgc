#!/usr/bin/python3
"""SoftDisk Family Tree to Gramps CSV"""
DEBUG = False
import sys

from struct import iter_unpack
from ftgc.format import ft2person, ft2marriage
from ftgc.objects import Marriage, Person, Family

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

people = []
# Read People
ftbuffer = open("test/ft2/SAMPLE.FTD", "rb").read()

first = True
for row in iter_unpack(ft2person.fmt, ftbuffer):
    # Skip the first entry since it is the FT2 header
    if first:
        first = False
        continue

    person = Person(row)
    people.append(person)
    if DEBUG:
        print(row)

families = []
# Parse all of the people to find their parent's marriage and create Families.
for person in people:
    mom = person.mom_id
    dad = person.dad_id
    for marriage in marriages:
        if marriage.husband is dad and marriage.wife is mom:
            # Found your family!
            family = Family(marriage.marriage, person.person)
            families.append(family)

            if DEBUG:
                # Note -1 because FT2 is one-based, but the data is zero-based
                print('{} {}\n  Dad: {} {}\n Mom: {} {}'.format(
                    person.firstname, person.lastname,
                    people[dad-1].firstname, people[dad-1].lastname,
                    people[mom-1].firstname, people[mom-1].lastname))
