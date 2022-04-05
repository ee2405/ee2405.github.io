mbed Lab 8 (Integration Lab) Audio Synthesis
############################################
:Date:    2020-04-22 15:00
:Tags:    Labs
:Summary: To build a music note player
:Status: Draft

.. sectnum::
	:depth: 2

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

   The goal of this lab is to learn:

   #. To build the hardware and software for generating single tone sound
   #. We will learn the audio DAC on K66F
   #. We will review Interrupt and EventQueue API

****************
Lab Introduction
****************

We use this lab to build an example circuit for playing a tune and single music
notes with a keyboard.  In this lab, we use components from previous labs and
integrate them together for the player including an audio DAC, UART,
interrupts, and PC Python programs.

*******************
Preview Topics
*******************

Please answer the prelab questions in Microsoft Teams.

*******************
Equipment List
*******************

- FRDM-K66F * 1
- Earphone * 1
- Buttons * 3
- Breadboard * 1

***************
Lab Description
***************

Prepare your git environment for this lab
=========================================

#. Create a remote repository name :hl:`mbed08`.

#. Create a folder for this lab: :cmd_host:`$ mkdir ~/ee2405/mbed08`

#. Open the folder :file:`~/ee2405/mbed08` by VS Code:
   :cmd_host:`$ code ~/ee2405/mbed08`

#. Initialize Repository with VS Code.

#. Link remote repository to your local repository.

.. container:: instruct

    If you forget how to use git with VS Code, please visit
    `Linux Lab 1 <https://www.ee.nthu.edu.tw/ee240500/linux-lab-1-introduction-to-linux.html>`_.

Play a single note with DA7212
================================

#. Switch to a terminal or start a terminal with :hotkey:`Ctrl+Alt+T`

#. Create a new Mbed project.

   :cmd_host:`$ cd ~/ee2405/mbed08`

   :cmd_host:`$ mbed new 8_1_261Hz --scm none`

   :cmd_host:`$ cd 8_1_261Hz`

   :cmd_host:`$ mbed add https://gitlab.larc-nthu.net/ee2405_2020/DA7212`

#. Start VSCode to edit.

   :cmd_host:`$ code main.cpp`

#. Copy the following code into :file:`main.cpp`.
   Note in the following codes, the SW2 button is an interrupt input to trigger
   to schedule playNoteC() in the event queue.

   The playNoteC() will output a sine waveform[] table to DAC output according to the specified frequency (C=261).
   The waveform[] table is of size kAudioSampleFrequency, and a complete sine waveform is repeated for freq times (by definition of frequency).
   Note that the sine values are scaled as int16 by (1<<16) - 1).

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include <cmath>
      #include "DA7212.h"

      int idC, i;
      Thread t;
      DA7212 audio;
      InterruptIn button(SW2);
      int16_t waveform[kAudioTxBufferSize];
      EventQueue queue(32 * EVENTS_EVENT_SIZE);

      void playNote(int freq)
      {
        for (i = 0; i < kAudioTxBufferSize; i++)
        {
          waveform[i] = (int16_t) (sin((double)i * 2. * M_PI / (double) (kAudioSampleFrequency / freq)) * ((1<<16) - 1));
        }
        // the loop below will play the note for the duration of 1s
        for(int j = 0; j < kAudioSampleFrequency / kAudioTxBufferSize; ++j)
        {
          audio.spk.play(waveform, kAudioTxBufferSize);
        }
      }
      void playNoteC(void) {idC = queue.call_every(1, playNote, 261);}
      void stopPlayNoteC(void) {queue.cancel(idC);}

      int main(void)
      {
        t.start(callback(&queue, &EventQueue::dispatch_forever));
        button.fall(queue.event(playNoteC));
        button.rise(queue.event(stopPlayNoteC));
      }

#. Create a new build profile :file:`audio.json`.

   :cmd_host:`$ code audio.json`

   .. code-block:: json
      :linenos: inline

      {
          "GCC_ARM": {
              "common": ["-Wall", "-Wextra",
                         "-Wno-unused-parameter", "-Wno-missing-field-initializers",
                         "-fmessage-length=0", "-fno-exceptions",
                         "-ffunction-sections", "-fdata-sections", "-funsigned-char",
                         "-MMD",
                         "-fomit-frame-pointer", "-Os", "-DNDEBUG", "-g"],
              "asm": ["-c", "-x", "assembler-with-cpp"],
              "c": ["-c", "-std=gnu11"],
              "cxx": ["-c", "-std=gnu++14", "-fpermissive", "-fno-rtti", "-Wvla"],
              "ld": ["-Wl,--gc-sections", "-Wl,--wrap,main", "-Wl,--wrap,_malloc_r",
                     "-Wl,--wrap,_free_r", "-Wl,--wrap,_realloc_r", "-Wl,--wrap,_memalign_r",
                     "-Wl,--wrap,_calloc_r", "-Wl,--wrap,exit", "-Wl,--wrap,atexit",
                     "-Wl,-n"]
          }
      }

#. Compile the program.

   :cmd_host:`$ sudo mbed compile --source . --source ~/ee2405/mbed-os/ -m K66F -t GCC_ARM -f --profile audio.json`

#. Replug the K66F to the PC.

#. Once the SW2 is pressed, you will hear a C note sound from the audio interface.

#. Push the code to your git remote repository, and check your remote repository for new files.

Play a sequence of notes 
================================

#. Switch to a terminal or start a terminal with :hotkey:`Ctrl+Alt+T`

#. Create a new Mbed project.

   :cmd_host:`$ cd ~/ee2405/mbed08`

   :cmd_host:`$ mbed new 8_2_Audio_Player --scm none`

   :cmd_host:`$ cd 8_2_Audio_Player`

   :cmd_host:`$ mbed add https://gitlab.larc-nthu.net/ee2405_2020/DA7212`

#. Start VSCode to edit :file:`main.cpp`.

   :cmd_host:`$ code main.cpp`

#. Copy the following code into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include <cmath>
      #include "DA7212.h"

      DA7212 audio;
      int16_t waveform[kAudioTxBufferSize];
      EventQueue queue(32 * EVENTS_EVENT_SIZE);
      Thread t;

      int song[42] = {
        261, 261, 392, 392, 440, 440, 392,
        349, 349, 330, 330, 294, 294, 261,
        392, 392, 349, 349, 330, 330, 294,
        392, 392, 349, 349, 330, 330, 294,
        261, 261, 392, 392, 440, 440, 392,
        349, 349, 330, 330, 294, 294, 261};

      int noteLength[42] = {
        1, 1, 1, 1, 1, 1, 2,
        1, 1, 1, 1, 1, 1, 2,
        1, 1, 1, 1, 1, 1, 2,
        1, 1, 1, 1, 1, 1, 2,
        1, 1, 1, 1, 1, 1, 2,
        1, 1, 1, 1, 1, 1, 2};

      void playNote(int freq)
      {
        for(int i = 0; i < kAudioTxBufferSize; i++)
        {
          waveform[i] = (int16_t) (sin((double)i * 2. * M_PI/(double) (kAudioSampleFrequency / freq)) * ((1<<16) - 1));
        }
        audio.spk.play(waveform, kAudioTxBufferSize);
      }

      int main(void)
      {
        t.start(callback(&queue, &EventQueue::dispatch_forever));

        for(int i = 0; i < 42; i++)
        {
          int length = noteLength[i];
          while(length--)
          {
            // the loop below will play the note for the duration of 1s
            for(int j = 0; j < kAudioSampleFrequency / kAudioTxBufferSize; ++j)
            {
              queue.call(playNote, song[i]);
            }
            if(length < 1) wait(1.0);
          }
        }
      }

#. Create a new build profile :file:`audio.json`.

   :cmd_host:`$ code audio.json`

   .. code-block:: json
      :linenos: inline

      {
          "GCC_ARM": {
              "common": ["-Wall", "-Wextra",
                         "-Wno-unused-parameter", "-Wno-missing-field-initializers",
                         "-fmessage-length=0", "-fno-exceptions",
                         "-ffunction-sections", "-fdata-sections", "-funsigned-char",
                         "-MMD",
                         "-fomit-frame-pointer", "-Os", "-DNDEBUG", "-g"],
              "asm": ["-c", "-x", "assembler-with-cpp"],
              "c": ["-c", "-std=gnu11"],
              "cxx": ["-c", "-std=gnu++14", "-fpermissive", "-fno-rtti", "-Wvla"],
              "ld": ["-Wl,--gc-sections", "-Wl,--wrap,main", "-Wl,--wrap,_malloc_r",
                     "-Wl,--wrap,_free_r", "-Wl,--wrap,_realloc_r", "-Wl,--wrap,_memalign_r",
                     "-Wl,--wrap,_calloc_r", "-Wl,--wrap,exit", "-Wl,--wrap,atexit",
                     "-Wl,-n"]
          }
      }

#. Compile the program.

   :cmd_host:`$ sudo mbed compile --source . --source ~/ee2405/mbed-os/ -m K66F -t GCC_ARM -f --profile audio.json`

#. Replug the K66F to the PC and then you will hear the song *Twinkle, Twinkle, Little Star*.
   Note that we need to unplug and plug K66F to reset the DA7212.

#. Push the code to your git remote repository, and check your remote repository for new files.

Audio Synthesizer
=================

#. Switch to a terminal or start a terminal with :hotkey:`Ctrl+Alt+T`

#. Create a new Mbed project.

   :cmd_host:`$ cd ~/ee2405/mbed08`

   :cmd_host:`$ mbed new 8_3_Audio_Synthesizer --scm none`

   :cmd_host:`$ cd 8_3_Audio_Synthesizer`

   :cmd_host:`$ mbed add https://gitlab.larc-nthu.net/ee2405_2020/DA7212`

#. Start VSCode to edit :file:`main.cpp`.

   :cmd_host:`$ code main.cpp`

#. Copy the following code into :file:`main.cpp`.

   Note that we also implement a loadWaveform() to load an arbitrary waveform from
   a PC Python program.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include <cmath>
      #include "DA7212.h"

      #define bufferLength (32)
      #define signalLength (1024)

      DA7212 audio;
      Serial pc(USBTX, USBRX);

      InterruptIn button(SW2);
      InterruptIn keyboard0(SW3);

      EventQueue queue(32 * EVENTS_EVENT_SIZE);
      Thread t;
      int idC = 0;

      float signal[signalLength];
      int16_t waveform[kAudioTxBufferSize];
      char serialInBuffer[bufferLength];
      int serialCount = 0;

      DigitalOut green_led(LED2);

      void loadSignal(void)
      {
        green_led = 0;
        int i = 0;
        serialCount = 0;
        audio.spk.pause();
        while(i < signalLength)
        {
          if(pc.readable())
          {
            serialInBuffer[serialCount] = pc.getc();
            serialCount++;
            if(serialCount == 5)
            {
              serialInBuffer[serialCount] = '\0';
              signal[i] = (float) atof(serialInBuffer);
              serialCount = 0;
              i++;
            }
          }
        }
        green_led = 1;
      }

      void playNote(int freq)
      {
        for (int i = 0; i < kAudioTxBufferSize; i++)
        {
          waveform[i] = (int16_t) (signal[(uint16_t) (i * freq * signalLength * 1. / kAudioSampleFrequency) % signalLength] * ((1<<16) - 1));
        }
        // the loop below will play the note for the duration of 1s
        for(int j = 0; j < kAudioSampleFrequency / kAudioTxBufferSize; ++j)
        {
          audio.spk.play(waveform, kAudioTxBufferSize);
        }
      }

      void loadSignalHandler(void) {queue.call(loadSignal);}

      void playNoteC(void) {idC = queue.call_every(1, playNote, 261);}

      void stopPlayNoteC(void) {queue.cancel(idC);}

      int main(void)
      {
        green_led = 1;
        t.start(callback(&queue, &EventQueue::dispatch_forever));
        button.rise(queue.event(loadSignalHandler));
        keyboard0.rise(queue.event(playNoteC));
        keyboard0.fall(queue.event(stopPlayNoteC));
      }


#. Create a new build profile :file:`audio.json`.

   :cmd_host:`$ code audio.json`

   .. code-block:: json
      :linenos: inline

      {
          "GCC_ARM": {
              "common": ["-Wall", "-Wextra",
                         "-Wno-unused-parameter", "-Wno-missing-field-initializers",
                         "-fmessage-length=0", "-fno-exceptions",
                         "-ffunction-sections", "-fdata-sections", "-funsigned-char",
                         "-MMD",
                         "-fomit-frame-pointer", "-Os", "-DNDEBUG", "-g"],
              "asm": ["-c", "-x", "assembler-with-cpp"],
              "c": ["-c", "-std=gnu11"],
              "cxx": ["-c", "-std=gnu++14", "-fpermissive", "-fno-rtti", "-Wvla"],
              "ld": ["-Wl,--gc-sections", "-Wl,--wrap,main", "-Wl,--wrap,_malloc_r",
                     "-Wl,--wrap,_free_r", "-Wl,--wrap,_realloc_r", "-Wl,--wrap,_memalign_r",
                     "-Wl,--wrap,_calloc_r", "-Wl,--wrap,exit", "-Wl,--wrap,atexit",
                     "-Wl,-n"]
          }
      }

#. Compile the program.

   :cmd_host:`$ sudo mbed compile --source . --source ~/ee2405/mbed-os/ -m K66F -t GCC_ARM -f --profile audio.json`

#. Start VSCode to edit :file:`sendSignal.py`.

   :cmd_host:`$ code sendSignal.py`

#. Copy the following code into :file:`sendSignal.py`.

   .. code-block:: python
      :linenos: inline

      import numpy as np
      import serial
      import time

      waitTime = 0.1

      # generate the waveform table
      signalLength = 1024
      t = np.linspace(0, 2*np.pi, signalLength)
      signalTable = (np.sin(t) + 1.0) / 2.0

      # output formatter
      formatter = lambda x: "%.3f" % x

      # send the waveform table to K66F
      serdev = '/dev/ttyACM0'
      s = serial.Serial(serdev)
      print("Sending signal ...")
      print("It may take about %d seconds ..." % (int(signalLength * waitTime)))
      for data in signalTable:
        s.write(bytes(formatter(data), 'UTF-8'))
        time.sleep(waitTime)
      s.close()
      print("Signal sended")

#. Replug the K66F to the PC.

#. Press SW2 and then run the python script to load the signal from the PC.

#. Press SW3 to play the C4 note.

#. Push the code to your git remote repository, and check your remote repository for new files.

********************
Demo and Checkpoints
********************

#. Show your git remote repository.

#. Demo the Audio Synthesizer.

**************
Reference List
**************

#. `DA7212 data sheet pdf <https://www.dialog-semiconductor.com/sites/default/files/da7212_datasheet_3v4.pdf>`__
