Git Command Line (Basic)
########################
:Date:    2018-03-07 17:00
:Tags:    Tutorial
:Summary: Use Git command line tutorial (Basic)
:Status: Draft

.. sectnum::
	 :depth: 2

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

	The goal of this lab is to learn:

	#. How to use Git in command line
.. container:: instruct

   For advanced information about Git, please visit
   `Git Command Line (Advanced) <git-command-line-advanced.html>`_.

Install Git on Ubuntu
=====================

#. Run the following command to install Git:

   :cmd_host:`$ sudo apt install git-all`

#. Verify the installation and the version by running:

   :cmd_host:`$ git --version`

#. Set git configuration values.

   :cmd_host:`$ git config --global user.name <your name>`

   :cmd_host:`$ git config --global user.email <your email>`

   Every Git commit will use the above information after these configurations.

Create a Remote Repository
==========================

#. To start, you will need a git remote repository account,
   e.g., `GitHub <https://github.com/>`__, `GitLab <https://gitlab.com/>`__,
   or `Bitbucket <https://bitbucket.org/>`__.

#. Follow the instructions in
   `GitHub Tutorial <https://help.github.com/en/github/getting-started-with-github/create-a-repo>`__,
   `GitLab Tutorial <https://docs.gitlab.com/ee/gitlab-basics/create-project.html#create-a-project-in-gitlab>`__,
   or
   `Bitbucket Tutorial <https://confluence.atlassian.com/bitbucket/create-a-git-repository-759857290.html>`__
   to create project.

#. Remember the remote repository :hl:`<URL>`:
   :file:`https://<gitserver.com>/<username>/<repo-name>.git`.

   For example, :file:`https://gitlab.larc-nthu.net/ee2405_2019/mbed_rpc.git`

Clone a Remote Repository to your Local Machine
===============================================

#. Browse to the location where you want to put the repository on your local
   machine.

   For example, :cmd_host:`$ cd ~/ee2405/git-tutorial`

#. Clone your own project to your local machine.
   (You can find the :hl:`<URL>` as mentioned in the previous section.)

   :cmd_host:`$ git clone <URL>`

#. Browse to the repository on your local machine.
   (You can find the :hl:`<repo-name>` as mentioned in the previous section.)

   :cmd_host:`$ cd <repo-name>`

Start version-controlling
=========================

#. To check the state, whether there are tracked, untracked, or modified files,
   of the current working directory, run

   :cmd_host:`$ git status`

#. Open vs code and create a file named :file:`helloworld.py`.

   #. :cmd_host:`$ code helloworld.py &`
   #. Enter the following codes:

   .. code-block:: python
      :linenos: inline

      def main():
          for i in range(1, 10):
              print('hello world', i, 'times!' )
      main()

#. Check the state and you will see :file:`helloworld.py` is in the untracked
   files field.

   :cmd_host:`$ git status`

#. To track the :file:`helloworld.py`:

   :cmd_host:`$ git add helloworld.py`

#. Check the state and you will see :file:`helloworld.py` is marked
   :hl:`new file`.

   :cmd_host:`$ git status`

#. To commit your changes:

   :cmd_host:`$ git commit -m "Add helloworld.py"`

#. To view the commit history:

   :cmd_host:`$ git log`

#. Open vs code and modify the file named :file:`helloworld.py`.

   #. :cmd_host:`$ code helloworld.py &`
   #. Modify the code to be like this:

   .. code-block:: python
      :linenos: inline

      def main():
          for i in range(1, 10):
              print('hello ee2405', i, 'times!' )
      main()

#. Check the state and you will see :file:`helloworld.py` is marked
   :hl:`modified`.

   :cmd_host:`$ git status`

#. To compare the difference between the modified file and the previous one.

   :cmd_host:`$ git diff helloworld.py`

#. Discard changes and roll back to the last version committed in your local
   repository.

   :cmd_host:`$ git checkout -- helloworld.py`

Sync between Local Repository and Remote Repository
===================================================

#. Push your commit to the remote repository.

   :cmd_host:`$ git push`

#. Pull the commit from the remote repository.

   :cmd_host:`$ git pull`
