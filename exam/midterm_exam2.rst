EE240502 Embedded System Laboratory Midterm Exam
##################################################
:Date:    2019-04-30 15:00
:Tags:    Exams
:Summary: The Midterm Exam (EE240502)
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

* Due time: 18:00, April 30th, 2019

* Submit your answer (source codes, local history and photos):

#. `Keyboard Encoder (Multi-Key Keyboard Input) <https://forms.gle/UqjUVe3PEQ5wSUeh6>`__

#. `Keyboard Encoder (Message Bits Logger) <https://forms.gle/nnmxndhoRHPJT43Y9>`__

#. `Waveform Loopback <https://forms.gle/kicovTq3ybsLHH8Q8>`__

*********
Questions
*********

Keyboard Encoder (50pt)
=======================
There are 2 parts in this question.

.. container:: instruct

   - Please wire the keyboard circuit introduced in `Lab 7 Audio Synthesizer - Keyboard <https://www.ee.nthu.edu.tw/ee240500/mbed-lab-7-integration-lab-audio-synthesis.html#keyboard>`__ first.
   - The number of button is arbitrary, but must be in range from 3 to 7.

Multi-Key Keyboard Input (20pt)
-------------------------------

#. Please generate 8 bits from keyboards and print the hexadecimal number on uLCD (e.g., as 0x6D).
   For example, if you have four keys on your keyboard, you will need to collect 4+4 bits.
   As another example, if you use only 3 keys, you will need to collect 3+3+3-1 bits. One bit will be discarded.

#. Note that a 4-button keyboard can form 15 different input combination (without 0000).

   .. math::

         \text{input conbination} = 2 ^ \text{N} - 1 \text{(without 0000)}

   .. image:: exam/img/q1_key.png
      :alt: Keyboard


Message Bits Logger (30pt)
--------------------------

#. Please collect 40 bits through the keyboard in mbed.
#. Write a Python program that reads all bits. The program will divide the bits into groups of 4 bits. 
   Then the program will count and print a table to show the occurrence of each 4-bit group.
#. For example: '0100', '0100', '0101', '1000', '1100', '1100', '0001', '0010', '0100', '0110'

   .. class:: terminal

   ::

      '0001': 1
      '0010': 1
      '0100': 3
      '0101': 1
      '0110': 1
      '1000': 1
      '1100': 2

Waveform Loopback (50pt)
========================

.. container:: instruct

   - Please wire the amplifier circuit introduced in `Lab 7 Audio Synthesizer - Speaker <https://www.ee.nthu.edu.tw/ee240500/mbed-lab-7-integration-lab-audio-synthesis.html##speaker-headphone-with-3-5mm-audio-interface>`__ first.

Triangle Wave
-------------

#. In mbed, generate an analog triangle-wave (not sawtooth!) signal from DAC.
#. Send the signal from DAC to the amplifier circuit.
#. Sample the amplified output signal by A0.
#. Write a Python program in PC to get the sampled value and then plot the sampled signal.
