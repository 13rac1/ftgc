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
    if sum(ftdate) is 0:
        # Do not output an empty 0/0/0 date.
        return ''
    return '{0}/{1}/{2}'.format(ftdate[0], ftdate[1], ftdate[2])


def getDateStatus(status):
    """
    Retuns a string given the FT2 status
    """
    return (
        'NullDate',
        'Inapplicable',
        'Unknown',
        'Approximate',
        'Known',
    )[status]


def getGender(gender):
    """
    Retuns a string given the FT2 status
    """
    return (
        '',
        'Male',
        'Female',
    )[gender]


def bytesToString(in_bytes):
    if type(in_bytes) is not bytes:
        return ''

    string = in_bytes.decode(encoding='ascii')
    return string.strip()


class IndexedObject:
    """
    Base class with index counter static variable and getter.
    """
    # 0 to start at one
    index = 0

    @classmethod
    def getIndex(cls):
        cls.index += 1
        return cls.index


class Marriage(IndexedObject):
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

    def __init__(self, attr):
        self.marriage = self.getIndex()

        # Some data cannot be converted to Gramps CSV, put in the notes field
        notes = []

        self.husband = attr[0]
        self.wife = attr[1]

        self.date = ""
        if attr[2] not in (DATE_STATUS_NULL, DATE_STATUS_KNOWN):
            self.date = getDate(attr[3:6])
            notes.append('Start Date Status: ' + getDateStatus(attr[2]) + '.')

        # FT2 has an "EndingDate" field, but Gramps CSV doesn't. If there is
        # any date information put it in the notes field.
        if attr[6] is not DATE_STATUS_NULL:
            notes.append('End Date Status: ' + getDateStatus(attr[6]) + '.')
            # Only show the date if it's useful.
            if attr[6] in (DATE_STATUS_APROXIMATE, DATE_STATUS_KNOWN):
                notes.append('End Date: ' + getDate(attr[7:]) + '.')
        self.notes = ' '.join(notes)

    def csvHeader():
        return ('Marriage', 'Husband', 'Wife', 'Date', 'Notes')

    def __getitem__(self, index):
        return (
            self.marriage,
            self.husband,
            self.wife,
            self.date,
            self.notes,
        )[index]


class Person(IndexedObject):
    """
    Gramps CSV Person object.

    Fields accepted by Gramps:
    person -  a reference to be used for families (marriages, and children)
    firstname - a person's first name
    surname/lastname - a person's last name
    gender - male or female (you should use the translation for your language)
    note - a note for the person's record
    birthdate - date of birth
    birthplace - place of birth
    deathdate - date of death
    deathplace - place of death

    Fields provided by FT2:
    Person = RECORD
        name         : NameLine; 31 chars
        sex          : (Null, Male, Female);
        mom, dad     : integer; (one-indexed since the header is skipped)
        BirthPlace,
        DeathPlace   : NameLine; 31 chars
        BirthDate,
        DeathDate    : date;
        comments     : CommentLine; 66 chars
        Biography    : boolean;
    END;
    Date = RECORD
        status : (NullDate, Inapplicable, Unknown, Approximate, Known)
        month  : 0..12;
        day    : 0..31;
        year   : INTEGER
    END;
    """

    def __init__(self, attr):
        self.person = self.getIndex()

        # Some data cannot be converted to Gramps CSV, put in the notes field
        notes = []

        name = bytesToString(attr[0]).title()

        # It's far too complex to figure out every edge case, here is a couple
        # important ones.
        # @todo: Name Suffix? I, II, III, Jr should be straightforward
        names = name.split(maxsplit=2)
        if len(names) is 1:
            # No last name
            self.firstname = names[0]
            self.lastname = ''
        elif len(names) is 2:
            self.firstname = names[0]
            self.lastname = names[1]
        elif len(names) is 3:
            # Three names, assume second is middle
            self.firstname = names[0] + ' ' + names[1]
            self.lastname = names[2]

        # All fields go by Gramps names
        self.gender = getGender(attr[1])
        # These ID numbers are used in later processing, not by Gramps
        self.mom_id = attr[2]
        self.dad_id = attr[3]

        self.birthplace = bytesToString(attr[4]).title()
        self.deathplace = bytesToString(attr[5]).title()
        self.birthdate = getDate(attr[7:10])
        self.deathdate = getDate(attr[11:14])

        ftnote = bytesToString(attr[14])
        if ftnote:
            notes.append(ftnote)

        # Show date status if not null or simply known
        if attr[6] not in (DATE_STATUS_NULL, DATE_STATUS_KNOWN):
            notes.append('Birth Date Status: ' + getDateStatus(attr[6]) + '.')
        if attr[10] not in (DATE_STATUS_NULL, DATE_STATUS_KNOWN):
            notes.append('Death Date Status: ' + getDateStatus(attr[10]) + '.')
        self.note = ' '.join(notes)

    def csvHeader():
        return ('Person', 'Firstname', 'Lastname', 'Gender', 'Birthplace',
                'Deathplace', 'Birthdate', 'Deathdate', 'Note')

    def __getitem__(self, index):
        return (
            self.person,
            self.firstname,
            self.lastname,
            self.gender,
            self.birthplace,
            self.deathplace,
            self.birthdate,
            self.deathdate,
            self.note
        )[index]


class Family():
    """
    Gramps CSV Family object.

    Fields accepted by Gramps:
    family - a reference to tie this to a marriage above (required)
    child - the reference of the person above who is a child
    """

    def __init__(self, family, child):
        self.family = family
        self.child = child

    def csvHeader():
        return ('Family', 'Child')

    def __getitem__(self, index):
        return (
            self.family,
            self.child
        )[index]
