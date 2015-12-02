# Date Python Struct Format

fmt = ''
# Date = RECORD
#     status : StatusType 1 byte
# (NullDate, Inapplicable, Unknown, Approximate, Known)
fmt += 'b'
#     month  : 0..12 1 byte
fmt += 'b'
#     day    : 0..31 1 byte
fmt += 'b'
#     year   : "INTEGER" (16-bit?) 2 byte short
fmt += 'h'
#END;
