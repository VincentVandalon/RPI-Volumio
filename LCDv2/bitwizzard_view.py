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
            return map(lambda c:ord(c),s)

        charText = writeString(self.displayedText)
        l2 = charText[:19] + charText[19:38]
        l1 = writeString("*********************") + charText[38:]
        bus.write_i2c_block_data(self.lcdAddress, 0x00, l1[:30])

        bus.write_i2c_block_data(self.lcdAddress, 0x00, l2[:30])
        bus.close()


if __name__ == "__main__":
        # execute only if run as a script
            bw = BitwizzardDisplay()
            bw.setText("asdfasdf")
            bw.setText("This is a test for the display with a longer string")
