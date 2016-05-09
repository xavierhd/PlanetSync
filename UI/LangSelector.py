from yaml import load, dump

def getLang(language):
	returnData = None
	try:
		with open("./lang/{0}".format(language)) as file:
			returnData = load(file.read())
	except FileNotFoundError as e:
		returnData = -1
	return returnData
		