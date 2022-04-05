EE2405 Embedded System Laboratory Midterm Exam (Make Up)
########################################################
:Date:    2019-05-05 15:00
:Tags:    Exams
:Summary: The Midterm Exam (Make Up)
:Status:  Draft

.. sectnum::
   :depth: 2

.. include:: ../LARC_def.txt

.. contents::

*******
Rules
*******

#. Search on the Internet is allowed.

#. Any communication with others is strictly prohibited.

#. To the coding progress, you **must** upload your local history or check in codes to a git repo.
   If you don't know how to record your coding history,
   please go through the instruction
   `here <https://www.ee.nthu.edu.tw/ee240500/exam-preparation.html#record-your-coding-histroy>`__.

#. Please take a photo of each major step of your work.
   If you don't know how to take a photo, please go through the instruction
   `here <https://www.ee.nthu.edu.tw/ee240500/exam-preparation.html#use-cheese-to-take-a-picture>`__.

**********
Submission
**********

* Due time: TBD

* Submit your answer (source codes, local history and photos):

#. `Keyboard Encoder (Multi-Key Keyboard Input) <https://forms.gle/yCWuJcStvMyixejbA>`__

#. `Waveform Loopback <https://forms.gle/UCjRUTSkrAod73fLA>`__

*********
Questions
*********

Keyboard Encoder (50pt)
=======================

.. container:: instruct

   - Please wire the keyboard circuit introduced in `Lab 7 Audio Synthesizer - Keyboard <https://www.ee.nthu.edu.tw/ee240500/mbed-lab-7-integration-lab-audio-synthesis.html#keyboard>`__ first.
   - The number of button is arbitrary, but must be in range from 3 to 7.

Multi-Key Keyboard Function
---------------------------

#. Assume you will use 3 keys on the keyboard. Therefore, we can encode a total of 7 functions (except for 000 pattern).

#. Please map keys to functions listed below:

   #. Part A (20pt): (Choose 2 of them)

      #. Show your student id on the uLCD.

      #. Show binary pattern of the pressed key the uLCD.

      #. Display the values of the accelerometer on the uLCD.

      #. Toggle the blue led.

   #. Part B (30pt): (Choose 2 of them)

      #. Send and print the tilt angle of the accelerometer respect to ground to PC.

      #. Generate from keyboard a 16-bit 0/1 string and send to print with a PC Python program.

      #. Display the date sent from PC on the uLCD.

      #. Display the time sent from PC on the uLCD.

Waveform Loopback (50pt)
==========================

.. container:: instruct

   - Please wire the amplifier circuit introduced in `Lab 7 Audio Synthesizer - Speaker <https://www.ee.nthu.edu.tw/ee240500/mbed-lab-7-integration-lab-audio-synthesis.html##speaker-headphone-with-3-5mm-audio-interface>`__ first.

Hyperbolic Tangent Wave
-----------------------

#. In mbed, generate an analog hyperbolic tangent signal (tanh: https://www.geeksforgeeks.org/numpy-tanh-python/) from DAC.
#. Send the signal from DAC to the amplifier circuit.
#. Sample the amplified output signal by A0.
#. Write a Python program in PC to get the sampled value and then plot the waveform of the sampled signal.
