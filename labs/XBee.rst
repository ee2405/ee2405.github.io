mbed Lab 11 XBee
#########################################
:Date:    2022-05-04 15:00
:Tags:    Labs
:Summary: To establish wireless communication between an embedded Linux board and a micro-controller board.

.. sectnum::
   :depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

   The goal of this lab is to learn:

   #. ZigBee protocol
   #. Programming with ZigBee

****************
Lab Due
****************

**May. 4, 2022**

****************
Lab Introduction
****************

In this lab, we will learn
`the ZigBee standard <http://en.wikipedia.org/wiki/ZigBee>`__
for communications between devices.
ZigBee or XBee for short is a common low-power wireless protocol used
in smart homes.

We use UART interface to work with XBee module.
The XBee module (or similar communication module) usually has a set of "AT" commands (a command string starting with "AT").
These "AT" commands are used to configure parameters of the XBee module.
A few essential "AT" commands will be demonstrated in this lab.

In this lab, we test the following configurations:

#. (Test and configuration) Both XBees on PC (CoolTerm) or One XBee on B_L4S5I_IOT01A (mbed) connected to PC (CoolTerm)
#. (Point to point) One XBee on PC (Python) + The other XBee on B_L4S5I_IOT01A (mbed); We will also try RPC on this configuration.

***************
Equipment List
***************

#. B_L4S5I_IOT01A * 1
#. XBee S2C * 2
#. XBee S2C Adaptor * 2
#. Mini USB to USB * 2
#. Wire * n
#. Breadboard * 1

***************
Lab Description
***************

Lecture Notes
=============

- Chapter 12: Zigbee `ch12_xbee.pdf <notes/ch12_xbee.pdf>`__

Test and configure XBee
=======================

.. container:: instruct

   In this section, we use CoolTerm app to test, configure and control a XBee module.
   We will work in "AT command" mode, in which a command starts with an "AT" string.
   We will try two ways to connect XBee module to a PC:
   (1) XBee modules are plug to the host's USB port `like this <labs/img/XBee/XBee_USB.jpg>`__.
   (2) One XBee module is connected to the mbed B_L4S5I_IOT01A `like this <labs/img/XBee/191359.png>`__ .

Use CoolTerm to configure one XBee chip (A)
----------------------------------------------

#. Plug in the XBee module to the host's USB port with a USB-to-Serial cable `like this <labs/img/XBee/XBee_USB.jpg>`__.
   Our configuration is PC -> USB -> XBee Chip A.

#. Start CoolTerm app and connect to XBee chip with UART device:
   Click **"Options"** and select Port with the pull down menu.
   Note that USB-to-Serial cable will create a UART device like COM* (Windows) or /dev/cu.usbserial-* (Mac OS).

   Also click **"Terminal"** (under "Options") at left panel. Check **"Local Echo"** box.
   This will enable echo back everything you typed to send to the other XBee chip.

   Then click **"Connect"**.

#. Configure MY & DL addresses

   .. container:: instruct

      What are MY and DL?

      :file:`MY (Source Address)`: Sets the address of the node itself (the default value is 0).

      :file:`DL (Destination Low address)`: The destination address of the XBee for which the transmitted packets will be sent (the default value is 0).

      We will use DL to indicate which node receives data.
      A hexadecimal value of FFFF performs a broadcast and sends data to all nodes on the PAN.

      Note that you will get two XBee chips (we call them base XBee and remote XBee;
      The :file:`base` is plugged in our :file:`PC` `like this <labs/img/XBee/XBee_USB.jpg>`__ ,
      and the :file:`remote` is at :file:`mbed B_L4S5I_IOT01A` `like this <labs/img/XBee/191359.png>`__ ).
      Currently, for both chips, we have MY and DL as 0.
      So when you loop back the remote XBee, our network for the two chips are as follows:

      Send from base XBee (DL=0) --> Received by remote XBee (MY=0) --> Send by remote XBee (DL=0) --> Received by base Xbee (MY=0).

   **We need to setup each pair with individual addresses to avoid conflicts.**

   .. container:: instruct

      **How to set MY and DL:**

      Note that you have to use hexadecimal number in the setup.

      Assume seat number = 40 (Decimal).
      **Set MY and DL with your seat number!**
      **No credit for the demo of this lab (1pt) if you don't follow the MY/DL address rules.**

      - XBEE A MY = :hl:`use hexadecimal 0x140`

      - XBEE A DL = :hl:`use hexadecimal 0x240`

      - XBEE B MY = 0x240

      - XBEE B DL = 0x140

      - PAN ID = 0x1

   #. Type :cmd_host:`+++` to enter the AT Command mode. (No :hotkey:`Enter` is necessary).

      Wait 2 more seconds, and you should see “OK.”

      .. container:: instruct

         If "+++" did not return "OK", please simply try again.
	 It sometimes does not work, specially when booting up the first time.

      .. container:: instruct

         The AT command mode will time out in 10 second by default.
	 If time out interrupts your configuration, you may use the following command to 
	 set a longer time out in AT command mode (after "+++"):

         #. :cmd_host:`ATCT 512` (default is 64).

   #. Use :cmd_host:`ATDL xx` to change DL in AT Command mode. 
      For example, if your seat number is 40 in decimal, you can type "ATDL 0x240" in XBee A, and "ATDL 0x140" in XBee B.
      Change above addresses according to your seat number!

   #. Use :cmd_host:`ATMY xx` to change MY in AT Command mode.
      For example, if your seat number is 40 in decimal, you can type "ATMY 0x140" in XBee A, and "ATMY 0x240" in XBee B.

   #. Use :cmd_host:`ATID xx` to change PAN ID in AT Command mode.

   #. Use :cmd_host:`ATWR` to store your setting.

#. Check XBee configuration

   #. Type :cmd_host:`+++` to enter the AT Command mode. 

   #. Use :cmd_host:`ATDL` to display current DL in AT Command mode.

   #. Use :cmd_host:`ATMY` to display current MY in AT Command mode.

   #. Use :cmd_host:`ATCN` to exit AT Command mode.

#. Please keep the CoolTerm app open after configuration, we will use it later.

Use CoolTerm to configure the other XBee chip (B)
--------------------------------------------------

#. Please repeat above process for the second XBee module with another USB-to-Serial cable.
   This configuration is PC -> USB -> XBee Chip B.

#. In CoolTerm app, please click **File -> New** to open a new Window and connect to XBee chip with UART device.
   Click **"Options"** and select Port with the pull down menu for USB serial cable.
   Note that it should be a different device name from XBee Chip A.
   Also set **Echo** for terminal and click **Connect**.

#. Please set correct MY and DL addresses for XBee Chip B.

   .. container:: instruct

      **Set MY and DL for XBee Chip B:**

      Assume seat number = 40 (Decimal).
      **Set MY and DL with your seat number!**
      **No credit for the demo of this lab (1pt) if you don't follow the MY/DL address rules.**

      - XBEE B MY = 0x240

      - XBEE B DL = 0x140

      - PAN ID = 0x1

#. After above two XBees (Chip A and B) are setup. You may now type some messages on either CoolTerm terminal.
   You should see the message appearing right away at the other terminal.

   Note that the configurations of MY/DL are permanently written on the XBee chips, so the above setup only 
   have to be done once for each pair of XBee chips.
   

Use B_L4S5I_IOT01A to test XBee Chip (B)
----------------------------------------------------------------

#. Please wire XBee Chip B to the mbed B_L4S5I_IOT01A `like this <labs/img/XBee/191359.png>`__ .
   Once we connect the USB to B_L4S5I_IOT01A, our configuration is PC -> USB -> B_L4S5I_IOT01A -> XBee Chip B.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *11_1_XBee_config* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   This mbed program works as a pass-through channel from USB to UART (XBee B), 
   which is similar to the above USB-Serial cable.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      static BufferedSerial pc(USBTX, USBRX);
      static BufferedSerial xbee(D1, D0);
      EventQueue queue(32 * EVENTS_EVENT_SIZE);
      Thread t;

      void pc_rx_interrupt(void);
      void pc_rx(void);
      void xbee_rx_interrupt(void);
      void xbee_rx(void);

      int main(){

         pc.set_baud(9600);
         xbee.set_baud(9600);
         printf("Begin test\r\n");
         t.start(callback(&queue, &EventQueue::dispatch_forever));

         // Setup a serial interrupt function of receiving data from pc

         pc.set_blocking(false);
         pc.sigio(mbed_event_queue()->event(pc_rx_interrupt));

         // Setup a serial interrupt function of receiving data from xbee

         xbee.set_blocking(false);
         xbee.sigio(mbed_event_queue()->event(xbee_rx_interrupt));

      }

      void pc_rx_interrupt(void){
         queue.call(&pc_rx);
      }

      void pc_rx(void){
         static int i = 0;
         static char str[50] = {0};
         while(pc.readable()){
            char *c = new char[1];
            pc.read(c, 1);
            if(*c!='\r' && *c!='\n'){

               pc.write(c, 1);
               str[i] = *c;
               i++;
               str[i] = '\r';
               str[i+1] = '\n';
               str[i+2] = '\0';

               if(strncmp(str, "+++", 3) == 0){
                  xbee.write("+++", 3);
                  i = 0;
               }

            }else{
               i = 0;
               xbee.write(str, sizeof(str));
               printf("\r\n");
            }
         }
            ThisThread::sleep_for(1ms);
      }

      void xbee_rx_interrupt(void){
         queue.call(&xbee_rx);
      }

      void xbee_rx(void){
         while(xbee.readable()){
            char *c = new char[1];
            xbee.read(c, 1);
            if(*c!='\r' && *c!='\n'){
               printf("%c",*c);
            }
            else{
               printf("\r\n");
            }
         }
         ThisThread::sleep_for(1ms);
      }

#. Compile and flash the program.

#. Push the reset button on the B_L4S5I_IOT01A and the program will start.

#. In CoolTerm, click **File -> New** to open a new Windows and connect to B_L4S5I_IOT01A.
   Note that this is a different UART device from Chip A or Chip B.
   Do not turn on Echo for this part, because our mbed program automatically return entered characters.

#. The monitor will be `like this <labs/img/XBee/begintest.png>`__ .

#. Check XBee configuration

   #. Type “+++” to enter the AT Command mode. 

   #. Use :cmd_host:`ATDL` to display current DL in AT Command mode.

   #. Use :cmd_host:`ATMY` to display current MY in AT Command mode.

   #. Use :cmd_host:`ATCN` to exit AT Command mode.

#. Again, you may now type some messages on either CoolTerm terminal.
   You should see the message appearing right away at the other terminal.

XBee Programming 
=========================

.. container:: instruct

   The connection of XBee A and B are the same as in previous section:

   In this section, we connect a XBee Chip A to our :file:`PC` `like this <labs/img/XBee/XBee_USB.jpg>`__.
   And the other XBee Chip B is connected to a :file:`mbed B_L4S5I_IOT01A` `like this <labs/img/XBee/191359.png>`__ ).

XBee B (mbed)
---------------------------------------

.. container:: instruct

   Note that after we setup Xbee chips and connect them to either a PC or mbed board,
   the Xbee chips work like a regular UART device. In the following programs, we demonstrate this
   by sending and receiving messages through the UART interface by both mbed and Python.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *11_4_XBee_remote* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   This mbed program will wait for messages from XBee A and it will return the same message back to XBee A.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      
      int main() {
         BufferedSerial serdev(D1, D0, 9600);
      
         //Get a message from remote and resend the message to remote
         char c;
         char instr[128];
         memset(instr, '\0', 128); //clear buffer
         int i=0;
         while(true){
            serdev.read(&c, 1);
            if(c!='\r' && c!='\n'){
               printf("%c",c);
               //prepare echo back
               instr[i]=c;
               i++;
            }
            else{ //Either '\r' or '\n'
              printf("string=%s, strlen=%d.\r\n", instr, strlen(instr));
              //Echo back when eol
              serdev.write(instr,strlen(instr));
              ThisThread::sleep_for(1ms);
              i=0;
              memset(instr, '\0', 128);
            }
         }
      }
      
#. Compile and run the program.

XBee A (Python)
---------------------------------------

#. Edit XBee_host.py and copy the following codes.

   This send messages to XBee B and read back the messages from XBee B.

   .. code-block:: python
      :linenos: inline

      import serial
      import time
      import sys
      
      if len(sys.argv) < 1:
          print ("No port input specified.")
	  sys.exit()
      
      serdev = serial.Serial(sys.argv[1])
      
      for i in range(5):
          print(f"message: {i}")
          outstr="Send message: "+str(i)+"\n" #send only one ENTER 
          serdev.write(outstr.encode())
          time.sleep(0.001)
          line=serdev.readline()
          print(line)

      serdev.close()

#. Start a Terminal app and execute above Python script.
   Replace the device name in the command with COM* (Windows) or /dev/cu.usbserial-* (Mac OS).
   It will be the same UART device we connected above with CoolTerm for Chip A.

   :cmd_host:`python3 XBee_host.py COM*` (Windows) 
   
   or 

   :cmd_host:`python3 XBee_host.py /dev/cu.usbserial-*`  (Mac OS)

#. Please check if you see a message received by both XBee Chips. 

#. Push the code to your GitHub repo.

XBee Application with RPC
=========================

.. container:: instruct

   We use the same XBee connections as in previous section: One XBee on PC (Python) + The other XBee on B_L4S5I_IOT01A (mbed).
   The XBee Chip A is plugged in our :file:`PC` `like this <labs/img/XBee/XBee_USB.jpg>`__ ,
   and the XBee Chip B is connected to :file:`mbed B_L4S5I_IOT01A` `like this <labs/img/XBee/191359.png>`__ ).

#. Please repeat the example in *9_1_erpc_blinky*. You should be able to run the example without any modification.
   However, because XBee is an wireless communication, there may be interference noises. Therefore, it will not be as reliable as a wired UART interface. 
   Some conditions may appear as follows, when running the Python script. Please simply use :hotkey:`Ctrl+C` to stop the Python program and execute it again.

   (1) The Python program stops at one iteration of the loop without any message.

   (2) The Python program stops with the following message: (this means the message has errors during XBee transfer).

       .. class:: terminal

       ::

	  ...
          erpc.client.RequestError: invalid message CRC

   If you see the following terminal message, you have to quit CoolTerm that is connected to the USB serial device of Chip A.

   .. class:: terminal

   ::

      ...
      erial.serialutil.SerialException: [Errno 16] could not open port /dev/cu.usbserial-AC00CNOQ: [Errno 16] Resource busy: '/dev/cu.usbserial-AC00CNOQ'

********************
Demo and Checkpoints
********************

#. Show your git remote repository.

#. Know the configuration and connection of XBee.

#. Send and receive messages with XBee in mbed and Python.

**************
Reference List
**************

#. `XBee S2C User Guide <https://www.digi.com/resources/documentation/digidocs/pdfs/90002002.pdf>`__.
