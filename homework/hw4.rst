Homework 4 XBee, BB Car 
######################################

:Date:      2022-05-25  15:00
:Tags:      Homework
:Summary:   Working with XBee, BB Car
:Status: Draft

.. sectnum::
   :depth: 2

.. include:: ../LARC_def.txt

.. contents::

*********************
Prerequisites
*********************

#. **mbed Lab 11 XBee**
#. **mbed Lab 13 BOE BOT Car**

*********************
Submission
*********************

#. Due date: noon, June 9th, 2021

#. Please create your own hw4 github repo.

#. Please push your codes and Readme to your hw4 github repo, and submit `the google form <https://forms.gle/mQtj6H91Fmv26zDj9>`_.

   - The Readme file should explain: (1) how to setup and run your program (2) what are the results

#. **Please find a TA during lab seesion to demo your codes and explain how it works when you are done.**

*********************
Equipment List
*********************

#. PC or notebook
#. B_L4S5I_IOT01A
#. XBee chips
#. PING 
#. Encoder
#. Boe Bot Car
#. OpenMV H7 Plus board


*********************
Homework Description
*********************

- **(35pt) XBee Controlled BB Car**

  #. PC/Python sends a RPC command though XBee (with position parameters) to reverse park a BB car.

  #. The BB Car will park automatically according to the position parameters.

  #. The width of parking space is no more than 4cm of BB car width.

  #. BB car could start at different initial positions. 
     Each position can be identified by the relative distance between BB car and the parking space and the car forward-facing direction. 
     For example, in the following figure, we have set the BB car at (d1, d2, west) position. This parameter will be sent
     from PC to mbed for the reverse parking. 

     .. image:: homework/img/hw4-1.png
        :alt: reverse parking

- **(35pt) Line Following BB Car**

  We can use this part to steer the BB car to follow a straight line.

  #. Use OpenMV to detect a straight line (printed on a paper).

  #. Send the parameters of the detected line (end points of lines as x1, y1, x2, y2) to mbed through UART connections.

  #. Steer BB car to go forward and follow the line.

- **(30pt) BB Car Position Calibration**

  We can use this part to identify the location of the BB car with respect to a surface (with an AprilTag).

  #. Print or show an AprilTag (from mbed lab 14).

  #. Please use OpenMV to scan the above AprilTag codes. 
     We can use the scanned AprilTag to determine the viewing angle from OpenMV to the AprilTag surface.

  #. Please steer BB Car such that the car is facing directly and perpendicular to the AprilTag surface.

  #. Also use PING to measure the distance between BB Car and AprilTag surface.

  #. Please show and verify (use a ruler) the distance measured above.


