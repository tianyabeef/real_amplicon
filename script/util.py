import os

def mkdir(dirname):
    if os.path.isdir(dirname):
        return None
    if dirname == '':
        return None
    os.mkdir(dirname)
    return None
