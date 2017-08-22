# Format:
# first comes the board size (4 bits)
# subsequent entries depend on board size:
#       h3-h4:  3 bits per number
#       h5-h8:  4 bits per number
# each move is then written as 8 numbers:
#       first      second
#     from  to    from  to
#     q r  q r    q r  q r (the s's can be derived)
# in the case of captures, the "to" part is all 1's
# the file is delimited by a 0 and then enough 1's to fill the byte
from game import *
import re
import struct
from time import gmtime, strftime


def createReplay(moveList):
    content = ""
    content += format(BOARD_SIZE, "04b")
    bitLen = 3 if BOARD_SIZE < 4 else 4
    binaryFormat = '0' + str(bitLen) + 'b'
    pack = lambda n: format(n + BOARD_SIZE, binaryFormat)
    for i in moveList:
        for j in i:
            if type(j) == Hex:
                content += pack(j.q)
                content += pack(j.r)
                content += 2 * bitLen * '1'
            else:
                content += pack(j.start.q)
                content += pack(j.start.r)
                content += pack(j.end.q)
                content += pack(j.end.r)
    content += '0'
    while len(content) % 8 != 0:
        content += '1'
    content = [chr(int(i, 2)) for i in re.findall('.{8}?', content)]
    f = open("replays/" + strftime("%y%m%d%H%M", gmtime()) + ".replay", "wb")
    f.write("".join(content))
    f.close()


def readReplay(fileName):
    f = open(fileName, "rb")
    content = f.read()
    f.close()
    content = struct.unpack('c' * len(content), content)
    data = ''
    for i in content:
        data += format(ord(i), '08b')
    bs = int(data[:4], 2)
    while data[-1] == '1':  # remove trailing 1's
        data = data[:-1]
    data = data[4:-1]  # remove traling 0 and board size header
    bitLen = 3 if bs < 4 else 4
    data = [int(data[i:i + bitLen], 2) - bs for i in range(0, len(data), bitLen)]  # bits to numbers
    data = [(data[i], data[i + 1]) for i in range(0, len(data), 2)]  # pair the numbers
    data = [Hex(i[0], i[1], -(i[0] + i[1])) for i in data]  # convert pairs to hexes by deriving 's'
    data = [Move(data[i], data[i + 1]) for i in range(0, len(data), 2)]  # convert hexes to moves
    for i in range(len(data)):
        if data[i].end.q == 2 ** bitLen - bs - 1:  # convert captures back to hexes
            data[i] = data[i].start
    # data = [data[i:i + 1] for i in range(0, len(data), 2)] # pair moves into full moves
    return bs, data
