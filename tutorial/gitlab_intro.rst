GitLab Introduction
##########################
:Date:    2018-03-07 17:00
:Tags:    Tutorial
:Summary: Use Git in GUI
:Status: Draft

.. sectnum::
	 :depth: 2

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

	The goal of this lab is to learn:

	#. How to use Gitlab in GUI interface

Profile Settings
=================

Register
-------------------------
TAs will register an account for you with the following information (from school's registration system
or filled by you at the time of adding the course).

1. Name (your real name)
2. Student ID (your user name)
3. Email

Gitlab will send confirmation mail to you, please hit the confirmation link
and sets up a password.

If the mail is in the SPAM directory, please add the gitlab
EMAIL to contact or address book.
Most Email providers treat Email contact or address book as white list.


Add SSH Key 
-------------------------

#. Start a new terminal with :hotkey:`Ctrl+Alt+T`

#. To generate a ssh key pair

   The generated ssh public key is usually located at :file:`~/.ssh/id_rsa.pub`
   Please enter the following command
  
   #. :cmd_host:`$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`
 
      Please replace ``your_email@example.com`` with your own email address.

      .. code-block:: terminal

         $ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
         Enter a file in which to save the key (/Users/you/.ssh/id_rsa): <Enter>
         Enter passphrase (empty for no passphrase): <Enter>


#. To add ssh key

   |go_ssh_setting|
   |put_ssh_key|

   #. Go to Gitlab site `Gitlab <http://gitlab.larc-nthu.net>`_
   #. click top-right avatar after login.
   #. click **settings**
   #. click **SSH Keys** on the top side bar.
   #. fill the public key(.ssh/id_rsa.pub) and give a name to it.

#. Check Email again

   After adding SSH key, the Gitlab will send you a mail for newly added
   ssh key. Please check whether it is treated as spam.

Create Project on Gitlab
==================================

This course use git repository(aka repo) to submit homeworks, projects
and reports. To have a repo of your own, You need to
create a new project in `Gitlab website <http://gitlab.larc-nthu.net>`_.

#. Click the **New...** (a cross symbol in the upper left corner) and select the **New project** to create a new project (`Screenshot <notes/mbed0/img/Selection_018.png>`__).
            
#. Enter your project name, e.g., :file:`mbed0` in the **Project name** field, click the **Public** in the **Visibility Level** and click **Create project** (`Screenshot <notes/mbed0/img/Selection_022.png>`__).

#. Copy the URL/location of the new repository to your clipboard by clicking the button in the screenshot (`Screenshot <notes/mbed0/img/Selection_023.png>`__). This is your gitlab repository address.
      For example, ``URL=git@gitlab.larc-nthu.net:106061600/mbed0.git``.


Upload/Download Files via Web
==============================

Users can either choose to transmit files through web interface or Git.
If you are interested in Git, please visit for basic git operations.
Here shows the steps to upload/download files of a Gitlab project.
We will introduce how to create a Gitlab project later.

If you are interested in Git flow, please visit 
`Git Command Line Basics <git-command-line-basics.html>`_ 

Create A First File
--------------------

It is impossible to upload files for a newly created Gitlab project,
so you need to create a `README.md` at first.

|new_file|

Write down something in `README.md`

|new_file_content|

Upload Files
---------------
Drag and drop to upload files!
Note that uploading requires at least one file in Gitlab project.
|upload_file|
|drag_file|

Download Files
---------------

Download files in ZIP or other format.

|download_file|

Edit Files
---------------
In case if you want to edit file online.

|edit_file|


|pagelist|

.. |go_ssh_setting| image:: ./tutorial/images/gitlab_intro/goto_ssh.png
.. |put_ssh_key| image:: ./tutorial/images/gitlab_intro/put_ssh_key.png
.. |change_notification| image:: ./tutorial/images/gitlab_intro/change_notification.png
.. |make_issue| image:: ./tutorial/images/gitlab_intro/make_issue.png
.. |newpage| image:: ./tutorial/images/gitlab_intro/newpage.png
.. |pagelist| image:: ./tutorial/images/gitlab_intro/pagelist.png
.. |pagecontent| image:: ./tutorial/images/gitlab_intro/pagecontent.png
.. |page_slug| image:: ./tutorial/images/gitlab_intro/page_slug.png
.. |newproject| image:: ./tutorial/images/gitlab_intro/newproject.png
.. |setproject| image:: ./tutorial/images/gitlab_intro/setproject.png
.. |sharegroup| image:: ./tutorial/images/gitlab_naming/mem_sel.png
.. |custom_notification| image:: ./tutorial/images/gitlab_intro/custom_notification.png
.. |custom_toissue| image:: ./tutorial/images/gitlab_intro/custom_toissue.png
.. |drag_file| image:: ./tutorial/images/gitlab_intro/drag_file.png
.. |edit_file| image:: ./tutorial/images/gitlab_intro/editfile.png
.. |new_file_content| image:: ./tutorial/images/gitlab_intro/new_file_content.png
.. |new_file| image:: ./tutorial/images/gitlab_intro/new_file.png
.. |upload_file| image:: ./tutorial/images/gitlab_intro/uploadfile.png
.. |download_file| image:: ./tutorial/images/gitlab_intro/download.png
