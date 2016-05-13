from yaml import load, dump, YAMLError

def readYaml(filepath):
    content = None
    try:
        content = load(read(filepath))
    except YAMLError as e:
        print ("An error occured while parsing the yaml file: {0}\n{1}".format(filepath, e))
    return content

def read(filepath):
    content = None
    try:
        with open(filepath) as file:
            content = file.read()
    except FileNotFoundError as e:
        print ("Could not find file: {0}\n {1}".format(filepath, e))
    return content