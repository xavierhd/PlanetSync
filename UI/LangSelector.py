from yaml import load, dump

def getLang(language):
    returnData = None
    try:
        s = "./UI/lang/{0}.yaml".format(language)
        print (s)
        with open(s) as file:
            returnData = load(file.read())
    except FileNotFoundError as e:
        returnData = -1
    return returnData
