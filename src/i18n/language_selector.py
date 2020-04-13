

from utils import FileReader


def get_lang(language):
    if language:
        langfile = "./i18n/{0}.yaml".format(language)
        return FileReader.readYaml(langfile)
