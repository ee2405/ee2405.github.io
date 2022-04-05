Homework 5 Wifi and MQTT
########################
:Date:      2019-05-14  15:00
:Tags:      Homework
:Summary:   Working with Wifi communication in mbed.
:Status:    Draft

.. sectnum::
   :depth: 2

.. include:: ../LARC_def.txt

.. contents::

*********************
Prerequisites
*********************

#. **mbed Lab 9 XBee**

#. **mbed Lab 10 Wifi and MQTT**

*********************
Submission
*********************

#. Due date: noon, May 29, 2019

#. Please submit your homework via Google form.

    - For EE240501 students (Prof. Liou): `EE240501_link <https://forms.gle/1eVY2c8VYTUY885y5>`__.

    - For EE240502 students (Prof. Jong): `EE240502_link <https://forms.gle/qMu8Ek6hcmtfXTHw8>`__.

#. **Please find a grading TA to demo this homework and explain how it works in the class when you are done.**

*********************
Equipment List
*********************

#. PC or notebook
#. FRDM-K66F
#. ESP8266
#. XBee
#. Wires


*********************
Homework Description
*********************

Sensor Data Processing with MQTT
==============================================

#. Please connect your systems as follows (note that we can use the same PC in the following configuration): 

   PC with XBee (Python/lm_sensors) --> K66 with XBee and ESP8266 --> PC with WiFi (Python/MQTT)

#. The PC with XBee will get some kernel information by these commands.

   (This part is to emulate the remote sensors on XBee network).

   #. For VMware users, you can use the command below to get the memory information.

      :cmd_host:`$ free -m`

   #. For native ubuntu users, you can install lm_sensors to measure the core tempurature.

      #. Install lm_sensors

      #. :cmd_host:`$ sudo sensors-detect`

         You may simply answer Yes to all questions (to include all sensors).

      #. :cmd_host:`$ sensors`

         The output will show measured sensor data of your PC.

   #. For mac users, please install `iStats <https://github.com/Chris911/iStats>`__ and use the command below.

      :cmd_host:`$ istats all`

#. Please write a Python script to parse the output of these commands periodically (e.g., every 1s).

   You only need to select a few readings (>=3) based on the output for your PC.

   For example, you can select CPU temp, Core temp, CPU fan speed, MB fan speed to report.

   There is no need to create a general script to handle all possible output formats.

#. Use the same Python script to send sensor data through XBee channels.

#. Connect your K66F board with an XBee module.

   #. Write an mbed code to read from XBee with sensor data.

#. Connect your K66F board with an ESP8266 module.

   #. Write an mbed code on the same K66 to publish sensor data to a Mosquitto server through ESP8266.

#. Write a Python script (this is completely independent to above Python code) to subscribe to above sensor data and plot the output with Matplot (sensor values vs. time).
