# Person Python Struct Format

from . import ft2date

fmt = ''

# Little Endian (Cross Platform Compatiblity)
fmt += '<'
#MarriageData = RECORD
#    husband      : short 2 bytes (16-bit int)
# 02 00
fmt += 'h'
#    wife         : short 2 bytes (16-bit int)
# 01 00
fmt += 'h'
#    MarriageDate : date
# 04 01 01 AF 07
fmt += ft2date.fmt
#    EndingDate   : date
# 01 00 00 00 00
fmt += ft2date.fmt
#END;
