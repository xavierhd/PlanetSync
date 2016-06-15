

from Utils import FileReader

def getLang(language):
    langfile = "./UI/locale/{0}.yaml".format(language)
    return FileReader.readYaml(langfile)
