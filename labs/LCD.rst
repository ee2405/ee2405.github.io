mbed Lab 5 Liquid Crystal Displays
##################################
:Date:    2022-03-9 15:00
:Tags:    Labs
:Summary: In this lab, we learn to use LCD displays: QC1602A and uLCD-144G2-AR.

.. sectnum::
      :depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

      The goal of this lab is to learn:

      #. How to display texts with LCD QC1602A in HD44780 interface
      #. How to display graphics with uLCD-144G2-AR

****************
Lab Due
****************

**Mar. 9, 2022**

**************
Equipment List
**************

#. B_L4S5I_IOT01A * 1
#. Breadboard * 1
#. LCD QC1602A * 1
#. uLCD 144G2 AR * 1

***************
Lab Description
***************

Lecture Notes
=============

- Chapter 6: Liquid Crystal Displays `ch6_lcd.pdf <notes/ch6_lcd.pdf>`__

LCD QC1602A with HD44780 interface
=============================================

.. container:: instruct

   In this section, we explore two methods to control QC1602A: (1) we build our
   own LCD library; and (2) we use an online library.  The first method creates
   a custom libary, so we have the flexbility to change and extend the libary
   to better fit our purpose. In the second method, the existing libary makes
   it easier for regular user of the LCD.  Still we can learn from the
   interface design from this pre-built library.

.. container:: warning

   For all the following, please unplug B_L4S5I_IOT01A from power while wiring
   circuits.

#. Connect your LCD to mbed as the following picture. `picture <labs/img/LCD/Lab4_LCD.png>`__

   .. container:: warning

                  **Be careful about pin connections. Double check before you turn on the power.**

                  +------------+------------+
                  | LCD        | mbed       |
                  +============+============+
                  | VSS        | GND        |
                  +------------+------------+
                  | VDD        | 5V         |
                  +------------+------------+
                  | vo         | GND        |
                  +------------+------------+
                  | RS         | D2         |
                  +------------+------------+
                  | R/W        | GND        |
                  +------------+------------+
                  | E          | D3         |
                  +------------+------------+
                  | DB0        | X          |
                  +------------+------------+
                  | DB1        | X          |
                  +------------+------------+
                  | DB2        | X          |
                  +------------+------------+
                  | DB3        | X          |
                  +------------+------------+
                  | DB4        | D4         |
                  +------------+------------+
                  | DB5        | D5         |
                  +------------+------------+
                  | DB6        | D6         |
                  +------------+------------+
                  | DB7        | D7         |
                  +------------+------------+
                  | A          | 5V         |
                  +------------+------------+
                  | K          | GND        |
                  +------------+------------+

Build your own LCD library
-----------------------------

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *5_1_LCD_QC1602A* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "LCD.h"

      int main()
      {
            LCD_init();                     // call the initialise function
            display_to_LCD(0x48);           // ‘H’
            display_to_LCD(0x45);           // ‘E’
            display_to_LCD(0x4C);           // ‘L’
            display_to_LCD(0x4C);           // ‘L’
            display_to_LCD(0x4F);           // ‘O’
            for(char x=0x30;x<=0x39;x++)
            {
                  display_to_LCD(x);      // display numbers 0-9
            }
      }


#. Add a LCD.h under 5_1_LCD_QC1602A. And enter the following source code in LCD.h.

   .. code-block:: c++
      :linenos: inline

      #ifndef LCD_H
      #define LCD_H

      #include "mbed.h"

      void toggle_enable(void);        //function to toggle/pulse the enable bit
      void LCD_init(void);             //function to initialise the LCD
      void display_to_LCD(char value); //function to display characters
      void set_location(char location);//function to set display location

      #endif

#. Add a LCD.cpp under 5_1_LCD_QC1602A. And enter the following source code in LCD.cpp.

   .. code-block:: c++
      :linenos: inline

      #include "LCD.h"

      DigitalOut RS(D2);            //check out these pin numbers CAREFULLY!!!
      DigitalOut E(D3);
      BusOut data(D4,D5,D6,D7);

      void toggle_enable(void)
      {
            E=1;
            ThisThread::sleep_for(1ms);
            E=0;
            ThisThread::sleep_for(1ms);
      }

      //initialise LCD function
      void LCD_init(void)
      {
            ThisThread::sleep_for(20ms);             // pause for 20 ms
            RS=0;                   // set low to write control data
            E=0;                    // set low

            //function mode
            data=0x2;               // 4 bit mode (data packet 1, DB4-DB7)
            toggle_enable();
            data=0x8;               // 2-line, 7 dot char (data packet 2, DB0-DB3)
            toggle_enable();
            //display mode
            data=0x0;               // 4 bit mode (data packet 1, DB4-DB7)
            toggle_enable();
            data=0xF;               // display on, cursor on, blink on
            toggle_enable();

            //clear display
            data=0x0;
            toggle_enable();
            data=0x1;               // clear
            toggle_enable();
      }

      //display function
      void display_to_LCD(char value)
      {
            RS=1;               // set high to write character data
            data=value>>4;      // value shifted right 4 = upper nibble
            toggle_enable();
            data=value;         // value bitmask with 0x0F = lower nibble
            toggle_enable();
      }

      void set_location(char location)
      {
            RS=0;
            data=(location|0x80)>>4;        // upper nibble
            toggle_enable();
            data=location&0x0F;             // lower nibble
            toggle_enable();
      }

#. Compile and run the program

#. Please record your results and push codes to GitHub.

Import "textLCD" library
------------------------

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *5_2_textLCD* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Add a library to the current project

   #. Click **+** in the Library tab under program source.

   #. Fill in `https://gitlab.larc-nthu.net/ee2405_2021/textlcd.git`
      And click "Next"

   #. Select "Master" branch and click "Finish"

#. Please run each of the following 3 example codes as :file:`main.cpp`.

   #. Example 1

      .. code-block:: c++
         :linenos: inline

         #include "mbed.h"
         #include "TextLCD.h"

         TextLCD lcd(D2, D3, D4, D5, D6, D7); // RS, E, DB4-DB7

         int main()
         {
               lcd.printf("HELLO\n");
               for (char x = 0x00; x <= 0x09; x++)
               { // display numbers 0-9
                     lcd.printf("%u", x);
               }
         }   

   #. Example 2

      .. code-block:: c++
         :linenos: inline

         #include "mbed.h"
         #include "TextLCD.h"

         DigitalOut led(LED1);      //LED1 = PA_5
         TextLCD lcd(D2, D3, D4, D5, D6, D7);

         int main()
         {
               int x=0;
               lcd.printf("Hello World!\n");
               while(true)
               {
                     led = !led;             // toggle led
                     lcd.locate(5,1);
                     lcd.printf("%5i",x);    //counter display
                     ThisThread::sleep_for(1s);
                     x++;
               }
         }
      
   #. Example 3
      In this example, please connect picoscope as a source to pin A0.
      Please do not power up the circuit, during wiring the circuit.

      .. code-block:: c++
         :linenos: inline

         //Display ADC input data
         #include "mbed.h"
         #include "TextLCD.h"

         TextLCD lcd(D2, D3, D4, D5, D6, D7);
         AnalogIn Ain(A0);

         int main()
         {
               float percentage;
               int D;
               while (1)
               {
                     percentage = Ain * 100;
                     D = int(percentage);
                     float B = percentage - D;
                     int C = B * 1000000;

                     lcd.printf("%d.", D);
                     lcd.printf("%d", C);
                     ThisThread::sleep_for(250ms);
                     lcd.cls();
               }
         }


#. Compile and run the program.

#. Record your results and push the codes.

Color LCD display - uLCD-144G2-AR
=============================================

.. container:: instruct

      (From 4D Systems): The uLCD-144G2 display module is compact and cost
      effective and features a 1.44” LCD TFT screen. Driven by the GOLDELOX
      processor, the uLCD-144G2 is the compact display solution for
      any application requiring a small embedded screen.

      * 128xRGBx128 resolution, 65K true to life colours, LCD-TFT screen.
      * 1.44" diagonal size, 43 x 31 x 6.4mm. Active Area: 25.5mm x 26.5mm.
      * Easy 10 pin interface to any external device: 3.3Vout, IO2, GND, IO1, RESET, GND, RX, TX, +5V, 5V OUT.
      * 10K bytes of flash memory for user code storage and 510 bytes of RAM for user variables (255 x 16bit vars).
      * 1 x Asynchronous hardware serial port, TTL interface, with 300 baud to 600K baud.
      * On-board micro-SD memory card adaptor for storing of icons, images, animations, etc.

#. Connect your LCD to mbed as the following `picture <labs/img/LCD/board_uLCD.jpg>`__ .

   .. container:: warning

                  **Please be careful about pin connections. Double check before you turn on the power.**

                  +------------+------------+
                  | LCD        | mbed       |
                  +============+============+
                  | +5V        | 5V         |
                  +------------+------------+
                  | TX         | D1         |
                  +------------+------------+
                  | RX         | D0         |
                  +------------+------------+
                  | GND        | GND        |
                  +------------+------------+
                  | RES        | D2         |
                  +------------+------------+

#. Go to `the link <https://developer.mbed.org/users/4180_1/notebook/ulcd-144-g2-128-by-128-color-lcd/>`__ and read the web page carefully.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *5_3_uLCD* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Add "4DGL-uLCD-SE" library to the current project

   #. Click **+** in the Library tab under program source.

   #. Fill in `https://gitlab.larc-nthu.net/ee2405_2021/4dgl-ulcd-se.git`
      And click "Next"

   #. Select "Master" branch and click "Finish"

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"
      #include "uLCD_4DGL.h"
      
      uLCD_4DGL uLCD(D1, D0, D2);
      
      int main() {
        printf("uLCD printing...\n");
        uLCD.color(WHITE);
        uLCD.printf("\nHello uLCD World\n");
        ThisThread::sleep_for(1s);
        uLCD.printf("Counting down:\n");
        uLCD.text_width(4); // 4X size text
        uLCD.text_height(4);
        uLCD.color(RED);
        for (int i = 10; i >= 0; --i) {
          uLCD.locate(1, 2);
          uLCD.printf("%2d", i);
          ThisThread::sleep_for(1000ms);
        }
        printf("Done.\n");
      }

#. Compile and run the program.

#. Record your results and push the code to your GitHub repo

#. uLCD functions

   .. container:: instruct

         There are five types of commands set up by the library for easier control.
         Here we introduce some of them for your reference.

   Please dive into **uLCD_4DGL.h** for more information of the programming interface (API).

   #. General functions

      - **uLCD.cls()** clears the entire screen using the background color.

      - **uLCD.reset()** wipes the entire screen.

      - **uLCD.background_color(int color)** changes the background color.

        Ex. uLCD.background_color(0xFFFFFF) // white

   #. Graphic functions

      These functions draws simple shapes.

      - **uLCD.circle(int x , int y , int radius, int color)**

      - **uLCD.triangle(int x1, int y1, int x2, int y2, int x3, int y3, int color)**

      - **uLCD.line(int x1, int y1 , int x2, int y2, int color)**

   #. Text functions

      - **uLCD.set_font(char mode)**. ex. uLCD.set_font(FONT_7X8)

        This function set the size of the font(width=7, height=8).

      - **uLCD.locate(char col, char row)**. ex. uLCD.locate(0, 0)

        This function sets the location of the cursor. Then we can put our text anywhere we want to.

   #. Media

      This type of command is for displaying video or image from SD card. If you are interested in doing so, please go to `the link <https://developer.mbed.org/users/4180_1/notebook/ulcd-144-g2-128-by-128-color-lcd/>`__ and scroll to the buttom part for complete tutorial.

   #. Screen data

      We can get LCD hardware information via this type of command.

      Ex. int a=uLCD.type;

   #. Text data

      We can get text information via this type of command.

      Ex. Get cursor location: char column=uLCD.current_col;


********************
Demo and Checkpoints
********************

#. Show your git remote repository.
#. Show your student ID number and a 30 second count down on QC1602A.
#. Show your student ID number in blue, a 30 second count down in green, and a white background on uLCD-144G2.
