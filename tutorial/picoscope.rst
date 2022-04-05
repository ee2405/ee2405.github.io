PicoScope Tutorial
############################
:Date:    2019-03-07 20:00
:Tags:    Tutorial
:Summary: Use PicoScope class
:Status: Draft

.. sectnum::
	 :depth: 2

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

	The goal of this lab is to learn:

	#. What is PicoScope
	#. How to use PicoScope

****************
Lab Introduction
****************

***************
Lab Description
***************

Picoscope 2204A
===============

#. **Introduction**

   .. container:: question
 

      What is `Picoscope <https://www.picotech.com/oscilloscope/2000/picoscope-2000-overview>`__?

      The PicoScope 2000 Series includes mixed signal models that include 16 digital inputs so that you can :hl:`view digital and analog signals` simultaneously.

      The digital inputs can be displayed individually or in named groups with binary, decimal or hexadecimal values shown in a bus-style display. A separate logic threshold from –5 V to +5 V can be defined for each 8-bit input port. The digital trigger can be activated by any bit pattern combined with an optional transition on any input. Advanced logic triggers can be set on either the analog or digital input channels, or both to enable complex mixed-signal triggering.

      The digital inputs bring extra power to the serial decoding options.  You can decode serial data on all analog and digital channels simultaneously, giving you up to 18 channels of data.  You can for example decode :hl:`multiple SPI, I²C, CAN bus, LIN bus and FlexRay signals` all at the same time!

#. **Installation**

   #. Open the terminal. (:hotkey:`Ctrl+Alt+T`)

   #. Add repository to the updater.
      
      :cmd_host:`$ sudo bash -c 'echo "deb https://labs.picotech.com/debian/ picoscope main" >/etc/apt/sources.list.d/picoscope.list'`

   #. Import public key.

      :cmd_host:`$ wget -O - https://labs.picotech.com/debian/dists/picoscope/Release.gpg.key | sudo apt-key add -`

   #. Update package manager cache.

      :cmd_host:`$ sudo apt-get update`

   #. Install PicoScope.

      :cmd_host:`$ sudo apt-get install picoscope`

#. **Locating the Driver Package Files**

   #. Open a terminal window.
    
   #. Navigate to the :dir:`/opt/picoscope` directory.

      :cmd_host:`cd /opt/picoscope`
    
   #. The following directories will be available:
   
      .. class:: terminal

      ::

         bin  include  lib  share

      bin - (if you have installed the PicoScope software)
        
      include - C/C++ header files for the libraries (in a sub-directory according to the library name) and wrapper libraries
        
      lib - shared object (so) library files
        
      share/doc/ - a set of directories corresponding to the various drivers, each containing a usbtest application e.g. /share/doc/libps2000 for the PicoScope 2000 Series Oscilloscopes

#. **Execute the PicoScope**

   #. Connect the picoscope to your computer. `Screenshot <labs/img/Analog_Input/1_1_2.jpg>`__

   #. Connect one probe to the :hl:`Channel A` `like this <labs/img/Analog_Input/1_1_3.jpg>`__. 

   #. Back to :file:`/home`

      :cmd_host:`$ cd ~`

   #. Add installation path to your :file:`.bashrc`

      :cmd_host:`$ code .bashrc`

   #. Add the following line to the end of the file

      :file:`PATH=$PATH:"/opt/picoscope/bin"`

   #. Source :file:`.bashrc` to enable the PATH setup 
   
      :cmd_host:`$ source ~/.bashrc`

      Above setup of PATH should be done only once.

   #. Execute the picoscope

      :cmd_host:`$ picoscope &`

   #. If you install successfully, you will see `this <labs/img/Analog_Input/1_1_4.png>`__.


Generate Arbitrary Waveform
===========================

#. To use picoscope to generate arbitrary waveform, open the function generator first. And click **"Arbitrary"** `this <tutorial/images/pico/arbitrary01.png>`__.

#. We will use "Clear all" and "Line drawing mode" in this tutorial.

   #. To reset waveform first, click "Clear all" first, and you will see no other signal on the screen. `this <tutorial/images/pico/arbitrary02.png>`__

   #. Use "Line drawing mode" to create an arbitrary waveform. `this <tutorial/images/pico/arbitrary03.png>`__

   #. Click "Apply" to generate the waveform

#. To test the correctness of this part. You should connect like `this <tutorial/images/pico/self_testing.png>`__

**************
Reference List
**************

- `PicoScope 6 User's Guide <https://www.picotech.com/download/manuals/picoscope-6-users-guide.pdf>`__

