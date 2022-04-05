Midterm Project
#######################
:Date:  2022-04-13 14:00
:Summary: Information of midterm project
:Status: Draft

.. sectnum::
   :depth: 2

.. include:: ../LARC_def.txt

.. contents::


************
Project Goal
************

The goal of the midterm project is to build an extended version of the Audio Synthesizer introduced on mbed8.

********
Schedule
********

+------------------+------------------------------------------------------+
| **Date (Y/M/D)** | **Event**                                            |
+==================+======================================================+
| 2022/04/13       | Demo midterm project                                 |
+------------------+------------------------------------------------------+

.. container:: warning

   **Please do the project yourself. Do not read or copy others' codes.**

*********************
Submission
*********************

#. Due date: noon, May 6th, 2020
#. Please submit your midterm project via Microsoft Teams.
#. **Please find a grading TA to demo this project and explain how it works in the class when you are done.**

********************
Project requirements
********************

Music Player and Taiko Beats
============================
#. (80%) Build up **Music functions for playing wave formats**:

   - Display songs and play info on uLCD. 
   - Use a switch button to interrupt and pause the current function, and entering mode selection (modes are forward/backward/change songs). 
   - In the mode selection, use gestures DNN (with accelerometers) to scroll modes and confirm selection with a switch.
   - In the song selection mode, also use gestures DNN to scroll songs and confirm selection with a switch. 
   - Use Python/PC to maintain a list of music files from PC. Python will load and unload songs to K66F, 
     and generate a searchable list for K66F to handle these files. Note that if no extra file system is used,
     K66F has a limited size of memory to store songs.

#. (20%) Taiko game mode:

   - Please add a Taiko game mode.
   - Show pre-defined beats on uLCD along with a music.
   - Use accelerometers to detect at least two different beats. If DNN models are applied to detect beats, add 10% bonus.
   - Records the beats and compare beat timings with a pre-defined beats of the music.
   - Calculate scores and show on uLCD.

**************
Demo process
**************

#. We will start demo and grading project parts at 4:30pm.
#. Demo live when TAs grade your project.
#. TAs will ask relevant questions.
