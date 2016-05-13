

from Utils import FileReader

def getLang(language):
    langfile = "./UI/lang/{0}.yaml".format(language)
    return FileReader.readYaml(langfile)
