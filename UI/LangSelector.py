

from Utils import FileReader

lang = None

def getLang(language=None):
    if not language and lang:
        language = lang
    if language:
        langfile = "./UI/locale/{0}.yaml".format(language)
        return FileReader.readYaml(langfile)
    else:
        raise Exception("No language selected")
