mbed Lab 9 Serial RPC
##########################################
:Date:    2022-04-20 15:00
:Tags:    Labs
:Summary: Learn to use remote procedural calls with serial ports

.. sectnum::
	:depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

	The goal of this lab is to learn:

	#. Learn to use remote procedural calls (RPC) with serial ports

****************
Lab Due
****************

**Apr. 20, 2022**

****************
Lab Introduction
****************

A common application of RPC is to send commands to a remote device through serial
communication (or any form of communication like Ethernet). For such a purpose,
it's useful to implement commands based on a RPC library.

***************
Equipment List
***************

#. B-L4S5I-IOT01A * 1

***************
Lab Description
***************

Lecture Notes
=============

- Chapter 10: Remote Procedure Call `ch10_RPC.pdf <notes/ch10_RPC.pdf>`__

Install EPRC Library and Tool
==============================

#. For Windows

   #. Download "Windows.zip" from https://github.com/EmbeddedRPC/erpc/releases and extract it (assuming at ~/Downloads).

   #. Switch to Git Bash app and go to the folder with "erpcgen"

      :cmd_host:`$ cd ~/Downloads/`

      Copy "eprcgen" to ~/Downloads/ for easier reference.

      :cmd_host:`$ cp ./Windows/erpcgen .`

      Test "eprcgen" execution.

      :cmd_host:`$ ./erpcgen -h`

      .. class:: terminal

      ::

        usage: erpcgen [-?|--help] [-V|--version] [-o|--output <filePath>]
               [-v|--verbose] [-I|--path <filePath>] [-g|--generate <language>]
               [-c|--codec <codecType>] files...

        Options:
          -?/--help                    Show this help
          -V/--version                 Display tool version
          -o/--output <filePath>       Set output directory path prefix
          -v/--verbose                 Print extra detailed log information
          -I/--path <filePath>         Add search path for imports
          -g/--generate <language>     Select the output language (default is C)
          -c/--codec <codecType>       Specify used codec type
        
        Available languages (use with -g option):
          c    C/C++
          py   Python

        Available codecs (use with --c option):
          basic   BasicCodec

   #. Download "erpc-develop.zip" from https://github.com/EmbeddedRPC/erpc/ and extract it (assuming at ~/Downloads).
      Please click the green "Code" and select "Download ZIP". (This is the full ERPC source codes).

   #. Start a Git Bash Terminal to install erpc Python library

      :cmd_host:`$ cd ~/Downloads/erpc-develop`

      :cmd_host:`$ cd erpc_python/`

      :cmd_host:`$ pip3 install .`

#. For Mac OS

   #. Download "Mac.zip" from https://github.com/EmbeddedRPC/erpc/releases and extract it (assuming at ~/Downloads).

   #. Start a Terminal app

      :cmd_host:`$ cd ~/Downloads/Mac`

      Make sure "eprcgen" is in the folder with ls.

      :cmd_host:`$ ls`

      Change "eprcgen" execution permission.

      :cmd_host:`$ chmod +x erpcgen`

   #. Use Finder app to locate "eprcgen" (at ~/Downloads/Mac) and, 
      right-click with two fingers to select "Open with Apps" and choose "Terminal".
      Mac OS will show a warning `like this <labs/img/erpc/set_erprcgen_with_permission.png>`__.
      Please click "Open" to set the security permission to execute "eprcgen".
      A terminal will show up and close quickly.

   #. Switch to Terminal app and go to the folder with "erpcgen"

      :cmd_host:`$ cd ~/Downloads/`

      Copy "eprcgen" to ~/Downloads/ for easier reference.

      :cmd_host:`$ cp ./Mac/erpcgen .`

      Test "eprcgen" execution.

      :cmd_host:`$ ./erpcgen -h`

      .. class:: terminal

      ::

        usage: erpcgen [-?|--help] [-V|--version] [-o|--output <filePath>]
               [-v|--verbose] [-I|--path <filePath>] [-g|--generate <language>]
               [-c|--codec <codecType>] files...

        Options:
          -?/--help                    Show this help
          -V/--version                 Display tool version
          -o/--output <filePath>       Set output directory path prefix
          -v/--verbose                 Print extra detailed log information
          -I/--path <filePath>         Add search path for imports
          -g/--generate <language>     Select the output language (default is C)
          -c/--codec <codecType>       Specify used codec type
        
        Available languages (use with -g option):
          c    C/C++
          py   Python

        Available codecs (use with --c option):
          basic   BasicCodec

      If otherwise a warning show up `like this <labs/img/erpc/erprcgen_no_permission.png>`__,
      please try to set the security permission again for "eprcgen" as above or
      explained in https://support.apple.com/en-us/HT202491 for "If you want to open an app 
      that hasn’t been notarized or is from an unidentified developer". You can go to "Settings".
      And under "Security and Privacy" to allow "Open Anyway" for "eprcgen".

   #. Download "erpc-develop.zip" from https://github.com/EmbeddedRPC/erpc/ and extract it (assuming at ~/Downloads).
      Please click the green "Code" and select "Download ZIP". (This is the full ERPC source codes).

   #. Start a Terminal app to install erpc Python library

      :cmd_host:`$ cd ~/Downloads/erpc-develop`

      :cmd_host:`$ cd erpc_python/`

      :cmd_host:`$ pip3 install .`

         
eRPC Over Serial
=================

Introduction to mbed RPC
------------------------

#. What is eRPC?

   **Remote Procedure Call (RPC)** allows a computer program to execute subroutines on another computer. It’s generally used in networks of computing devices. In the case of mbed, you can manipulate variables and execute subroutines on the mbed by simply calling the name of the variable or function on the host computer through a terminal or a browser.

   eRPC is an implementation of RPC for embedded systems. Please read `the introduction <https://github.com/EmbeddedRPC/erpc/wiki>`__ and
   `the Getting Started Chapter <https://github.com/EmbeddedRPC/erpc/wiki/Getting-Started>`__.

Generate eRPC Shim Codes
----------------------------

These are interface codes (objects) to encode and decode the RPC function calls.
These codes are generated automatically from an IDL file (from our blinky example :file:`led-service.erpc`):

.. code-block:: c++
   :linenos: inline

   /*!
    * You can write copyrights rules here. These rules will be copied into the outputs.
    */

   //@outputDir("erpc_outputs") // output directory

   program blink_led; // specify name of output files

   interface LEDBlinkService // cover functions for same topic
   {
       led_on(in uint8 led) -> void
       led_off(in uint8 led) -> void
   }

#. Create a folder :file:`~/Mbed\ Programs/blinky_erpc` to store :file:`led-service.erpc`.
   
#. Start a Terminal app and go to folder :file:`~/Mbed\ Programs/blinky_erpc`

   :cmd_host:`$ cd ~/Mbed\ Programs/blinky_erpc/blinky_erpc`

#. Generate C codes

   :cmd_host:`$ ~/Downloads/erpcgen led-service.erpc`

   :cmd_host:`$ ls`

   .. class:: terminal

   ::

     blink_led.h blink_led_client.cpp blink_led_server.cpp blink_led_server.h led-service.erpc

   Four new files are generated. We will use blink_led.h, blink_led_server.cpp, and blink_led_server.h in 
   our mbed program in the following.

#. Generate Python codes

   :cmd_host:`$ ~/Downloads/erpcgen -g py led-service.erpc`

   A new folder will be created to keep the Python erpc codes:
   We will use these interface codes for the host Python program.

   :cmd_host:`$ ls blink_led/`

   .. class:: terminal

   ::

     __init__.py client.py common.py interface.py server.py

Build a USB Serial Connection
-----------------------------

We will use a USB serial shield to create another USB connection
between mbed and PC host (besides the mbed USBTX and USBRX).
We use this connection to send/receive RPC commands.

#. Use the XBee USB serial shield without the XBee chip.

#. Connect mbed D1 to Rx and mbed D0 to Tx of the USB serial shield.
   Also connect mbed Gnd to Gnd of the USB serial shield.


Create a mbed eRPC server
----------------------------

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *9_1_erpc_blinky* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Add a erpc library to the current project

   #. Click **+** in the Library tab under program source.

   #. Fill in `https://gitlab.larc-nthu.net/ee2405_2022/erpc_c.git`
      And click "Next"

   #. Select "Main" branch and click "Finish"

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include "drivers/DigitalOut.h"

      #include "erpc_simple_server.h"
      #include "erpc_basic_codec.h"
      #include "erpc_crc16.h"
      #include "UARTTransport.h"
      #include "DynamicMessageBufferFactory.h"
      #include "blink_led_server.h"
      
      /**
       * Macros for setting console flow control.
       */
      #define CONSOLE_FLOWCONTROL_RTS     1
      #define CONSOLE_FLOWCONTROL_CTS     2
      #define CONSOLE_FLOWCONTROL_RTSCTS  3
      #define mbed_console_concat_(x) CONSOLE_FLOWCONTROL_##x
      #define mbed_console_concat(x) mbed_console_concat_(x)
      #define CONSOLE_FLOWCONTROL mbed_console_concat(MBED_CONF_TARGET_CONSOLE_UART_FLOW_CONTROL)
      
      mbed::DigitalOut led1(LED1, 1);
      mbed::DigitalOut led2(LED2, 1);
      mbed::DigitalOut led3(LED3, 1);
      mbed::DigitalOut* leds[] = { &led1, &led2, &led3 };
      
      /****** erpc declarations *******/
            
      void led_on(uint8_t led) {
      	if(0 < led && led <= 3) {
      		*leds[led - 1] = 0;
              printf("LED %d is On.\n", led);
      	}
      }
      
      void led_off(uint8_t led) {
	if(0 < led && led <= 3) {
		*leds[led - 1] = 1;
        printf("LED %d is Off.\n", led);
	}
      }
      
      /** erpc infrastructure */
      ep::UARTTransport uart_transport(D1, D0, 9600);
      ep::DynamicMessageBufferFactory dynamic_mbf;
      erpc::BasicCodecFactory basic_cf;
      erpc::Crc16 crc16;
      erpc::SimpleServer rpc_server;
      
      /** LED service */
      LEDBlinkService_service led_service;

      int main(void) {
      
      	// Initialize the rpc server
      	uart_transport.setCrc16(&crc16);
      
      	// Set up hardware flow control, if needed
      #if CONSOLE_FLOWCONTROL == CONSOLE_FLOWCONTROL_RTS
      	uart_transport.set_flow_control(mbed::SerialBase::RTS, STDIO_UART_RTS, NC);
      #elif CONSOLE_FLOWCONTROL == CONSOLE_FLOWCONTROL_CTS
      	uart_transport.set_flow_control(mbed::SerialBase::CTS, NC, STDIO_UART_CTS);
      #elif CONSOLE_FLOWCONTROL == CONSOLE_FLOWCONTROL_RTSCTS
      	uart_transport.set_flow_control(mbed::SerialBase::RTSCTS, STDIO_UART_RTS, STDIO_UART_CTS);
      #endif
      	
        printf("Initializing server.\n");
        rpc_server.setTransport(&uart_transport);
        rpc_server.setCodecFactory(&basic_cf);
        rpc_server.setMessageBufferFactory(&dynamic_mbf);

        // Add the led service to the server
        printf("Adding LED server.\n");
        rpc_server.addService(&led_service);

	// Run the server. This should never exit
        printf("Running server.\n");
        rpc_server.run();
      }

#. Copy blink_led.h, blink_led_server.cpp, and blink_led_server.h in :file:`~/Mbed\ Programs/blinky_erpc/`
   to our mbed program folder (:file:`~/Mbed\ Programs/9_1_erpc_blinky/`).

#. Compile and run the program.

   The following messages will be in the console:

   .. class:: terminal

   ::

     Initializing server.
     Adding LED server.
     Running server.

Create a Python eRPC client
----------------------------

#. Copy the following codes into :file:`led_test_client.py`.
   Also assume the file is in :file:`~/Mbed\ Programs/9_1_erpc_blinky/`.

   .. code-block:: python
      :linenos: inline

      # led_test_client.py
      # Test client for erpc led server example
      # Author: becksteing/Jing-Jia Liou
      # Date: 02/13/2022
      # Blinks LEDs on a connected Mbed-enabled board running the erpc LED server example
      
      from time import sleep
      import erpc
      from blink_led import *
      import sys
      
      if __name__ == "__main__":
      
          if len(sys.argv) != 2:
              print("Usage: python led_test_client.py <serial port to use>")
              exit()
      
          # Initialize all erpc infrastructure
          xport = erpc.transport.SerialTransport(sys.argv[1], 9600)
          client_mgr = erpc.client.ClientManager(xport, erpc.basic_codec.BasicCodec)
          client = client.LEDBlinkServiceClient(client_mgr)

          # Blink LEDs on the connected erpc server
          turning_on = True
          while True:
              for i in range(1, 4):
                  if(turning_on):
                      print("Call led_on ", i)
                      client.led_on(i)
                  else:
                      print("Call led_off ", i)  
                      client.led_off(i)
                  sleep(0.5)
                  
              turning_on = not turning_on

#. Copy folder :file:`blink_led/` in :file:`~/Mbed\ Programs/blinky_erpc/`
   to our mbed program folder (:file:`~/Mbed\ Programs/9_1_erpc_blinky/`).

#. Start a Terminal app

#. Check the USB serial port

   For example, it's "/dev/cu.usbserial-AC00CNOQ" in Mac OS or COM7 in Windows.

   :cmd_host:`$ python3 -m serial.tools.list_ports -v`

#. Run python codes

   :cmd_host:`$ cd ~/Mbed\ Programs/9_1_erpc_blinky/`

   :cmd_host:`$ python3 led_test_client.py /dev/cu.usbserial-AC00CNOQ`

   or 

   :cmd_host:`$ python3 led_test_client.py COM7`

#. The LEDs will blink in order and the following messages will be in Mbed Studio repetitively:

   .. class:: terminal

   ::

     LED 1 is On.
     LED 2 is On.
     LED 3 is On.
     LED 1 is Off.
     LED 2 is Off.
     LED 3 is Off.
     ...

   The following messages will be in Python terminal repetitively:

   .. class:: terminal

   ::

     Call led_on  1
     Call led_on  2
     Call led_on  3
     Call led_off  1
     Call led_off  2
     Call led_off  3
     ...
          
#. Record your results and push the code to your GitHub repo.
 
********************
Demo and Checkpoints
********************

#. Show your git remote repository.
#. Know how to send RPC commands with serial ports.
#. Create a custom RPC function that blink the red led and blue led respectively. (You should modify the RPC Function in the cpp file.)


Reference List
==============

#. `mbed Serial RPC <https://os.mbed.com/teams/mbed/code/mbed-rpc/>`__
