EE240500 Embedded System Laboratory Exam #2
###########################################
:Date:    2020-04-29 15:30
:Tags:    Exams
:Summary: The Exam #2
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

* Due time: 16:50, April 29th, 2020

* Submit your answer: `Exam #2 <https://forms.gle/UZ7Q1xu1MGv5w35aA>`__
   #. Source codes
   #. URL of your git remote repo

*********
Questions
*********

- Please create a git remote repository named :hl:`exam02`, initialize local repository, and link remote repository to your local repository.

- (80%) In the first part, you will implement a horizontal movement logger.

  #. Initially please hold K66F in your hand.

  #. Then please use a button to trigger a movement logger function in mbed and start to blink a LED as an indicator.

  #. Please use accelerometers of K66F to measure and store acceleration vectors periodically every 0.1s.

  #. Next please move K66F periodically in horizontal direction (displacement > 5cm).

  #. The movement logger will detect if K66F moves horizontally with > 5cm of displacements.
     The event logger in Mbed will also record this condition.

     #. Note that displacement can be estimated by :raw-latex:`\(a*t^2/2\)`. If the displacement is in the same direction, we will add up
        all displacements to see if accumulated displacement is larger than 5cm. 
        Note that the value measured with accelerometers :raw-latex:`\(q\)` should be multiplied by 9.8 to get the actual acceleration :raw-latex:`\(a=9.8*q \ \text{cm}/\text{s}^2\)`.
     #. Please make sure only horizontal movement is calculated (horizontal direction is defined by a plane perpendicular to
        gravity).
     #. Please use call() APIs of EventQueue in mbed for the logger.

  #. After 10 seconds, the logger will stop and transfer all data to PC. Please display logged accelerometer vectors
     and horizontal movement events with Matplotlib.

- (20%) In the second part, please run the Colab script.
  Please fill in correct statements in the right of the codes to finish the scripts.
  Data sample is generated with a quadratic function and we will train a regression model to fit the data.
  And we convert and interpret the trained model with a Tensorflow lite APIs.

  Link to Colab script: https://colab.research.google.com/drive/1ilT9URXGWCHCXxwZk0kB0XYoeuK6lyKZ

.. container:: instruct

   #. Commit your changes every time you compile your code.
   #. Remember to push your code to git remote repository.

