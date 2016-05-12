#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Convert a list of base64 encoded objectSid lines from an Active
# Directory LDAP query to the standard SID representation. See
# http://stackoverflow.com/q/33188413/807307 for details.

import sys
import struct
import base64

def convert(binary):
    version = struct.unpack('B', binary[0])[0]
    # I do not know how to treat version != 1 (it does not exist yet)
    assert version == 1, version
    length = struct.unpack('B', binary[1])[0]
    authority = struct.unpack('>Q', '\x00\x00' + binary[2:8])[0]
    string = 'S-%d-%d' % (version, authority)
    binary = binary[8:]
    assert len(binary) == 4 * length
    for i in xrange(length):
        value = struct.unpack('<L', binary[4*i:4*(i+1)])[0]
        string += '-%d' % (value)
    return string

def main():
    for line in sys.stdin:
        line = line.strip()
        if line == '':
            continue
        binary = base64.b64decode(line)
        sid = convert(binary)
        print sid

if __name__ == '__main__':
    main()
