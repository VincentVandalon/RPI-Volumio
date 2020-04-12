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

class BitwizzardDisplay(LCDDisplay):

    def __init__(self):
        super(BitwizzardDisplay, self).__init__()
        self.lcdAddress = 00
        self.clearDisplay()

    def clearDisplay(self):
        bus = smbus.SMBus(1)
        bus.write_byte_data(self.lcdAddress,0x10,1)
        # Backlight
        bus.write_byte_data(self.lcdAddress,0x13,0xfe)
        # Contrast
        bus.write_byte_data(self.lcdAddress,0x12,0x00)
        bus.close()

    def showText(self):
        bus = smbus.SMBus(1)
        # Set cursor
        bus.write_byte_data(self.lcdAddress,0x11,0)
        # Write data
        def writeString(s):
            maxLength = 80
            chars = maxLength*[ord(' ')]
            i = 0
            for c in s:
                chars[i] = ord(c)
                if c == '\n':
                    i = (int(i/10)+1)*10 - 1
                    if i > maxLength:
                        break
                i += 1
            return chars

        charText = writeString(self.displayedText)
        l1 = writeString("")[:20] + charText[20:40]
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
