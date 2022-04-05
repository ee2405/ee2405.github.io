EE240500 Embedded System Laboratory Exam #3
###########################################
:Date:    2020-06-03 15:30
:Tags:    Exams
:Summary: The Exam #3
:Status: Draft

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

****
Rule
****

#. Search on the Internet is allowed.

#. Any communication with others is strictly prohibited.

#. You should commit your changes every time you compile your code

**********
Submission
**********

* Due time: 16:50, June 3rd, 2020

* Submit your answer: `Exam #3 <https://forms.gle/PR88Mmn5rvASQdV59>`__
   #. Source codes
   #. URL of your git remote repo

*********
Questions
*********

- Please create a git remote repository named :hl:`exam03`, initialize local repository, and link remote repository to your local repository.

#. Please use the accelerometer of K66F to measure and store the horizontal velocity every 0.1s with call() API of EventQueue.

   #. Note that velocity can be estimated by :raw-latex:`\(a*t\)`.

   #. Please make sure only horizontal velocity is calculated (horizontal direction is defined by a plane perpendicular to gravity).

#. Write an mbed RPC function in :file:`main.cpp`, whose function is 
   to send the stored horizontal velocity in batch to PC through Xbee.

#. Write a Python program (a MQTT client) to publish the horizontal velocity data (obtained by calling RPC functions with Xbee) to a MQTT broker with a topic named :hl:`velocity`.

#. Write another Python program to subscribe to :hl:`velocity` topic and print the horizontal velocity values received from 
   this topic of the MQTT broker.

.. container:: instruct

   #. Commit your changes every time you compile your code.
   #. Remember to push your code to git remote repository.

