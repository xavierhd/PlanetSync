
from os.path import expanduser, dirname, abspath
from fstab import FstabFile

def get_fstab(path):
    return FstabFile(path)


x = get_fstab(dirname(abspath(__file__)) + '/test_fstab')
print(x)