Exam Preparation
################
:Date:    2019-04-30 15:00
:Tags:    Tutorial
:Summary: Preparations before the exam
:Status: Draft

.. sectnum::
     :depth: 2

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

    The goal of this tutorial is to learn:

    #. How to record your coding histroy

    #. How to use "cheese" to take a picture

    #. How to create a screenshot on Linux

Record your coding histroy
==========================

.. container:: instruct

   You must choose at least **ONE METHOD** for your exam!

Method 1: Using "Local History" Plugin in VS Code
-------------------------------------------------

#. Run the VS Code, and install the Local History extensions.

   #. :cmd_host:`$ code`

   #. (:hotkey:`Ctrl+Shift+X`) or click the Extensions icon
      (`Screenshot <labs/img/Linux_Intro/vscode_extension.png>`__) in
      the :file:`Activity Bar` on the side of VS Code to bring up
      the Extensions view.

   #. Type :file:`Local History` to search the extension
      which publisher name is :file:`xyz`
      and click the green icon to install.
      `Screenshot <tutorial/images/exam_preparation_stu/local-history-plugin.png>`__

   #. Quit VS Code when done.

#. Open the folder where you want to enable the recording feature
   using VS Code.

   :cmd_host:`$ code <path to folder>`

   Note: :file:`<path to folder>` should be like
   :file:`~/ee2405/midterm/midterm01`

#. Every time you save any file under the folder you opened,
   the plugin will automatically backup the file into the .history folder.

#. After the exam, please hand in the compress file of the .history folder.

   #. Compress the .history folder.

      :cmd_host:`$ tar cfJP <your student id>_<foldername>.tar.xz <path to folder>/.history`

      Note: :file:`<path to folder>/.history` should be like
      :file:`~/ee2405/midterm/midterm01/.history`;
      :file:`<your student id>_<foldername>.tar.xz` should be like
      :file:`107061100_midterm01.tar.xz`

   #. After entering the command above, you will found a file
      named :file:`<your student id>_<foldername>.tar.xz`
      where you enter the command.

   #. Upload the file :file:`<your student id>_<foldername>.tar.xz`.

Method 2: Using Git Integration in VS Code
------------------------------------------

#. You will need a git remote repository account,
   e.g., `GitHub <https://github.com/>`__, `GitLab <https://gitlab.com/>`__,
   or `Bitbucket <https://bitbucket.org/>`__.

#. Set git configuration values.

   :cmd_host:`$ git config --global user.name <your name>`
   
   :cmd_host:`$ git config --global user.email <your email>`

#. Open the folder where you want to use git by VS Code.

   :cmd_host:`$ code <path to folder>`

   Note: :file:`<path to folder>` should be like
   :file:`~/ee2405/midterm/midterm01`

#. (:hotkey:`Ctrl+Shift+G`) or click the Source Control icon
   (`Screenshot <tutorial/images/exam_preparation_stu/vscode-source-control.png>`__)
   in the :file:`Activity Bar` on the side of VS Code to bring up
   the Source Control view.

#. If it shows "No source control providers registered." in the Source Control
   view, please click on the "Initialize Repository" button showed in
   `Screenshot <tutorial/images/exam_preparation_stu/vscode-git-init.png>`__.

#. Commit your changes.

   #. When your mouse hovering over a file,
      there will be several buttons beside the file name.

   #. Click on the "Plus" button to stage the changes.

   #. If you select the wrong file,
      you can cancel it by click on the "Minus" button.

   #. Enter the some description in the Message box.

   #. Click on the "Check" to confirm.

#. You should commit your changes
   when you create a new project and every time you compile your code.

#. After the exam, please hand in the url of your remote repository.

   #. Create a new repository on the `GitHub <https://github.com/>`__,
      `GitLab <https://gitlab.com/>`__, or `Bitbucket <https://bitbucket.org/>`__.

   #. Remember the remote repository url :file:`https://<gitserver.com>/<user>/<repo>.git`.
      For example, :file:`https://gitlab.larc-nthu.net/ee2405_2019/mbed_rpc.git`

   #. Push local repository to remote repository.

      :cmd_host:`$ cd <path to folder>`

      :cmd_host:`$ git remote add origin <remote repository url>`

      :cmd_host:`$ git push -u orgin master`

      Note: :file:`<path to folder>` should be like
      :file:`~/ee2405/midterm/midterm01`

   #. Fill the url to the remote repository in the google form.


Use cheese to take a picture
============================

#. Plug in the webcam and connect it into the virtual machine.

#. Install Cheese.

   :cmd_host:`$ sudo apt install cheese`

#. Open Cheese.

   :cmd_host:`$ cheese &`

#. If you cannot see the view of the webcam in cheese,
   open the preference of cheese and select to the correct device.
   `Screenshot <tutorial/images/exam_preparation_stu/open-preferences-of-cheese.png>`__
   `Screenshot <tutorial/images/exam_preparation_stu/preferences-of-cheese.png>`__

#. Use the button which looks like a camera to take a picture.

#. Pictures will be stored in the folder :file:`~/Pictures/Webcam`.

Take a screenshot
=================

#. Press the button :hotkey:`prt sc` or :hotkey:`print sreen` on the keyboard.

#. Screenshots will be stored in the folder :file:`~/Pictures`.
