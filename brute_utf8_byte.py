import sys
fromhex = bytearray.fromhex

if len(sys.argv) == 1:
    print(sys.argv[0], 'FORMAT')  # , '[CANDIDATES]'
    print('ex.', sys.argv[0], 'e382xx', '')
    exit(1)

FORMAT = sys.argv[1].lower().replace('xx', '%02x')

CANDIDATES = range(256)
if len(sys.argv) > 2:
    pass  # TODO

for c in CANDIDATES:
    try:
        print('%02x' % c, fromhex(FORMAT % c).decode('utf-8'))
    except UnicodeDecodeError:
        pass
