# Person Python Struct Format

from . import ft2date

fmt = ''
# Little Endian (Cross Platform Compatiblity)
fmt += '<'
# DiskData = RECORD
#     name         : NameLine 31 bytes (Not 30 bytes!)
# 09 4A 61 6E 20 42 72 61 64 79 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
fmt += '31p'
#     padding
# 00
#fmt += 'x'
#     sex          : SexType 1 byte (Null, Male, Female)
# 00, 01, 02
fmt += 'b'
#     mom          : short 2 bytes (16-bit int)
# 01 00
fmt += 'h'
#     dad          : short 2 bytes (16-bit int)
# 02 00
fmt += 'h'
#     BirthPlace   : NameLine 31 bytes (Not 30 bytes!)
# 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
fmt += '31p'
#     DeathPlace   : NameLine; 31 bytes (Not 30 bytes!)
# 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
fmt += '31p'
#     Double padding?
# 00 00
#fmt += 'xx'
#     BirthDate    : date
# 04 01 01 A8 07
fmt += ft2date.fmt
#     DeathDate    : date
# 00 00 00 00 00
fmt += ft2date.fmt
#     comments     : CommentLine; 66 bytes (Not 65 bytes!)
# 22 68 61 64 20 68 61 69 72 20 6F 66 20 67 6F 6C 64 20 28 6C 69 6B 65 20 68 65
# 72 20 6D 6F 74 68 65 72 29 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
# 00 00 00 00 00 00 00 00 00 00 00 00 00
fmt += '66p'
#     Biography    : boolean
fmt += 'b'
#     padding
# 00
#fmt += 'x'
# END; 175 bytes total
