mbed Lab 8 Wireless Communication - Bluetooth 
####################################################
:Date:    2019-03-28 18:00
:Tags:    Labs
:Summary: To learn about how to communicate with HC05 Bluetooth modules
:Status: Draft

.. sectnum::
	:depth: 2

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

        The goal of this lab is to learn:

        #. Using AT Command Mode to control HC05
        #. Send and receive messages with HC05s 
        #. Send RPC commands over Bluetooth channels

****************
Lab Introduction
****************

HC‐05 module is an easy to use Bluetooth SPP (Serial Port Protocol) module,
designed for transparent wireless serial connection setup. The HC-05 Bluetooth
Module can be used in a Master or Slave configuration, making it a practical
and inexpensive solution for wireless communication. In this lab, you can learn
how to setup HC05 modules by AT Commands, and then communicate between two
connected devices with Bluetooth.


***************
Lab Description
***************

Lecture Notes
=============

- `Introduction to Bluetooth pdf <notes/mbed8/Bluetooth_Introduction.pdf>`__ (`pptx <notes/mbed8/Bluetooth_Introduction.pptx>`__)

Preparation
===========

#. Please login gitlab and add a :file:`result.md` under :file:`mbed08` for writing lab records.
   Please also copy the gitlab project URL.

#. Start a terminal with :hotkey:`Ctrl+Alt+T`

#. Clone and prepare a working directory

   #. :cmd_host:`$ cd ~/ee2405`

   #. :cmd_host:`$ git clone <URL>`

      <URL> is the gitlab project URL: ``git@gitlab.larc-nthu.net:106061600/mbed08.git``.

.. container:: warning

        For all the following, please unplug K64F from power while wiring circuits.

How to connect with 2 HC05s
=============================

#. Pin connection

   +-------------------+----------------+
   | **HC05 pin**      | **Mbed pin**   |
   +===================+================+
   | 1 - Tx(TXD)       | D7 - Rx        |
   +-------------------+----------------+
   | 2 - Rx(RXD)       | D9 - Tx        |
   +-------------------+----------------+
   | 12 - 3.3V(VCC)    | Vout - 3.3V    |
   +-------------------+----------------+
   | 13 - GND(GND)     | GND            |
   +-------------------+----------------+
   | 31 - PIO8         | --             |
   +-------------------+----------------+
   | 32 - PIO9         | --             |
   +-------------------+----------------+
   | 34 - PIO11(KEY)   | D10            |
   +-------------------+----------------+
   

   :hl:`PIO11` connect to :hl:`3.3V` would be in AT Command Mode, and connect to :hl:`GND` would be in Communication Mode.
  
   The picture below is Slave connection(Master has HC05 only).   
 
   .. image:: labs/img/mbed8/combine.png
      :alt: Wiring for LCD & HC05

Manually Connection
====================

#. HC05-Slave Setting

   #. Switch to a terminal or start a new terminal with :hotkey:`Ctrl+Alt+T`.

   #. Create a new Mbed project.

      :cmd_host:`$ cd ~/ee2405/mbed08`

      :cmd_host:`$ mbed new 8_1_HC05-ATCommand`

      :cmd_host:`$ cd 8_1_HC05-ATCommand`

   #. Start VS code to edit :file:`main.cpp`.

      :cmd_host:`$ code main.cpp &`

   #. Copy the following codes into :file:`main.cpp`.
      
      .. code-block:: c++
         :linenos: inline

         #include "mbed.h"

         Serial pc(USBTX, USBRX);
         Serial HC05(D9, D7);
         DigitalOut KEY(D10);
         InterruptIn button(SW2);

         char str[50];

         void mode(){
              if(KEY == 1.0) KEY = 0;
              else KEY = 1.0;

              HC05.printf("AT+RESET\r\n");
         }

         int main(){
             int i=0;
             pc.baud(115200);
             HC05.baud(38400);
             
             pc.printf("Begin test\r\n");
             HC05.printf("AT\r\n");
             
             KEY = 1.0;
             
             button.rise(&mode);

             while(1){
                 if(pc.readable()){
                    char c = pc.getc();
                    if(c!='\r'&&c!='\n'){
                       pc.printf("%c", c);
                       str[i++] = c;
                    }
                    else{
                       pc.printf("(%d)\r\n", c);
                       str[i] = 0;
                       i=0;
                       HC05.printf("%s\r\n", str);
                    }
                 }
                 while(HC05.readable()){
                    char c = HC05.getc();
                    pc.printf("%c",c);

                 }
                 wait(.001);
             }          
         }


   #. Compile the project.
      
      :cmd_host:`$ sudo mbed compile -m K64F -t GCC_ARM -f`

      .. code-block:: c++
         :linenos: inline
      
         void mode(){
              if(KEY == 1.0) KEY = 0;
              else KEY = 1.0;
      
              HC05.printf("AT+RESET\r\n");
         }
      
      The above code uses a interrupt (SW2) to switch between 2 modes, and restart HC05 automatically.

   #. Use screen to enter AT command mode for setting up HC05.
      
      #. Open the serial terminal on Ubuntu
      
         :cmd_host:`$ sudo screen /dev/ttyACM* 115200`

      #. Test if HC05 is setup correctly.
         
         Press the :hl:`RESET` on the K64F, and see the :hl:`Begin test` and :hl:`OK`
         on the screen.

         :cmd_host:`AT`

         After typing :cmd_host:`AT`, you should receive :hl:`OK` from HC05.

      #. Set the baud rate of HC05.
      
         To check the baud rate of HC05, :cmd_host:`AT+UART?`

         The default value is :hl:`9600,0,0`. And we set a new baud rate at 38400.

         :cmd_host:`AT+UART=38400,1,0`
      
      #. Set name string for HC05.
         
         :cmd_host:`AT+NAME=Slave`
      
      #. Set the role of HC05.
         
         :cmd_host:`AT+ROLE=0` 
         
         .. container:: instruct

            If your device is a master, then :cmd_host:`AT+ROLE=1`. Otherwise, if your device is a slave, then :cmd_host:`AT+ROLE=0`
            
            If a HC05 is a slave, it can be searched by other master devices.

      #. Set connection mode.

         Check the connected mode with command :cmd_host:`AT+CMODE?`
       
         Here we would like to set it to 0. If it is not 0, set the mode with the following command:
         
         :cmd_host:`AT+CMODE=0`
         
         .. container:: instruct

            When mode=0, you must bind a specified slave's address manually. 
            When mode=1, a master will bind slave with the same password automatically.

      #. Set the password (please use your seat number).
      
         :cmd_host:`AT+PSWD=12XX`

	 Where XX=your seat number.

         Password 1234 is the default value, you must use another value.
         
         Please set up master's and slave's password the same as each other,
         so later master will connect to a slave automatically.

	 Also we do not want to connect to other students' HC05 automatically.
	 Please avoid the default password and setup your own password according to your seat number.
      
      #. Look up the slave address and please copy-and-paste it to a text file (for master to connect to).

         :cmd_host:`AT+ADDR?`

      #. Reset HC05 to apply new settings.
      
         :cmd_host:`AT+RESET`

         `Setting complete <labs/img/mbed8/SAV.png>`__

   #. Enter the communication mode.
      
      - Change KEY to GND.
      
        Press SW2, and HC05 will enter communication mode (and Reset again).

      - If you want to back to AT mode, just press SW2 again.
         
   .. container:: instruct

      If you want to reset all the setup to factory settings, you can use the following command.
   
      :cmd_host:`AT+ORGL`


#. HC05-Master Setting and Link to Slave

   #. Connect another HC05 and K64F (or K66F) boards (the master device).

      Please unplug slave device, so mbed cli tool works correctly on master device.

   #. Switch to a terminal or start a new terminal with :hotkey:`Ctrl+Alt+T`.

   #. Go into the previous Mbed project.

      :cmd_host:`$ cd ~/ee2405/mbed08/HC05-ATCommand`

      In manual settings, master will run the same code as slave device.

   #. Compile the project.
      
      :cmd_host:`$ sudo mbed compile -m K64F -t GCC_ARM -f`

   #. Use screen to enter the AT command mode to setup HC05.
      
      #. Open the serial terminal on Ubuntu
      
         :cmd_host:`$ sudo screen /dev/ttyACM* 115200`

      #. Test if HC05 is setup correctly.
         
         Press the :hl:`RESET` on the K64F, and see the :hl:`Begin test` and :hl:`OK`
         on the screen.

         :cmd_host:`AT`

         After typing :cmd_host:`AT`, you should receive :hl:`OK` from HC05.

      #. Set the baud rate of HC05.
      
         To check the baud rate of HC05, :cmd_host:`AT+UART?`

         The default value is :hl:`9600,0,0`. And we set a new baud rate at 38400.

         :cmd_host:`AT+UART=38400,1,0`
      
      #. Set name string for HC05.
      
         :cmd_host:`AT+NAME=Master`
         
      #. Set the role of HC05.
         
         :cmd_host:`AT+ROLE=1`
         
         .. container:: instruct

            Since this device is a master, :cmd_host:`AT+ROLE=1`. A master device will not be searched during inquiry phase.

      #. Set connection mode.

         Check the connected mode with command :cmd_host:`AT+CMODE?`
       
         Here we would like to set it to 0. If it is not 0, set the mode with the following command:
         
         :cmd_host:`AT+CMODE=0`
         
         .. container:: instruct

            When mode=0, you must bind a specified slave's address manually. 
            When mode=1, a master will bind slave with the same password automatically.

      #. Check binding address.

         :cmd_host:`AT+BIND?`

         Default binding address :hl:`+BIND:0:0:0`.

      #. Set the password (please use the same password as your slave device).
      
         :cmd_host:`AT+PSWD=12XX`
         
         Please set up master's and slave's password the same as each other,
         so later master will connect to a slave automatically.

         `Setting complete <labs/img/mbed8/MST.png>`__

      #. Reset and initialize the HC05.
      
         :cmd_host:`AT+RESET`

         :cmd_host:`AT+INIT`

      #. Set inquiring mode.
      
         :cmd_host:`AT+INQM=1,9,48`

      #. Inquire (Search the bluetooth device). `Inquire <labs/img/mbed8/INQ.png>`__
      
         :cmd_host:`AT+INQ`
         
         You can see bluetooth devices nearby, and screen will show their addresses.
         
         And try to use :cmd_host:`AT+STATE?` command, which will respond :hl:`+STATE:INQUIRING`.

      #. End of Inquiry.
      
         :cmd_host:`AT+INQC`
         
         If you recieve the response :hl:`OK`, your device is back to initialization state.
	 To confirm, use command :cmd_host:`AT+STATE?`.
         
         After you leave the inquiring state, you should reset and initial it again.
   
   #. Connect to target Slave
   
      #. Bind device.
      
         :cmd_host:`AT+BIND=<device's address you want to bind>`

	 This is the address you recorded in earlier section.
         For example, you find that the slave address is AAAA:BB:CCCCCC, you should type
         :hl:`AT+BIND=AAAA,BB,CCCCCC`
      
      #. Pair device.
      
         :cmd_host:`AT+PAIR=<device's address you want to pair>,<pair time>`
         
         For example, you find that the slave address is AAAA:BB:CCCCCC, you should type
         :hl:`AT+PAIR=AAAA,BB,CCCCCC,10`
         
         When you recieve the response :hl:`OK`, check the state is in PAIRED or not.
      
      #. Link device.
      
         :cmd_host:`AT+LINK=<device's address you want to link>`
         
         For example, you find that the slave address is AAAA:BB:CCCCCC, you should type
         :hl:`AT+LINK=AAAA,BB,CCCCCC`
         
         After linking to slave successfully, master will be in communication mode
         without changing the KEY to GND.

         `ScreenShot <labs/img/mbed8/Send.png>`__

   #. If you want to return to AT mode, press SW2 twice and type :cmd_host:`AT+RESET`.

   #. After you boot both slave and master up, you can type and transmit messages between master and slave .

Automatical connection
=======================

#. We change a few settings for automatic pairing of master and slave.

   You need to connect both devices to apply AT commands. Please make sure screen is connect to the correct ACM devices.

   #. HC05-Slave Setting

      #. Change the cmode of HC05.

         :cmd_host:`AT+CMODE=1`

      #. Restart the HC05.

         :cmd_host:`AT+RESET`

      #. Press the SW2 to enter the communication mode.

   #. HC05-Master Setting

      #. Change the cmode of HC05.

         :cmd_host:`AT+CMODE=1`

      #. Restart the HC05.

         :cmd_host:`AT+RESET`

      #. Check the bind address is the default value. 
         If not, please initialize it:

         :cmd_host:`AT+BIND=0,0,0`

      #. Press the SW2 to enter the communication mode.

   #. When 2 HC05s enter the communication mode, they will link automatically.

      The Master port can return to AT mode to check that it's bound to your slave device.

      :cmd_host:`AT+BIND?`

   #. Again, you can type and transmit messages between master and slave .

.. container:: warning

      Please set CMODE to the same value, either to connect to slave manually or automatically.

#. Record your results in :file:`result.md`.

#. Publish your finished codes and :file:`result.md`.

   :cmd_host:`$ cd ~/ee2405/mbed08`

   :cmd_host:`$ git pull`

   :cmd_host:`$ git add 8_1_HC05-ATCommand/main.cpp`

   :cmd_host:`$ git commit -m "8_1_HC05-ATCommand"`

   :cmd_host:`$ git push`


HC05 application
====================

#. Master links through the Password and Address Slave shows on the LCD.
   
   #. Prepare for Slave.

      #. Switch to a terminal or start a new terminal with :hotkey:`Ctrl+Alt+T`.

      #. Create a new Mbed project.

         :cmd_host:`$ cd ~/ee2405/mbed08`

         :cmd_host:`$ mbed new 8_2_Slave_LCD`

         :cmd_host:`$ cd 8_2_Slave_LCD`

      #. Start VS code to edit :file:`main.cpp`.

         :cmd_host:`$ code main.cpp &`

      #. Copy the following codes into :file:`main.cpp`.
         
         .. code-block:: c++
            :linenos: inline
        
            #include "mbed.h"
            #include "TextLCD.h"

            Serial pc(USBTX, USBRX);
            Serial HC05(D9, D7);
            DigitalOut KEY(D10);
            InterruptIn button2(SW2);
            InterruptIn button3(SW3);
            TextLCD lcd(D2,D3,D4,D5,D6,D8);

            char str[50];
            char pwd[15];
            int  n[4];
            int  cnt = 0;

            void mode(){
                 if(KEY == 1.0){
                    KEY = 0;
                 }
                 else{
                    KEY = 1.0;
                 }
                 HC05.printf("AT+RESET\r\n");
            }

            void show(){
                 int o;
                 char p;
                 
                 HC05.printf("AT+PSWD?\r\n");
                 while(HC05.getc() != ':'){}
                 for(o=0;o<6;o++){
                    p = HC05.getc();
                    pc.printf("%c", p);
                    lcd.putc(p);
                 }
                 HC05.printf("AT+ADDR?\r\n");
                 while(HC05.getc() != ':'){}
                 for(o=0;o<16;o++){
                    p = HC05.getc();
                    pc.printf("%c", p);
                    lcd.putc(p);
                 }
                 cnt++;
                 if(cnt==2){
                    cnt = 0;
                    lcd.cls();
                 }

            }

            int main(){
                int i=0;
                int j=0;
                pc.baud(115200);
                HC05.baud(38400);
                pc.printf("Begin test\r\n");

                srand(time(NULL));
                for(j=0;j<4;j++){ 
                    n[j] = rand()%10;
                }
                sprintf(pwd,"AT+PSWD=%d%d%d%d\0",n[0],n[1],n[2],n[3]);
                HC05.printf("%s\r\n",pwd);

                KEY = 1.0;

                button2.rise(&mode);
                button3.rise(&show);
                    
                while(1){
                    if(pc.readable()){
                       char c = pc.getc();
                       if(c!='\r'&&c!='\n'){
                          pc.printf("%c", c);
                          str[i++] = c;
                       }
                       else{
                          pc.printf("(%d)\r\n", c);
                          str[i] = 0;
                          i=0;
                          HC05.printf("%s\r\n", str);
                       }
                    }
                    while(HC05.readable()){
                       char c = HC05.getc();
                       pc.printf("%c",c);

                    }
                    wait(.001);
                }
            }

      #. Add a library to the current project

         #. Before adding a library, we need to install an required package mercurial.

            :cmd_host:`$ sudo apt install mercurial`

         #. Add the library.

            :cmd_host:`$ mbed add https://os.mbed.com/users/wim/code/TextLCD/`

      #. Compile the project.
      
         :cmd_host:`$ sudo mbed compile -m K64F -t GCC_ARM -f`
     
         .. code-block:: c++
            :linenos: inline
         
            srand(time(NULL));
            for(j=0;j<4;j++){ 
                n[j] = rand()%10;
            }
            sprintf(pwd,"AT+PSWD=%d%d%d%d\0",n[0],n[1],n[2],n[3]);
            HC05.printf("%s\r\n",pwd);
         
         When pressing the reset on the K64F, it will set a new password randomly.
         
         .. code-block:: c++
            :linenos: inline
         
             HC05.printf("AT+PSWD?\r\n");
             while(HC05.getc() != ':'){}
             for(o=0;o<6;o++){
                p = HC05.getc();
                pc.printf("%c", p);
                lcd.putc(p);
             }
         
         To show the random password on LCD screen.

      #. Try to press SW3, and it trigger an interrupt to inquire the HC05's password and print on screen and LCD.

      #. Please check setting so that Master would link together.

      #. Remember to change to communication mode by pressing SW2.
      
   #. Prepare for Master. 

      #. Switch to a terminal or start a new terminal with :hotkey:`Ctrl+Alt+T`.

      #. Create a new Mbed project.

         :cmd_host:`$ cd ~/ee2405/mbed08`

         :cmd_host:`$ mbed new 8_3_Master`

         :cmd_host:`$ cd 8_3_Master`

      #. Start VS code to edit :file:`main.cpp`.

         :cmd_host:`$ code main.cpp &`

      #. Copy the following codes into :file:`main.cpp`.
         
         .. code-block:: c++
            :linenos: inline

            #include "mbed.h"

            Serial pc(USBTX, USBRX);
            Serial HC05(D9, D7);
            DigitalOut KEY(D10);
            InterruptIn button(SW2);
            InterruptIn button1(SW3);

            char str[50];
            int R;

            void mode(){
                 if(KEY == 1.0) KEY = 0;
                 else KEY = 1.0;

                 HC05.printf("AT+RESET\r\n");
            }

            void RPCPY(){
                 if(R==0) R=1;
                 else     R=0;
            }

            int main(){
                int i=0;
                pc.baud(115200);
                HC05.baud(38400);
                pc.printf("Please Select Slave Address to Bind !!!\r\n");
                pc.printf("Please Enter The Corresponding Password !!!\r\n");
                HC05.printf("AT\r\n");
                
                KEY = 1.0;
                R=0;
                
                button.rise(&mode);
                button1.rise(&RPCPY);
                 
                while(1){
                  if(R==0){
                    if(pc.readable()){
                       char c = pc.getc();
                       if(c!='\r'&&c!='\n'){
                          pc.printf("%c", c);
                          str[i++] = c;
                       }
                       else{
                          pc.printf("(%d)\r\n", c);
                          str[i] = 0;
                          i=0;
                          HC05.printf("%s\r\n", str);
                       }
                    }
                  }
                  else{
                     for(i=0;i<20;i++){
                        str[i] = pc.getc();
                        str[i+1] = 0;
                     }
                     HC05.printf("%s\r\n",str);
                     pc.printf("%s\r\n",str);
                  
                  }
                    while(HC05.readable()){
                       char c = HC05.getc();
                       pc.printf("%c",c);
                    }
                    wait(.001);
                }
            }

      #. Compile the project.
      
         :cmd_host:`$ sudo mbed compile -m K64F -t GCC_ARM -f`

      #. Use screen to enter the AT command mode to setup HC05.
      
         :cmd_host:`$ sudo screen /dev/ttyACM* 115200`

      #. Please setup HC05 step by step and link to Slave with password and address
         shows on the LCD in previous section. `picture <labs/img/mbed8/LCD.jpg>`__

      #. After pairing, you can type and transmit messages between master and slave .

      #. Record your results in :file:`result.md`.

      #. Publish your finished codes and :file:`result.md`.

         :cmd_host:`$ cd ~/ee2405/mbed08`

         :cmd_host:`$ git pull`

         :cmd_host:`$ git add 8_3_Master/main.cpp 8_2_Slave_LCD/main.cpp`

         :cmd_host:`$ git commit -m "8_2_8_3_Master&Slave"`

         :cmd_host:`$ git push`

#. Slave control through RPC.

   #. Prepare for Slave.

      #. Switch to a terminal or start a new terminal with :hotkey:`Ctrl+Alt+T`.

      #. Create a new Mbed project.

         :cmd_host:`$ cd ~/ee2405/mbed08`

         :cmd_host:`$ mbed new 8_4_Slave_RPC`

         :cmd_host:`$ cd 8_4_Slave_RPC`

      #. Add the RPC library into the project.

         :cmd_host:`$ cd mbed-os/drivers`

         :cmd_host:`$ cp ../features/unsupported/rpc/* .`

      #. Start VS code to edit :file:`main.cpp`.

         :cmd_host:`$ cd ~/ee2405/mbed08/8_4_Slave_RPC`

         :cmd_host:`$ code main.cpp &`

      #. Copy the following codes into :file:`main.cpp`.
         
         .. code-block:: c++
            :linenos: inline
      
            #include "mbed.h"
            #include "mbed_rpc.h"
            #include "TextLCD.h"

            Serial pc(USBTX, USBRX);
            Serial HC05(D9, D7);
            DigitalOut KEY(D10);
            InterruptIn button2(SW2);
            InterruptIn button3(SW3);
            RpcDigitalOut myled1(LED1, "myled1");
            RpcDigitalOut myled2(LED2, "myled2");
            RpcDigitalOut myled3(LED3, "myled3");
            TextLCD lcd(D2,D3,D4,D5,D6,D8);

            char str[50];
            char pwd[15];
            int  p[4];
            int  cnt = 0;

            void mode(){
                 if(KEY == 1.0) KEY = 0;
                 else           KEY = 1.0;
         
                 HC05.printf("AT+RESET\r\n");
            }

            void show(){
                 int o;
                 char p;

                 if(KEY == 1){
                    HC05.printf("AT+PSWD?\r\n");
                    while(HC05.getc() != ':'){}
                    for(o=0;o<6;o++){
                       p = HC05.getc();
                       lcd.putc(p);
                    }
                    HC05.printf("AT+ADDR?\r\n");
                    while(HC05.getc() != ':'){}
                    for(o=0;o<16;o++){
                       p = HC05.getc();
                       lcd.putc(p);
                    }
                    cnt++;
                    if(cnt==2){
                       cnt = 0;
                       lcd.cls();
                    }
                }
                else{
                    myled1.write(0);
                    myled2.write(0);
                    myled3.write(0);
                }
            }

            int main(){
                int i=0;
                int j=0;
                int k=0;
                char buf[64],outbuf[64];
                pc.baud(115200);
                HC05.baud(38400);
                pc.printf("Begin test\r\n");

                srand(time(NULL));
                for(j=0;j<4;j++){     //password generator
                    p[j] = rand()%10; //random OK
                }
                sprintf(pwd,"AT+PSWD=%d%d%d%d\0",p[0],p[1],p[2],p[3]); //setting string
                HC05.printf("%s\r\n",pwd); //setting the password, return OK
                    
                KEY = 1.0;
                
                button2.rise(&mode);     //AT <--> Comm
                button3.rise(&show);     //PSWD & ADDR
                    
                while(1){                //slave just receive the information
                    if(pc.readable()){   //another setting requirment
                       char c = pc.getc();
                       if(c!='\r'&&c!='\n'){
                          pc.printf("%c", c);
                          str[i++] = c;
                       }
                       else{
                          pc.printf("(%d)\r\n", c);
                          str[i] = 0;
                          i=0;
                          HC05.printf("%s\r\n", str);
                       }
                    }
                    while(HC05.readable()){     //receive command from PC or another HC05
                        char c = HC05.getc();
                    
                        if(KEY ==1) pc.printf("%c",c);  //KEY=0,1 print back receive word
                        else{                           //KEY=0 Communication mode
                            HC05.printf("%c",c);
                            if(c!='\r'&&c!='\n'){
                                buf[k++] = c;
                            }
                            else{
                                buf[k] = 0;
                                k=0;
                                RPC::call(buf,outbuf);
                                HC05.printf("%s\r\n",outbuf);
                            }
                        }
                    }
                    wait(.001);
                }
            }

      #. Compile the project.
      
         :cmd_host:`$ sudo mbed compile -m K64F -t GCC_ARM -f`

      #. Use screen to enter the AT command mode to setup HC05.
      
         :cmd_host:`$ sudo screen /dev/ttyACM* 115200`

   #. Prepare for Master.

      #. You can compile with the same code from previous section.

      #. Link to slave.

      #. Send the RPC command to control the Slave's LEDs.

         :cmd_host:`/myled1/write 1`
        
         :cmd_host:`/myled2/write 1`
        
         :cmd_host:`/myled3/write 1`
        
         :cmd_host:`/myled1/write 0`
        
         :cmd_host:`/myled3/write 0`
        
         :cmd_host:`/myled2/write 0`

   #. Record your results in :file:`result.md`.

   #. Publish your finished codes and :file:`result.md`.

      :cmd_host:`$ cd ~/ee2405/mbed08`

      :cmd_host:`$ git pull`

      :cmd_host:`$ git add 8_4_Slave_RPC/main.cpp`

      :cmd_host:`$ git commit -m "8_4_Slave_RPC"`

      :cmd_host:`$ git push`

RPC Over HC05 through Python
=============================

#. Switch to a terminal or start a new terminal with :hotkey:`Ctrl+Alt+T`.

#. Change to the target project.

   :cmd_host:`$ cd ~/ee2405/mbed08/8_3_Master`

#. Start VS code to edit :file:`myled.py`.

   :cmd_host:`$ code myled.py &`

#. Copy the following code into :file:`myled.py`.
      
   .. code-block:: python 
 
      import serial
      import time
      serdev = '/dev/ttyACM0'
      s = serial.Serial(serdev)
      s.baudrate = 115200

      s.write("/myled1/write 1     ")
      line=s.readline() # Read an echo string from K64F terminated with '\n'
      print(line)
      time.sleep(1)

      s.write("/myled2/write 1     ")
      line=s.readline() # Read an echo string from K64F terminated with '\n'
      print(line)
      time.sleep(1)

      s.write("/myled3/write 1     ")
      line=s.readline() # Read an echo string from K64F terminated with '\n'
      print(line)
      s.close()


#. Before running the python code, press the SW3 on the Master K64F.

#. Execute above Python script with :hl:`sudo`

   Please locate where you store myled.py in shell and cd into the directory. 

   :cmd_host:`$ sudo python myled.py`

#. Record your results in :file:`result.md`.

#. Publish your finished codes and :file:`result.md`.

   :cmd_host:`$ cd ~/ee2405/mbed08`

   :cmd_host:`$ git pull`

   :cmd_host:`$ git add 8_3_Master/myled.py`

   :cmd_host:`$ git commit -m "8_3_myled"`

   :cmd_host:`$ git push`

HC05 connect to mobile device (Optional)
========================================

#. HC05(Slave) and Phone(Master)
   
   #. HC05 go into the AT mode, and setup with the same as previous work about slave.
   
   #. Your phone can install the app **Terminal Multi FREE** and open the bluetooth to search HC05.
   
   #. When pairing is OK, open the app and choose HC05 to connect.
   
   #. Open the screen and try to do communication.

#. HC05(Master) and Phone(Slave)
   
   HC05 go into the AT mode.
   
   #. Test AT mode is workable.
   
      :cmd_host:`AT`
   #. Change role to master.
   
      :cmd_host:`AT+ROLE=1`
   #. Change name.
   
      :cmd_host:`AT+NAME=Master`
   #. Change key.
   
      :cmd_host:`AT+PSWD=1234`
   #. Change connect mode.
   
      :cmd_host:`AT+CMODE=0`
      
      HC05 in this mode is set to connect SPECIFIED device(through device address).
   #. Reset and initialize HC05.
   
      :cmd_host:`AT+RESET`

      :cmd_host:`AT+INIT`
   #. Set inquiring mode.
   
      :cmd_host:`AT+INQM=1,9,48`
   #. Inquire (Search the bluetooth device).
   
      :cmd_host:`AT+INQ`
      
      You can see bluetooth device searched around, and screen will show some device's addresses.
      
      And try to use :cmd_host:`AT+STATE?` command, then recieve response of :hl:`+STATE:INQUIRING`.
   #. End of Inquiry.
   
      :cmd_host:`AT+INQC`
      
      If you recieve the response :hl:`OK`, you can check the bluetooth is back to initialization state or not by using command :cmd_host:`AT+STATE?`.
      
      When you leave the inquiring state, you should reset and initial it again.
   #. Bind device.
   
      :cmd_host:`AT+BIND=<device's address you want to bind>`
   #. Pair device.
   
      :cmd_host:`AT+PAIR=<device's address you want to pair>,<pair time>`
      
      When you recieve the response :hl:`OK`, check the state is in PAIRED or not.
   #. Link device.
   
      :cmd_host:`AT+LINK=<device's address you want to link>`
      
      And then your phone will show a window to input the password of HC05(master).
   #. Communication.
      
      Use your phone and open the app, and try to do communication.
      
      .. container:: instruct

         Note that if HC05 be a master, it would communicate in AT Command mode.


 
******************
Reference List
******************

#. `How to work from mbed <https://os.mbed.com/users/edodm85/notebook/HC-05-bluetooth/>`__

#. `Tutorial <https://swf.com.tw/?p=712>`__

#. `Bluetooth Connection <https://sites.google.com/a/ntut.org.tw/jimmyhu/projectlist/hc-05-bluetooth-connect>`__
