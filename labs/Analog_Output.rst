mbed Lab 3 Analog Output
########################
:Date:    2022-03-02 15:00
:Tags:    Labs
:Summary: Use mbed's AnalogOut class

.. sectnum::
	 :depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

	The goal of this lab is to learn:

	#. Analog output of mbed
	#. PWM output of mbed
	#. Comparison between analog output and PWM

****************
Lab Due
****************

**Mar. 2, 2022**

****************
Lab Introduction
****************

Mbed has two interfaces to support non-digital outputs: AnalogOut and PwmOut.
The AnalogOut Interface uses digital to analog converter (DAC) circuit on chip
to generate desired voltage level at an analog output pin.  The voltage output
of AnalogOut Interface has the characteristic of the DAC: voltage range between
VSS and VCC, driving current, conversion speed and accuracy.

The PwmOut interface can be used to set the frequency and duty-cycle ratio
(percentage of voltage high in a cycle) of a digital pulse train.  PWM signals
are often used to drive a motor servo. We will use PWM to control the Boe Bot
Car at later lab.

***************
Equipment List
***************

#. B_L4S5I_IOT01A * 1
#. Picoscope * 1
#. Wire * 20

***************
Lab Description
***************

Lecture Notes
=============

- Chapter 4: Analog Output `ch4_dac.pdf <notes/ch4_dac.pdf>`__

How to Use PicoScope
====================

#. Please read through chapter 4 of `PicoScope 6 User's Guide <https://www.picotech.com/download/manuals/picoscope-6-users-guide.pdf>`__
   to get a general idea of picoscope's function.

   .. container:: instruct
 

      What is `Picoscope <https://www.picotech.com/oscilloscope/2000/picoscope-2000-overview>`__?

      The PicoScope 2000 Series includes mixed signal models that include 16
      digital inputs so that you can :hl:`view digital and analog signals`
      simultaneously.

      The digital inputs can be displayed individually or in named groups with
      binary, decimal or hexadecimal values shown in a bus-style display. A separate
      logic threshold from –5 V to +5 V can be defined for each 8-bit input port. The
      digital trigger can be activated by any bit pattern combined with an optional
      transition on any input. Advanced logic triggers can be set on either the
      analog or digital input channels, or both to enable complex mixed-signal
      triggering.

      The digital inputs bring extra power to the serial decoding options.
      You can decode serial data on all analog and digital channels simultaneously,
      giving you up to 18 channels of data.  You can for example decode :hl:`multiple
      SPI, I²C, CAN bus, LIN bus and FlexRay signals` all at the same time!

#. Please go to `Picoscope download site <https://www.picotech.com/downloads>`__

#. Select "Picoscope 2000 Series" --> "Picoscope 2204A" --> "Software" and select Windows or Mac version.
   Install the downloaded Picoscope 6 software.

Analog output
=============

.. container:: warning

	 For all the following, please unplug B_L4S5I_IOT01A from power while wiring circuits.

.. container:: instruct

   For all Mbed programs, please push the source codes to your GitHub repo.


#. Using the probe with picoscope to measure the voltage at :hl:`PA_4`.

   Connect the probe to the pin of PA_4 and the ground. `Screenshot <labs/img/Analog_Output/lab2_PA_4.jpg>`__

   .. image:: labs/img/Analog_Output/B_L4S5I_IOT01A_pico_probe_PA_4_new.jpg
      :alt: Wiring for PicoScope probe

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *3_1_Analog_Output* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      AnalogOut Aout(PA_4);
      int main(){
        while(1){
          Aout = 0.25;  // 0.25 * 3.3 = 0.825 v
          ThisThread::sleep_for(2s);
          Aout = 0.5;   // 0.50 * 3.3 = 1.650 v
          ThisThread::sleep_for(2s);
          Aout = 0.75;  // 0.75 * 3.3 = 2.475 v
          ThisThread::sleep_for(2s);
        }
      }

   AnalogOut is a class which is used for setting the voltage on a pin. We will show you where the PA_4 at the B_L4S5I_IOT01A is.

   .. code-block:: c++

      AnalogOut Aout(PA_4);

   .. image:: labs/img/Analog_Output/PA_4.jpg
      :alt: B_L4S5I_IOT01A PA_4

#. Compile and run the program

#. Start the picoscope app

#. Select "input range A" as +-5 and collection time as 1 s/div

#. The voltage will shows on the `monitor <labs/img/Analog_Output/2_1_5.png>`__.

#. Screenshot your result of picoscope.

Generate a sawtooth waveform
============================

.. container:: warning

   Since this circuit is as same as the previous circuit, there's no need to turn off the PicoScope and unplug B_L4S5I_IOT01A.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *3_2_Sawtooth_Waveform* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      // Initialize a pins to perform analog and digital output functions
      // Adjust analog output pin name to your board spec.
      AnalogOut  aout(PA_4);
      DigitalOut dout(LED1);

      int main(void)
      {
         while (1) {
            // change the voltage on the digital output pin by 0.1 * VCC
            //  and print what the measured voltage should be (assuming VCC = 3.3v)
            for (float i = 0.0f; i < 1.0f; i += 0.1f) {
                  aout = i;
                  printf("aout = %f volts\n", aout.read() * 3.3f);
                  // turn on the led if the voltage is greater than 0.5f * VCC
                  dout = (aout > 0.5f) ? 1 : 0;
                  ThisThread::sleep_for(1s);
            }
         }
      }

#. Compile and run the program

#. Switch to the picoscope application

   If you already left picoscope application, please start it again.

#. Select collection time as 5 s/div

#. Using the probe with picoscope to measure the voltage at :hl:`PA_4`.

#. The voltage will shows on the `monitor <labs/img/Analog_Output/2_2_Sawtooth_Waveform_wave.jpg>`__.

#. Screenshot your result of picoscope.

#. The Output terminal will show the Mbed printf output.

#. Screenshot your result on the Output terminal.

Generate a sine waveform
========================

.. container:: warning

   Since this circuit is as same as the previous circuit, there's no need to turn off the PicoScope and unplug B_L4S5I_IOT01A.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *3_3_Sine_Waveform* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      const double pi = 3.141592653589793238462;
      const double amplitude = 0.5f;
      const double offset = 65535 / 2;

      // The sinewave is created on this pin
      // Adjust analog output pin name to your board spec.
      AnalogOut aout(PA_4);

      int main()
      {
         double rads = 0.0;
         uint16_t sample = 0;

         while (1) {
            // sinewave output
            for (int i = 0; i < 360; i++) {
                  rads = (pi * i) / 180.0f;
                  sample = (uint16_t)(amplitude * (offset * (cos(rads + pi))) + offset);
                  aout.write_u16(sample);
            }
         }
      }

#. Compile and run the program

#. Switch to the picoscope application

#. Using the probe with picoscope to measure the voltage at :hl:`PA_4`.

#. Select collection time as 20 ms/div

#. The waveform will shows on the `monitor <labs/img/Analog_Output/2_3_Sine_Waveform_wave.jpg>`__.

#. Screenshot your result of picoscope.

mbed PWM Output
===============

#. We will measure a different pinout, so please unplug B_L4S5I_IOT01A and probe D13 pin.

   Make sure the selected pin can support PWM. Please refer to `Pinmap <labs/img/Mbed_Intro/B_L4S5I_IOT01A_pinmap.jpg>`__ of B_L4S5I_IOT01A on PWM signals.

   Using the probe with picoscope to measure the voltage at `D13 <labs/img/Analog_Output/lab2_PWM_D13.jpg>`__.

   .. image:: labs/img/Analog_Output/B_L4S5I_IOT01A_pico_probe_D13_new.jpg
      :alt: Wiring for PicoScope probe 

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *3_4_PWM_Ouput* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      // Adjust pin name to your board specification.
      // You can use LED1/LED2/LED3/LED4 if any is connected to PWM capable pin,
      // or use any PWM capable pin, and see generated signal on logical analyzer.
      PwmOut led(LED1);

      int main()
      {
         // specify period first
         led.period_ms(4000);         // 4 second period
         led.write(0.50f);            // 50% duty cycle, relative to period
         //led = 0.5f;                // shorthand for led.write()
         //led.pulsewidth_ms(2000);   // alternative to led.write, set duty cycle time in milliseconds   
         while (1);
      }

   PWMOut is a class which generates a pulse-width modulation digital output. This is the PWM  `pinout <labs/img/Analog_Output/lab2_PWM_D13.jpg>`__ which we use.

   .. code-block:: c++

      PwmOut led(LED1);

#. Compile and run the program

#. Switch to the picoscope application

#. Using the probe with picoscope to measure the voltage at :hl:`D13`.

#. The waveform will shows on the `monitor <labs/img/Analog_Output/2_4_PWM_Ouput_wave.jpg>`__.

#. Screenshot your result of picoscope.

********************
Demo and Checkpoints
********************

#. Show the waveform results above.

#. Show your git remote repository.

#. How to find analog output pins and PWM pins from `Pinmap <labs/img/Mbed_Intro/B_L4S5I_IOT01A_pinmap.jpg>`__?

**************
Reference List
**************

#. `B_L4S5I_IOT01A introduction <https://os.mbed.com/platforms/B-L4S5I-IOT01A/>`__

#. `Analog output introduction of mbed <https://developer.mbed.org/handbook/AnalogOut>`__
