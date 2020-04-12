import time 
import smbus

class LCDDisplay(object):
    def __init__(self):
        self. displayedText = ''

    def setText(self, newText):
        try:
            if self.displayedText != newText:
                self.displayedText = newText
                self.showText()
        except ValueError as e:
            print(e)
            print('You are trying to displaying a non-string character')

    def showText(self):
        pass
    def clearDisplay(self):
        pass
    def forceRefresh(self):
        pass

class BitwizzardDisplay(LCDDisplay):

    def __init__(self):
        super(BitwizzardDisplay, self).__init__()
        self.lcdAddress = 00
        self.lcdBus = smbus.SMBus(1)
        bus = self.lcdBus
        lastByte = 1
        bytesRead = 0 
        bus.write_byte_data(self.lcdAddress,0x10,1)
        bus.close()

    def showText(self):
        self.lcdBus = smbus.SMBus(1)
        bus = self.lcdBus
        # Set cursor
        bus.write_byte_data(self.lcdAddress,0x11,0)
        # Write data
        def writeString(s):
            chars = 80*[ord(' ')]
            i = 0
            for c in s:
                chars[i] = ord(c)
                i += 1
            return chars

        charText = writeString(self.displayedText)
        l1 = writeString("*******************.")[:20] + charText[20:40]
        l2 = charText[:20] + charText[40:]
        bus.write_i2c_block_data(self.lcdAddress, 0x00, l1[:20])
        time.sleep(0.015)
        bus.write_i2c_block_data(self.lcdAddress, 0x00, l1[20:40])
        time.sleep(0.015)

        bus.write_byte_data(self.lcdAddress,0x11,0x20)
        bus.write_i2c_block_data(self.lcdAddress, 0x00, l2[:20])
        time.sleep(0.015)
        bus.write_i2c_block_data(self.lcdAddress, 0x00, l2[20:40])
        time.sleep(0.015)
        bus.close()


if __name__ == "__main__":
        # execute only if run as a script
            bw = BitwizzardDisplay()
            i = 0
            while i < 10:
                if i%2 ==0:
                    bw.setText("This is a test for the display with a longer string")
                else:
                    bw.setText("Nope")
                time.sleep(0.5)
                i += 1
