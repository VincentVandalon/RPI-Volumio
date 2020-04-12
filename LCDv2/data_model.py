import json
import urllib

class DataSource(object):

    def __init__(self):
        self.stateURL = "http://192.168.1.105:3000/api/v1/getState"

    def getData(self):
        return json.load(urllib.urlopen(self.stateURL))

if __name__ == "__main__":
    dataSource = DataSource()
    print(dataSource.getData()['title'])
