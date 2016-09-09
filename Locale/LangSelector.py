

from Utils import FileReader


def getLang(language):
    if language:
        langfile = "./Locale/{0}.yaml".format(language)
        return FileReader.readYaml(langfile)
