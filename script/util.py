import os

cols_brewer = ['#00447E', '#F34800', '#64A10E', '#930026', '#464E04', '#049a0b', '#4E0C66', '#D00000', '#FF6C00',
               '#FF00FF', '#c7475b', '#00F5FF', '#BDA500', '#A5CFED', '#f0301c', '#2B8BC3', '#FDA100', '#54adf5',
               '#CDD7E2', '#9295C1']


def mkdir(dirname):
    if os.path.isdir(dirname):
        return None
    if dirname == '':
        return None
    os.system("mkdir -p %s" % dirname)
    return None


def image_trans(pdf, png):
    os.system('convert -density 200 %s %s' % (pdf, png))
