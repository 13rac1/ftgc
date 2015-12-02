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

### Why
It was time to dispose of my parent's old computers. In the process, I found my
mom's genealogy database on a 1.3GB Maxtor 71336A (manufactured 06-06-96) hard
disk. There wasn't a way to export the data, so I wrote one.

### Todo

* Family Tree version 1 and 3 support.
