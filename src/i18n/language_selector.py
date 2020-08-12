

from utils import file_reader


def get_lang(language):
    if language:
        langfile = "./i18n/{0}.yaml".format(language)
        return file_reader.readYaml(langfile)
