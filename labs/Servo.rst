mbed Lab 12 Servos, encoder and ping
####################################
:Date:    2022-05-11 15:00
:Tags:    Labs
:Summary: Learn how to use servos, encoder and ping.

.. sectnum::
	:depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

   The goal of this lab is to learn:

   #. Continuous servo control
   #. Encoder and ping

****************
Lab Due
****************

**May. 11, 2022**

****************
Lab Introduction
****************

In this lab, we will work with servo control (programmable electric
motors).
We will also experiment a few sensing techniques to assist the BB car
to navigate, such as encoder and ping.

.. container:: instruct

   Please google the difference between a standard and continuous servo.
   Basically a standard servo control the rotation degree to certain
   angles, while continuous servo set the speed/direction of the motor (the
   motor will continuously rotate).

***************
Equipment List
***************

#. B_L4S5I_IOT01A * 1
#. Continuous Servo * 2
#. Optical encoder * 2
#. Ping * 1
#. 2.2k-ohm resistor * 1
#. 10k-ohm resistor * 1
#. M3*8mm screws * 2
#. M3 nuts * 2
#. Wheel * 1
#. micro-USB to 5V * 1

***************
Lab Description
***************

Lecture Notes
=============

- Chapter 13: Servo `ch13_servo.pdf <notes/ch13_servo.pdf>`__

Center and Test the Continuous Servos
=====================================

.. container:: warning

    #. For the following steps, please unplug B_L4S5I_IOT01A from power while wiring circuits.

    #. Note that you should not use power servo modules by sources from B_L4S5I_IOT01A.
       Servo may draw a large instaneous current when in operation, which may impact operations of B_L4S5I_IOT01A if sharing the same power source.


#. A servo circuit is shown `here <labs/img/bbcar_installation/bbcar_servo.png>`__. Note that the white line on power supply is GND.

.. container:: warning

    Before you use a continuous servo, you should calibrate it first.
    You should set **speed** to 0 in the code below, and make sure that the servo stay still.
    If not, use a screwdriver to adjust the potentiometer inside the continuous servo until it stay still.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *12_1_Continuous_Servos_Test* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   We use the following code to test servos.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      #define CENTER_BASE 1500

      PwmOut servo(D11);

      void servo_control(int speed) {
         if (speed > 200)       speed = 200;
         else if (speed < -200) speed = -200;

         servo = (CENTER_BASE + speed)/20000.0f;
      }

      int main() {
         servo.period_ms(20);

         while(1) {
            servo_control(100);
            ThisThread::sleep_for(2000ms);
            servo_control(-100);
            ThisThread::sleep_for(2000ms);
         }
      }

   .. container:: instruct

      How does it work?

      #. Above program will run the servo forward and backward continuously due to the changes of PWM signal.

      #. If we set PWM pulse width = 1500us (with a period of 20ms), servo will stay still.
         Otherwise, if < 1500us, servo will rotate clockwise.
         And, if > 1500us, servo will rotate counterclockwise.


#. Compile and run the program.

#. Please change above program to set the servo speed to 0, and calibrate such that the servo does not run at this speed.

#. Push the code to your git remote repository, and check your remote repository for new files.

Optical encoder
===============

.. container:: instruct

   What is an optical encoder?

   An optical rotary encoder is an electro-mechanical device that converts the angular motion to digital signal, using a light shining onto a photodiode through slits.

   Please read the official reference about `Boe-Bot Digital Encoder Kit <labs/doc/mbed12/28107-Boe-Bot-Digital-Encoder-Product-Guide-v2.0.pdf>`__.

.. container:: instruct

   How to test an encoder?

   Optical encoder count the number of times the light is detected through slits.
   For a simple test of the function, swing your hand in front of the sensor and count the sensor values.

#. Connect the encoder

   #. Encoder red <-> B_L4S5I_IOT01A 5V

   #. Encoder black <-> B_L4S5I_IOT01A GND

   #. Encoder white <-> B_L4S5I_IOT01A D11

   #. Encoder white <-> 10k-ohm resistor <-> B_L4S5I_IOT01A 5V

   #. After connection, it will be like this `picture <labs/img/bbcar_installation/bbcar_encoder.jpg>`__

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *12_3_Optical_Encoder* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      BufferedSerial pc(USBTX, USBRX);
      DigitalIn encoder(D11);

      Ticker encoder_ticker;

      volatile int steps;
      volatile int last;

      void encoder_control() {
         int value = encoder;
         if (!last && value) steps++;
         last = value;
      }

      int main() {
         pc.set_baud(9600);
         printf("Before start\r\n");

         encoder_ticker.attach(&encoder_control, .01);

         steps = 0;
         last = 0;

         while(1) {
            ThisThread::sleep_for(2000ms);
            printf("encoder = %d\r\n", steps);
         }
      }

   .. container:: instruct

      How does it work?

      #. After the :hl:`encoder_control` is attached to ticker, mbed program will monitor the encoder pin every 10ms.
         The sensor counts the change from low to high.

#. Compile and run the program.

#. Use your hand to block the encoder on and off, and try to change the recorded encoder value.

#. Push the code to your GitHub repo. 

Ping
====

.. container:: instruct

   What is Ping?

   Ping is an ultrasonic distance sensor. It sends a sound wave to an object, and measure the distance by calculate the time interval between sending the signal and receiving the echo.

   Please read the official reference about `Ping Reference <http://learn.parallax.com/activitybot/build-and-test-ping-sensor-circuit>`__

.. container:: instruct

   How it works?

   #. First, set the pin to output mode and output a 5us pulse.
      After the echo pulse is received (by setting pin to input mode),
      we use a mbed timer to calculate the pulse width.

.. container:: warning

        Notice that ping will not function correctly in the following situations :

        #. Blind zone effect : the distance is shorter than 2 cm.
        #. The sensor is oblique to the object.

        Please check the conclusion part in `this page <https://deepbluembedded.com/ultrasonic-sensor-hc-sr04-pic-microcontrollers-tutorial/>`__ for the detail.

#. Connect the ping

   #. ping red <-> B_L4S5I_IOT01A 5V

   #. ping black <-> B_L4S5I_IOT01A GND

   #. ping white <-> 2.2k-ohm resistor <-> B_L4S5I_IOT01A D11

   #. After connection, it will be like this `picture <labs/img/bbcar_installation/bbcar_ping.jpg>`__

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *12_4_Ping* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      BufferedSerial pc(USBTX, USBRX);
      DigitalInOut ping(D11);
      Timer t;

      int main() {

         float val;
         pc.set_baud(9600);

         while(1) {

            ping.output();
            ping = 0; wait_us(200);
            ping = 1; wait_us(5);
            ping = 0; wait_us(5);

            ping.input();
            while(ping.read() == 0);
            t.start();
            while(ping.read() == 1);
            val = t.read();
            printf("Ping = %lf\r\n", val*17700.4f);
            t.stop();
            t.reset();

            ThisThread::sleep_for(1s);
         }
      }

#. Compile and run the program.

#. Record your results and push the code to your GitHub repo.

Continuous Servos calibration table
===================================

.. container:: warning

   Before you do this part, please make sure that your servos are calibrated.
   In other words, when you set **speed** to 0 in the code in :hl:`4.3 Center and
   Test the Continuous Servos`, the servos should stay still.

.. container:: instruct

   Why do we need calibration table?

   Every servo has different rotation speed even if we give them the same pwm
   signal. We can use the encoder to measure the actual rotation speed by
   inputting several values of PWM, and get a table (for each servo) of PWM v.s
   rotation speed.

#. First, we need to put the encoder and the continuous servo together.

   #. Align the sensor on encoder with center of continuous servo, and lock them with M3*8mm screws and M3 nuts like `this <labs/img/bbcar_installation/encoder_servo1.jpg>`__.

   #. Plug in the wheel and lock with screws like `this <labs/img/bbcar_installation/encoder_servo2.jpg>`__.

#. Wire encoder and servo to Mbed as previous parts like `this <labs/img/bbcar_installation/encoder_servo3.jpg>`__ (encoder:D10, servo:D11). **Notice that GND on encoder, servo, powerbank and Mbed should be wired together**
   If you don't use a powerbank, you can connect servo power source to another USB cable from PC.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *12_5_Continuous_Servos_Table* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.


   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      #define CENTER_BASE 1500

      BufferedSerial pc(USBTX, USBRX);
      DigitalIn encoder(D10);
      PwmOut servo(D11);

      Timer t;
      Ticker encoder_ticker;

      volatile int steps;
      volatile int last;

      void servo_control(int speed) {
         if (speed > 200)       speed = 200;
         else if (speed < -200) speed = -200;

         servo = (CENTER_BASE + speed) / 20000.0f;
      }

      void encoder_control() {
         int value = encoder;
         if (!last && value) steps++;
         last = value;
      }

      int main() {

         pc.set_baud(9600);

         encoder_ticker.attach(&encoder_control, .01);

         servo.period_ms(20);

         int i = 0;
         while (i <= 150) {

            servo_control(i);

            steps = 0;
            t.reset();
            t.start();

            ThisThread::sleep_for(8000ms);

            float time = t.read();

            printf("%1.3f\r\n", (float)steps * 6.5 * 3.14 / 32 / time);

            i += 30;
         }
         servo_control(0);

         while(1);
      }

#. Edit :file:`speed_table.py` Python program.

#. Copy the following codes into :file:`speed_table.py`.

   .. code-block:: python
      :linenos: inline

      import matplotlib.pyplot as plt
      import numpy as np
      import serial

      Ts = 30;   # signal interval
      end = 150; # signal end point
      n = int(end/Ts)+1;

      x = np.linspace(0, end, num=n) # x axis
      y = np.zeros(n)                # y axis

      serdev = '/dev/ttyACM0'
      s = serial.Serial(serdev)

      for i in range(0, n):
          line=s.readline() # Read a string from B_L4S5I_IOT01A terminated with '\n'
          print (line)
          y[i] = float(line)

      plt.figure()
      plt.plot(x,y)
      plt.xlabel('signal')
      plt.ylabel('speed (cm/sec)')
      plt.show()
      s.close()

#. Compile and flash the mbed program.

#. Quit mbed Studio.

#. Replace "serdev" in above :file:`speed_table.py` created by your Operating System for B_L4S5I_IOT01A.

#. Execute above Python script.

   .. container:: warning

    The powerbank will turn off automatically if we only use power line and ground line like this situation, so you have to push the power button every several seconds. **Don't let the powerbank turn off during meaturement!!!!!**. Or you will have to meature it again.

#. The result will be like `this <labs/img/bbcar_installation/servo_table.PNG>`__

#. Screenshot the result, and record the speed values (python output).

#. Push the code to your GitHub repo.

Use of calibration table
========================

.. container:: instruct

   How can we use the calibration table?

   Use a regression curve fitting (numpy can do this) to find a polynomial with proper parameters. We can use the inverse of the polynomial to find a function that convert speed to the real PWM setting.

#. Edit :file:`regression.py`.

   Understand the codes in :file:`regression.py`, and modify :hl:`speed array` according to your results above.

   .. code-block:: python
      :linenos: inline

      import matplotlib.pyplot as plt
      import numpy as np

      Ts = 30;   # signal interval
      end = 150; # signal end point
      n = int(end/Ts)+1; 

      x = np.linspace(0, end, num=n) # signal vector

      # TODO: revise this array to your results
      y = np.array([0.000, 5.900, 10.843, 11.880, 11.401, 12.199]) # speed vector

      z = np.polyfit(x, y, 2) # Least squares polynomial fit, and return the coefficients.

      goal = 7             # if we want to let the servo run at 7 cm/sec
                           # equation : z[0]*x^2 + z[1]*x + z[2] = goal
      z[2] -= goal         # z[0]*x^2 + z[1]*x + z[2] - goal = 0

      result = np.roots(z) # Return the roots of a polynomial with coefficients given

      # output the correct one
      if (0 <= result[0]) and (result[0] <= end):
          print(result[0])
      else:
          print(result[1])

#. Execute :file:`regression.py`

   The program will output a result, which is the speed you need to set in :hl:`main.cpp` when we want to make the servo run at 7 cm/sec.

#. Create a new mbed program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *12_6_use_servo_table* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   Understand the codes in :file:`main.cpp`, and modify :hl:`speed` according to your result above.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      #define CENTER_BASE 1500

      BufferedSerial pc(USBTX, USBRX);
      DigitalIn encoder(D10);
      PwmOut servo(D11);

      Timer t;
      Ticker encoder_ticker;

      volatile int steps;
      volatile int last;

      void servo_control(int speed) {
         if (speed > 200)       speed = 200;
         else if (speed < -200) speed = -200;

         servo=(CENTER_BASE + speed)/20000.0f;
      }

      void encoder_control() {
         int value = encoder;
         if(!last && value) steps++;
         last = value;
      }


      int main() {

         pc.set_baud(9600);

         encoder_ticker.attach(&encoder_control, .01);

         servo.period_ms(20);

         while(1) {

         //TODO: revise this value according to your result
         servo_control(37.222);

         steps = 0;
         t.reset();
         t.start();
         
         ThisThread::sleep_for(8000ms);

         float time = t.read();

         printf("%1.3f\r\n", (float) steps * 6.5 * 3.14 / 32 / time);
         
         }
      }

#. Compile and run the program.

#. You should see the actual result is close to 7.

#. Push the code to your GitHub repo.

.. container:: instruct

   Can you create a PWM table for B_L4S5I_IOT01A to control servo to run at a range of speeds?

********************
Demo and Checkpoints
********************

#. Show your git remote repository.

#. Show the results above (increasing encoder value, ping value and python plot).

#. Show that your two continuous servos are calibrated (when you set **speed** to 0 in the code in :hl:`4.3 Center and Test the Continuous Servos`, the servos should stay still) .

#. The lab above only creates a calibration table when servo rotates in counterclockwise. Please creates the table when servo rotates in clockwise, and let it run at 5 cm/sec in clockwise for 5 seconds, then run at 8 cm/sec in counterclockwise for 5 seconds (actual result +-0.5 cm/sec is acceptable).
