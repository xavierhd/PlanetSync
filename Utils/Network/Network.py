def internetExist(self):
    r = requests.head("http://google.ca")
    return str(r.status_code) == '301'



def readIP(self, path):
    ip = None
    try:
        with open(path) as file:
            ip = f.readline()
    except:
        print ("no file named %s" %path)
    return ip