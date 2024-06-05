import binascii
import sys
sys.path.append('venv/lib/python3.11/site-packages')
from bluepy.btle import Scanner, DefaultDelegate

macaddr = 'xx:xx:xx:xx:xx:xx'

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr == macaddr:
            for (adtype, desc, value) in dev.getScanData():
                if (adtype == 22):
                    servicedata = binascii.unhexlify( value[4:] )

                    isTemperatureAboveFreezing = servicedata[4] & 0b10000000
                    temperature = ( servicedata[3] & 0b00001111 ) / 10 + ( servicedata[4] & 0b01111111 )
                    if not isTemperatureAboveFreezing:
                        temperature = -temperature
                    humidity = servicedata[5] & 0b01111111

                    print( 'temperature: ' + str( temperature ) )
                    print( 'humidity: '    + str( humidity ) )

                    if humidity >= 60:
                         self.control_plugmini(humidity)

    def control_plugmini(self, humidity):
            print('湿度は60%以上です。')

scanner = Scanner().withDelegate( ScanDelegate() )
scanner.scan( 0 )
