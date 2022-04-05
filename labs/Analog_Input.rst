mbed Lab 4 Analog Input
##############################
:Date:    2022-03-2 16:00
:Tags:    Labs
:Summary: Use mbed's AnalogIn class

.. sectnum::
	 :depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

	The goal of this lab is to learn:

	#. Analog input of mbed
	#. Serial communication with PC

****************
Lab Due
****************

**Mar. 2, 2022**

****************
Lab Introduction
****************

The AnalogIn API is used to read (measure) an external voltage applied to an input pin.
An analog to digital converter circuit (ADC) will sample and quantized the signal to digital formats.

Because we need a ADC circuit to read from an analog signal, only certain pins of B_L4S5I_IOT01A are
connected to ADC and capable of making these measurements.
Please check the documentation of B_L4S5I_IOT01A for ADC pins.

***************
Equipment List
***************

#. B_L4S5I_IOT01A * 1
#. PicoScope * 1
#. Wire * 20
#. Breadboard * 1
#. LED * 1

***************
Lab Description
***************

Lecture Notes
=============

- Chapter 5: Analog Input `ch5_adc.pdf <notes/ch5_adc.pdf>`__

Control LED by AnalogOut
========================

.. container:: warning

	For the following, please unplug B_L4S5I_IOT01A from power while wiring circuits.

.. container:: instruct

   For all Mbed and Python programs, please push the source codes to your GitHub repo.

#. Connect the B_L4S5I_IOT01A to the picoscope

   In this configuration, B_L4S5I_IOT01A will read an analog signal and convert it back to analog signal again
   to an output pin. We will observe the output pin with both picoscope and a LED.

   #. Connect the picoscope to your computer. `Screenshot <labs/img/Analog_Input/1_1_2.jpg>`__

   #. Connect the first probe to the :hl:`Channel A` `like this <labs/img/Analog_Input/1_1_3.jpg>`__.

   #. Connect the second probe to the port :hl:`AWG` of picoscope `like this <labs/img/Analog_Input/3_1_4.jpg>`__

   #. Connect the first probe to the pin of :hl:`D7` and the second to the pin of :hl:`A0` . `Screenshot <labs/img/Analog_Input/B_L4S5I_IOT01A_A0_D7_LED.jpg>`__

      .. image:: labs/img/Analog_Input/3_1_LED_Analog_A0_D7_new1.jpg
         :alt: circuit 

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *4_1_LED_Analog* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      AnalogOut Aout(D7);
      AnalogIn Ain(A0);
      int main(){
        while(1){
          Aout = Ain;
        }
      }


#. Compile and run the program

#. Start the picoscope app

#. Setup picoscope to generate a square wave

   #. Select "input range A" as :hl:`+-5` and collection time as :hl:`1 ms/div`:
      `screenshot <labs/img/Analog_Input/3_1_1.png>`__

   #. Generate the `analog signal <labs/img/Analog_Input/3_1_2.png>`__.

      There are many different signal types that we can select.
      Please choose :hl:`square wave` as a demo: `screenshot <labs/img/Analog_Input/3_1_3.png>`__

#. A square wave will show on the `monitor <labs/img/Analog_Input/3_1_6.png>`__.

   Also note that the LED will blink according to the frequency of the square wave.

#. Screenshot your result of picoscope.

Control LED by PwmOut
===============================

.. container:: warning

	For the following, please unplug B_L4S5I_IOT01A from power while wiring circuits.

#. Connect the B_L4S5I_IOT01A to the picoscope

   In this configuration, B_L4S5I_IOT01A will read an analog signal and convert it to a PWM signal again
   to an output pin. We will observe the output pin with both picoscope and a LED.

   #. Connect the picoscope to your computer. `Screenshot <labs/img/Analog_Input/1_1_2.jpg>`__

   #. Connect the first probe to the :hl:`Channel A` `like this <labs/img/Analog_Input/1_1_3.jpg>`__.

   #. Connect the second probe to the port :hl:`AWG` of picoscope `like this <labs/img/Analog_Input/3_1_4.jpg>`__

   #. Connect the first probe to the pin of :hl:`D6` and the second to the pin of :hl:`A0` . `Screenshot <labs/img/Analog_Input/B_L4S5I_IOT01A_A0_D6_LED.jpg>`__

      .. image:: labs/img/Analog_Input/3_2_LED_PWM_A0_D6_new1.jpg
         :alt: circuit 

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *4_2_LED_PWM* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      PwmOut PWM1(D6);
      AnalogIn Ain(A0);
      int main()
      {
         while (1)
         {
            PWM1.period_ms(5);
            PWM1 = Ain;
            printf("%f\n\r", PWM1.read());
            ThisThread::sleep_for(50ms);
         }
      }

#. Compile and run the program

#. Switch to the picoscope app

#. Setup picoscope to generate a sine wave

   #. Select "input range A" as :hl:`+-5` and collection time as :hl:`200 ms/div`:
      `screenshot <labs/img/Analog_Input/4_2_1.jpg>`__

   #. Generate the analog signal.

      Please choose :hl:`sine wave` as a demo: `screenshot <labs/img/Analog_Input/4_2_2.jpg>`__

#. The Output terminal will show the analog input voltage values every 50ms: `like this <labs/img/Analog_Input/4_2_4.jpg>`__.

#. Screenshot your result on the terminal.

#. The PWM signal will shows on the `monitor <labs/img/Analog_Input/4_2_3.jpg>`__.

#. Observe the light of LED. It will be like a :hl:`breathing led`.

#. Screenshot your result of picoscope.

AnalogIn with FFT analysis
==========================

Connect circuit
---------------

.. container:: warning

	For the following, please unplug B_L4S5I_IOT01A from power while wiring circuits.

#. Connect the B_L4S5I_IOT01A to the picoscope

   In this configuration, B_L4S5I_IOT01A will read an analog signal and convert it back to analog signal again
   to an output pin. We will observe the output pin with both picoscope and a LED.

   #. Connect the picoscope to your computer. `Screenshot <labs/img/Analog_Input/1_1_2.jpg>`__

   #. Connect the first probe to the :hl:`Channel A` `like this <labs/img/Analog_Input/1_1_3.jpg>`__.

   #. Connect the second probe to the port :hl:`AWG` of picoscope `like this <labs/img/Analog_Input/3_1_4.jpg>`__

   #. Connect the first probe to the pin of :hl:`D7` and the second to the pin of :hl:`A0` . `Screenshot <labs/img/Analog_Input/B_L4S5I_IOT01A_A0_D7_LED.jpg>`__

      .. image:: labs/img/Analog_Input/3_1_LED_Analog_A0_D7_new1.jpg
         :alt: circuit 

New Mbed program
-----------------------

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *4_4_FFT_analysis* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".


#. Copy the following codes into :file:`main.cpp`.


   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      AnalogOut Aout(D7);
      AnalogIn Ain(A0);

      int sample = 128;
      int i;

      float ADCdata[128];

      int main(){
        for (i = 0; i < sample; i++){
          Aout = Ain;
          ADCdata[i] = Ain;
          ThisThread::sleep_for(1000ms/sample);
        }
        for (i = 0; i < sample; i++){
          printf("%f\r\n", ADCdata[i]);
          ThisThread::sleep_for(100ms);
        }
      }

#. Compile and flash the program.

#. Please quit Mbed Studio, so it does not use the serial port of the B_L4S5I_IOT01A.

Setup Picoscope
-----------------------

#. Start the picoscope

#. Setup picoscope to generate a sine wave

   #. Select "input range A" as :hl:`+-5` and collection time as :hl:`1 s/div`:
      `screenshot <labs/img/Analog_Input/3_2_1.png>`__

   #. Generate the `analog signal <labs/img/Analog_Input/3_1_2.png>`__.

      Please choose :hl:`sine wave`, start frequency :hl:`30 Hz` and set offset to 1V: `screenshot <labs/img/Analog_Input/FFT_30HZ.png>`__

Install Python packages
-----------------------

#. Start a Terminal app in Mac OS or Git Bash in Windows.

#. Install matplotlib

   #. :cmd_host:`$ python3 -m pip install -U matplotlib`

   For Windows, please replace :cmd_host:`python3` with :cmd_host:`python.exe`, if you installed Python from www.python.org. 
   If you use MinGW's Python, the command is the same.
   Also, for Python installed from www.python.org, please check that in Window Path environment variable,
   Path "C:\\msys64\\mingw64\\bin." should be set after "C:\\Users\\<your user name>\\AppData\\Local\\Programs\\Python\\Python310\\"
   in order to use the Windows Python in Git Bash.

   If the installation gives warning about PATH, please add and modify PATH environment variable according to your OS.

#. Install PySerial

   #. :cmd_host:`$ python3 -m pip install pyserial`

   If the installation gives warning about PATH, please add and modify PATH environment variable according to your OS.

#. Copy the following codes into FFT.py in VS code and save the script to :file:`~/Mbed Programs/4_4_FFT_analysis`.

   .. code-block:: python
      :linenos: inline

      import matplotlib.pyplot as plt
      import numpy as np
      import serial
      import time

      Fs = 128.0;  # sampling rate
      Ts = 1.0/Fs; # sampling interval
      t = np.arange(0,1,Ts) # time vector; create Fs samples between 0 and 1.0 sec.
      y = np.arange(0,1,Ts) # signal vector; create Fs samples

      n = len(y) # length of the signal
      k = np.arange(n)
      T = n/Fs
      frq = k/T # a vector of frequencies; two sides frequency range
      frq = frq[range(int(n/2))] # one side frequency range

      serdev = '/dev/ttyACM0'
      s = serial.Serial(serdev)
      for x in range(0, int(Fs)):
          line=s.readline() # Read an echo string from B_L4S5I_IOT01A terminated with '\n'
          # print line
          y[x] = float(line)

      Y = np.fft.fft(y)/n*2 # fft computing and normalization
      Y = Y[range(int(n/2))] # remove the conjugate frequency parts

      fig, ax = plt.subplots(2, 1)
      ax[0].plot(t,y)
      ax[0].set_xlabel('Time')
      ax[0].set_ylabel('Amplitude')
      ax[1].plot(frq,abs(Y),'r') # plotting the spectrum
      ax[1].set_xlabel('Freq (Hz)')
      ax[1].set_ylabel('|Y(freq)|')
      plt.show()
      s.close()

#. Replace "serdev" in above FFT.py created by your Operating System.
   Go to a Terminal app or Git Bash in Windows.

   Use the following command to find the device name of the mbed USB serial connection.

   #. :cmd_host:`$ python3 -m serial.tools.list_ports -v`

      In general, lookup for "STM" or "STLink".

      In Windows, you may get the following message. The **COM3** is the device name.

      .. class:: terminal

      ::

        1 ports found
        COM3
            desc: STMicroelectronics STLink Virtual COM Port (COM3)
            hwid: USB VID:PID=0483:374B SER=0671FF3134354D5043094618 LOCATION=1-3.2:x.2

      In Mac OS, you may get the following message (there are many other devices). The **/dev/cu.usbmodem14603** is the device name.

      .. class:: terminal

      ::

        /dev/cu.usbmodem14603
            desc: STM32 STLink - ST-Link VCP Data
            hwid: USB VID:PID=0483:374B SER=0671FF3134354D5043094618 LOCATION=20-6

#. Execute above Python script in a Terminal app in Mac OS or Git Bash in Windows.

   #. :cmd_host:`$ cd ~/Mbed\ Programs/4_4_FFT_analysis`

   #. :cmd_host:`$ python3 FFT.py`

#. Please push the "Reset" button on B_L4S5I_IOT01A to start the mbed program again.
   Also make sure Picoscope is generating a sine wave signal.

#. The result will be `like this <labs/img/Analog_Input/FFT_30_result.png>`__

#. Generate another signal with other frequency.

   #. Generate the `analog signal <labs/img/Analog_Input/3_1_2.png>`__.

      Please choose :hl:`sine wave`, start frequency :hl:`10 Hz` and set offset to 1V: `screenshot <labs/img/Analog_Input/FFT_10HZ.png>`__

#. Re-execute the Python script, the result will `like this <labs/img/Analog_Input/FFT_10_result.png>`__

#. Save the plot of python code.

Measure the conversion timing
=============================

.. container:: warning

	For the following, please unplug B_L4S5I_IOT01A from power while wiring circuits.

#. Connect the B_L4S5I_IOT01A to the picoscope

   #. Connect the picoscope to your computer. `Screenshot <labs/img/Analog_Input/1_1_2.jpg>`__

   #. Connect the first probe to the :hl:`Channel A` `like this <labs/img/Analog_Input/1_1_3.jpg>`__.

   #. Connect the second probe to the port :hl:`AWG` of picoscope `like this <labs/img/Analog_Input/3_1_4.jpg>`__

   #. Connect the first probe to the pin of :hl:`D7` and the second to the pin of :hl:`A0` . `Screenshot <labs/img/Analog_Input/B_L4S5I_IOT01A_A0_D7.jpg>`__

      .. image:: labs/img/Analog_Input/3_5_Exploring_Nyquist_A0_D7_new.jpg
         :alt: circuit 

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *4_5_Exploring_Nyquist* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      AnalogOut Aout(D7);
      AnalogIn Ain(A0);
      float ADCdata;

      int main(){
        while(1){
          ADCdata = Ain;
          Aout = ADCdata;
          ThisThread::sleep_for(2s);
        }
      }


#. Compile and run the program

#. Switch to the picoscope

#. Setup picoscope to generate a square wave

   #. Select "input range A" as :hl:`+-5` and collection time as :hl:`1 s/div`:
      `screenshot <labs/img/Analog_Input/3_2_1.png>`__

   #. Generate the `analog signal <labs/img/Analog_Input/3_1_2.png>`__.

      Please choose :hl:`sine wave`, set Start Frequency to :hl:`1 HZ` and set offset to 1V. `Screenshot <labs/img/Analog_Input/3_4_4.png>`__

#. Change the sampling rate and observe the difference between each wave

   .. container:: warning

      If the sampling frequency is less than the twice of signal frequecy (The signal frequency is 1 Hz), the signal may not be sampled completely.
      Compare the difference of the following results.

   #. To set sampling frequency, you need to change the wait time.

      .. code-block:: c++

         ThisThread::sleep_for(2s);

   #. Wait time = 2 s, sampling frequency = 0.5 Hz. `Screenshot <labs/img/Analog_Input/wait1.png>`__

   #. Wait time = 200 ms, sampling frequency = 5 Hz. `Screenshot <labs/img/Analog_Input/wait01.png>`__

   #. Wait time = 20 ms, sampling frequency = 50 Hz. `Screenshot <labs/img/Analog_Input/wait001.png>`__

   #. Wait time = 2 ms, sampling frequency = 500 Hz. `Screenshot <labs/img/Analog_Input/wait0001.png>`__

#. Screenshot your result of picoscope.

********************
Demo and Checkpoints
********************

#. Show your git remote repository.

#. Demo the breathing LED.

#. Show all the results you recorded above.

**************
Reference List
**************

#. `Introduction of AnalogIn <https://developer.mbed.org/handbook/AnalogIn>`__
