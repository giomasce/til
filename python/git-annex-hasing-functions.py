# Implement the two hashing functions use by git-annex to divide
# content is subdirectories. See docs in
# http://git-annex.branchable.com/internals/hashing/ and Haskell
# implementation in
# http://sources.debian.net/src/git-annex/5.20140227/Locations.hs/?hl=408#L408. See
# also https://gist.github.com/giomasce/a7802bda1417521c5b30.

import hashlib
import struct

def hashdirlower(key):
    hasher = hashlib.md5()
    hasher.update(key)
    digest = hasher.hexdigest()
    return "%s/%s/" % (digest[:3], digest[3:6])

def hashdirmixed(key):
    hasher = hashlib.md5()
    hasher.update(key)
    digest = hasher.digest()
    first_word = struct.unpack('<I', digest[:4])[0]
    nums = [first_word >> (6 * x) & 31 for x in xrange(4)]
    letters = ["0123456789zqjxkmvwgpfZQJXKMVWGPF"[i] for i in nums]
    return "%s%s/%s%s/" % (letters[1], letters[0], letters[3], letters[2])
