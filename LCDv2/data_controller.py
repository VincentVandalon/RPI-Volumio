import data_model
import bitwizzard_view
import time
import datetime
from time import gmtime, strftime
import uptime
import socket

class Sheets(object):
    def __init__(self):
        pass

    def getText(self):
        pass 

    def canBeShown(self):
        return True

class AudioSettings(Sheets):
    def __init__(self, dataSource):
        self.dataSource = dataSource

    def _getVolBar(self):
        s = self.dataSource.getData()
        solidBars = int(s['volume']) / 10

        s = '['
        sEnd = ']'
        for i in range(10):
            if i < solidBars:
                s += '#'
            else:
                s += ' ' 
                sEnd = ']'
        s += sEnd
        return s

    def getText(self):
        s = self.dataSource.getData()
        status = '[Volumio: '
        if s['status'] in ['pause', 'play']:
            status += 'Playing'
        else:
            status += 'Off'
        status += ']'

        dacState = ''
        if len(s['samplerate'])>2:
            dacState +=str(s['samplerate']) + '@' + str(s['bitdepth'])
        elif 'bitrate' in s.keys():
            dacState += str(s['bitrate'])
        else:
            dacState += '-'

        return status + "\nDAC:" +  dacState + '\nVol: ' + self._getVolBar() + '\n' 


class NowPlaying(Sheets):
    def __init__(self, dataSource):
        self.dataSource = dataSource

    def getText(self):
        s = self.dataSource.getData()
        processBar = ''
        if s['duration'] > 0:
            curPos = time.gmtime(s['seek']/1000.)
            trackDuration = time.gmtime(s['duration'])
            processBar = '['+time.strftime('%M:%S',curPos) + '/' + time.strftime('%M:%S',trackDuration) + '] '
        return processBar + s['artist'] + " - " + s['title']

    def canBeShown(self):
        s = self.dataSource.getData()
        return s['status'] == 'play'

class DateMisc(Sheets):
    def __init__(self):
        pass

    def getText(self):
        def get_ip_address():
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]

        def formatTimeDelta(d):
            return ':'.join(str(d).split(':')[:-1])

        s = strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '\n'
        s += 'Uptime: ' + formatTimeDelta(datetime.timedelta(seconds=uptime.uptime())) + '\n'
        s += 'IP    : ' + str(get_ip_address()).split('.')[-1]
        print(s)
        return s

class SheetController(object):
    def __init__(self, display):
        self.sheets = []
        self.delay = 3
        self.display = display

    def addSheet(self, sheet):
        self.sheets.append(sheet)

    def runIt(self):
        i = 0
        refreshInterval = 10
        for sheet in self.sheets:
            if sheet.canBeShown():
                bw.setText(sheet.getText())
                time.sleep(self.delay)
                i +=1
            if i > refreshInterval:
                bw.clearDisplay()

if __name__ == "__main__":
    # execute only if run as a script
    dataSource = data_model.DataSource()

    bw = bitwizzard_view.BitwizzardDisplay()
    controller = SheetController(bw)

    controller.addSheet(DateMisc())
    controller.addSheet(NowPlaying(dataSource))
    controller.addSheet(AudioSettings(dataSource))
    while True:
        controller.runIt()
