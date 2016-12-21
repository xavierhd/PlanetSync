

from Utils import FileReader

string = None

def setLang(language="english"):
    langfile = "./Locale/{0}.yaml".format(language)
    global string
    string = FileReader.readYaml(langfile)
    return string
