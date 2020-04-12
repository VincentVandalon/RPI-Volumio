import data_model
import bitwizzard_view
import time
from time import gmtime, strftime

class Sheets(object):
    def __init__(self):
        pass

    def getText(self):
        pass 

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
        return str(s['samplerate']) + ' @ ' + str(s['bitdepth']) + '\n' + self._getVolBar()

class NowPlaying(Sheets):
    def __init__(self, dataSource):
        self.dataSource = dataSource

    def getText(self):
        s = self.dataSource.getData()
        return s['artist'] + " - " + s['title']

class DateMisc(Sheets):
    def __init__(self):
        pass

    def getText(self):
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

class SheetController(object):
    def __init__(self, display):
        self.sheets = []
        self.delay = 3
        self.display = display

    def addSheet(self, sheet):
        self.sheets.append(sheet)

    def runIt(self):
        for sheet in self.sheets:
            bw.setText(sheet.getText())
            time.sleep(self.delay)

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
