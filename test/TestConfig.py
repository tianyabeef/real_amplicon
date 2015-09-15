import sys
sys.path.insert(1,'../src')
import ConfigParser
import time
import re

def readConfig():
    def optionxform(self,str):
        return str
    ConfigParser.RawConfigParser.optionxform = lambda self,str:str
    config = ConfigParser.SafeConfigParser()
    config.readfp(open('analy.cfg'))
    print config.get('analysis2','time.out')
    return config

def writeConfig():
    config = ConfigParser.RawConfigParser()

    try:
        task = {} 
        task["id"] = 1
        task["package"] = "exe"
        task["timeout"] = 150
        task["dst_filename"] = "1.exe"
        task["custom"] = "" 
        config.add_section("analysis2")
        config.set("analysis2", "id", task["id"])
        config.set("analysis2", "target", task["dst_filename"]) 
        config.set("analysis2", "pac kage", task["package"]) 
        config.set("analysis2", "time.out", task["timeout"]) 
        config.set("analysis2", "started", time.asctime()) 
        fp = open("analy.cfg", "w") 
        config.write(fp)
    except ConfigParser.DuplicateSectionError,ex:
        print ex
    except ValueError,ex:
        print ex


if __name__ == '__main__':

    writeConfig()
    readConfig()
