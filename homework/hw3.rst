Homework 3 TF Lite, WiFi and MQTT
###################################################

:Date:      2022-04-27  15:00
:Tags:      Homework
:Summary:   Homework to use serial port, TF Lite and MQTT in mbed.
:Status: Draft

.. sectnum::
   :depth: 2

.. include:: ../LARC_def.txt

.. contents::

*********************
Prerequisites
*********************

#. **mbed Lab 7 Serial Communication**
#. **mbed Lab 8 Machine Learning on mbed**
#. **mbed Lab 9 Serial RPC**
#. **mbed Lab 10 Wifi and MQTT**

*********************
Submission
*********************

#. Due date: noon, May 5th, 2021

#. Please create your own hw3 github repo.

#. Please push your codes and Readme to your hw3 github repo, and submit `the google form <https://forms.gle/STC5n979tDBxRqho8>`_.

   - The Readme file should explain: (1) how to setup and run your program (2) what are the results

#. **Please find a TA during lab seesion to demo your codes and explain how it works when you are done.**

*********************
Equipment List
*********************

#. PC or notebook
#. B_L4S5I_IOT01A
#. uLCD display

*********************
Homework Description
*********************

- Complete work flow

  #. mbed run a RPC loop with two custom functions (operation modes): (1) gesture UI, and (2) tilt angle detection

  #. PC/Python use RPC over serial to send a command to call gesture UI mode on mbed

     #. The gesture UI function will start a thread function.

     #. In the thread function, user will use gesture to select from a few threshold angles.

     #. After the selection is confirmed with a user button, the selected threshold angle is published through WiFi/MQTT to a broker (run on PC).

     #. After the PC/Python get the published confirmation from the broker, it sends a command to mbed to stop the guest UI mode.
        Therefore, the mbed is back to RPC loop.
	Also PC/Python will show the selection on screen.

  #. PC/Python use RPC over serial to send a command to call tilt angle detection mode on mbed

     #. The tilt angle function will start a thread function.

     #. If the tilt angle is over the selected threshold angle, mbed will publish the event and angle through WiFi/MQTT to a broker.

     #. After the PC/Python get a preset number of tilt events, e.g., 10, from the broker, it sends a command to mbed to stop the tilt detection mode.
        Therefore, the mbed is back to RPC loop.
	Also PC/Python will show all tilt events on screen.

- More about gesture UI mode

  #. Please use LEDs to indicate the start of UI mode.

  #. Please use your gesture TF Lite model from mbed lab 8 to identify user's selection.

  #. The purpose to to select from a list of angles, e.g., 30, 35, 40, 45, etc.

  #. Before confirmation, please show the selection on uLCD (so a user can see their current selection).

- More about tilt angle detection mode 

  #. Please use LEDs to indicate the start of tilt mode.

  #. Before we start the tilt measurement, we should measure the reference acceleration vector.
     Please use LEDs to show this initialization process for a user to place the mbed on table.
     We assume this is the stationary position of the mbed.
     Please use accelerometer to measure this acceleration vector as the reference (the direction should align with gravity).

  #. After we initialize the gravity vector, please use LEDs to indicate for a user to tilt the mbed.
     In this mode, we use the accelerometer vectors to detect the tilt angles for each predefined period, e.g., 100ms.
     A MQTT message will publish if mbed tilts over the selected threshold degree to the stationary position.

  #. For each predefined period (100ms as above), please show the tilt angle on uLCD (so a user can determine how to tilt mbed).
