import re
import os

COLS_BREWER = ['#00447E', '#F34800', '#64A10E', '#930026', '#464E04', '#049a0b', '#4E0C66', '#D00000', '#FF6C00',
               '#FF00FF', '#c7475b', '#00F5FF', '#BDA500', '#A5CFED', '#f0301c', '#2B8BC3', '#FDA100', '#54adf5',
               '#CDD7E2', '#9295C1']

LEVELS = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']

TAX_DICT = {
    'k': 'kingdom',
    'p': 'phylum',
    'c': 'class',
    'o': 'order',
    'f': 'family',
    'g': 'genus',
    's': 'species',
}

SEARCH_REG = {
    'k': re.compile('(k__[^;]+)'),
    'p': re.compile('(p__[^;]+)'),
    'c': re.compile('(c__[^;]+)'),
    'o': re.compile('(o__[^;]+)'),
    'f': re.compile('(f__[^;]+)'),
    'g': re.compile('(g__[^;]+)'),
    's': re.compile('(s__[^;]+)'),
}


def mkdir(dirname):
    if os.path.isdir(dirname):
        return None
    if dirname == '':
        return None
    os.system("mkdir -p %s" % dirname)
    return None


def image_trans(pdf, png):
    os.system('convert -density 200 %s %s' % (pdf, png))


def float_trans(string):
    try:
        num = float(string)
    except ValueError:
        return string
    if num >= 0.01:
        value = format(num, '.2f')
    else:
        value = format(num, '.2e')
    if num == 0:
        value = 0
    return value
