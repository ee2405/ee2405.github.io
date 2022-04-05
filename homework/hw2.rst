Homework 2 LCD, Serial Port and RTOS 
#######################################

:Date:      2022-04-06  15:00
:Tags:      Homework
:Summary:   Homework to use digital and analog I/O in mbed.

.. sectnum::
   :depth: 2

.. include:: ../LARC_def.txt

.. role:: raw-latex(raw)
            :format: latex html

.. raw:: html

          <script id="MathJax-script" async
                  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js">
          </script> 

.. contents::

**update 3/23** Add a Ticker example for DAC/ADC threads.

**update 3/24** Replace a Ticker example with attach_us().

**update 3/25** Add waveform DAC sample rate specification.

**update 3/28** (1) Remove Ticker example, since it is deprecated in Mbed OS 6.
(2) Change waveform spec to 10Hz. (3) Extend due day to April 6.

*********************
Prerequisites
*********************

#. **mbed Lab 5 Liquid Crystal Displays**
#. **mbed Lab 6 Interrupts, Timers, Tasks and RTOS**
#. **mbed Lab 7 Serial Communication**

*********************
Submission
*********************

#. Due date: noon, April 6, 2022

#. Please create your own hw2 github repo.

#. Please push all your codes and README to your hw2 github repo, and submit the report in pdf to eeclass.

   - The Readme file should explain: (1) how to setup and run your program (2) what are the results

   - The pdf is a record and explanation of your codes (don't print out codes).
     You may include the following contents (but not limited to):
     (1) implementation (data structure and algorithm) in each part (2) Results and validation of each step 
     (3) Encountered issues (4) Discussion

#. **Please demo your homework and explain how it works before 6:20pm on March 30.**

*********************
Equipment List
*********************

#. B_L4S5I_IOT01A
#. Bread board
#. Buttons * 3
#. Picoscope
#. Wires * 20
#. uLCD

*********************
Homework Description
*********************

#. Threads and waveform generation

   We will repeat a simplified version of homework 1 with threads and interrupts.
   In the following we partition our mbed program into several threads or interrupt service routines.

   #. Please implement two push buttons: Button A is for starting waveform generation and Button B is for
      stopping the generation.

   #. Button A will trigger an ISR to start the waveform generation by setting a global variable "GenWave" to true.
      Picoscope can be used to check the waveform. There is no need to include a RC filter.

   #. Button B will trigger an ISR to stop the waveform generation by setting the global variable "GenWave" to false,
      and output the stored waveforms to PC through printf().
      The function to transfer the waveform data will be called from an EventQueue.
      Please also write a Python program to display and analyze the received waveform.

   #. A thread will run in a while(true) loop to generate waveforms to a DAC pin if "GenWave"=true.
      Otherwise, it sleep_for() the same period as the DAC waveform sampling rate.

      The waveform from HW1 has a frequency faster 10Hz. So, the base waveform period is 1/10s.
      The waveform of HW1 digitize each period for 10 parts, so for each digit the duration is 1/100s.
      Assume we send 10 samples or less for each digit. We will need 1/10 the digit duration for each DAC sample.
      Therefore, each DAC sample rate will be at most 1kHz (at most 1ms).

      Note that we don't schedule events above 1ms, so we can use regular sleep_for().

   #. A thread will run in a while(true) loop to store waveforms from a ADC pin if "GenWave"=true to
      an mbed C++ array.
      Otherwise, it sleep_for() the same period as the ADC waveform sampling rate.

      The C++ array can be either static or dynamic. Note that the number of data capture will increase
      as the duration increases between the clicks of Button A and B. Please check the size of input data
      to avoid array overflow.

      If you encounter stack overflow issue when executing the mbed program, it may be caused by the C++ array size.
      The solution is to increase the default stack size setup. Please create mbed_app.json in the project folder
      and add the following configuration. The original size is 4K, we set it to 8192:

      .. code-block:: c++

         {
           "config": {
               "main-stack-size": {
                   "value": 8192
               }
           }
         }

   #. Waveforms are the same signal waveforms in HW1 with frequencies above 10Hz.
      Only one and fixed frequency is required in this homework.

   #. Please show the status of mbed on uLCD: (1) waveform generation (2) data transfer (3) when interrupts from
      Button A and B are detected, etc. Please only update uLCD status during the transition of operations. Do not output
      to uLCD during waveform generation to avoid interfering ADC/DAC.
