# ftgc: SoftDisk Family Tree to Gramps CSV

Import Softdisk Family Tree version 2 (Enhanced Family Tree) genealogy database
files. Output a CSV file formatted for the [Gramps](https://gramps-project.org/)
genealogy software [CSV Import](https://gramps-project.org/wiki/index.php?title=Gramps_4.2_Wiki_Manual_-_Manage_Family_Trees:_CSV_Import_and_Export#Import) format.

### Input Specifics
Multiple files of differing extensions are used to create the Family Tree
database:

* .FTD - person data
* .FTM - marriage data
* .FTI - index data
* .FTP - place name data

The FTD and FTM files are the only ones needed for export. The index data is
just for display, and the place name data is sadly just a top ten list of the
last used place names.

### Usage

```
$ ftgc.py example.FTD example.FTM output.csv
```

### Requirements

* Python 3

### Before and After
Before in Family Tree 2 with sample data
![Family Tree 2 with sample data](docs/before-ft2.png?raw=true)

After [Gramps](https://gramps-project.org/) with converted sample data
![Gramps with converted sample data](docs/after-gramps.png?raw=true)

### Example CSV

Example output from ft2 sample data. Created with:
```bash
$ ./ftgc.py test/ft2/SAMPLE.FTD test/ft2/SAMPLE.FTM test.csv
```
test.csv:
```
Person,Firstname,Lastname,Gender,Birthplace,Deathplace,Birthdate,Deathdate,Note
1,Carol,Brady,Female,,,1/1/1940,,"a lovely lady; always said ""Don't play ball in the house."""
2,Mike,Brady,Male,,,1/1/1940,,was once living with three boys of his own
3,Greg,Brady,Male,,,1/1/1958,,was one of the four men living all together who were all alone
4,Jan,Brady,Female,,,1/1/1960,,had hair of gold (like her mother)
5,Marcia,Brady,Female,,,1/1/1958,,was allergic to Tiger's flea powder
6,Peter,Brady,Male,,,1/1/1960,,"allergic to strawberries.  Famous Line: ""pork chops & applesauce"""
7,Bobby,Brady,Male,,,1/1/1962,,
8,Cindy,Brady,Female,,,1/1/1962,,"had hair of gold like her mother, in curls"
9,Alice,,Female,,,1/1/1933,,added to cast at last minute to fill center square

Marriage,Husband,Wife,Date,Notes
1,2,1,,End Date Status: Inapplicable.

Family,Child
1,3
1,4
1,5
1,6
1,7
1,8
```

### Why
It was time to dispose of my parent's old computers. In the process, I found my
mom's genealogy database on a 1.3GB Maxtor 71336A (manufactured 06-06-96) hard
disk. There wasn't a way to export the data, so I wrote one.

### Thanks
Thanks to the Archive Team for creating the [Just Solve the File Format
Problem!](http://justsolve.archiveteam.org/) website. Special thanks to Dan
Tobias for writing up the structure of these files: http://justsolve.archiveteam.org/wiki/Softdisk_Family_Tree

### Todo

* Family Tree version 1 and 3 support.
* Input file error checking.
* Additional export formats.
* Handle NAME.BIO Biography directory, filename: TREE{person id number}.BIO
* Handle Person name suffixes.
