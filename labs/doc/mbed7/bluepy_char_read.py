import binascii
import struct
import time
from bluepy.btle import Scanner, DefaultDelegate, UUID, Peripheral

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(5.0)

for dev in devices:
    print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
    for (adtype, desc, value) in dev.getScanData():
        print "  %s = %s" % (desc, value)
 
dev_name_uuid = UUID(0x2A00)
battery_uuid = UUID(0x2A19)
 
p = Peripheral("00:1e:c0:37:76:08", "public")
 
try:
    ch1 = p.getCharacteristics(uuid=dev_name_uuid)[0]
    if (ch1.supportsRead()):
        
        val = binascii.b2a_hex(ch1.read())
        val = binascii.unhexlify(val)
        #val = struct.unpack('s', val)[0]
        print "Device name: " + str(val)
 
    ch2 = p.getCharacteristics(uuid=battery_uuid)[0]
    if (ch2.supportsRead()):
        while 1:
           val = binascii.b2a_hex(ch2.read())
           val = int(val,16)
           #val = struct.unpack('!2s', val)[0]
           print "Battery Level: " + str(val) + " %"
           time.sleep(1)  
            
finally:
    p.disconnect()
