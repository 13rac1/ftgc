#!/usr/bin/python3
"""
SoftDisk Family Tree to Gramps CSV
2015 Brad Erickson (eosrei)
Licensed GPLv3
"""
DEBUG = False
import sys
import csv
import argparse

from struct import iter_unpack
from ftgc.format import ft2person, ft2marriage
from ftgc.objects import Marriage, Person, Family

if sys.version_info < (3, 4):
    # For struct.iter_unpack
    print('ERROR: this script requires Python 3.4 or greater.')
    sys.exit(1)

desc="""
Import Softdisk Family Tree version 2 (Enhanced Family Tree) genealogy
database files. Output a CSV file formatted for the Gramps genealogy software
CSV Import format.
"""

parser = argparse.ArgumentParser(description=desc)

parser.add_argument('FTD', help='Input: A Family Tree 2 FTD Person file')
parser.add_argument('FTM', help='Input: A Family Tree 2 FTM Marriage file')
parser.add_argument('CSV', help='Output: A CSV formatted for Gramps')

args = parser.parse_args()

# @todo: File exists error checking.

marriages = []
# Read marriages
ftbuffer = open(args.FTM, "rb").read()
for row in iter_unpack(ft2marriage.fmt, ftbuffer):
    marriage = Marriage(row)
    marriages.append(marriage)

people = []
# Read People
ftbuffer = open(args.FTD, "rb").read()

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

# Write out the CSV!
with open(args.CSV, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(Person.csvHeader())
    # csv.writer.writerow() does not accept generator (must be coerced to list)
    # http://bugs.python.org/issue23171
    writer.writerows(list(p) for p in people)
    writer.writerow('')
    writer.writerow(Marriage.csvHeader())
    writer.writerows(list(m) for m in marriages)
    writer.writerow('')
    writer.writerow(Family.csvHeader())
    writer.writerows(list(f) for f in families)
