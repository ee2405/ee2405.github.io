mbed Lab 13 BOE BOT Car
#######################
:Date:    2022-05-18 15:00
:Tags:    Labs
:Summary: Use mbed to control Boe-bot car, including servos and related sensors.

.. sectnum::
   :depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

   The goal of this lab is to learn:

   #. A two-wheel robot control
   #. Boe-bot car remote control

****************
Lab Due
****************

**May 18, 2022**

****************
Lab Introduction
****************

In this lab, we will work with servo control (programmable electric
motors) on a Propeller Boe-Bot car, which is a two-wheel robot.
We will also experiment a few sensing techniques to assist the BB car
to navigate, such as PING and accelerometer.

***************
Equipment List
***************

#. B-L4S5I-IOT01A * 1
#. Continuous Servo * 2
#. Optical encoder * 2
#. Ping * 1
#. 2.2k-ohm resistor * 1
#. 10k-ohm resistor * 2
#. M3*8mm screws * 4
#. M3*6mm screws * 6
#. M3 nuts * 4
#. Metal frame
#. Wheel * 2
#. Copper pillar * 3
#. Dupont line * dozens
#. Portable charger
#. USB cable
#. Parallax servo shield
#. Screwdriver
#. USB to pin converter

****************
Lab Description
****************

Assemble Your Propeller Boe-Bot
===============================

.. container:: warning

         For all the following, please unplug B-L4S5I-IOT01A from power while wiring circuits.

.. container:: instruct

   The continuous rotation servos should be calibrated to stay still when
   they receive a specific "stay still" signal before you assemble your
   Prop Boe-Bot. It's a quick and easy procedure. All you have to do is
   connect the servos to B-L4S5I-IOT01A board and run a program that
   sends them the stay-still signal. If a servo turns in response to this
   signal, just use a #1 Phillips screwdriver to adjust its built-in
   feedback potentiometer to make it stop.

   Note that before assembling your Boe-Bot car, you need to calibarate
   both servos. If either assembled servos on Boe-Bot car is not calibrated,
   you will need to disassemble the car for calibration.

   In addition to step-by-step instructions for servo connection and
   calibration, this lesson also includes example programs for speed and
   direction control, speed ramping, and a look inside the signals that
   control a continuous rotation servo's speed and direction.

.. container:: instruct

   If your BB car has been assembled, please skip this section.

#. Car_base

   #. You have to use the following parts, including metal frame and `six M3*6mm screws and three copper pillars <labs/img/bbcar_installation/01_car_base/IMAG0314.jpg>`__.

   #. Install the pillars, then it should become like `this <labs/img/bbcar_installation/01_car_base/IMAG0319.jpg>`__, and `bottom of the model <labs/img/bbcar_installation/01_car_base/IMAG0320.jpg>`__.
   
   .. container:: warning
   
      We can not fit all four copper pillars on the frame, since the B-L4S5I-IOT01A board is too big.

#. Install wheels

   #. The `parts <labs/img/bbcar_installation/02_wheels/IMAG0315.jpg>`__ including plastic wheels, optical encoders, continuous servos, four M3*8mm screws and four M3 nuts.

   #. First, align the sensor on encoder with center of continuous servo like `this <labs/img/bbcar_installation/02_wheels/IMAG0321.jpg>`__. And lock them onto the car. After this step, the car should look like `this <labs/img/bbcar_installation/02_wheels/IMAG0322.jpg>`__.

   #. Second, after the installation of both sides of continuous servos and encoders, plug in the wheels. `Your car <labs/img/bbcar_installation/02_wheels/IMAG0323.jpg>`__ will be able to stand on the table.

   #. Wires may be messy. Pull wires from top of the car and it will be `tidier <labs/img/bbcar_installation/03_battery_box/IMAG0328.jpg>`__.

#. Install the portable charger

   #. Use `Hook-and-loop fastener <https://en.wikipedia.org/wiki/Hook-and-loop_fastener>`__ to join the portable charger and the Car_base together.

#. Install and lock the parallax servo shield, then wire the parts on the breadboard. 

   .. container:: instruct

      Five pins on the USB to pin converter are GND, IO, D+, D-, VBUS. GND is portable charger's ground. VBUS is charger's 5V. D+ and D- are for USB communicate use, we will not use it here.

#. Your Boe Bot car is finished. `Screenshot <labs/img/bbcar_installation/bbcar.jpg>`__

.. container:: warning

   Parallax servo shield board has three power modes. If you want to use the servo
   socket (black) on the top of the board, please select :hl:`MODE 0`, and
   connect V+ of battery box with one of the middle pin. The connection will be

   #. Battery V+ --- middle of servo socket
   #. Battery GND --- any GND on adapting board
   #. Servo signal (white) --- top of servo socket
   #. Servo signal (red) --- middle of servo socket
   #. Servo signal (black) --- bottom of servo socket

   In the following connection, power of battery box is connected to first row of breadboard, and there is another
   wire connect this row into middle of pin10. So the schmatic will be like `this <labs/img/bbcar_installation/adapting.png>`__
   For more detail about schmatic of this adapting board, you can visit its `datasheet <https://www.parallax.com/sites/default/files/downloads/35000-BOE-Shield-Schematic-RevB.pdf>`__

Modulize BBCar Control
======================

.. container:: instruct

   We created a high-level library to wrap the BB Car function for easier handling.

   We make Boe-Bot car go forward with certain speed.
   Note that we use two continuous servo, and they rotate in opposite directions
   to move forward or backward (because the servos face different side of the car).

.. container:: instruct

   We provide three pins only. So you have better use the servo socket (black), and follow the power supply shown above.

#. Connect servos like `this <labs/img/bbcar_installation/bbcar_servo.png>`__. One servo wire to D5, the other wire to D6.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *13_1_Simple_test* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".
   
#. Import BB Car library.

   #. Click **+** in the Library tab under program source.

   #. Fill in "https://gitlab.larc-nthu.net/ee2405_2022/bbcar.git"
      And click "Next"

   #. Select "main" branch and click "Finish"
   
#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include "bbcar.h"

      Ticker servo_ticker;
      PwmOut pin5(D5), pin6(D6);
      BBCar car(pin5, pin6, servo_ticker);

      int main() {
         while(1){
            car.goStraight(200);
            ThisThread::sleep_for(5s);
            car.stop();
            ThisThread::sleep_for(5s);
         }
      }

#. Compile and run the program to test BB Car.

#. Push the code to your GitHub repo. 


#. BB Car control library

   We implemented a damping mechanism in bbcar library. For every movement, instead of abruptly
   set servo motor to new desire speed. We change a small amount of speed every small time interval. If the car
   going to stop when moving, it will stop slowly (in 1s). You can see this `link <https://learn.parallax.com/tutorials/robot/shield-bot/robotics-board-education-shield-arduino/chapter-4-boe-shield-bot-10>`__ for more information. 
   Our implementation in damping is mainly modified in parallex_servo.h and parallax_servo.cpp. You can modify your 
   library if you are not satisfied.


   This is how we implement the library for the part above.
   For more details, please check `the BB Car library <https://gitlab.larc-nthu.net/ee2405_2022/bbcar.git>`__

   In :hl:`bbcar.h` :

   .. code-block:: c++
      :linenos: inline

      class BBCar {
         public:
            BBCar ( PwmOut &pin_servo0, PwmOut &pin_servo1, Ticker &servo_ticker );

            parallax_servo servo0;
            parallax_servo servo1;

            void controlWheel();
            void stop();
            void goStraight ( int speed );

            // turn left/right with a factor of speed
            void turn ( int speed, double factor );

            // limit the value by max and min
            float clamp ( float value, float max, float min );
            int turn2speed ( float turn );
      };


   In :hl:`bbcar.cpp` :

   .. code-block:: c++
      :linenos: inline

      #include "bbcar.h"

      BBCar::BBCar( PwmOut &pin_servo0, PwmOut &pin_servo1, Ticker &servo_ticker ):servo0(pin_servo0), servo1(pin_servo1){
         servo0.set_speed(0);
         servo1.set_speed(0);
         servo_ticker.attach(callback(this, &BBCar::controlWheel), 20ms);
      }

      void BBCar::controlWheel(){
         servo0.control();
         servo1.control();
      }

      void BBCar::stop(){
         servo0.set_speed(0);
         servo1.set_speed(0);
         servo0.set_factor(1);
         servo1.set_factor(1);
      }

      void BBCar::goStraight( double speed ){
         servo0.set_speed(speed);
         servo1.set_speed(-speed);
         servo0.set_factor(1);
         servo1.set_factor(1);
      }

      void BBCar::setCalibTable( int len0, double pwm_table0[], double speed_table0[], int len1, double pwm_table1[], double speed_table1[] ){
         servo0.set_calib_table(len0, pwm_table0, speed_table0);
         servo1.set_calib_table(len1, pwm_table1, speed_table1);
      }
      void BBCar::goStraightCalib ( double speed ){
         servo0.set_speed_by_cm(speed);
         servo1.set_speed_by_cm(-speed);
         servo0.set_factor(1);
         servo1.set_factor(1);
      }

      /*	speed : speed value of servo
         factor: control the speed value with 0~1
                  control left/right turn with +/-
      */
      void BBCar::turn( double speed, double factor ){
         servo0.set_speed(speed);
         servo1.set_speed(-speed);
         if(factor>0){
            servo0.set_factor(factor);
            servo1.set_factor(1);
         }
         else if(factor<0){
            servo0.set_factor(1);
            servo1.set_factor(-factor);
         }
      }

      float BBCar::clamp( float value, float max, float min ){
         if (value > max) return max;
         else if (value < min) return min;
         else return value;
      }

      int BBCar::turn2speed( float turn ){
         return 25+abs(25*turn);
      }


Go Certain Distance
===================

.. container:: instruct

   Optical encoder can be used to track the rotation of wheels, becuase we know the number of
   slits on a wheel. By the total count of detected light transmitting by an encoder, we
   can calculate the number of rotations of wheels. Then we can convert the rotation into
   distance by the wheels.

   Note that it is more accurate to track distance with encoders than just using assigned
   speed of servos, because many factors (mostly friction on the wheel surface and torque of servo)
   will influence the actual rotation.

#. Connect encoder like `this <labs/img/bbcar_installation/bbcar_encoder.jpg>`__, but wire the signal pin to D11.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *13_2_Distance* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".
   
#. Import BB Car library.

   #. Click **+** in the Library tab under program source.

   #. Fill in "https://gitlab.larc-nthu.net/ee2405_2022/bbcar.git"
      And click "Next"

   #. Select "main" branch and click "Finish"
   
#. Copy the following codes into :file:`main.cpp`. 

   We use the code to make the car go about 30cm.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include "bbcar.h"
      BufferedSerial pc(USBTX, USBRX);

      Ticker servo_ticker;
      Ticker encoder_ticker;
      PwmOut pin5(D5), pin6(D6);
      DigitalIn encoder(D11);
      volatile int steps;
      volatile int last;

      BBCar car(pin5, pin6, servo_ticker);
      void encoder_control() {
         int value = encoder;
         if (!last && value) steps++;
         last = value;
      }

      int main() {
         pc.set_baud(9600);
         encoder_ticker.attach(&encoder_control, 10ms);
         steps = 0;
         last = 0;
         car.goStraight(200);
         while(steps*6.5*3.14/32 < 30) {
            // printf("encoder = %d\r\n", steps); 
            ThisThread::sleep_for(100ms);
         }
         car.stop();
      }

#. Compile and test the program.

#. Push the code to your GitHub repo. 

Control BBCar Using Calibration Table
=====================================

#. Connect servos like `this <labs/img/bbcar_installation/bbcar_servo.png>`__. One servo wire to D8, the other wire to D9.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *13_3_BBCar_Calibration* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".
   
#. Import BB Car library.

   #. Click **+** in the Library tab under program source.

   #. Fill in "https://gitlab.larc-nthu.net/ee2405_2022/bbcar.git"
      And click "Next"

   #. Select "main" branch and click "Finish"
   
#. Copy the following codes into :file:`main.cpp`. We use the code to make the car go about 30cm.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include "bbcar.h"

      Ticker servo_ticker;
      PwmOut pin5(D5), pin6(D6);

      BBCar car(pin5, pin6, servo_ticker);

      int main() {
         // please contruct you own calibration table with each servo
         double pwm_table0[] = {-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150};
         double speed_table0[] = {-10.445, -9.812, -9.647, -9.408, -5.900, 0.000, 5.900, 10.843, 11.880, 11.401, 12.199};
         double pwm_table1[] = {-150, -120, -90, -60, -30, 0, 30, 60, 90, 120, 150};
         double speed_table1[] = {-10.445, -9.812, -9.647, -9.408, -5.900, 0.000, 5.900, 10.843, 11.880, 11.401, 12.199};

         // first and fourth argument : length of table
         car.setCalibTable(11, pwm_table0, speed_table0, 11, pwm_table1, speed_table1);

         while (1) {
            car.goStraightCalib(5);
            ThisThread::sleep_for(5s);
            car.stop();
            ThisThread::sleep_for(5s);
         }
      }

#. Generate calibration table by yourself.

   #. Generate calibration tables for two servo with the method in 
      `mbed Lab 12 Servos, encoder and ping <{filename}/labs/Servo.rst>`__

   #. Replace **pwm_table0** and **speed_table0** by your result of first servo in :file:`main.cpp` .

   #. Replace **pwm_table1** and **speed_table1** by your result of second servo in :file:`main.cpp` .

#. Please try to understand the function **set_speed_by_cm()** in :file:`parallax_servo.cpp`.

#. Compile and test the program.

   How does the results compare with the previous section?

#. Push the code to your GitHub repo.

Navigate by Ultrasound (Ping)
=============================

#. Plug the ping on car like `this <labs/img/bbcar_installation/bbcar.jpg>`__ ,and wire it like `this <labs/img/bbcar_installation/bbcar_ping.jpg>`__, but wire the signal pin to D10.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *13_4_Navigate_by_Ultrasound* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".
   
#. Import BB Car library.

   #. Click **+** in the Library tab under program source.

   #. Fill in "https://gitlab.larc-nthu.net/ee2405_2022/bbcar.git"
      And click "Next"

   #. Select "main" branch and click "Finish"

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include "bbcar.h"

      DigitalOut led1(LED1);
      Ticker servo_ticker;
      PwmOut pin5(D5), pin6(D6);
      DigitalInOut pin10(D10);

      BBCar car(pin5, pin6, servo_ticker);

      int main() {
         parallax_ping  ping1(pin10);
         car.goStraight(100);
         while(1) {
            if((float)ping1>10) led1 = 1;
            else {
               led1 = 0;
               car.stop();
               break;
            }
            ThisThread::sleep_for(10ms);
         }
      }


#. Compile and test the program.

#. Push the code to your GitHub repo.

Remote Controlled BOE BOT Car with UART
===========================================

In this part, we send eRPC commands to Boe-Bot car through serial port and XBee.
In the following, we follow basically the same steps as in 
`mbed Lab 9 Serial RPC <{filename}/labs/Serial_RPC.rst>`__
except for the service function calls.

Generate eRPC Shim Codes
----------------------------

These are interface codes (objects) to encode and decode the RPC function calls.
These codes are generated automatically from an IDL file: :file:`bbcar-service.erpc`:

.. code-block:: c++
   :linenos: inline

   program bbcar_control; // specify name of output files

   interface BBCarService // cover functions for same topic
   {
      stop(in uint8 car) -> void //car is an index to a BBCar object
      goStraight(in uint8 car, in int32 speed) -> void
      turn(in uint8 car, in int32 speed, in double factor) -> void
   }

#. Create a folder :file:`~/Mbed\ Programs/bbcar_erpc` to store :file:`bbcar-service.erpc`.
   
#. Start a Terminal app and go to folder :file:`~/Mbed\ Programs/bbcar_erpc`

   :cmd_host:`$ cd ~/Mbed\ Programs/bbcar_erpc`

#. Generate C codes

   :cmd_host:`$ ~/Downloads/erpcgen bbcar-service.erpc`

   :cmd_host:`$ ls`

   .. class:: terminal

   ::

     bbcar-service.erpc		bbcar_control_client.cpp	bbcar_control_server.h
     bbcar_control.h		bbcar_control_server.cpp

   Four new files are generated. We will use bbcar_control.h, bbcar_control_server.cpp, and bbcar_control_server.h in 
   our mbed program in the following.

#. Generate Python codes

   :cmd_host:`$ ~/Downloads/erpcgen -g py bbcar-service.erpc`

   A new folder will be created to keep the Python erpc codes:
   We will use these interface codes for the host Python program.

   :cmd_host:`$ ls bbcar_control/`

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
   Enter *13_5_BBCar_uart_RPC* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Add a erpc library to the current project

   #. Click **+** in the Library tab under program source.

   #. Fill in `https://gitlab.larc-nthu.net/ee2405_2022/erpc_c.git`
      And click "Next"

   #. Select "Main" branch and click "Finish"
   
#. Import BB Car library.

   #. Click **+** in the Library tab under program source.

   #. Fill in "https://gitlab.larc-nthu.net/ee2405_2022/bbcar.git"
      And click "Next"

   #. Select "main" branch and click "Finish"

#. Copy the following codes into :file:`main.cpp`.

   Note that we comment out the actual codes to control the BB Car
   to test the operations by printf on mbed. To run the BB Car,
   please uncomment the control codes.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include "drivers/DigitalOut.h"
      
      #include "erpc_simple_server.h"
      #include "erpc_basic_codec.h"
      #include "erpc_crc16.h"
      #include "UARTTransport.h"
      #include "DynamicMessageBufferFactory.h"
      #include "bbcar_control_server.h"
      /* Uncomment for actual BB Car operations
      #include "bbcar.h"
      
      Ticker servo_ticker;
      PwmOut pin5(D5), pin6(D6);
      
      BBCar car(pin5, pin6, servo_ticker);
      */
      
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
      /* Uncomment for actual BB Car operations
      BBCar* cars[] = {&car}; //Control only one car
      */
      /****** erpc declarations *******/
      
      void stop(uint8_t car){
          if(car == 1) { //there is only one car
      		*leds[car - 1] = 0;
              // Uncomment for actual BB Car operations
              //*cars[car -1].stop();
              printf("Car %d stop.\n", car);
      	}
      }
      
      void goStraight(uint8_t car, int32_t  speed){
          if(car == 1) { //there is only one car
      		*leds[car - 1] = 0;
              // Uncomment for actual BB Car operations
              //*cars[car -1].goStraight(speed);
              printf("Car %d go straight at speed %d.\n", car, speed);
      	}
      }
          
      void turn(uint8_t car, int32_t speed, double factor){
          if(car == 1) { //there is only one car
      		*leds[car - 1] = 0;
              // Uncomment for actual BB Car operations
              //*cars[car -1].turn(speed, factor);
              printf("Car %d turn at speed %d with a factor of %f.\n", car, speed, factor);
      	}
      }
      
      /** erpc infrastructure */
      ep::UARTTransport uart_transport(D1, D0, 9600);
      ep::DynamicMessageBufferFactory dynamic_mbf;
      erpc::BasicCodecFactory basic_cf;
      erpc::Crc16 crc16;
      erpc::SimpleServer rpc_server;
      
      /** LED service */
      BBCarService_service car_control_service;
      
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
        printf("Adding BBCar server.\n");
      	rpc_server.addService(&car_control_service);
      
      	// Run the server. This should never exit
        printf("Running server.\n");
      	rpc_server.run();
      }

#. Copy bbcar_control.h, bbcar_control_server.cpp, and bbcar_control_server.h in :file:`~/Mbed\ Programs/bbcar_erpc/`
   to our mbed program folder (:file:`~/Mbed\ Programs/13_5_BBCar_uart_RPC/`).

#. Compile and run the program.

   The following messages will be in the console:

   .. class:: terminal

   ::

     Initializing server.
     Adding BBCar server.
     Running server.


Using Python to remote control BBCar
---------------------------------------

#. Copy the following codes into :file:`car_control.py`.
   Also assume the file is in :file:`~/Mbed\ Programs/13_5_BBCar_uart_RPC/`.

   .. code-block:: python
      :linenos: inline

      import curses
      import time
      import sys
      import erpc
      from bbcar_control import *
      
      def main():
      
          """
          The curses.wrapper function is an optional function that
          encapsulates a number of lower-level setup and teardown
          functions, and takes a single function to run when
          the initializations have taken place.
          """
      
          if len(sys.argv) != 2:
              print("Usage: python bbcar_control.py <serial port to use>")
              exit()
      
          # Initialize all erpc infrastructure
          global client
          xport = erpc.transport.SerialTransport(sys.argv[1], 9600)
          client_mgr = erpc.client.ClientManager(xport, erpc.basic_codec.BasicCodec)
          client = client.BBCarServiceClient(client_mgr)
      
          curses.wrapper(curses_main)
      
      
      def curses_main(w):
      
          """
          This function is called curses_main to emphasise that it is
          the logical if not actual main function, called by curses.wrapper.
          """
      
          w.addstr("----------------------------------\n")
          w.addstr("| Use arrow keys to control car. |\n")
          w.addstr("| s to stop car and q to exit.   |\n")
          w.addstr("---------------------------------\n")
          w.refresh()
      
          bbcar_control(w)
      
      
      def bbcar_control(w):
          w.nodelay(True)
          while True:
              char = w.getch()
              w.move(5, 0)
              w.clrtobot()
              if char == ord('q'): break  # q
              elif char == curses.KEY_RIGHT: 
                 w.addstr("Turn right.")
                 w.refresh()
                 client.turn(1, 100, -0.3)
              elif char == curses.KEY_LEFT: 
                 w.addstr("Turn left.")
                 w.refresh()
                 client.turn(1, 100, 0.3)
              elif char == curses.KEY_UP: 
                 w.addstr("Go straight.")
                 w.refresh()
                 client.goStraight(1, 100)
              elif char == curses.KEY_DOWN: 
                 w.addstr("Go backward.")
                 w.refresh()
                 client.goStraight(1, -100)
              elif char == ord('s'): 
                 w.addstr("Stop.")
                 w.refresh()
                 client.stop(1)
              else: pass
              time.sleep(0.1)
      
      main()
      
      
   .. container:: instruct
  
      This program uses curses library to control the terminal.

      #. Key UP: go forward
      #. Key DOWN: go backward
      #. Key RIGHT: go right
      #. Key LEFT: go left
      #. Key s: stop
      #. Key q: quit


#. Copy folder :file:`bbcar_control/` in :file:`~/Mbed\ Programs/bbcar_erpc/`
   to our mbed program folder (:file:`~/Mbed\ Programs/13_5_BBCar_uart_RPC/`).

#. Start a Terminal app

#. Check the USB serial port

   Note that USB-to-Serial cable will create a UART device like COM* (Windows) or /dev/cu.usbserial-* (Mac OS).
   For example, it's "/dev/cu.usbserial-AC00CNOQ" in Mac OS or COM7 in Windows.

   :cmd_host:`$ python3 -m serial.tools.list_ports -v`

#. Run python codes

   :cmd_host:`$ cd ~/Mbed\ Programs/13_5_BBCar_uart_RPC/`

   :cmd_host:`$ python3 car_control.py /dev/cu.usbserial-AC00CNOQ`

   or 

   :cmd_host:`$ python3 car_control.py COM7`

   #. Press arrow key on the keyboard to control the car and s to stop the car. And press 'q' to leave the program

      The LEDs will blink and the following messages will show in Mbed Studio according to the key press at Python program:

      .. class:: terminal

      ::

        Car 1 go straight at speed 100.
        Car 1 turn at speed 100 with a factor of -0.3.
        Car 1 go straight at speed 100.
        ...
          
#. Record your results and push the code to your GitHub repo.

Remote Controlled BOE BOT Car with Xbee
========================================

Continuing from previous USB-serial cable control, we can also send RPC commands to Boe-Bot car through Xbee.

#. Connect one of your Xbee to the mbed `like this <labs/img/XBee/191359.png>`__ onto BBCar (Chip B), and plug the other Xbee to the host's USB port (Chip A).

#. Please test previous UART control codes. The programs should run without modification (except for serial device names).

Boe Bot Controls with PID (Optional)
========================================

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *13_8_PID_control* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".
   
#. Import BSP library.

   #. Click **+** in the Library tab under program source.

   #. Fill in `https://gitlab.larc-nthu.net/ee2405_2022/bsp-b-l475e-iot01.git`
      And click "Next"

   #. Select "main" branch and click "Finish"

   #. Delete the following file:
      :file:`bsp-b-l475e-iot01/Drivers/BSP/B-L475E-IOT01/stm32l475e_iot01_qspi.*`
      "*" means any file extension.
   
#. Import BB Car library.

   #. Click **+** in the Library tab under program source.

   #. Fill in "https://gitlab.larc-nthu.net/ee2405_2022/bbcar.git"
      And click "Next"

   #. Select "main" branch and click "Finish"

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include "bbcar.h"
      #include <math.h>
      #include <stdlib.h>
      #include "stm32l475e_iot01_magneto.h"

      #define bound 0.9
      #define PI 3.14159

      BufferedSerial pc(USBTX, USBRX);

      Ticker servo_ticker;
      PwmOut pin5(D5), pin6(D6);
      BBCar car(pin5, pin6, servo_ticker);


      float state[3] = {0};
      float Kp = 0, Ki = 0, Kd = 0;
      float a0 = 0, a1 = 0, a2 = 0;

      //The formula is:
      //y[n] = y[n-1] + A0 * x[n] + A1 * x[n-1] + A2 * x[n-2]
      //A0 = Kp + Ki + Kd
      //A1 = (-Kp ) - (2 * Kd )
      //A2 = Kd
      void pid_init(){
         state[0] = 0;
         state[1] = 0;
         state[2] = 0;
         a0 = Kp + Ki + Kd;
         a1 = (-Kp) - 2*Kd;
         a2 = Kd;
      }
      float pid_process(float in){
         int out = in*a0 + a1*state[0] + a2*state[1] + state[2];

         //update state
         state[1] = state[0];
         state[0] = in;
         state[2] = out;

         return out;
      }

      int main() {
         int16_t pDataXYZ[3] = {0};
         char rotation;
         char buff[256];
         float degree, target_degree, diff;
         FILE *devin = fdopen(&pc, "r");
         FILE *devout = fdopen(&pc, "w");

         //pid control setup
         Kp = 2.0; Ki = 1.0; Kd = 0;
         pid_init();

         // acc sensor setup
         BSP_MAGNETO_Init();

         while(1) {
            ThisThread::sleep_for(100ms);
            // read wanted degree
            for( int i = 0; i < 1; i++ ) {
               rotation = fputc(fgetc(devin), devout);
            }
            for( int i = 0; i < 2; i++ ) {
               buff[i] = fputc(fgetc(devin), devout);
            }
            printf("\r\n");

            int turn = atoi(buff);

            // judge current car degree
            BSP_MAGNETO_GetXYZ(pDataXYZ);
            degree = atan2(pDataXYZ[1], pDataXYZ[0]) * 180 / PI;

            if (rotation == 'l') {
               target_degree = degree - turn;
            } else if (rotation == 'r') {
               target_degree = degree + turn;
            } else {
               target_degree = degree;
            }

            if (target_degree < -180) {
               target_degree = 360 + target_degree;
            } else if (target_degree > 180) {
               target_degree = 360 - target_degree;
            }
            diff = degree - target_degree;

            //The car will continue to turn to the target degree until the error is small enough
            while( abs(diff) > 8) {
               //Process the PID control
               float correction = pid_process(diff);
               //bound the value from -0.9 to -.9
               correction = car.clamp(correction, bound, -bound);
               float turn = (rotation == 'l') ? (1-abs(correction)) : (-1+abs(correction));
               car.turn(car.turn2speed(turn),turn);
               ThisThread::sleep_for(100ms);

               BSP_MAGNETO_GetXYZ(pDataXYZ);
               degree = atan2(pDataXYZ[1], pDataXYZ[0]) * 180 / PI;

               diff = degree - target_degree;
               printf("degree:%f, target: %f, diff:%f \r\n", degree, target_degree, diff);
            }
            car.stop();
            pid_init();
         }
      }

#. Compile and run the program.

#. The portable power bank is made in lithium battery, and it will disturb the magnetometer severely.

   **So you have to hold the portable power bank in hand and let the distance between power bank and the car as far as possible.**

#. Start CoolTerm app and connect to mbed to control the car.

   #. Enter :cmd_host:`l` or :cmd_host:`r` and followed by degrees(00~99) to make the car turn left or right.
      For example, If you want to make the car turn right 30 degrees, please enter :cmd_host:`r30`.

   #. Screenshot the result.

#. Push the code to your GitHub repo. 

********************
Demo and Checkpoints
********************

#. Show your git remote repository.
#. Use xbee to remote control BBCar, and make sure your car can go **straight** forward and backward by using calibration table or other method.

**************
Reference List
**************

#. `Parallax Standard Servo <labs/doc/mbed12/900-00005-Standard-Servo-Product-Documentation-v2.2.pdf>`__, by Parallax Inc.
#. `Parallax Continuous Rotation Servo <labs/doc/mbed12/900-00008-Continuous-Rotation-Servo-Documentation-v2.2.pdf>`__, by Parallax Inc.
#. `Boe-Bot Digital Encoder Kit <labs/doc/mbed12/28107-Boe-Bot-Digital-Encoder-Product-Guide-v2.0.pdf>`__, by Parallax Inc.

.. |CENTER_AND_TEST_THE_SERVOS| image:: notes/lab10/img/center_and_test_the_servos.jpg
