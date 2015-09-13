import ConfigParser
import time

def readConfig():
    def optionxform(self,str):
        return str
    ConfigParser.RawConfigParser.optionxform = optionxform
    config = ConfigParser.SafeConfigParser()
    config.readfp(open('default.conf'))
    for item in config.items('environment'):
        print item[0] + '=' + item[1]


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
        config.set("analysis2", "package", task["package"]) 
        config.set("analysis2", "timeout", task["timeout"]) 
        config.set("analysis2", "started", time.asctime()) 
        fp = open("analy.conf", "w") 
        config.write(fp)
    except ConfigParser.DuplicateSectionError,ex:
        print ex
    except ValueError,ex:
        print ex


if __name__ == '__main__':
    readConfig()
