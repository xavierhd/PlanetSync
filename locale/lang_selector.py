

from utils import file_reader

string = None

def setLang(language="english"):
    langfile = "./locale/{0}.yaml".format(language)
    global string
    string = file_reader.readYaml(langfile)
    return string
