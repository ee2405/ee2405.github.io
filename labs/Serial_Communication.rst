mbed Lab 7 Serial Communication
###############################
:Date:    2022-03-23 15:00
:Tags:    Labs
:Summary: Use mbed's serial interface

.. sectnum::
	:depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

	The goal of this lab is to learn:

	#. Use UART to communicate between two boards
	#. Use I2C to get access to slave module

****************
Lab Due
****************

**Mar. 23, 2022**

****************
Lab Introduction
****************

This lab introduces mbed objects about serial communication: **SPI**,
**BufferedSerial** and **I2C**.  BufferedSerial, usually called UART or RS-232,
is a generic protocol used by computers and electronic modules to send and
receive control information and data. The UART serial link has two uni-directional
asynchronous channels (wires), one for sending and one for receiving. Note that
both ends of the serial links must be configured with the same settings (packet
format and baud rate, etc.).

SPI interface is a synchronous interface (with a MISO, a MOSI, and a clock) to
serially transfer data between a master and a slave device. The transfer is like
connecting two shift registers (of both master and slave): output from a master's
shift register is connected to slave shift register input (MOSI), and also
the slave's shift register output is connected to master's input (MISO). Therefore,
with two data wires and a clock, we can transfer data between master and slave.
SPI can provide a speed of 60M bps for applications.

The I2C interface also provides a synchronous serial channel between masters
and slaves. The I2C has only one data wire and one clock. The data wire will be
used in either write or read mode. The I2C also include an addressing protocol.
I2C usually connects micro-controllers to on-board sensors at low-cost and
low-speed (1-5M bps).

**************
Equipment List
**************

#. B_L4S5I_IOT01A * 1
#. Breadboard * 1
#. Picoscope * 1
#. TextLCD * 1

***************
Lab Description
***************

Lecture Notes
=============

- Chapter 8: Serial Communication `ch8_serial.pdf <notes/ch8_serial.pdf>`__

mbed SPI Self Loopback
=========================

.. container:: warning

        For the following, please unplug B_L4S5I_IOT01A from power while wiring circuits.

#. Use the following SPI pins to connect loop back between two SPI interfaces on the board.
   Note that "PD" pins are at the PMOD connector.

   #. Use SPI1_MOSI(D11)、SPI1_MISO(D12)、SPI1_SCK(D13)、SPI1_CS(D9)、SPI2_MOSI(PD_4)、SPI2_MISO(PD_3)、SPI2_SCK(PD_1)、SPI2_CS(PD_0)
      
      Here is the example about connect SPI to B_L4S5I_IOT01A. `Picture <labs/img/Serial_Communication/SPIboard2.jpg>`__

      .. image:: labs/img/Serial_Communication/SPIboard3.jpg
         :alt: loop back SPI connections 

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *7_1_SPI* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.
   
   We have a SPI Master and Slave to run on two different threads:

   .. code-block:: c++
           :linenos: inline

      #include "mbed.h"

      Thread thread_master;
      Thread thread_slave;

      //master

      SPI spi(D11, D12, D13); // mosi, miso, sclk
      DigitalOut cs(D9);

      SPISlave device(PD_4, PD_3, PD_1, PD_0); //mosi, miso, sclk, cs; PMOD pins

      DigitalOut led(LED3);

      int slave()
      {
         device.format(8, 3);
         device.frequency(1000000);
         //device.reply(0x00); // Prime SPI with first reply
         while (1)
         {
            if (device.receive())
            {
                  int v = device.read(); // Read byte from master
                  printf("First Read from master: v = %0x\n", v);
                  if (v == 0xAA)
                  {                      //Verify the command
                     v = device.read(); // Read another byte from master
                     printf("Second Read from master: v = %d\n", v);
                     v = v + 10;
                     device.reply(v); // Make this the next reply
                     v = device.read(); // Read again to allow master read back
                     led = !led;      // led turn blue/orange if device receive
                  }
                  else
                  {
                     printf("Default reply to master: 0x00\n");
                     device.reply(0x00); //Reply default value
                  };
            }
         }
      }

      void master()
      {
         int number = 0;

         // Setup the spi for 8 bit data, high steady state clock,
         // second edge capture, with a 1MHz clock rate
         spi.format(8, 3);
         spi.frequency(1000000);

         for(int i=0; i<5; ++i){ //Run for 5 times
            // Chip must be deselected
            cs = 1;
            // Select the device by seting chip select low
            cs = 0;

            printf("Send handshaking codes.\n");

            int response = spi.write(0xAA); //Send ID
            cs = 1;                       // Deselect the device
            ThisThread::sleep_for(100ms); //Wait for debug print
            printf("First response from slave = %d\n", response);

            // Select the device by seting chip select low
            cs = 0;
            printf("Send number = %d\n", number);

            spi.write(number); //Send number to slave
            ThisThread::sleep_for(100ms); //Wait for debug print
            response = spi.write(number); //Read slave reply
            ThisThread::sleep_for(100ms); //Wait for debug print
            printf("Second response from slave = %d\n", response);
            cs = 1; // Deselect the device
            number += 1;
         }
      }

      int main()
      {
         thread_slave.start(slave);
         thread_master.start(master);
      }

#. Compile and run the program. The results are `like this <labs/img/Serial_Communication/SPI_result.jpg>`__.
   
#. Record your results and push your codes to github.

mbed UART loopback
==================

.. container:: warning

        For the following, please unplug B_L4S5I_IOT01A from power while wiring circuits.

UART Loopback Connection
------------------------

.. image:: labs/img/Serial_Communication/UART_board.jpg
   :alt: UART crossover connections with Picoscope

#. Connect loop back UART wires between two UART Tx/Rx interfaces.

   #. The :hl:`TX(D10) of master` is connected to the :hl:`RX(D0) of slave`

   #. The :hl:`RX(D9) of master` is connected to the :hl:`TX(D1) of slave`

#. Connect the UART to the picoscope

   #. Connect the picoscope to your computer. `Screenshot <labs/img/Analog_Input/1_1_2.jpg>`__

   #. Connect the first probe to the :hl:`Channel A` `like this <labs/img/Analog_Input/1_1_3.jpg>`__.

   #. Connect the probe to the pin named :hl:`TX(D10)` of master.

mbed UART Loopback Program
--------------------------

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *7_2_UART_loopback* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      
      #define MAXIMUM_BUFFER_SIZE 6
      
      static DigitalOut led1(LED1); // led1 = PA_5
      static DigitalOut led2(LED2); // led2 = PB_14
      
      Thread thread1;
      Thread thread2;
      
      static BufferedSerial device1(D10, D9); // tx, rx  D10:tx  D9:rx
      static BufferedSerial device2(D1, D0);  // tx, rx   D1:tx   D0:rx
      static BufferedSerial serial_port(USBTX, USBRX);
      
      void master_thread() {
        char buf1[MAXIMUM_BUFFER_SIZE] = {'0', '1', '2', '0', '1', '2'};
        printf("Blinking LED1 and LED2 in order twice\n");
        for (int i = 0; i < 6; i++) {
          device1.write(&buf1[i], 1);
          ThisThread::sleep_for(1s);
        }
        printf("Waiting for command from terminal. 0: turn off both. 1: turn on LED1. 2: turn on LED2.\n");
        while(1){
            if (serial_port.readable()) {
                char input;
                uint32_t num = serial_port.read(&input, 1);
                device1.write(&input, 1);
            }
        }
      }
      
      void slave_thread() {
        led1 = 0;
        led2 = 0;

        while (1) {
          char buf2[MAXIMUM_BUFFER_SIZE];
          if (device2.readable()) {
            device2.read(buf2, 1);
       
            if (buf2[0] == '1') {
              led1 = 1;
              led2 = 0;
            } else if (buf2[0] == '2') {
              led1 = 0;
              led2 = 1;
            } else {
              led1 = 0;
              led2 = 0;
            }
            printf("Got: %s\n", buf2);
          }
        }      
      }
      
      int main() {
        // Set desired properties (9600-8-N-1).
        device1.set_baud(9600);
        device1.set_format(
            /* bits */ 8,
            /* parity */ BufferedSerial::None,
            /* stop bit */ 1);
      
        // Set desired properties (9600-8-N-1).
        device2.set_baud(9600);
        device2.set_format(
            /* bits */ 8,
            /* parity */ BufferedSerial::None,
            /* stop bit */ 1);
      
        thread1.start(master_thread);
        thread2.start(slave_thread);
      }
      
#. Compile and flash the program. 

#. Quit Mbed Studio.

#. Start CoolTerm app and connect to board with UART device (e.g. COM7 or /dev/cu.usbmodem14603).
   Set "Local Echo" if you want to see the character you typed into CoolTerm.

#. Rest the board and start the program.

#. Push the reset button on B_L4S5I_IOT01A and the master thread will start and blinking LED1 and LED2 twice,
   and go into a loop to take user input.

   Enter '0' in CoolTerm terminal, the B_L4S5I_IOT01A will turn off both LED1 and LED2.

   Enter '1' in CoolTerm terminal, the B_L4S5I_IOT01A will turn on the LED1 and turn off LED2.

   Enter '2' in CoolTerm terminal, the B_L4S5I_IOT01A will turn on the LED2 and turn off LED1.

#. Record your results and push your codes to github.

Picoscope UART Decoding
------------------------

#. Start the picoscope app.

   #. Select "input range A" as :hl:`+-5V` and collection time as :hl:`1 ms/div`:`screenshot <labs/img/Analog_Input/3_1_1.png>`__

   #. Choose :hl:`Tools` -> :hl:`Serial Decoding` `like this <labs/img/Serial_Communication/step1.png>`__.

   #. Choose :hl:`UART(RS-232, RS-422, RS-485)` `like this <labs/img/Serial_Communication/step2.png>`__ and `this <labs/img/Serial_Communication/step2_2.png>`__.

   #. Choose :hl:`Add`, change :hl:`Data`, :hl:`Baud Rate`, and :hl:`Display` `like this <labs/img/Serial_Communication/step3.png>`__ and `this <labs/img/Serial_Communication/step3_2.png>`__.

#. The UART waveform will show on the monitor.
   The waveform may look like `this <labs/img/Serial_Communication/char_0.png>`__.

#. Record your results and push your codes to github.

Build your own LCD library I2C version
================================================

In this part, we build another library for a I2C version of text LCD.  We only
need two wires (SDA and SDL) for connection as compared to 12-wire interface of
QC1602A.

The program structure of the I2C version is similar to the QC1602A except for 
the I2C interface. In the I2C version, we encode the parallel-wire bits into 
a **char** for both command and data. And then we use i2c.write() to send the 
char to the I2C bus, which will be converted to parallel signals as QC1602A. 


#. Connect your LCD to mbed as the following. `picture <labs/img/Serial_Communication/LCD_board.jpg>`__ .

   .. container:: warning

                  **Please be careful about pin connections. Double check before you turn on the power.**

                  +------------+------------+
                  | LCD        | mbed       |
                  +============+============+
                  | VCC        | 5V         |
                  +------------+------------+
                  | GND        | GND        |
                  +------------+------------+
                  | SDA        | SDA        |
                  +------------+------------+
                  | SCL        | SCL        |
                  +------------+------------+

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *7_3_textLCD_I2C* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "LCD.h"

      int main()
      {
            LCD_init();                     // call the initialise function
            display_to_LCD(0x48);           // ‘H’
            display_to_LCD(0x45);           // ‘E’
            display_to_LCD(0x4C);           // ‘L’
            display_to_LCD(0x4C);           // ‘L’
            display_to_LCD(0x4F);           // ‘O’
            for(char x=0x30;x<=0x39;x++)
            {
                  display_to_LCD(x);      // display numbers 0-9
            }
      }


#. Add a LCD.h under 7_3_textLCD_I2C. And enter the following source code in LCD.h.

   .. code-block:: c++
      :linenos: inline

      #ifndef LCD_H
      #define LCD_H

      #include "mbed.h"


      #define LCD_BUS_I2C_RS (1 << 0)
      #define LCD_BUS_I2C_RW (1 << 1)
      #define LCD_BUS_I2C_E  (1 << 2)
      #define LCD_BUS_I2C_BL (1 << 3)
      #define LCD_BUS_I2C_D4 (1 << 4)
      #define LCD_BUS_I2C_D5 (1 << 5)
      #define LCD_BUS_I2C_D6 (1 << 6)
      #define LCD_BUS_I2C_D7 (1 << 7)
      #define LCD_BUS_I2C_MSK (LCD_BUS_I2C_D4 | LCD_BUS_I2C_D5 | LCD_BUS_I2C_D6 | LCD_BUS_I2C_D7)

      // void toggle_enable(void);      //function to toggle/pulse the enable bit
      void LCD_init(void);             //function to initialise the LCD
      void display_to_LCD(int value);  //function to display characters
      void _setDataBits(int value);
      void _writeByte(int value);
      void _writeCommand(int);


      #endif


#. Add a LCD.cpp under 7_3_textLCD_I2C. And enter the following source code in LCD.cpp.

   .. code-block:: c++
      :linenos: inline

      #include "LCD.h"

      I2C _i2c(D14, D15);
      char _slaveAddress = 0x4E;
      char _lcd_bus;

      void display_to_LCD(int value)
      {
            _lcd_bus |= LCD_BUS_I2C_RS; // Set RS bit
            _i2c.write(_slaveAddress, &_lcd_bus, 1);
            ThisThread::sleep_for(1ms / 1000);
            _writeByte(value);
            ThisThread::sleep_for(40ms / 1000);
      }

      //initialise LCD function
      void LCD_init(void)
      {
            _i2c.frequency(100000);
            ThisThread::sleep_for(20ms);

            _writeCommand(0x02);
            // Controller is now in 4-bit mode

            _writeCommand(0x28); // Function set 001 DL N F - -
                                 //  DL(Data Length)=0 (4 bits bus)
                                 //  N=1 (2 lines)
                                 //  F=0 (5x7 dots font, only option for 2 line display)
                                 //  -  (Don't care)

            ThisThread::sleep_for(10ms);

            // display mode
            _writeCommand(0x0F); // display on, cursor on,  blink on  ; Display Ctrl 0000 1 D C B

            _writeCommand(0x01); // cls, and set cursor to 0
            ThisThread::sleep_for(20ms);

            // _writeCommand(0x80);

            //set cursor blink (0x1)
            // _writeCommand(0x0D);

            // set backlight
            // _lcd_bus |= LCD_BUS_I2C_BL;
            // _i2c.write(_slaveAddress, &_lcd_bus, 1);
      }

      void _setDataBits(int value)
      {

            //Clear all databits
            _lcd_bus &= ~LCD_BUS_I2C_MSK;

            // Set bit by bit to support any mapping of expander portpins to LCD pins
            if (value & 0x01) {     _lcd_bus |= LCD_BUS_I2C_D4;   } // Set Databit

            if (value & 0x02) {     _lcd_bus |= LCD_BUS_I2C_D5;   } // Set Databit

            if (value & 0x04) {     _lcd_bus |= LCD_BUS_I2C_D6;   } // Set Databit

            if (value & 0x08) {     _lcd_bus |= LCD_BUS_I2C_D7;   } // Set Databit
      }

      void _writeByte(int value)
      {
            char data[4];
            _lcd_bus |= LCD_BUS_I2C_E; // Set E bit
            _setDataBits(value >> 4);  // set data high
            data[0] = _lcd_bus;

            _lcd_bus &= ~LCD_BUS_I2C_E; // clear E
            data[1] = _lcd_bus;

            _lcd_bus |= LCD_BUS_I2C_E; // Set E bit
            _setDataBits(value);       // set data low
            data[2] = _lcd_bus;

            _lcd_bus &= ~LCD_BUS_I2C_E; // clear E
            data[3] = _lcd_bus;

            // write the packed data to the I2C portexpander
            _i2c.write(_slaveAddress, data, 4);
      }

      void _writeCommand(int command)
      {
            _lcd_bus &= ~LCD_BUS_I2C_RS; // Reset RS bit
            _i2c.write(_slaveAddress, &_lcd_bus, 1);
            ThisThread::sleep_for(1ms / 1000);
            _writeByte(command);
            ThisThread::sleep_for(40ms / 1000); // most instructions take 40us
      }

#. Compile and run the program. 
   
#. Record your results and push your codes to github.

Import TextLCD library for I2C
================================================

Here we import a I2C TextLCD library to control the text LCD module.
This part is similar to textLCD library in mbed Lab 5 but with an I2C interface for LCD module.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *7_4_textLCD_Library* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Add a library to the current project

   #. Click **+** in the Library tab under program source.

   #. Fill in `https://gitlab.larc-nthu.net/ee2405_2021/textlcd.git`
      And click "Next"

   #. Select "Master" branch and click "Finish"

#. Configure the textLCD library

   Edit :file:`TextLCD_Config.h` under :file:`textlcd`

   Go to line 71, change it from :cmd_host:`#define DEFAULT        1` to :cmd_host:`#define DEFAULT        0`

   Go to line 75, change it from :cmd_host:`#define YWROBOT        0` to :cmd_host:`#define YWROBOT        1`

   So you will have the something like the following

   .. code-block:: c++
      :linenos: inline

      #define DEFAULT        0
      #define ADAFRUIT       0
      #define DFROBOT        0
      #define LCM1602        0
      #define YWROBOT        1
      #define GYLCD          0
      #define MJKDZ          0
      #define SYDZ           0
      #define WIDEHK         0
      #define LCDPLUG        0

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include "TextLCD.h"

      // Host PC Communication channels
      static BufferedSerial pc(USBTX, USBRX); // tx, rx

      // I2C Communication
      I2C i2c_lcd(D14, D15); // SDA, SCL

      //TextLCD_SPI lcd(&spi_lcd, p8, TextLCD::LCD40x4);   // SPI bus, 74595 expander, CS pin, LCD Type
      TextLCD_I2C lcd(&i2c_lcd, 0x4E, TextLCD::LCD16x2);   // I2C bus, PCF8574 Slaveaddress, LCD Type
                                                           //TextLCD_I2C lcd(&i2c_lcd, 0x42, TextLCD::LCD16x2, TextLCD::WS0010); 
                                                           // I2C bus, PCF8574 Slaveaddress, LCD Type, Device Type
                                                           //TextLCD_SPI_N lcd(&spi_lcd, p8, p9);               
                                                           // SPI bus, CS pin, RS pin, LCDType=LCD16x2, BL=NC, LCDTCtrl=ST7032_3V3
      //TextLCD_I2C_N lcd(&i2c_lcd, ST7032_SA, TextLCD::LCD16x2, NC, TextLCD::ST7032_3V3); 
      // I2C bus, Slaveaddress, LCD Type, BL=NC, LCDTCtrl=ST7032_3V3

      FileHandle *mbed::mbed_override_console(int fd)
      {
         return &pc;
      }

      int main()
      {

         printf("LCD Test. Columns=%d, Rows=%d\n\r", lcd.columns(), lcd.rows());

         for (int row = 0; row < lcd.rows(); row++)
         {
            int col = 0;
            printf("MemAddr(Col=%d, Row=%d)=0x%02X\n\r", col, row, lcd.getAddress(col, row));
            //      lcd.putc('-');
            lcd.putc('0' + row);

         for (col = 1; col < lcd.columns() - 1; col++)
         {
            lcd.putc('*');
         }

            printf("MemAddr(Col=%d, Row=%d)=0x%02X\n\r", col, row, lcd.getAddress(col, row));
            lcd.putc('+');
         }

         // Show cursor as blinking character
         lcd.setCursor(TextLCD::CurOff_BlkOn);

         // Set and show user defined characters. A maximum of 8 UDCs are supported by the HD44780.
         // They are defined by a 5x7 bitpattern.
         lcd.setUDC(0, (char *)udc_0); // Show |>
         lcd.putc(0);                  //lcd.putc(0);
         lcd.setUDC(1, (char *)udc_1); // Show <|
         lcd.putc(1);                  //lcd.putc(1);
      }

#. Compile and run the program. 
   
#. Record your results and push your codes to github.

TMP102 with I2C
=====================

TMP102 is a temperature measurement sensor module with a I2C interface.
We also use Picoscope to read the I2C signal patterns from TMP102.

.. container:: warning

        For the following, please unplug B_L4S5I_IOT01A from power while wiring circuits.

Connect to TMP102 with I2C 
----------------------------------

#. Connect B_L4S5I_IOT01A to TMP102.
   
   To connect this I2C sensor to B_L4S5I_IOT01A, we need to connect :hl:`SCL` and :hl:`SDA` to B_L4S5I_IOT01A.
   
   Here is the example about connect I2C to B_L4S5I_IOT01A. `Picture <labs/img/Serial_Communication/new_TMP_.png>`__

Connect Picoscope to I2C 
----------------------------------

#. Connect Picoscope probes to the :hl:`Channel A` and :hl:`Channel B`. 

#. Connect the probe to I2C pins

   - Connect probe A with the pin named :hl:`SDA(D14)` 
        
   - Connect probe B with the pin named :hl:`SCL(D15)`

   .. image:: labs/img/Serial_Communication/new_TMP_.png
      :alt: TMP 102 schematic

Create a Program to Read TMP102
----------------------------------

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *7_5_TMP102* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
           :linenos: inline

      #include "mbed.h"

      I2C m_i2c(D14, D15);
      char m_addr = 0x90;
      int main()
      {
         while (1)
         {
            const char tempRegAddr = 0x00;

            m_i2c.write(m_addr, &tempRegAddr, 1); 
            //Set pointer to the temperature register

            char reg[2] = {0, 0};
            m_i2c.read(m_addr, reg, 2); //Read

            unsigned short res = (reg[0] << 4) | (reg[1] >> 4);
            float temp =  (float) ((float)res * 0.0625);
            printf("Temp code=(%d, %d)\r\n", reg[0], reg[1]);
            printf("Temp = %f.\r\n", temp);
            ThisThread::sleep_for(1s);
         }
      }

#. Compile and run the program. 
   As a result, :hl:`TMP102` will start to return the temperature to your terminal `like this <labs/img/Serial_Communication/I2C_temp.jpg>`__.
   
#. Record your results and push your codes to github.

#. Start the picoscope app

   #. Setup the picoscope

      - Select "input range A" and "input range B" as :hl:`+-5`

      - collection time as :hl:`1 ms/div`
     
      - Number of sample as :hl:`100 kS`  

      - Stop recording and move the view scope to have your target signal to zoom in like `this <labs/img/Serial_Communication/I2C_wave.jpg>`__. 

#. The I2C waveform will shows on the `monitor <labs/img/Serial_Communication/I2C_waveDetail.jpg>`__.    

#. Record your results and push your codes to GitHub repo.

********************
Checkpoints
********************

#. Know how to transfer data via UART.
#. Configure the UART setting, like baud rate.
#. Know how to send command to I2C module.
#. Show your git remote repository.

********************
Reference List
********************

#. `mbed SPI <https://os.mbed.com/docs/mbed-os/v6.15/apis/spi.html>`__
#. `mbed I2C <https://os.mbed.com/docs/mbed-os/v6.15/apis/i2c.html>`__
#. `mbed UART Serial <https://os.mbed.com/docs/mbed-os/v6.15/apis/serial-uart-apis.html>`__
