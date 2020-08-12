
from yaml import load, dump as ydump, YAMLError


def readYaml(filePath):
    content = None
    try:
        content = load(read(filePath))
    except YAMLError as e:
        print ("An error occured while parsing the yaml file: {0}\n{1}".format(filePath, e))
    return content


def read(filePath):
    content = None
    try:
        with open(filePath) as f:
            content = f.read()
    except FileNotFoundError as e:
        print ("Could not find file: {0}\n {1}".format(filePath, e))
    return content

def readLine(filePath):
    content = []
    try:
        with open(filePath) as f:
            content = f.readlines()
    except FileNotFoundError as e:
        print ("Could not find file: {0}\n {1}".format(filePath, e))
    return content

def dump(filePath, content, append=False):
    print(content)
    openOption = "w"

    if append:
        openOption = "w+"

    try:
        with open(filePath, openOption) as file:
            file.write(content)
    except FileNotFoundError as e:
        print ("Could not find file: {0}\n {1}".format(filePath, e))
