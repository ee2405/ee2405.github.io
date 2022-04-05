mbed Lab 1 Mbed Introduction
############################
:Date:    2022-02-23 15:00
:Tags:    Labs
:Summary: Setup Mbed programming environments 
:Last-Modified: $Date$

.. sectnum::
   :depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

   The goal of this lab is to learn:

   #. How to setup the Mbed programming environments 
   #. Familiar with the STMicroelectronics Discovery kit for IoT node (B-L4S5I-IOT01A board)

****************
Lab Due
****************

**Feb. 23, 2022**

****************
Lab Introduction
****************

With the STMicroelectronics Discovery kit for IoT node, users develop applications
with direct connection to cloud servers. The Discovery kit enables a wide
diversity of applications by exploiting low-power communication, multiway
sensing and Arm® Cortex®-M4 core-based STM32L4+ Series features. The support
for ARDUINO® Uno V3 and Pmod™ connectivity provides unlimited expansion
capabilities with a large choice of specialized add-on boards.


**************
Equipment List
**************

#. B-L4S5I-IOT01A * 1

***************
Lab Description
***************

Lecture Notes
=============

- Introduction to Course `Course_Intro.pdf <notes/Course_Intro.pdf>`__

- Chapter 1: Embedded Systems and Microcontrollers `ch1_intro.pdf <notes/ch1_intro.pdf>`__

- Chapter 2: Introducing STM32L4 and mbed `ch2_STM32L4.pdf <notes/ch2_STM32L4.pdf>`__

Reference Website
=================

.. container:: instruct

	Please find details in the following website:

	#. `Mbed and B-L4S5I-IOT01A <https://os.mbed.com/platforms/B-L4S5I-IOT01A/>`__
	
	#. `ARM Mbed Studio Documentation <https://os.mbed.com/docs/mbed-studio/current/introduction/index.html>`__

	#. `GitHub Quickstart <https://help.github.com/en/github/getting-started-with-github/quickstart>`__

	#. `Pro Git book <https://git-scm.com/book/en/v2>`__

Revision Control with Git 
==========================

.. container:: instruct

   Git is an essential tool in a programming development. It is also a convenient way to
   sync source codes between different computers and developers. 
   For example, you can write a code and push to a git server, which can be accessed
   in another computer by pulling the codes. This can be done with multiple programmers, too.
   You can also trace all the changes during your development.
   Please get familiar with Git in this course.
   You will need to push all your lab/homework/project to your github.com repo.

Sign Up github.com and Create a Remote Repository
--------------------------------------------------

#. To start, you will need a git remote repository account.
   We recommend you to use `GitHub <https://github.com/>`_.

   #. Fill the sign up form and click on :hl:`Sign up for GitHub`.
      `screenshot <labs/img/Linux_Intro/github-signup-1.png>`__

   #. Verify that you are not robot and click on :hl:`Join a free plan`.
      `screenshot <labs/img/Linux_Intro/github-signup-2.png>`__

   #. Scroll down and click on :hl:`Skip this step`.
      `screenshot <labs/img/Linux_Intro/github-signup-3.png>`__

   #. After above steps, you will see
      `screenshot <labs/img/Linux_Intro/github-signup-4.png>`__.

   #. Check your email inbox and click on :hl:`Verify email address` link.
      `screenshot <labs/img/Linux_Intro/github-signup-5.png>`__

#. Create a remote repository.

   #. Go to `GitHub <https://github.com/>`_ and click on :hl:`New` button on
      the left of the website.
      `screenshot <labs/img/Linux_Intro/github-new-repo-1.png>`__

   #. Fill the repository name (e.g., mbed01), choose the repository to be private,
      and then click on :hl:`Create repository`.

   #. Click "Code" (a green button) and select "SSH" (under Clone).
      The repository link will show for copying.
      Copy the remote repository link :hl:`<URL>`:
      :file:`git:@gitserver.com/<username>/<repo-name>.git`.

      For example, :file:`git@github.com:ee2405/mbed01.git`

Add Course GitHub as a Collaborator 
------------------------------------

#. Click "Settings" at top menu under your repo.

#. Click "Collaborators" and "Add people"

#. Please add "ee2405" to your collaborator, so TAs can check your git repo.

Setup Host Programming Tools 
============================

.. container:: instruct

   In this section, we will install GCC, Python and VS Code
   for host programming.

Install Visual Studio Code
-----------------------------------

.. container:: instruct

   Visual Studio Code is a lightweight but powerful source code editor
   which runs on your desktop and is available for Windows, macOS and Linux.
   It comes with built-in support for JavaScript, TypeScript and Node.js
   and has a rich ecosystem of extensions for other languages
   (such as C++, C#, Java, Python, PHP, Go) and runtimes (such as .NET and Unity).

   VS Code tutorial can be found at https://code.visualstudio.com/docs/.

#. Download and install VS Code 

   https://code.visualstudio.com/

#. Run the VS Code, and install the C/C++ and Python extensions.
   (Done only once per installation)

   #. Start VS Code

   #. Click the Extensions icon
      (`Screenshot <labs/img/Linux_Intro/vscode_extension.png>`__) in the
      :file:`Activity Bar` on the side of VS Code to bring up the Extensions
      view.

   #. Type :file:`C/C++` to search the extension which publisher name is
      :file:`Microsoft` and click the green icon to install.

   #. Type :file:`Python` to search the extension which publisher name is
      :file:`Microsoft` and click the green icon to install.

   #. Quit VS Code when done.


Install C/C++ Compiler
-----------------------------------

For Windows, please follow https://code.visualstudio.com/docs/cpp/config-mingw
We will also install MSYS2 environment (a Unix port) and use it as our main terminal application in Windows.

For MAC OS, please follow https://code.visualstudio.com/docs/cpp/config-clang-mac

Please create a folder "ee2405" under your home directory. This will be your main course directory for host programming projects.
Please create "helloworld_cpp" directory under "ee2405" (instead of using "project" folder in above tutorial). 
And the commands are:

Please start a Terminal app.

:cmd_host:`$ cd ~` 

:cmd_host:`$ mkdir ee2405` 

:cmd_host:`$ cd ee2405` 

:cmd_host:`$ mkdir helloworld_cpp` 

:cmd_host:`$ cd helloworld_cpp` 

:cmd_host:`$ code .`

Please follow all steps until "Step through the code".


Git in VS Code
-----------------------------------

#. From menu, select SCM under View.

#. Click the "Publish to GitHub".
   Select "Publish to GitHub private repository ee2405/helloworld_cpp".
   For the first github publish, VS Code will direct to your default browser and ask your permission to access github.com.
   After setting permission correctly in github.com, you will be prompted a file selection for pushing to the repo.
   Please select source codes and VS code setup files.
   After confirmation, you should see selected files in the repo.


Programming with Python
-----------------------------------

Please follow instructions on how to install and run Python3: https://code.visualstudio.com/docs/python/python-tutorial
Please create "helloworld_py" directory under "ee2405".

Please start a Terminal app.

:cmd_host:`$ cd ~` 
:cmd_host:`$ cd ee2405` 
:cmd_host:`$ mkdir helloworld_py` 
:cmd_host:`$ cd helloworld_py` 
:cmd_host:`$ code .`

#. From menu, select SCM under View.

#. Click the "Publish to GitHub".
   Select "Publish to GitHub private repository ee2405/helloworld_py".
   After setting permission correcly in github.com, you will be prompted a file selection for pushing to the repo.
   Please select source codes and VS code setup files.
   After confirmation, you should see selected files in the repo.


Programming with mbed Studio
============================

Install Git Desktop Tools 
--------------------------

#. Follow instructions to install Git for your OS:

   https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

#. Open a terminal app. 
   In Windows, please use "Git Bash" just installed by git Desktop.
   In Mac OS, you search and can use terminal app.

#. Verify the installation and the version by running:

   :cmd_host:`$ git --version`

#. Set git configuration values.

   :cmd_host:`$ git config --global user.name "your name"`

   :cmd_host:`$ git config --global user.email "your email"`

   Every Git commit will use the above information after these configurations.

Setup SSH Key 
--------------------------

#. Follow instructions to setup SSH key

   https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

#. Open a terminal app. 
   In Windows, please use "Git Bash" just installed by git Desktop.
   In Mac OS, you can search and use the terminal app.

#. Paste the text below, substituting in your GitHub email address.

   :cmd_host:`$ ssh-keygen -t ed25519 -C "your_email@example.com"`

   This will generate a public/private key pair for you.
   You will copy the public key to GitHub to enable your PC to link to GitHub.

   When you're prompted to "Enter a file in which to save the key," press Enter. This accepts the default file location.

    > Enter a file in which to save the key (/Users/you/.ssh/id_algorithm): [Press enter]

   At the prompt, type a secure passphrase (this is your password to use the private key). For more information, see "Working with SSH key passphrases."

    > Enter passphrase (empty for no passphrase): [Type a passphrase]
    > Enter same passphrase again: [Type passphrase again]

#. Adding your SSH key to the ssh-agent

   #. Start the ssh-agent in the background.

      :cmd_host:`$ eval "$(ssh-agent -s)"`

       > Agent pid 59566

   #. Add your SSH private key to the ssh-agent.

      :cmd_host:`$ ssh-add ~/.ssh/id_ed25519`

   #. Add the SSH key to your account on GitHub. For more information, see `"Adding a new SSH key to your GitHub account." <https://docs.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account>`__

   #. For MAC OS, please modify also :file:`~/.ssh/config` to include the following contents:

      :cmd_host:`$ code -add ~/.ssh/config`

         Host *
         AddKeysToAgent yes
         UseKeychain yes
         IdentityFile ~/.ssh/id_ed25519



Install mbed Studio
--------------------

.. container:: instruct

   Mbed Studio is a free IDE for Mbed OS application and library development,
   including all the dependencies and tools you need in a single package so
   that you can create, compile and debug your Mbed programs on the desktop. 

#. Create an account at mbed.com: https://os.mbed.com/account/login/

#. Download and install mbed Studio from https://os.mbed.com/studio/

Create and Compile a mbed progrem
----------------------------------

#. Follow instructions to create and compile a mbed program: https://os.mbed.com/docs/mbed-studio/current/create-import/index.html

#. Note that mbed Studio automatically creates :file:`~/Mbed\ Programs` folder to store all mbed programs.
   You may change it by **File --> Open Workspace....**.

   .. container:: warning

      Mbed Studio automatically uses your user folder for :file:`~/Mbed\ Programs`.
      However, if your user folder uses Chinese characters (e.g., your user name),
      mbed Studio will not compile in the following.
      In such case, please create another folder and make sure the path names are without Chinese characters.
      Then you can use this new folder as the mbed Workspace by selecting **File --> Open Workspace....**.
      This only has to be done for once. All following mbed programs will be created under the new folder.

#. Open the **File** menu and select **New Program....**

#. Select mbed-os-example-blinky under **MBED OS 6**
   Enter mbed01 for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Store Mbed OS in the program folder (+1GB)"
   Click "Add Program".

#. The mbed-os-example-blinky project will be created.
   Please double-click on main.cpp to check its contents:

   .. code-block:: c++
      :linenos: inline

      /* mbed Microcontroller Library
       * Copyright (c) 2019 ARM Limited
       * SPDX-License-Identifier: Apache-2.0
       */

      #include "mbed.h"
      
      // Blinking rate in milliseconds
      #define BLINKING_RATE     500ms
      
      int main()
      {
          // Initialise the digital pin LED1 as an output
          DigitalOut led(LED1);
      
          while (true) {
             led = !led;
             ThisThread::sleep_for(BLINKING_RATE);
          }
      }
      

   .. container:: instruct

      ThisThread::sleep_for() will put the micro-controller into a low-power mode (not doing any computation).

      led.write(0) is the same as led=0. It will pull myled pin low.

#. Note that mbed-os / stores the current Mbed OS. We will reuse this copy of Mbed OS for other labs.

#. Plugin the B_L4S5I_IOT01A mbed board to your PC.

   .. image:: labs/img/Mbed_Intro/board_top.jpg
      :alt: mbed board

   The board should be automatically recognized as "DISCO-L4S5I (B-L4S5I-IOT01A)

   Note: if the RED LED besides the micro USB port keeps blinking, it means you have used a USB power cable.
   Please change port of the cable or find a cable that support USB signals. You can also verify this that no "DIS_L4S5VI" folder
   is created by your O.S. like an external flash drive.

#. Build and running the program

   Please follow instructions in https://os.mbed.com/docs/mbed-studio/current/building-running/index.html
   
   Click **Run** button to build and run the program.
   It will take a while to build Mbed OS first and then the example blinky program.


      .. container:: instruct

         In the :file:`BUILD/B_L4S5I_IOT01A/` folder, there is a mbed01.bin file which is the compiled program.
         You can copy the .bin file to DIS_L4S5VI folder to flash the program onto B_L4S5I_IOT01A.

Push source code to github
----------------------------------

#. Follow instructions to link a mbed program to a github rep: https://os.mbed.com/docs/mbed-studio/current/source-control/index.html

#. First we follow instructions in https://os.mbed.com/docs/mbed-studio/current/source-control/index.html#configuring-a-program-for-source-control-and-collaboration
   to configure the github for the program:

   #. Go to the Source Control view.

   #. Click the Set Remote URL button.
      The Set Remote URL dialog box opens.
      Enter a URL for your remote repository, for example: git@github.com:ee2405/mbed01.git.

   #. Click Set Remote Repository.
      mbed Studio will ask you to login github to authenticate git operations.

#. Push the code to your git remote repository, and check your remote repository for new files.

   #. Add the main.cpp by clicking "+".

   #. Enter a commit Message and commit by click "V".

   #. Push your commit to the remote repository by clicking "..." and select "Push".

   #. Start the web browser and go to github.com. Check if your main.cpp is uploaded to the remote repository.

#. If, for some reason, the above git operations do not work in mbed Studio,
   you may simply use "Add file" menu --> "Upload files" at the repo. And select
   files you want to upload to github without mbed Studio or git tools.

Create a second mbed progrem
----------------------------------

We will use this example to show a multiple cpp project and
also we use the existing Mbed OS from mbed01.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *mbed-os-test-program2* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Add copy the following source code into the main program :file:`main.cpp` under :file:`mbed-os-test-program2`.

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      DigitalOut myLED(LED1);
      DigitalOut myLED2(LED3);

      void Led(DigitalOut &ledpin);

      int main()
      {
         myLED = 1;
         myLED2 = 1;
         while (true)
         {
            Led(myLED);
            Led(myLED2);
         }
      }

#. Add the following source code as another cpp source file :file:`led.cpp`. 

   .. code-block:: c++
      :linenos: inline

      #include "mbed.h"

      void Led(DigitalOut &ledpin)
      {
         for (int i = 0; i < 10; ++i)
         {                     //blink for 10 times
            ledpin = !ledpin; // toggle led
            ThisThread::sleep_for(100ms);
         }
      }

#. Compile and test the program

   The LED will light green light five times. After that, the blue and orange light will light five times.
   And the above sequence will repeat until we unplug the board.

Debugging mbed Programs
------------------------

Pyocd does NOT work with our mbed board currently. Do NOT proceed with your board in this part.
There is no demo for this section.

https://os.mbed.com/docs/mbed-studio/current/monitor-debug/index.html

Create a third mbed progrem
----------------------------------

We will use this example to show how to use printf for floating points.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *mbed-os-test-program3* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". 

#. Add copy the following source code into the main program :file:`main.cpp` under :file:`mbed-os-test-program3`.

   .. code-block:: c++
      :linenos: inline

      /* mbed Microcontroller Library
       * Copyright (c) 2019 ARM Limited
       * SPDX-License-Identifier: Apache-2.0
       */
      
      #include "mbed.h"
      
      
      // Blinking rate in milliseconds
      #define BLINKING_RATE     1000ms
      
      
      int main()
      {
          // Initialise the digital pin LED1 as an output
          DigitalOut led(LED1);
      
          for(int i=0; i<10; i++){
              led = !led;
              ThisThread::sleep_for(BLINKING_RATE);
              printf("%1.5f\n", 3.14159);
          }
      }

#. Compile and test the program

   The LED will light green light 10 times. And there are printout in the "Output". What are they? 

Setup mbed OS
----------------------------------

#. Change the default printf library to "std"

   Please find :file:`~/Mbed Programs/mbed01/mbed-os/targets/targets.json`
   in the file browser and click to edit it.
   Search for "printf_lib", and replace "minimal-printf" with "std"

   We will modify the application configuration file to override the parameter
   :hl:`printf_lib` with the value :hl:`std` (to replace "minimal-printf"). `Screenshot <labs/img/Mbed_Intro/fixed_std_new.jpg>`__
   The purpose is to support floating point printf.

#. Please find :file:`~/Mbed Programs/mbed01/mbed-os/platform/mbed_lib.json`
   Search and Set "callback-nontrivial" parameter to :hl:`true` .
   This will enable a callback feature in task scheduling, which will be used in later labs.

#. After set above parameters, please compile and test the :file:`mbed-os-test-program3` again.

Hardware block diagram and Pinout
================================================

#. The hardware block diagram illustrates the
   connection between the STM32 and peripherals: embedded ST-LINK, ARDUINO® Uno V3 shields, Pmod™
   connector, Quad-SPI Flash memory, USB OTG connectors, digital microphones, various ST-MEMS sensors, and
   the three RF modules (Wi‑Fi®, Bluetooth®, and NFC):  `Board Block Diagram <labs/img/Mbed_Intro/hardware_block_diagram.jpg>`__

#. Board Pinout : `Board Pinout <labs/img/Mbed_Intro/B_L4S5I_IOT01A_pinmap.jpg>`__

Course Example Codes
-----------------------------------

#. You may check course example codes in :cmd_host:`https://gitlab.larc-nthu.net/ee2405_2022/code-example.git`.
   We will update the repo regularly for the latest version along with the course.
   You should be able to find example codes used in labs of this course here.
   If you clone or download the example, it will be easier to examine and copy codes than from course website.

********************
Demo and Checkpoints
********************

#. Please fill in a `questionnaire at EEClass course website <https://eeclass.nthu.edu.tw/course/questionnaire/727?next=login>`__
   to answer the following items:
   1. Name, 2. Student ID, 3. Email, 4. Cell phone, 5. GitHub account, 6. GitHub link

#. Create a new project to write for the following function. 
   Please repetitively turn on LED3 "three times" and then LED1 "twice". 

#. Please submit your lab report to EEClass as a pdf file.
   The pdf is a record of key lab parts you have done.
   You may include the following contents (but not limited to):
   (1) Steps or commands in each part
   (2) Results of each step
   (3) Encountered issues
   (4) Discussion
