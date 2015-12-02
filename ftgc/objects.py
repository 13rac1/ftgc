#Gramps CSV Objects

DATE_STATUS_NULL = 0
DATE_STATUS_INAPPLICABLE = 1
DATE_STATUS_UNKNOWN = 2
DATE_STATUS_APROXIMATE = 3
DATE_STATUS_KNOWN = 4


def getDate(ftdate):
    """
    # Parse FT2 Date objects and return useable strings 1/1/1970
    """
    return '{}/{}/{}'.format(ftdate[0], ftdate[1], ftdate[2])


def getDateStatus(status):
    """
    Retuns a string given the FT2 status
    """
    return {
        0: 'NullDate',
        1: 'Inapplicable',
        2: 'Unknown',
        3: 'Approximate',
        4: 'Known',
    }[status]


class Marriage:
    """
    Gramps CSV Marriage object.

    Marriage objects are created first, because they must be referenced during
    Person object creation to create Family objects.

    Fields accepted by Gramps:
    marriage - if you want to reference this from a family, you'll need a
               matching name here
    husband/father/parent1 - the reference of the person above who is the
                             husband (for female parent1, you'll need to put
                             gender in the person area, or edit it later in
                             gramps)
    wife/mother/parent2 - the reference of the person above who is the wife
                          (for male parent2, you'll need to put gender in the
                          person area, or edit it later in gramps)
    date - the date of the marriage
    place - the place of the marriage
    placeid - the place id of the marriage
    source - source title of the marriage
    note - a note about the marriage/wedding

    Fields provided by FT2:
    MarriageData = RECORD
        husband, wife: integer;
        MarriageDate, EndingDate: Date
    END;
    Date = RECORD
        status : (NullDate, Inapplicable, Unknown, Approximate, Known)
        month  : 0..12;
        day    : 0..31;
        year   : INTEGER
    END;
    """

    # Class variable as a counter, must increment before return so start at -1
    index = -1

    @classmethod
    def getIndex(cls):
        cls.index += 1
        return cls.index

    def __init__(self, attr):
        self.marriage = self.getIndex()

        # Some data cannot be converted to Gramps CSV, put in the notes field
        notes = ""

        self.husband = attr[0]
        self.wife = attr[1]

        self.date = ""
        if attr[2] != DATE_STATUS_NULL:
            self.date = getDate(attr[3:6])
            notes += 'Start Date Status: ' + getDateStatus(attr[2]) + '\n'

        # FT2 has an "EndingDate" field, but Gramps CSV doesn't. If there is
        # any date information put it in the notes field.
        if attr[6] != DATE_STATUS_NULL:
            notes += 'End Date Status: ' + getDateStatus(attr[6]) + '\n'
            # Only show the date if it's useful.
            if attr[6] in (DATE_STATUS_APROXIMATE, DATE_STATUS_KNOWN):
                notes += 'End Date: ' + getDate(attr[7:]) + '\n'
        self.notes = notes
