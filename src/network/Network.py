import requests

def internet_exist(self):
    r = requests.head("http://google.ca")
    return str(r.status_code) == '301'

def read_IP(self, path):
    ip = None
    try:
        with open(path) as f:
            ip = f.readline()
    except:
        print ("no file named %s" %path)
    return ip