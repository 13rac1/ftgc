# Person Python Struct Format

from . import ft2date

fmt = ''
# Little Endian (Cross Platform Compatiblity)
fmt += '<'
# DiskData = RECORD
#     name         : NameLine 31 bytes (Not 30 bytes!)
fmt += '31p'
#     sex          : SexType 1 byte (Null, Male, Female)
fmt += 'b'
#     mom          : short 2 bytes (16-bit int)
fmt += 'h'
#     dad          : short 2 bytes (16-bit int)
# 02 00
fmt += 'h'
#     BirthPlace   : NameLine 31 bytes (Not 30 bytes!)
fmt += '31p'
#     DeathPlace   : NameLine; 31 bytes (Not 30 bytes!)
fmt += '31p'
#     BirthDate    : date
fmt += ft2date.fmt
#     DeathDate    : date
fmt += ft2date.fmt
#     comments     : CommentLine; 66 bytes (Not 65 bytes!)
fmt += '66p'
#     Biography    : boolean
fmt += 'b'
# END; 175 bytes total
