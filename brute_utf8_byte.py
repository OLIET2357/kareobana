import sys
fromhex = bytearray.fromhex

if len(sys.argv) == 1:
    print('Usage', sys.argv[0], 'FORMAT', '[CANDIDATES]')
    print('ex.', sys.argv[0], 'e382xx', '')
    print('ex.', sys.argv[0], 'e382xx', '8a,a8')
    print('ex.', sys.argv[0], 'e382xx', 'dissipation')
    exit(1)


FORMAT = sys.argv[1].lower().replace('xx', '%02x')

CANDIDATES = range(0x100)  # all
if len(sys.argv) > 2:
    CANDIDATES_QUERY = sys.argv[2]
    if CANDIDATES_QUERY.lower().startswith('di'):  # dissipation
        CANDIDATES = list(range(0x80, 0xA0+1))+list(range(0xE0, 0xFF+1))
    # elif CANDIDATES_QUERY.lower().startswith('re'):  # replacement
    #     pass  # TODO
    else:
        CANDIDATES = map(lambda x: int(x, 16), CANDIDATES_QUERY.split(','))

for c in CANDIDATES:
    try:
        print('%02x' % c, fromhex(FORMAT % c).decode('utf-8'))
    except UnicodeDecodeError:
        pass
