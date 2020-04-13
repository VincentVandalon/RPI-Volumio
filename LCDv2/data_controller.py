import data_model
import bitwizzard_view
import time
from time import gmtime, strftime

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
        status = 'Not playing'
        if s['status'] == 'play':
            status = 'Playing'
        dacState = ''
        if len(s['samplerate'])>2:
            dacState +=str(s['samplerate']) + '@' + str(s['bitdepth'])
        elif 'bitrate' in s.keys():
            dacState += str(s['bitrate'])
        else:
            dacState += '-'

        return "DAC:" +  dacState + '\n' + "Vol: " + self._getVolBar() + '\n' +  status


class NowPlaying(Sheets):
    def __init__(self, dataSource):
        self.dataSource = dataSource

    def getText(self):
        s = self.dataSource.getData()
        processBar = ''
        if s['duration'] > 0:
            curPos = time.gmtime(s['seek']/1000.)
            trackDuration = time.gmtime(s['duration'])
            print(trackDuration)
            processBar = '['+time.strftime('%M:%S',curPos) + '/' + time.strftime('%M:%S',trackDuration) + '] '
        return processBar + s['artist'] + " - " + s['title']

    def canBeShown(self):
        s = self.dataSource.getData()
        return s['status'] == 'play'

class DateMisc(Sheets):
    def __init__(self):
        pass

    def getText(self):
        return strftime("%Y-%m-%d %H:%M", time.localtime())

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

    controller.addSheet(NowPlaying(dataSource))
    controller.addSheet(AudioSettings(dataSource))
    controller.addSheet(DateMisc())
    while True:
        controller.runIt()
