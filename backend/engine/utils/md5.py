import hashlib
BLOCKSIZE = 65536

def getHash(filePath):
    """
        Return file hash

        Get hash from a file
    """
    hasher = hashlib.md5()
    with open(filePath, "rb") as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()
