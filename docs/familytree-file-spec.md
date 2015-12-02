*The following text is from: http://justsolve.archiveteam.org/wiki/Softdisk_Family_Tree Stored here for all the reasons.*

The Family Tree program from Softdisk Publishing (some versions were called "Enhanced Family Tree") appeared in three major versions, and a number of minor revisions. Some were published on issues of the diskmagazine ''Big Blue Disk'' / ''On Disk Monthly'' / ''Softdisk PC'' (for PC/MS-DOS), while other versions were released as standalone programs in various places such as an online download store.  Later versions could import and export [[GEDCOM]] files, but the native data storage was in a binary format specific to the program. Like the program itself, the file format had three major versions (later program versions could import the data formats of the earlier ones).

#Family Tree 1

A "file" was actually stored in four files, with extensions .FPD, .FMD, .FIX, and .FCM, for person data, marriage data, index data, and comment data respectively. The filename before the extension was the same for all the files connected to a particular data set.

The .FPD (person) file was a set of binary records, stored directly from the Turbo/Borland Pascal structure:

    PersonData = RECORD
                    sex: SexType;
                    name, BirthPlace, DeathPlace: NameLine;
                    BirthDate, DeathDate: date;
                    mom, dad: integer;
                    marriages: MarriageList;
                    kids: ChildList;
                    comments: TextLine;
                 END;

with these data type definitions:

    SexType = (male, female, neuter, hermaphrodite);

    TextLine = STRING[80];
    NameLine = STRING[30];

    Date = RECORD
              status : StatusType;
              month  : 0..12;
              day    : 0..31;
              year   : INTEGER
           END;

    StatusType = (NullDate, Inapplicable, Unknown, Approximate, Known);

Alas, the "neuter" and "hermaphrodite" types were dropped from later versions. Strings are of the Pascal variety, with the first byte indicating the length, followed by the bytes of the string themselves (no [[Character Encoding]] specified, but presumed to be in the [[MS-DOS encodings|MS-DOS code page]] in use by the program's user). Dates are presumably in the Gregorian calendar, with no way to specify anything else.

The person records were numbered sequentially, with the 'mom' and 'dad' integer fields representing the record numbers of the mother and father of the person respectively, zero if unspecified.  The record numbers of people were also used in the marriage data below.

The .FMD (marriage) file was a binary dump of the structure:

    MarriageData = RECORD
                         husband, wife: integer;
                         MarriageDate, EndingDate: date
                   END;

(Same-sex marriages were unheard-of in those days.)

The .FIX (index) file contained two numbers, stored in the internal format of Turbo/Borland Pascal integers: the first had the number of persons in the file, and the second had the number of marriages.

The .FCM (comments) had a series of comment lines (up to 80 characters) stored in a text file; I believe they were stored in the same order as the person records they were associated with so they could be matched up, since the pointer stored in the structure wouldn't be portable given that it's associated with a particular memory location. I think there was only one comment line per person, and if there were no comments the pointer was NIL and no comment line was saved in the comments file (this was created in an era when memory and disk space was rather scarce). The way this was supposed to work is that, on reading in the person data, if the comments pointer was NIL it was left alone, but if it was anything else this signaled for another line of the commments file to be loaded and the pointer adjusted to point to it.

#Family Tree 2 (Enhanced Family Tree)

A "file" was actually stored in four files, with extensions .FTD, .FTM, .FTI, and .FTP, for person data, marriage data, index data, and place name data respectively.

The person (.FTD) file was a binary dump of this Turbo/Borland Pascal structure:

   DiskData = RECORD
                    name         : NameLine;
                    sex          : SexType;
                    mom, dad     : integer;
                    BirthPlace,
                    DeathPlace   : NameLine;
                    BirthDate,
                    DeathDate    : date;
                    comments     : CommentLine;
                    Biography    : boolean;
              END;

with these type definitions:

   NameLine     = STRING[30];

   StatusType = (NullDate, Inapplicable, Unknown, Approximate, Known);

   SexType = ( Null, Male, Female );

   Date = RECORD
             status : StatusType;
             month  : 0..12;
             day    : 0..31;
             year   : INTEGER
          END;

   CommentLine = STRING[65];

As in version 1, the records are numbered sequentially so that references to other person records are integers.

The first record in the person data file (not counted in the numbering) is a "dummy" record identifying the program that created the file. If you're looking for "magic bytes" to identify this file format, you can note that starting with the third byte (position 2 if you start counting at zero as computers do) you can find the string "Enhanced Family Tree Datafile".

The marriage data (.FTM) uses this structure:

   MarriageData = RECORD
                         husband, wife: integer;
                         MarriageDate, EndingDate: date
                   END;

The index data (.FTI) consists of two numbers stored as Pascal integers, containing the number of persons and number of marriages.

The place name file (.FTP) is a text file with 10 lines giving the top 10 place names used in the file, so they can be presented in a pick list for further entries.

#Family Tree 3

A "file" was actually stored in two files, with extensions .F3D and .F3M, for person and marriage data respectively.

The person data (.F3D) is a binary dump of this Turbo/Borland Pascal structure:

   PersonData = RECORD
                    IDNum : longint;
                    name: NameLine;
                    valid, flag, biography : boolean;
                    sex: SexType;
                    BirthPlace, DeathPlace: NameLine;
                    BirthDate, DeathDate: date;
                    comments: CommentLine;
                    mom, dad: longint;
                    FirstMarriage, FirstKid,
                      MomsNextKid, DadsNextKid,
                      TreeUp, TreeLess, TreeMore,
                      AlphaPrev, AlphaNext: longint
                 END;

with these type definitions:

   NameLine     = STRING[32];
   CommentLine  = STRING[61];
   SexType = ( Null, Male, Female );

   Date = RECORD
             status : StatusType;
             month  : 0..12;
             day    : 0..31;
             year   : INTEGER
          END;

   StatusType = (NullDate, Inapplicable, Unknown, Approximate,
                 Before, After, Known);

As with version 2, the first record is a dummy record identifying the program (starting at the 7th byte (position 6) is the string "Family Tree Data File"). Here, the number of persons in the file is stored in the 'mom' field and the number of marriages in the 'dad' field. The records have explicit ID numbers stored in them, so that persons keep their number even if some records are deleted. Various fields represent linked-list pointers (by record ID number) to lists of the children of the mother and the father, an alphabetical list of people, some sort of tree structure (I'm not sure the exact structure there) and a list of marriages (which uses the ID numbers of the marriage records below).

The marriage data (.F3M) file uses this binary record structure:

   MarriageData = RECORD
                        IDNum, husband, wife: longint;
                        MarriagePlace: NameLine;
                        MarriageDate, EndingDate: date;
                        EndingReason: ReasonType;
                        HusbandsNextMarriage, WifesNextMarriage: longint;
                        flag: boolean
                  END;

with the data types above plus this one:

   ReasonType = ( None, Divorce, Annulment, Death );
