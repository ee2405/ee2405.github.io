mbed Lab 0 Install an Embedded Development Environment 
######################################################
:Date:    2021-02-24 15:00
:Tags:    Labs
:Summary: Install a desktop Linux for embedded system development.
:Status: Draft

.. sectnum::
   :depth: 2

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

   The goal of the lab is to get familiar with a Linux workstation
   for developing embedded software and to learn basics of UNIX and 
   programming tools. We will install a virtual machine first.
   Then, we will install a copy of Ubuntu Linux on the virtual machine
   as our programming host. After that we try the host GCC toolchain
   and work on a few common Unix commands.

***************
Preview Topics
***************

#. Linux operating systems
#. Virtual machines
#. Unix commands

***************
Equipment List
***************

#. PC or notebook with internet connection

***************
Lab Description
***************


Preparation
===========
For Windows 10 users, please upgrade at least to **2020H1 version** (released May, 2020).
Otherwise, you will need to disable Hyper-V as shown in the following:

For **Windows 10 before 2020H1 version**, the process to disable Hyper-V before
start a VMWare session:

#. Right-click on the windows logo to open "Windows PowerShell (系統管理員)".
   `screenshot <labs/img/Linux_Intro/open-windows-powershell-admin.png>`__

#. :cmd_host:`PS> bcdedit /set hypervisorlaunchtype off`
   `screenshot <labs/img/Linux_Intro/turn-off-hyper-v-using-powershell.png>`__

   Note that :cmd_host:`PS>` is the prompt for the Windows PowerShell.
   Do **NOT** enter it.

#. Reboot the computer.

.. container:: warning

   If you disable Hyper-V, those services using Hyper-V (e.g. Docker Desktop)
   won't be available.


Install Ubuntu in a Virtual Machine 
=========================================

We will install VMware for this course.
For Windows, please go to `VMware Player for Windows`_.
For Mac OS, please go to `VMware Fusion for Mac OS`_.

VMware Player for Windows
----------------------------

Install VMware Player
`````````````````````````````````````

#. Download the installer of VMware Player on the desktop from
   `VMware Player Download Page.
   <https://www.vmware.com/products/workstation-player/workstation-player-evaluation.html>`__

#. Run the installer.

#. Click "Next". `screenshot <labs/img/Linux_Intro/new_1.jpg>`__

#. Select "I accept the terms in the License Agreement" and click "Next".
   `screenshot <labs/img/Linux_Intro/new_2.jpg>`__

#. `Screenshot <labs/img/Linux_Intro/new_3.jpg>`__,
   `screenshot <labs/img/Linux_Intro/new_4.jpg>`__
   and  `screenshot <labs/img/Linux_Intro/new_5.jpg>`__
   all click "Next".

#. Click "Install". `screenshot <labs/img/Linux_Intro/new_6.jpg>`__

#. Wait for the VMware Player installing and then click "Finish".
   `screenshot <labs/img/Linux_Intro/new_7.jpg>`__

#. At the first time you launch the VMware Player,
   it will ask you for entering the license key.
   Just select "Use VMware Workstation Player for free for non-commercial use"
   and then click "Continue".
   `screenshot <labs/img/Linux_Intro/vmware-installation-8.png>`__

#. The hotkey of the terminal in Ubuntu is :hotkey:`Ctrl + Alt + T`,
   but the default hotkey of releasing the mouse cursor of the VMware Player is
   :hotkey:`Ctrl + Alt`. So, we change the hotkey of the VMware Player to
   :hotkey:`Ctrl + Shift + Alt`.

   #. Open "Windows PowerShell".

   #. Use notepad to open the preferences.ini of the VMware Player.

      :cmd_host:`PS> notepad $env:appdata\VMware\preferences.ini`

   #. Append these four lines in the end of the file.

      .. code-block:: none

         pref.hotkey.gui = "false"
         pref.hotkey.control = "true"
         pref.hotkey.shift = "true"
         pref.hotkey.alt = "true"

   #. Reopen the VMware Player.

Install Ubuntu on VMware Player
````````````````````````````````

#. Download the iso image file for Ubuntu 18.04 from `Ubuntu Download Page
   <https://releases.ubuntu.com/18.04.5/?_ga=2.236360194.289688540.1612256673-1444479749.1611319365>`__ .
   `screenshot <labs/img/Linux_Intro/Ubuntu-installation-1.png>`__

#. Double click the shortcut of VMware Player on the Desktop.

#. Click "Create a New Virtual Machine".
   `screenshot <labs/img/Linux_Intro/new_8.jpg>`__

#. Configure the new virtual machine.
   `screenshot <labs/img/Linux_Intro/new_9.jpg>`__

   #. Select "Installer disc image file"

   #. Browse the downloaded iso image file for Ubuntu.

   #. Click "Next".

#. Fill in your name and user name with **ee2405**.

   Fill in the password with **eenthu2405**.

   Click "Continue". `screenshot <labs/img/Linux_Intro/new_10.jpg>`__

#. Name the virtual machine.
   `screenshot <labs/img/Linux_Intro/new_11.jpg>`__

   #. Name the virtual machine "your student ID number".

   #. Click "Next".

#. Specify disk capacity.
   `screenshot <labs/img/Linux_Intro/new_12.jpg>`__

   #. Set the maximum disk size (GB) to "20".

   #. Select "Store virtual disk as a single file".

   #. Click "Next".

#. Click "Finish".
   `screenshot <labs/img/Linux_Intro/new_13.jpg>`__

#. Launch the virtual machine that you just created. Follow the steps to complete Ubuntu installation.

   #. During the installation of Ubuntu, it will pop up a windows
      that wants you to download "VMware Tools for Linux".
      Just click "Install Tools".
      `screenshot <labs/img/Linux_Intro/new_14.jpg>`__

#. Update software.

   #. Find "Software Updater" and click to update. `screenshot <labs/img/Linux_Intro/new_16.jpg>`__

   #. Choose "Install Now".
      `screenshot <labs/img/Linux_Intro/new_17.jpg>`__

   #. Click "Restart Now" or restart the environment manually. `screenshot <labs/img/Linux_Intro/new_18.jpg>`__


.. container:: instruct

   Note that the hot key for **copy** and **paste** in terminal is: :hotkey:`Ctrl+Shift+C` and :hotkey:`Ctrl+Shift+V`.

.. container:: instruct

   To improve the performance of virtual machine, please visit
   `Virtual Machine Performance Improvement Tutorial <https://www.ee.nthu.edu.tw/ee240500/virtual-machine-performance-improvement-tutorial.html>`_.

   If your computer has more than 8G main memory, you may choose to increase the memory allocated for VM to 3G.
   Also if your computer has more than 4 cores, it is recommended to use 2 cores in VM for faster processing.

.. container:: instruct

   Note that if you have created a copy of Ubuntu VMWare Virtual Machine,
   you may copy the virtual disk (as a file) to another computer
   and boot into the VM.

VMware Fusion for Mac OS
-----------------------------

Install VMware Fusion 
````````````````````````````````

#. Download VMware Fusion from `VMware Fusion Download Page
   <https://www.vmware.com/tw/products/fusion.html>`__ .

#. Click through the installer:

   #. Click "Register now". `screenshot <labs/img/Linux_Intro/VMwareFusion-installation-1.png>`__

   #. Create an account. `screenshot <labs/img/Linux_Intro/VMwareFusion-installation-2.png>`__

   #. After login your account, please got to `VMware Fusion Player – Personal Use License page <https://my.vmware.com/group/vmware/evalcenter?p=fusion-player-personal>`_.

   #. Copy license keys and click "Manually Download". `screenshot <labs/img/Linux_Intro/VMwareFusion-installation-3.png>`__

   #. Double click to install. `screenshot <labs/img/Linux_Intro/VMwareFusion-installation-4.png>`__

   #. Click "Agree". `screenshot <labs/img/Linux_Intro/VMwareFusion-installation-5.png>`__

   #. Paste license keys and click "Continue". `screenshot <labs/img/Linux_Intro/VMwareFusion-installation-6.png>`__

   #. Click "Done". `screenshot <labs/img/Linux_Intro/VMwareFusion-installation-7.png>`__

Install Ubuntu on VMware Fusion
``````````````````````````````````````

#. Download the iso image file for Ubuntu 18.04 from `Ubuntu Download Page
   <https://releases.ubuntu.com/18.04.5/?_ga=2.236360194.289688540.1612256673-1444479749.1611319365>`__ .
   `screenshot <labs/img/Linux_Intro/Ubuntu-installation-1.png>`__

#. Double click to open VMware Fusion.

#. Click through the installer:

   #. Drag the downloaded ISO file (.iso) to install. `screenshot <labs/img/Linux_Intro/Ubuntu-installation-2.png>`__

   #. Click "Continue". `screenshot <labs/img/Linux_Intro/Ubuntu-installation-3.png>`__

   #. Fill in your name and user name with **ee2405**.

      Fill in the password with **eenthu2405**.

      Click "Continue". `screenshot <labs/img/Linux_Intro/Ubuntu-installation-4.png>`__

   #. Click "Finish". `screenshot <labs/img/Linux_Intro/Ubuntu-installation-5.png>`__

   #. Click "Save". `screenshot <labs/img/Linux_Intro/Ubuntu-installation-6.png>`__

#. Ubuntu should launch on VMware Fusion. Follow the steps to complete Ubuntu installation.

   #. If VMware Fusion showed "Pipe broken" as in `screenshot <labs/img/Linux_Intro/Ubuntu-installation-7.png>`__ 
      , then go through the steps in `VMware Website <https://kb.vmware.com/s/article/80467>`__ . 
      
   #. Make sure Admin Privileges is allowed for the application. `screenshot <labs/img/Linux_Intro/Ubuntu-installation-8.png>`__

   #. Wait for a while and VMware Fusion should be on with Ubuntu installed. `screenshot <labs/img/Linux_Intro/Ubuntu-installation-9.png>`__

.. container:: instruct

   Note that the hot key for **copy** and **paste** in terminal is: :hotkey:`Ctrl+Shift+C` and :hotkey:`Ctrl+Shift+V`.

.. container:: instruct

   To improve the performance of virtual machine, please visit
   `Virtual Machine Performance Improvement Tutorial <https://www.ee.nthu.edu.tw/ee240500/virtual-machine-performance-improvement-tutorial.html>`_.

   If your computer has more than 8G main memory, you may choose to increase the memory allocated for VM to 3G.
   Also if your computer has more than 4 cores, it is recommended to use 2 cores in VM for faster processing.

.. container:: instruct

   Note that if you have created a copy of Ubuntu Virtual Machine,
   you may copy the virtual disk (as a file) to another computer
   and boot into the VM.

Revision Control with Git 
==========================

.. container:: instruct

   Git is an essential tool in program development. It is also a convenient way to
   sync source codes between different computers and developers. 
   For example, you can write a code and push to a git server, which can be accessed
   in another computer by pulling the codes. This can be done with multiple programmers, too.
   You can also trace all the changes during your development.
   Please get familiar with Git in this course.
   For more information about Git Command Line, please visit
   `Git Command Line (Basic) <git-command-line-basic.html>`_
   and
   `Git Command Line (Advanced) <git-command-line-advanced.html>`_.

Install Git on Ubuntu
---------------------

#. Run the following command to install Git:

   :cmd_host:`$ sudo apt install git-all`

#. Verify the installation and the version by running:

   :cmd_host:`$ git --version`

#. Set git configuration values.

   :cmd_host:`$ git config --global user.name "your name"`

   :cmd_host:`$ git config --global user.email "your email"`

   Every Git commit will use the above information after these configurations.

Create a Remote Repository
--------------------------

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

   #. Fill the repository name, select the repository to be public,
      and then click on :hl:`Create repository`.
      `screenshot <labs/img/Linux_Intro/github-new-repo-2.png>`__

   #. Remember the remote repository :hl:`<URL>`:
      :file:`https://<gitserver.com>/<username>/<repo-name>.git`.

      For example, :file:`https://github.com/NTHUEE240500/lab1.git`
      `screenshot <labs/img/Linux_Intro/github-new-repo-3.png>`__

Setup VS Code with Linux
=========================

.. container:: instruct

   Now we will start work with Linux commands in a terminal.
   Please learn to start terminal from the GUI
   (`screenshot <labs/img/Linux_Intro/find-terminal.png>`__)
   or try to remember its hotkey :hotkey:`Ctrl+Alt+T`.
   Note that :cmd_host:`$` is the prompt for the system (terminal).
   Do **NOT** enter it.


.. container:: instruct

    In this section, we will use VS Code to edit the program.
    So, we first need to install VS Code before we proceed.

    Visual Studio Code is a lightweight but powerful source code editor
    which runs on your desktop and is available for Windows, macOS and Linux.
    It comes with built-in support for JavaScript, TypeScript and Node.js
    and has a rich ecosystem of extensions for other languages
    (such as C++, C#, Java, Python, PHP, Go) and runtimes (such as .NET and Unity).

    VS Code tutorial can be found at https://code.visualstudio.com/docs/.

#. Install GNU Compiler Suite for Ubuntu.

   :cmd_host:`$ sudo apt install -y build-essential`

   .. container:: question

      What is `sudo <http://en.wikipedia.org/wiki/Sudo>`__?

      :file:`sudo` is a program for Unix-like computer operating systems that
      allows users to run programs with the security privileges of another
      user (normally the superuser, or root).

      Its name is a concatenation of the su command
      (which grants the user a shell of another user, normally the superuser)
      and "do", or take action.

      When you would like to have the root permission,
      use :cmd_host:`$ sudo su`, and enter your password,
      which you entered during installation.

      Note that this will grant you the root access all the
      time on the current terminal (not necessary for most cases).
      If you only need a temporary execution right,
      use :cmd_host:`$ sudo SOME_COMMANDS`.

#. Install VS Code from command line.

   #. Install some requirements.

      :cmd_host:`$ sudo apt update`

      :cmd_host:`$ sudo apt install apt-transport-https curl`

   #. Add VS Code repository to Ubuntu.

      :cmd_host:`$ curl https://packages.microsoft.com/keys/microsoft.asc
      | gpg --dearmor > microsoft.gpg`

      :cmd_host:`$ sudo install -o root -g root -m 644 microsoft.gpg
      /etc/apt/trusted.gpg.d/`

      :cmd_host:`$ rm microsoft.gpg`

      :cmd_host:`$ sudo sh -c 'echo "deb [arch=amd64]
      https://packages.microsoft.com/repos/vscode stable main"
      > /etc/apt/sources.list.d/vscode.list'`

   #. Install VS Code.

      :cmd_host:`$ sudo apt update`

      :cmd_host:`$ sudo apt install code`

#. Run the VS Code, and install the C/C++ and Python extensions.
   (Done only once per installation)

   #. :cmd_host:`$ code &`

   #. Press :hotkey:`Ctrl+Shift+X` or click the Extensions icon
      (`Screenshot <labs/img/Linux_Intro/vscode_extension.png>`__) in the
      :file:`Activity Bar` on the side of VS Code to bring up the Extensions
      view.

   #. Type :file:`C/C++` to search the extension which publisher name is
      :file:`Microsoft` and click the green icon to install.

   #. Type :file:`Python` to search the extension which publisher name is
      :file:`Microsoft` and click the green icon to install.

   #. Quit VS Code when done.


Programming with C++ in Linux
=============================

#. Open a terminal or switch to a terminal.

   #. :hotkey:`Ctrl+Alt+T` to open a terminal.

#. Create a working directory in a terminal.

   #. :cmd_host:`$ mkdir -p ~/ee2405`

#. Go to the working directory in a terminal.

   #. :cmd_host:`$ cd ~/ee2405`

#. Clone the github repo.

   Please replace the following "NTHUEE240500" with your github account name.

   #. :cmd_host:`$ git clone https://github.com/NTHUEE240500/lab1.git`

   If above command works successfully, there will be a new :file:`lab1/`
   directory. It is a cloned git directory to the remote github.
   Every file activity will be now tracked by git.

#. Open VS codes for programming.

   #. :cmd_host:`$ cd lab1`
   #. :cmd_host:`$ code helloworld.cpp &`
   #. Enter the following codes:

   .. code-block:: c++
      :linenos: inline

      #include <iostream>
      using namespace std;

      int main (void) {
          // print hello world for 9 times
          for (int i=1; i<10; ++i) {
              cout << "hello world " << i << " times!\n";
          }
          return 0;
      }

#. Save above codes.

#. Compile the program.

   #. Switch to a terminal

   #. :cmd_host:`$ cd ~/ee2405/lab1`

   #. :cmd_host:`$ g++ -o helloworld helloworld.cpp`

#. Use command "ls" to check the executable file,
   :file:`helloworld`, has been generated.

   :cmd_host:`$ ls -al`

#. Make the program executable.

   #. :cmd_host:`$ chmod +x helloworld`

   #. :cmd_host:`$ ls -al helloworld`

#. Run the executable.

   :cmd_host:`$ ./helloworld`

#. The terminal output should look like this:

   .. class:: terminal

   ::

     hello world 1 times!
     hello world 2 times!
     hello world 3 times!
     hello world 4 times!
     hello world 5 times!
     hello world 6 times!
     hello world 7 times!
     hello world 8 times!
     hello world 9 times!

#. Push the code to your git remote repository, and check your remote repository for new files.

   #. Add the file.

      :cmd_host:`$ git add helloworld.cpp`

   #. Comment and commit the code above.

      :cmd_host:`$ git commit -m "add helloworld.cpp"`

   #. Push your commit to the remote repository.

      :cmd_host:`$ git push`

   #. In the web browser, please go to github.com. 
      Check if your helloworld.cpp is uploaded to the remote repository.

Programming with Python in Linux
================================

#. Install Python3 if it is not installed.

   #. :cmd_host:`$ sudo apt install python3 python3-pip`

#. Open codes.

   #. :cmd_host:`$ cd ~/ee2405/lab1`
   #. :cmd_host:`$ code helloworld.py &`
   #. Enter the following codes:

   .. code-block:: python
      :linenos: inline

      def main():
          for i in range(1, 10):
              print('hello world', i, 'times!' )
      main()

#. Save above codes.

#. Run the script.

   :cmd_host:`$ python3 helloworld.py`

#. The terminal output should look like this:

   .. class:: terminal

   ::

     hello world 1 times!
     hello world 2 times!
     hello world 3 times!
     hello world 4 times!
     hello world 5 times!
     hello world 6 times!
     hello world 7 times!
     hello world 8 times!
     hello world 9 times!

#. Push the code to your git remote repository, and check your remote repository for new files.

   #. Add the file.

      :cmd_host:`$ git add helloworld.py`

   #. Comment and commit the code above.

      :cmd_host:`$ git commit -m "add helloworld.py"`

   #. Push your commit to the remote repository.

      :cmd_host:`$ git push`

   #. In the web browser, please go to github.com. 
      Check if your helloworld.py is uploaded to the remote repository.


Using Git in VS Code (Optional)
================================

You may also use git operations in VS Code as shown in the following for your reference.
Yet, you can skip the this section if you use the git commands.

#. Open the folder where you want to use git by VS Code.

   :cmd_host:`$ code ~/ee2405/lab1`

#. Press :hotkey:`Ctrl+Shift+G` or click the Source Control icon
   (`screenshot <labs/img/Linux_Intro/vscode-source-control.png>`__)
   in the :file:`Activity Bar` on the side of VS Code to bring up
   the Source Control view.

#. If it shows "No source control providers registered." in the Source Control
   view, please click on the "Initialize Repository" button showed in
   `screenshot <labs/img/Linux_Intro/vscode-git-init-1.png>`__.
   After that, please confirm the path showed in the middle of the VS Code
   is as same as :file:`<path to folder>`.
   `screenshot <labs/img/Linux_Intro/vscode-git-init-2.png>`__

#. Commit your changes.

   #. When your mouse hovering over a file,
      there will be several buttons beside the file name.

   #. Click on the "Plus" button to stage the changes. `screenshot <labs/img/Linux_Intro/vscode-git-stage-changes.png>`__

   #. If you select the wrong file,
      you can cancel it by click on the "Minus" button. `screenshot <labs/img/Linux_Intro/vscode-git-unstage-changes.png>`__

   #. Enter the some description in the Message box. `screenshot <labs/img/Linux_Intro/vscode-git-commit-1.png>`__

   #. Click on the "Check" to confirm. `screenshot <labs/img/Linux_Intro/vscode-git-commit-2.png>`__

#. Discard your changes from last commit.

   #. When your mouse hovering over a file,
      there will be several buttons beside the file name.

   #. Click on the "Counter-clockwise arrow" button to discard the changes. `screenshot <labs/img/Linux_Intro/vscode-git-discard-changes.png>`__

#. The status of the files.

   The letter beside the filename in the Source Control view represents the
   status of the file. A stands for :hl:`Added to stage`; M stands for
   :hl:`Modified`; U stands for :hl:`Untracked`.
   `screenshot <labs/img/Linux_Intro/vscode-git-status.png>`__

#. Link remote repository to your local repository.

   #. Press :hotkey:`Ctrl+Shift+P` to bring up the :hl:`Command Palette`.
      `screenshot <labs/img/Linux_Intro/vscode-command-palette.png>`__

   #. Search :hl:`Git: Add Remote` and select :hl:`Git: Add Remote` in the
      panel. `screenshot <labs/img/Linux_Intro/vscode-git-remote-add-1.png>`__

   #. Name the remote repository nickname in the local repository.
      We recommend to name it :hl:`origin`.
      `screenshot <labs/img/Linux_Intro/vscode-git-remote-add-2.png>`__

   #. Paste the remote repository URL.
      `screenshot <labs/img/Linux_Intro/vscode-git-remote-add-3.png>`__

#. Push your commit to the remote repository.

   #. Please click on the "More Actions..." button showed in
      `Screenshot <labs/img/Linux_Intro/vscode-git-more-action.png>`__.

   #. Select :hl:`Push`. `screenshot <labs/img/Linux_Intro/vscode-git-push.png>`__

   #. For the first time push, it will bump up a window to confirm publishing
      the current branch to the reomte repository or not. Click on "OK".
      `screenshot <labs/img/Linux_Intro/vscode-git-push-2.png>`__

   #. Enter your username and password to verify your identity.
      `screenshot <labs/img/Linux_Intro/vscode-git-username.png>`__
      `screenshot <labs/img/Linux_Intro/vscode-git-password.png>`__

#. Pull the commit from the remote repository.

   #. Please click on the "More Actions..." button showed in
      `Screenshot <labs/img/Linux_Intro/vscode-git-more-action.png>`__.

   #. Select :hl:`Pull`. `screenshot <labs/img/Linux_Intro/vscode-git-pull.png>`__

Learning Linux Commands
========================

.. container:: instruct

   Reading the materials in reference list or search the Internet with the keywords
   (+"tutorial" or +"howto") and get familiar with Linux commands.

Use the following items as a check list to see if you have already leaned the topic:

#. File and directory handling
#. Input and Output redirection
#. Wildcards
#. File permission
#. Process and jobs

#. Tar package and gzip compression tool
   (`檔案的壓縮與打包 <http://linux.vbird.org/linux_basic/0240tarcompress.php>`__)

#. Ethernet setup and debug
   (`連上 Internet <http://linux.vbird.org/linux_server/0130internet_connect.php>`__)
   and
   (`Linux 網路偵錯 <http://linux.vbird.org/linux_server/0150detect_network.php>`__)


***********
Checkpoints
***********

#. You need to know how to use a file browser and a terminal in Ubuntu to
   find/create/copy/move files/directories.

#. You need to know how to use git to manage your source code in VS Code.

*********
Reference
*********

* `http://linux.vbird.org <http://linux.vbird.org/>`__ Recommended!!

  This website (in Chinese) provides an excellent reference for Linux
  (with more details and explanations).

  For starter, you can go with
  `Linux 基礎文件 <http://linux.vbird.org/linux_basic>`__,
  especially the following parts:

  - 第二部分：Linux 檔案、目錄與磁碟格式
  - 第五部分：Linux 系統管理員

  Also in `Linux 架站文件 <http://linux.vbird.org/linux_server/>`__

  - 第一部份：架站前的進修專區

* Class notes on Unix commands:

  A quick introduction to Linux command: `pdf <notes/lab1/embedded-linux-commands.pdf>`__

  The following class notes have more details of various Unix topics for your references.

  - Basic Unix Concept: `pdf <notes/lab1/IntroUnix.pdf>`__

  - Frequently used Unix commands: `pdf <notes/lab1/FrequentCommands.pdf>`__

  - VI Editor: `pdf <notes/lab1/vieditor.pdf>`__

  - Shell Programming: `pdf <notes/lab1/ShellProgramming.pdf>`__

* `GitHub Quickstart <https://help.github.com/en/github/getting-started-with-github/quickstart>`__
