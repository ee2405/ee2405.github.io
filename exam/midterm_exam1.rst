EE240501 Embedded System Laboratory Midterm Exam
################################################
:Date:    2019-05-01 15:00
:Tags:    Exams
:Summary: The Midterm Exam (EE240501)
:Status:  Draft

.. sectnum::
    :depth: 2

.. include:: ../LARC_def.txt

.. contents::

*******
Rule
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

* Due time: 18:00, May 1st, 2019

* Submit your answer (source codes, local history and photos):

#. `Keyboard Encoder (Multi-Key Keyboard Input) <https://forms.gle/MtyNdao2WPquiXUy6>`__

#. `Keyboard Encoder (Message Encoder) <https://forms.gle/67m7gSVcBV1E6STX7>`__

#. `Waveform Loopback <https://forms.gle/FbcvrXfJzyaNFLc27>`__

*********
Questions
*********

Keyboard Encoder (50pt)
=======================
There are 2 parts in this problem.

.. container:: instruct

   - Please wire the keyboard circuit introduced in `Lab 7 Audio Synthesizer - Keyboard <https://www.ee.nthu.edu.tw/ee240500/mbed-lab-7-integration-lab-audio-synthesis.html#keyboard>`__ first.
   - The number of button is arbitrary, but must be in range from 3 to 7.

Multi-Key Keyboard Input (20pt)
-------------------------------

#. Please push buttons on your keyboards (multiple keys may be used at the same time) for at least 4 times.
   Please add up all binary numbers and print the total summation on the uLCD.
   For example, if you have 3 keys, and the following binary patterns are generated from the keyboard as follows:
   101, 010, 111, 011. If we sum up the numbers, it will be 10001. We should see 0b10001 on the uLCD screen.
   We only need to consider positive binary patterns. However, please note that the sum may need more bits than keys
   (as shown in the above example).

Message Encoder (30pt)
----------------------

#. Please write a Python code to send a char string to mbed.

#. A mbed program will encode the char string by taking the XOR of the string and binary sum generated above.
   If the bit numbers of the sum is shorter than the string, please simply replicate sum pattern to cover all 8 bits in
   a char. For example, the ASCII of 'C' is 01000011 and the sum pattern is 10001. We first extend 10001 to 8 bits:
   10001+100=10001100 (the extension method is arbitrary of your choice). The encoded 'C'= 01000011 XOR 10001100=11001111.

#. Use a Python program to read the encoded string and sum.
   Please decode the string and print both encoded and decoded string on the screen.
   Note that encoded chars may not be printable on the screen. Please print their hexadecimal values instead.
   For example, in the above, we have encoded 'C' as 11001111. So we will print 0xCF.
   Please print out chars and values as in the following format ("CODE" is the string to be encoded):

   .. class:: terminal

   ::

      Input: "CODE"
      Sum Key: 0x8C
      'C': 0x43 --> 0xCF
      'O': 0x4F --> 0xC3
      'D': 0x44 --> 0xC8
      'E': 0x45 --> 0xC9

Waveform Loopback (50pt)
========================

.. container:: instruct

   - Please wire the amplifier circuit introduced in `Lab 7 Audio Synthesizer - Speaker <https://www.ee.nthu.edu.tw/ee240500/mbed-lab-7-integration-lab-audio-synthesis.html##speaker-headphone-with-3-5mm-audio-interface>`__ first.

Sinc Wave
---------

#. In mbed, generate an analog sinc wave (sinc: https://www.geeksforgeeks.org/numpy-sinc-in-python/) from DAC.
   The waveform should be like `this <exam/img/q2_sinc.png>`__.

#. Send the signal from DAC to the amplifier circuit.

#. Sample the amplified output signal by A0.

#. Write a Python program on PC to get the sampled value and then plot the frequency domain spectrum of the
   sampled signal.
