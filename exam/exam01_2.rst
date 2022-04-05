EE240500 Embedded System Laboratory Exam #1-2
################################################
:Date:    2020-04-06 16:00
:Tags:    Exams
:Summary: The Exam #1-2
:Status: Draft

.. sectnum::
    :depth: 2

.. include:: ../LARC_def.txt

.. contents::

****
Rule
****

#. Search on the Internet is allowed.

#. Any communication with others is strictly prohibited.

#. You should commit your changes every time you compile your code

**********
Submission
**********

* Due time: 17:50, April 6th, 2020

* Submit your answer: `Exam #1 (Make up) <https://forms.gle/yky1G9weKvNXLHFm7>`__

   #. Source codes
   #. URL of your git remote repo
   #. The plot of the waveform in PC
   #. The video of the result in Picoscope
   #. The photo of your circuit including uLCD

*********
Questions
*********

#. (10%) Please create a git remote repository named :hl:`exam01`, initialize local repository, and link remote repository to your local repository.

#. (25%) Draw a solid blue circle and display your English name besides the blue circle on uLCD.

#. (25%) In mbed, generate a sweeping Sine signal.

   #. The Sine frequency starts at 100 Hz.

   #. Your program will sweep the frequency of the Sine signal from 100Hz to 1000Hz every 0.5s by increasing with a 100Hz interval.
      After reaching 1000Hz, the frequency decreases back to 100Hz (again by a 100Hz interval).
      Please cycle above process in your program.

#. (10%) Sample the output signal by :hl:`A0` and send the sampled data to PC every 0.1s while generating the sweeping Sine signal.

#. (10%) Write a Python program in PC to get 128 sampled values and then plot the waveform of the sampled signal.

#. (10%) Measure the sweeping PWM signal with Picoscope.

#. (10%) Take a photo of your circuit including the uLCD.

.. container:: instruct

   #. Commit your changes every time you compile your code.
   #. Remember to push your code to git remote repository.

