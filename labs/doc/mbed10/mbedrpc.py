#mbedRPC.py - mbed RPC interface for Python
#
##Copyright (c) 2010 ARM Ltd
##
##Permission is hereby granted, free of charge, to any person obtaining a copy
##of this software and associated documentation files (the "Software"), to deal
##in the Software without restriction, including without limitation the rights
##to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
##copies of the Software, and to permit persons to whom the Software is
##furnished to do so, subject to the following conditions:
## 
##The above copyright notice and this permission notice shall be included in
##all copies or substantial portions of the Software.
## 
##THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
##IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
##FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
##AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
##LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
##OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
##THE SOFTWARE.
#
#Example:
#>from mbedRPC import*
#>mbed = SerialRPC("COM5",9600);
#>myled = DigitalOut(LED1);
#>myled.write(1)
#> 

import serial, urllib2, time

class pin():
        def __init__(self, id):
                self.name = id

LED1 = pin("LED1")
LED2 = pin("LED2")
LED3 = pin("LED3")

a0 = pin("A0")
a1 = pin("A1")
a2 = pin("A2")
a3 = pin("A3")
a4 = pin("A4")
a5 = pin("A5")

D5 = pin("D5")
D6 = pin("D6")
D7 = pin("D7")
D8 = pin("D8")
D9 = pin("D9")
D10 = pin("D10")
D11 = pin("D11")
D12 = pin("D12")
D13 = pin("D13")
D14 = pin("D14")
D15 = pin("D15")



#mbed super class
class mbed:
    def __init__(self):
            print("This will work as a demo but no transport mechanism has been selected")
        
    def rpc(self, name, method, args):
            print("Superclass method not overridden")

#Transport mechanisms, derived from mbed

class SerialRPC(mbed):

    def __init__(self,port, baud):
        self.ser = serial.Serial(port)
        self.ser.setBaudrate(baud)


        def rpc(self, name, method, args):
                self.ser.write("/" + name + "/" + method + " " + " ".join(args) + "\n")
        return self.ser.readline().strip()

class HTTPRPC(mbed):

    def __init__(self, ip):
        self.host = "http://" + ip

    def rpc(self, name, method, args):
        response = urllib2.urlopen(self.host + "/rpc/" + name + "/" + method + "%20" + " ".join(args)) # "%20" means white space!
        return response.read().strip()


#mbed Interfaces

class DigitalOut():

    def __init__(self, this_mbed , mpin):
        self.mbed = this_mbed
        if isinstance(mpin, str):
            self.name = mpin
        elif isinstance(mpin, pin):
            self.name = self.mbed.rpc("DigitalOut", "new", [mpin.name])
 
    def __del__(self):
        r = self.mbed.rpc(self.name, "delete", [])

    def write(self, value):
        r = self.mbed.rpc(self.name, "write", [str(value)])

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return int(r)
      
class AnalogIn():

    def __init__(self, this_mbed , mpin):
        self.mbed = this_mbed
        if isinstance(mpin, str):
            self.name = mpin
        elif isinstance(mpin, pin):
            self.name = self.mbed.rpc("AnalogIn", "new", [mpin.name])

    def __del__(self):
        r = self.mbed.rpc(self.name, "delete", [])
        
    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return float(r)

    def read_u16(self):
        r = self.mbed.rpc(self.name, "read_u16", [])
        return int(r)

class AnalogOut():

    def __init__(self, this_mbed , mpin):
        self.mbed = this_mbed
        if isinstance(mpin, str):
            self.name = mpin
        elif isinstance(mpin, pin):
            self.name = self.mbed.rpc("AnalogOut", "new", [mpin.name])

    def __del__(self):
        r = self.mbed.rpc(self.name, "delete", [])

    def write(self, value):
        r = self.mbed.rpc(self.name, "write", [str(value)])

    def write_u16(self, value):
        r = self.mbed.rpc(self.name, "write_u16", [str(value)])

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return float(r)

class DigitalIn():

    def __init__(self, this_mbed , mpin):
        self.mbed = this_mbed
        if isinstance(mpin, str):
            self.name = mpin
        elif isinstance(mpin, pin):
            self.name = self.mbed.rpc("DigitalIn", "new", [mpin.name])

    def __del__(self):
        r = self.mbed.rpc(self.name, "delete", [])

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return int(r)

class PwmOut():
    
    def __init__(self, this_mbed , mpin):
        self.mbed = this_mbed
        if isinstance(mpin, str):
            self.name = mpin
        elif isinstance(mpin, pin):
            self.name = self.mbed.rpc("PwmOut", "new", [mpin.name])

    def __del__(self):
        r = self.mbed.rpc(self.name, "delete", [])

    def write(self, value):
        r = self.mbed.rpc(self.name, "write", [str(value)])

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return float(r)

    def period(self, value):
        r = self.mbed.rpc(self.name, "period", [str(value)])
        
    def period_ms(self, value):
        r = self.mbed.rpc(self.name, "period_ms", [str(value)])

    def period_us(self, value):
        r = self.mbed.rpc(self.name, "period_us", [str(value)])
        
    def puslewidth(self, value):
        r = self.mbed.rpc(self.name, "pulsewidth", [str(value)])
        
    def puslewidth_ms(self, value):
        r = self.mbed.rpc(self.name, "pulsewidth_ms", [str(value)])

    def puslewidth_us(self, value):
        r = self.mbed.rpc(self.name, "pulsewidth_us", [str(value)])

class Serial():
        
    def __init__(self, this_mbed , tx, rx = ""):
        self.mbed = this_mbed
        if isinstance(tx, str):
            self.name = mpin
        elif isinstance(mpin, pin):
            self.name = self.mbed.rpc("Serial", "new", [tx.name, rx.name])
             
    def __del__(self):
        r = self.mbed.rpc(self.name, "delete", [])

    def putc(self, value):
        r = self.mbed.rpc(self.name, "putc", [str(value)])

    def puts(self, value):
        r = self.mbed.rpc(self.name, "puts", [ "\"" + str(value) + "\""])

    def getc(self):
        r = self.mbed.rpc(self.name, "getc", [])
        return int(r)

class RPCFunction():

    def __init__(self, this_mbed , name):
        self.mbed = this_mbed
        if isinstance(name, str):
            self.name = name

    def __del__(self):
        r = self.mbed.rpc(self.name, "delete", [])

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return int(r)

    def run(self, input):
        r = self.mbed.rpc(self.name, "run", [input])
        return r

class RPCVariable():

    def __init__(self, this_mbed , name):
        self.mbed = this_mbed
        if isinstance(name, str):
            self.name = name

    def __del__(self):
        r = self.mbed.rpc(self.name, "delete", [])

    def write(self, value):
        self.mbed.rpc(self.name, "write", [str(value)])

    def read(self):
        r = self.mbed.rpc(self.name, "read", [])
        return r

def wait(s):
    time.sleep(s)
