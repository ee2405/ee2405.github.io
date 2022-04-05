mbed Lab 6 Interrupts, timers, tasks and RTOS
#############################################
:Date:    2022-03-16 15:00
:Tags:    Labs
:Summary: Use mbed's timer, interrupt and thread classes

.. sectnum::
    :depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

   The goal of this lab is to learn:

   #. Schedule a timed function (periodic or nonperiodic)
   #. Process an interrupt input
   #. Threads and EventQueue

****************
Lab Due
****************

**Mar. 16, 2022**

****************
Lab Introduction
****************

External interrupt signal is often triggered by an external event (e.g., input data waiting for processing).
Interrupt signals happen at unexpected time (or asynchronous to the processor timing). Therefore, depending on
the preset priority of the interrupt signals, we context-switch from the current running application to handle
the request of interrupt signals (by an interrupt service routine; a function designed to process a specific
interrupt signal). The implementation of interrupt scheme is important to relieve processor (or software) to
constantly polling external devices (usually waste of time and power).

In the second part, we learn how to schedule functions to be executed at a fixed time or repeated at an interval.
We use timer or ticker to achieve the scheduled event. This is useful in control process. For example, we can
send a periodical beacon to neighbor nodes to make sure that the interconnected system is well and alive.

For the last part, we introduce **Thread** and **EventQueue** (both are mbed RTOS classes). These classes can be used
to execute multiple tasks (independently) and to schedule ISR functions at designed times and with preset priorities.
They are more flexible than a simple timer and ticker.

***************
Equipment List
***************

#. B_L4S5I_IOT01A * 1

***************
Lab Description
***************

Lecture Notes
=============

-  Chapter 7:Interrupts, Timers and Tasks `ch7_task.pdf <notes/ch7_task.pdf>`__

Interrupt
=========

This program use the button to trigger an interrupt signal and
run flip() function, when an infinite loop is running (blinking an LED).

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *6_1_Interrupt* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      InterruptIn button(BUTTON1);
      DigitalOut led(LED1);
      DigitalOut flash(LED2);

      void flip()
      {
         led = !led;
      }

      int main()
      {
         button.rise(&flip); // attach the address of the flip function to the rising edge
         while (1)
         { // wait around, interrupts will interrupt this!
            flash = !flash;
            ThisThread::sleep_for(250ms);
         }
      }

#. Compile and run the program.

#. Record your results and push the code to your GitHub repo.

Simple Timer
============

This program shows how to measure the time duration with a Timer object.
It also introduces an API to convert from Timer object to s, ms, or us.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *6_2_Simple_Timer* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      using namespace std::chrono;

      Timer t;

      int main()
      {
         t.start();
         printf("Hello World!\n");
         t.stop();
         auto s = chrono::duration_cast<chrono::seconds>(t.elapsed_time()).count();
         auto ms = chrono::duration_cast<chrono::milliseconds>(t.elapsed_time()).count();
         auto us = t.elapsed_time().count();
         printf ("Timer time: %llu s\n", s);
         printf ("Timer time: %llu ms\n", ms);
         printf ("Timer time: %llu us\n", us);
      }

#. Compile and run the program.

#. Record your results and push the code to your GitHub repo.

Multiple Timer
==============

This program creates two Timers, **timer_fast** and **timer_slow**. The main
program starts these running, and tests when each exceeds a certain number.
When the time value is exceeded, a function is called, which flips the
associated led.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *6_3_Multiple_Timer* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      using namespace std::chrono;

      Timer timer_fast, timer_slow;
      DigitalOut led1(LED1);
      DigitalOut led2(LED2);

      int main(){
          timer_fast.start();
          timer_slow.start();

          while(1){
              if(chrono::duration_cast<chrono::seconds>(timer_fast.elapsed_time()).count() > 1){
                  led1 = !led1;
                  timer_fast.reset();
              }
              if(chrono::duration_cast<chrono::seconds>(timer_slow.elapsed_time()).count() > 2){
                  led2 = !led2;
                  timer_slow.reset();
              }
          }
      }

#. Compile and run the program.

#. Record your results and push the code to your GitHub repo.

Simple Timeout
==============

This Program Example causes an action to be triggered a fixed period after
an external event. If the button is pressed, the **blink()** function gets
attached to the **Response** Timeout. The program is a microcosm of many
embedded systems - a time-triggered task needs to keep going, while an
event-triggered task takes place at unpredictable times.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *6_4_Simple_Timeout* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      using namespace std::chrono;

      Timeout flipper;
      DigitalOut led1(LED1);
      DigitalOut led2(LED2);

      void flip()
      {
         led2 = !led2;
      }

      int main()
      {
         led2 = 1;
         flipper.attach(&flip, 2s); // setup flipper to call flip after 2 seconds

         // spin in a main loop. flipper will interrupt it to call flip
         while (1)
         {
            led1 = !led1;
            ThisThread::sleep_for(200ms);
         }
      }

#. Compile and run the program.

#. Record your results and push the code to your GitHub repo.

Simple Ticker
=============

Creating a periodic event is one of the most common requirements in an
embedded system. This program switches the LED every 200 ms, using Timeout
rather than a **wait()** function.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *6_5_Simple_Ticker* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      using namespace std::chrono;

      Ticker flipper;
      DigitalOut led1(LED1);
      DigitalOut led2(LED2);

      void flip()
      {
         led2 = !led2;
      }

      int main()
      {
         led2 = 1;
         flipper.attach(&flip, 2s); // the address of the function to be attached (flip) and the interval (2 seconds)

         // spin in a main loop. flipper will interrupt it to call flip
         while (1)
         {
            led1 = !led1;
            ThisThread::sleep_for(200ms);
         }
      }

#. Compile and run the program.

#. Record your results and push the code to your GitHub repo.

Application -- Debounce
=======================

This program solves the switch bounce issue by starting a timer on a switch
event, and ensuring that 10 ms has elapsed before allowing a second event to be
processed.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *6_6_Debounce* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      using namespace std::chrono;

      Timer debounce;                  //define debounce timer
      InterruptIn button(BUTTON1); //Interrupt on digital push button input SW2
      DigitalOut led1(LED1);

      void toggle()
      {
         if (duration_cast<milliseconds>(debounce.elapsed_time()).count() > 1000)
         {
            //only allow toggle if debounce timer has passed 1s
            led1 = !led1;
            debounce.reset(); //restart timer when the toggle is performed
         }
      }
      int main()
      {
         debounce.start();
         button.rise(&toggle); // attach the address of the toggle
         while (1)
            ;
      }

#. Compile and run the program.

#. Record your results and push the code to your GitHub repo.

Multi-Thread Example
====================

A thread is a single sequential flow of control within a program.  Threads
allow defining, creating and controlling **''parallel tasks''**.  Using
multiple threads running at the same time can simultaneously perform different
tasks in a single program.  This helps an embedded system programmer to avoid
long super-loops.  In the following example, we have two threads executing in
parallel to turn on/off two LEDs at two different periods.

Note that main() is a special thread function that is started at system
initialization. (main thread)

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *6_7_Multi_Thread* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      using namespace std::chrono;

      DigitalOut led1(LED1);
      DigitalOut led2(LED2);
      Thread thread;

      void led2_thread()
      {
         while (true)
         {
            led2 = !led2;
            ThisThread::sleep_for(1s);
         }
      }

      int main()
      {
         thread.start(led2_thread);

         while (true)
         {
            led1 = !led1;
            ThisThread::sleep_for(500ms);
         }
      }

#. Compile and run the program.

#. Record your results and push the code to your GitHub repo.

EventQueue Example
===============================

The EventQueue class provides a flexible queue for scheduling events.
EventQueue is also thread-safe and ISR-safe, which means we can run EventQueue
functions inside a thread or ISR.  Note that functions called in
Timer/Timeout/Ticker should be ISR-safe, too.  It is **recommended to use
EventQueue** to schedule periodic or timer tasks instead of
Timer/Timeout/Ticker (except for very simple tasks).

You can use the EventQueue class for synchronization between multiple threads,
or to move events out of interrupt context (deferred execution of time
consuming or non-ISR safe operations).  Note that some I/O classes are not
allowed in ISR, e.g., printf(), DAC/ADC, etc.  Therefore, when we get an
interrupt, we usually run a simple ISR to (1) handle the interrupt, (2)
schedule an task in an EventQueue (maybe at a designed time or with a
priority), (3) return from the ISR.

You can use the dispatch() and dispatch_forever() APIs to execute pending events.
"break_dispatch()" can be used to terminate the execution of events in the
specified EventQueue.

In the following example, we show function calls to be executed immediately, at
a designed time, or periodically with an event queue. 

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *6_8_EventQueue* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      using namespace std::chrono;

      int main()
      {
         // creates a queue with the default size
         EventQueue queue;

         // printf will be put into queue and execute immediately
         queue.call(printf, "called immediately\r\n");
         // Replace Timeout
         queue.call_in(2s, printf, "called in 2 seconds\r\n");
         // Replace Ticker
         queue.call_every(1s, printf, "called every 1 seconds\r\n");

         // events are executed by the dispatch method
         queue.dispatch();
      }

#. Compile and run the program.

#. Record your results and push the code to your GitHub repo.

EventQueue in a Thread
==================================

In this part, we show an example to put an EventQueue in the context of a Thread.
Therefore, we can independently schedule calls of an EventQueue.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *6_9_Single_Thread_EventQueue* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"


      DigitalOut led1(LED1);
      InterruptIn sw2(BUTTON1);
      EventQueue queue(32 * EVENTS_EVENT_SIZE);

      Thread t;

      void led1_info() {
         // Note that printf is deferred with a call in the queue
         // It is not executed in the interrupt context
         printf("led1 is triggered! \r\n");
      }

      void Trig_led1()  {
         // Execute the time critical part first
         led1 = !led1;

	 // Ask the queue to schedule led1_info() immediately
         queue.call(led1_info);
      }

      int main() {
	 // callback() is used to wrap a API call to a queue object.
         // So, t will call queue.dispatch_forever(), 
	 // and it will start and run the queue scheduler of the EventQueue
         t.start(callback(&queue, &EventQueue::dispatch_forever));

         // 'Trig_led1' will execute in IRQ context
         sw2.rise(Trig_led1);
      }

#. Compile and run the program.

#. Record your results and push the code to your GitHub repo.

Scheduling of EventQueue Calls
====================================

The following steps are adapted from mbed `EventQueue tutorial <https://os.mbed.com/docs/mbed-os/v6.15/apis/scheduling-tutorials.html>`__

Let's consider an example of a program that attaches two interrupt handlers for
an InterruptIn object, using the InterruptIn rise and fall functions. The rise
handler will run in interrupt context, and the fall handler will run in user
context (more specifically, in the context of the event loop's thread).

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *6_10_Multi_Thread_EventQueue* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline
      
      /*
       * Copyright (c) 2020 Arm Limited and affiliates.
       * SPDX-License-Identifier: Apache-2.0
       */
      #include "mbed.h"
      
      DigitalOut led1(LED1);
      InterruptIn sw(BUTTON1);
      EventQueue queue(32 * EVENTS_EVENT_SIZE);
      Thread t;
      
      
      void rise_handler(void)
      {
          queue.call(printf, "rise_handler in context %p\n", ThisThread::get_id());
          // Toggle LED
          led1 = !led1;
      }
            
      void fall_handler(void)
      {
          printf("fall_handler in context %p\n", ThisThread::get_id());
          // Toggle LED
          led1 = !led1;
      }
      
      int main()
      {
          // Start the event queue
          t.start(callback(&queue, &EventQueue::dispatch_forever));
          printf("Starting in context %p\r\n", ThisThread::get_id());
          // The 'rise' handler will execute in IRQ context
          sw.rise(rise_handler);
          // The 'fall' handler will execute in the context of thread 't'
          sw.fall(queue.event(fall_handler));
      }

   The above code executes two handler functions (rise_handler and fall_handler) in two different contexts:

   #. In interrupt context when a rising edge is detected on SW2
      (rise_handler).
   #. In the context of the event loop's thread function when a falling edge is
      detected on SW2 (fall_handler). queue.event() is called with fall_handler as
      an argument to specify that fall_handler will run in user context instead of
      interrupt context.
            
#. Compile and run the program.

   We reset the board and pressed the SW2 button twice. 
   You should see a similar output as following print out:

   .. class:: terminal

      ::

	Starting in context 20001fe0
	fall_handler in context 20000b1c
	rise_handler in context 00000000
	fall_handler in context 20000b1c
	rise_handler in context 00000000
    
   The program starts in the context of the thread that runs the main function
   (20001fe0). When the user presses SW2, fall_handler is automatically queued
   in the event queue, and it runs later in the context of thread t (20000b1c).
   When the user releases the button, rise_handler is executed immediately, and
   it displays 00000000, indicating that the code ran in interrupt context.

#. Make the interrupt handler thread-safe

   The code for rise_handler is problematic because it calls printf in
   interrupt context, which is a potentially unsafe operation. Fortunately,
   this is exactly the kind of problem that event queues can solve. We can make
   the code safe by running rise_handler in user context (like we already do
   with fall_handler) by replacing this line:

   .. code-block:: c++

      sw.rise(rise_handler);

   with this line:

   .. code-block:: c++

      sw.rise(queue.event(rise_handler));
 
   Please run the program again.

#. Refactor ISR codes

   The code is safe now, but we may have introduced another problem: latency.
   After the change above, the call to rise_handler will be queued, which means
   that it no longer runs immediately after the interrupt is raised. For this
   example code, this isn't a problem, but some applications might need the
   code to respond as fast as possible to an interrupt.

   Let's assume that rise_handler must toggle the LED as quickly as possible in
   response to the user's action on SW2. To do that, it must run in interrupt
   context. However, rise_handler still needs to print a message indicating
   that the handler was called; that's problematic because it's not safe to
   call printf from an interrupt context.

   The solution is to split rise_handler into two parts: the time critical part
   will run in interrupt context, while the non-critical part (displaying the
   message) will run in user context. This is easily doable using queue.call:

   .. code-block:: c++

      void rise_handler_user_context(void) {
          printf("rise_handler_user_context in context %p\r\n", Thread::gettid());
      }
      
      void rise_handler(void) {
          // Execute the time critical part first
          led1 = !led1;
          // The rest can execute later in user context (and can contain code that's not interrupt safe).
          // We use the 'queue.call' function to add an event (the call to 'rise_handler_user_context') to the queue.
          queue.call(rise_handler_user_context);
      }
 
   After replacing the code for rise_handler as above, please run the program again.
   And the output will be like the following:

   .. class:: terminal

      ::

	Starting in context 0x20002c50
	fall_handler in context 0x20002c90
	rise_handler_user_context in context 0x20002c90
	fall_handler in context 0x20002c90
	rise_handler_user_context in context 0x20002c90

   The scenario above (splitting an interrupt handler's code into time critical
   code and non-time critical code) is another common pattern that you can
   easily implement with event queues; queuing code that's not interrupt safe
   is not the only thing you can use event queues for. Any kind of code can be
   queued and deferred for later execution.

   We used InterruptIn for the example above, but the same kind of code can be
   used with any attach()-like functions in the SDK. Examples include
   Serial::attach(), Ticker::attach(), Ticker::attach_us(), Timeout::attach().

#. Record your results and push the code to your GitHub repo.

Two Threads of EventQueue with Different Priorities
===================================================

We can differentiate between the importance of events by using multiple threads
that run with different priorities.  For more priority values detail, please
check Mbed OS Thread-APIs.

In this section, we add a Ticker to the program which toggles LED2 every
second, which runs with a higher priority than the printf calls by creating a
second event queue.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *6_11_OS_Priority* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include "mbed_events.h"
      using namespace std::chrono;

      DigitalOut led1(LED1);
      DigitalOut led2(LED2);
      InterruptIn btn(BUTTON1);

      EventQueue printfQueue;
      EventQueue eventQueue;

      void blink_led2() {
      // this runs in the normal priority thread
      led2 = !led2;
      }

      void print_toggle_led() {
      // this runs in the lower priority thread
      printf("Toggle LED!\r\n");
      }

      void btn_fall_irq() {
      led1 = !led1;
      // defer the printf call to the low priority thread
      printfQueue.call(&print_toggle_led);
      }

      int main() {

      // low priority thread for calling printf()
      Thread printfThread(osPriorityLow);
      printfThread.start(callback(&printfQueue, &EventQueue::dispatch_forever));

      // normal priority thread for other events
      Thread eventThread(osPriorityNormal);
      eventThread.start(callback(&eventQueue, &EventQueue::dispatch_forever));

      // call blink_led2 every second, automatically defering to the eventThread
      Ticker ledTicker;
      ledTicker.attach(eventQueue.event(&blink_led2), 1s);

      // button fall still runs in the ISR
      btn.fall(&btn_fall_irq);

      while (1) {ThisThread::sleep_for(1s);}
      }

#. Compile and run the program.

#. Record your results and push the code to your GitHub repo.

********************
Demo and Checkpoints
********************

#. You need to know how to write an interrupt service routine.
#. You need to know how to run a function at a designated time.
#. You need to know how to run a function periodically.
#. You need to know how to measure the latency between an interrupt event and an output signal.
#. You need to know how to process different tasks at the same time using thread and eventqueue.
#. Show your git remote repository.
#. Switch the blue LED every 500ms without using the sleep for function. (Hint: Maybe ticker will work.)
#. Demo Two Threads of EventQueue with Different Priorities.

**************
Reference List
**************

#. `Fast and embedded systems design <http://www.embedded-knowhow.co.uk/Book%203_files/LN_PDFs/mbed_bk_Ed2_Ch_9.pdf>`__
