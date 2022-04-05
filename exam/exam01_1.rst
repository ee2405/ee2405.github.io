EE240500 Embedded System Laboratory Exam #1
###########################################
:Date:    2020-04-01 16:00
:Tags:    Exams
:Summary: The Exam #1
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

* Due time: 17:50, April 1st, 2020

* Submit your answer: `Exam #1 <https://forms.gle/DPAN4wQc7XcTdwfPA>`__
   #. Source codes
   #. URL of your git remote repo
   #. The plot of the waveform in PC
   #. The video of the result in Picoscope
   #. The photo of your circuit including uLCD

*********
Questions
*********

#. (10%) Please create a git remote repository named :hl:`exam01`, initialize local repository, and link remote repository to your local repository.

#. (25%) Draw a square and display your student ID on uLCD.

#. (25%) In mbed, generate a sweeping PWM signal.

   #. The PWM frequency is 1000 Hz.

   #. Your program will sweep the duty-cycle of the PWM signal. The duty cycle will start at 0 and add 0.1 for each duration of 0.1s. After the duty-cycle reaches 1, it will gradually decrease back to 0. It decrease by 0.1 for each 0.1s. Please cycle above process in your program.

#. (10%) Sample the output signal by :hl:`D7` and send the sampled data to PC every 0.1s while generating the sweeping PWM signal.

#. (10%) Write a Python program in PC to get 128 sampled values and then plot the waveform of the sampled signal.

#. (10%) Measure the sweeping PWM signal with Picoscope.

#. (10%) Take a photo of your circuit including the uLCD.

.. container:: instruct

   #. Commit your changes every time you compile your code.
   #. Remember to push your code to git remote repository.

