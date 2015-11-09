import os

def mkdir(dirname):
    if os.path.isdir(dirname):
        return None
    if dirname == '':
        return None
    os.system("mkdir -p %s"%dirname)
    return None

def image_trans(pdf,png):
    os.system('convert -density 200 %s %s'%(pdf,png))
