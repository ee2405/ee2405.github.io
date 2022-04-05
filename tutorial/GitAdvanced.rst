Git Command Line (Advanced)
###########################
:Date:    2018-03-07 18:00
:Tags:    Tutorial
:Summary: Use Git command line tutorial (Advanced)
:Status: Draft

.. sectnum::
	 :depth: 2

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

	The goal of this lab is to learn:

	#. How to use Git in command line

Basic Concept
===============
This Git tutorial only discusses the basic operations.
For more information about Git, please refer to `ProGit <https://git-scm.com/book/en/v2>`_.

Git is a version control tool that keeps track of changing within your project (codes).
There are three main components of a Git project: working directory, staging area, and repository. (We'll mention them later.)
Each revision of your project is called :hl:`commit` and each project is called :hl:`repository` in Git.

Remember that all repositories can be kept in a distributed fashion which means
you can have a local repository (on a local computer) and a remote repository (on GitHub, GitLab, or Bitbucket) at the same time.
The changes made locally have to be pushed to the remote server if you want to
synchronize project on remotes.

In our labs, you are supposed to work on one branch if there isn't any other collaborator.
In this situation, you can simply pull and push commits without big problems.
However, if you're working with others on the same project (repo),
you need to be careful about merging and testing changes from your partner.

Refer to \ `Reference`_ for Git in detail, also you get help information about Git
with :cmd_host:`$ git help <verb>` or :cmd_host:`$ git <verb> --help`,

Install Git on Ubuntu
=====================

The easiest and recommended way to install Git is via the :hl:`apt` package management
tool from Ubuntu’s default repositories.

* Run the following command to install Git:

  :cmd_host:`$ sudo apt install git-all`

* Verify the installation and the version by running:

  :cmd_host:`$ git --version`

Now, you have successfully installed Git on your system and you'll want to customize
your Git environment by doing so:

.. code-block:: terminal

   $ git config --global user.name "Your Name"
   $ git config --global user.email "Your Email"

Every Git commit will use the above information after these configurations.

You should have to do the configurations only once on any given computer since they’ll stick
around between upgrades. You can also change them at any time by running through
the commands again.

Start a Local Repository
========================

Initialize a Repository
-----------------------

If you have a project directory that is not under Git version control, you'll need to
first go to that directory.

#. Start a terminal with :hotkey:`Ctrl+Alt+T`
#. Enter a working directory. For instance,

   :cmd_host:`$ cd ~/ee2405/mbed01`

#. Then type

   :cmd_host:`$ git init`

   This create a :file:`.git` that helps track/commit all your changes and perform version
   control.

At this point, you have a local Git repository with nothing being tracked
in your project. So let's go to the next section and learn version-controlling.

Start version-controlling
-------------------------

Typically, you’ll want to start making changes and committing snapshots of those
changes into your local repository each time the project reaches a state you want to record.
But before this, remember that each file in your working directory can be in one of two states:
tracked or untracked.

* To check the state, whether there are tracked, untracked, or modified files,
  of the current working directory, run

  :cmd_host:`$ git status`

* If there are files under the **Untracked files** heading in your status output, use
  the command below in order to begin tracking them .

  :cmd_host:`$ git add <filename>`

  Run :cmd_host:`$ git status` again and you'll see :file:`<filename>` labeled as **new file**,
  which means it is now in the staging area, waiting for commits.

* Now that your staging area is set up the way you want it, you can commit your changes.
  Remember that anything that is still unstaged (not in the staging area) — any files you have created or modified that
  you haven’t run :hl:`$ git add` on since you edited them — won’t go into this commit.

  :cmd_host:`$ git commit -m "<commit messages>"`

  Replace <commit messages> with any message you want.

* After creating several commits, you may want to view the commit history. The
  basic and powerful tool to do this is the following command:

  :cmd_host:`$ git log`

  By default, with no arguments, :hl:`$ git log` lists the commits made in that repository
  in reverse chronological order; that is, the most recent commits show up first.

  **Additional remark:** There is another command :hl:`$ git reflog` kind of
  similar to :hl:`$ git log`. Yet, :hl:`$ git reflog` can help inspect all history
  operations on branches including deleted commits and reset instructions, :hl:`$ git log`
  doesn't show removed commits.

Staging Modified Files
----------------------

If you modify a previously tracked file :file:`<filename>` and run :hl:`$ git status` again,
you'll see :file:`<filename>` appear under a section named **Changes not staged for commit**
and labeled as **modified**, and here comes two possibilities:

* You want your modified file to be committed to your local repository.

  In this situation, run the commands below to ensure you commit the latest and right version.

  :cmd_host:`$ git add <filename>`

  :cmd_host:`$ git commit -m "<commit messages>"`

* You accidentally screw up with this file.

  #. Under this circumstance, run the following command to compare the difference between the modified file and the previous one.

     :cmd_host:`$ git diff <filename>`

  #. Discard changes and roll back to the last version committed in your local repository.

     :cmd_host:`$ git checkout -- <filename>`

.gitignore File
------------------

Somehow, there will be files that you don't want to track and so here comes the
:file:`.gitignore` file.

Create a :file:`.gitignore` file by running :cmd_host:`$ touch .gitignore`.

:file:`.gitignore` must be edited by hand when you have new files that you wish to ignore.
It contains patterns that are matched against file names in your
repository to determine whether or not they should be ignored. Afterwards, you
should add and commit :file:`.gitignore` just like other files so that the
file can take effect.

For more information, please visit `gitignore <https://git-scm.com/docs/gitignore>`_.

So far, you've known the basic concepts of creating a local repository. We'll
now go further learning some simple Git operations and the remote repository.

Undoing Commits and Changes
===========================

**Notes:** :hl:`HEAD` points to the last commit on the currently check-out branch.
Usually, you can view :hl:`HEAD` as the current branch.

* Reset current :hl:`HEAD` to the specified state.

  :cmd_host:`$ git reset [mode] <commit>`

  This command resets the current branch head to :hl:`<commit>` and possibly updates the
  index and the working tree depending on :hl:`[mode]` which defaults to :hl:`--mixed`.
  Common used modes are as follows:

  * --soft

    Does not discard the file in working directory and staging area (but resets the head to :hl:`<commit>`,
    just like all modes do). All changed files will be listed under **Changes to be committed**,
    as git status shows.

  * --mixed

    Resets the index but not the working directory (i.e., the changed files are
    preserved but not marked for commit) and reports what has not been updated.

  * --hard

    The staging index/area and working directory are reset to match the specified commit.
    In other word, the pending work will be lost.

  If the commit history is as follows:

  .. code-block:: terminal

	  $ git log --oneline
	   313b3bd (HEAD -> master) bug fixed
	   460d288 update demo
	   278a10f initial commit

  Run the below command to reset to the last state.

  :cmd_host:`$ git reset HEAD^` or :cmd_host:`$ git reset 460d288`

* Revert some existing commits (often faulty ones).

  :cmd_host:`$ git revert <commit>`

  Say your commit history is as follows:

  .. code-block:: terminal

     $ git log --oneline
     313b3bd bug fixed
     460d288 update demo
     278a10f initial commit

  Run :hl:`$ git revert HEAD` (acts same as :hl:`$ git revert 460d288`),
  which reverts the latest commit and then examine the state again:

  .. code-block:: terminal

	   $ git log --oneline
	   81e1079 Revert "bug fixed"
	   313b3bd bug fixed
	   460d288 update demo
	   278a10f initial commit

  Instead of removing the commit from the project history, it creates a new revert
  commit. This prevents Git from losing history.

* Remove files.

  :cmd_host:`$ git rm <file>`

  Check the present state and you'll see as follows, the deleted file is already in the
  staging area and you can commit it afterwards to complete deletion.

  .. code-block:: terminal

     $ git status
     On branch master
     Changes to be committed:
     (use "git reset HEAD <file>..." to unstage)

         deleted:    <file>

* No longer under version control.

  :cmd_host:`$ git rm <file> --cached`

  This command doesn't remove the file; instead, it only helps get rid of Git control.
  The file will be listed under **Untracked files**. (:hl:`$ git status`)

* Change filename.

  :cmd_host:`$ git mv <filename> <new_filename>`

  Print status:

  .. code-block:: terminal

    $ git status
    On branch master
    Changes to be committed:
    (use "git reset HEAD <file>..." to unstage)

        renamed:    <filename> -> <new_filename>

* A convenience method for deleting untracked files in working directory of a repo.

  :cmd_host:`$ git clean -n / -f`

  :hl:`-n` option perform a “dry run”. It shows you which files
  are going to be removed without actually removing them.

  If **clean.requireForce** configuration is not set to false, :hl:`$ git
  clean` will refuse to delete files or directories. :hl:`-f` option initiates
  the actual deletion of untracked files from the current directory.

  For more options, please visit `git clean <https://git-scm.com/docs/git-clean>`_.


Git Branching
=============

Before working with remote repositories or collaborating with others, let's first
understand the basic concepts of branching and merging. If you want to debug or
test new functions on the project, you can add another branch to try new ideas and
merge with the current branch after solving problems without affecting what you're
working on.

Basic Branching
---------------

* Print branches on your repository

  :cmd_host:`$ git branch`

  .. code-block:: terminal

     $ git branch
     * master

  :hl:`master` is the default branch and :hl:`*` means you're now on this branch.

* Add new branch

  :cmd_host:`$ git branch <branch_name>`

  Run :hl:`$ git branch` again and you'll see:

  .. code-block:: terminal

     $ git branch
       <branch_name>
     * master

* Change branch name

  :cmd_host:`$ git branch -m <branch_name> <new_branch_name>`

* Delete branch

  :cmd_host:`$ git branch -d <branch_name>` or :cmd_host:`$ git branch -D <branch_name>`

  :hl:`-d` for merged branch, while :hl:`-D` for unmerged one

* Switch branch

  :cmd_host:`$ git checkout <branch_name>`

  Run :hl:`$ git branch` again and you'll see:

  .. code-block:: terminal

     $ git branch
     * <branch_name>
       master

  You've switched from master to <branch_name>. Also, you can  create a new branch
  and switch to it at the same time by running :cmd_host:`$ git checkout -b <branch_name>`

Basic Merging
-------------

* If you created two new branches, :hl:`test` and :hl:`update` for example, and commit :hl:`test` two times,
  the flow chart looks like this:

  .. image:: tutorial/images/git_basic/merge1.png
     :alt: merge1

  After making sure :hl:`test` is what you want, merge the :hl:`test` branch back
  into your :hl:`master` branch to deploy to production.

  #. :cmd_host:`$ git checkout master`

  #. :cmd_host:`$ git merge test`

  As a result, the flow chart looks like:

  .. image:: tutorial/images/git_basic/merge2.png
     :alt: merge2

  *(You can decide whether or not to delete the :hl:`test` branch by the command mentioned
  above since you no longer need it.)*

* Now suppose you switch to :hl:`update` branch and work on it.

  Finally, the work is complete and ready to be merged into your :hl:`master` branch.
  The process is much like that you merged the :hl:`test` branch earlier.

  #. :cmd_host:`$ git checkout master`

  #. :cmd_host:`$ git merge update`

  .. image:: tutorial/images/git_basic/merge3.png
     :alt: merge3

  This looks a bit different from the :hl:`test` merge you did.

  Because the commit on the branch you’re on isn’t a direct ancestor of the branch you’re merging in,
  Git has to do some work. Instead of just moving the branch pointer forward, Git generates a new commit,
  a merge commit, that deals with this case.

Basic Rebase
------------

* In Git, there are two main ways to integrate changes from one branch into another:
  :hl:`merge`, which we have talked about above and :hl:`rebase`. In this section
  you’ll learn the simplest idea of the latter.

  .. image:: tutorial/images/git_basic/rebase1.png
     :alt: rebase1

  Suppose the image shown above is your branching, with the commands below, you can
  take all the changes that were committed on :hl:`update` branch and replay them on :hl:`master` branch.

  .. code-block:: terminal

    $ git checkout update
    $ git rebase master

  This operation works by going to the common ancestor of the two branches, resetting
  the current branch to the same commit as the branch you are rebasing onto, and
  finally applying each change in turn.

  .. image:: tutorial/images/git_basic/rebase2.png
     :alt: rebase2

  At this point, you can go back to the :hl:`master` branch and do a fast-forward merge to
  ensure :hl:`master` always point to the latest commit. (:hl:`master` will point to
  the same commit as :hl:`update` in the above picture)

  .. code-block:: terminal

     $ git checkout update
     $ git rebase master

* To sum up, there is no difference between the end product of :hl:`merge` and :hl:`rebase`,
  but rebasing makes for a cleaner history. If you examine the log of a rebased branch, it looks like
  a linear history: it appears that all the work happened in series, even when it
  originally happened in parallel.

  However, for the question of whether merging or rebasing is better:
  it depends on how or what you're working on.

Merge conflict
--------------

* If you changed the same part of the same file differently in the two branches you’re
  merging, Git won’t be able to merge them cleanly. You’ll get a merge conflict
  that looks something like this:

  .. code-block:: terminal

    $ git merge <branch>
    Auto-merging <file>
    CONFLICT (content): Merge conflict in <file>
    Automatic merge failed; fix conflicts and then commit the result.

  Git has paused the process while you solve the conflict. Run :cmd_host:`$ git status`
  to check current state and you'll see :hl:`<file>` is listed as **unmerged**.
  Since Git marks the conflicted part in those files, you can open them manually
  and resolve those conflicts.

  After you've resolved each conflicted sections in each file, run :cmd_host:`$ git
  add` on each file to mark it as resolved. Staging the file marks it as resolved in Git.
  Then type :cmd_host:`$ git commit -m <message>` to finish merging.

* As for failing rebasing, you'll also get a merge-conflict message. The solution
  is similar to the one as just mentioned only with a slight difference.


  #. Modify the conflicted part in both files and add them to the staging area.

     :cmd_host:`$ git add <file>`

  #. Continue rebasing.

     :cmd_host:`$ git rebase --continue`

Create a Remote Repository
==========================

First, you will need a git remote repository account,
e.g., `GitHub <https://github.com/>`__, `GitLab <https://gitlab.com/>`__,
or `Bitbucket <https://bitbucket.org/>`__.

Follow the instructions in
`GitHub Tutorial <https://help.github.com/en/github/getting-started-with-github/create-a-repo>`__,
`GitLab Tutorial <https://docs.gitlab.com/ee/gitlab-basics/create-project.html#create-a-project-in-gitlab>`__,
or
`Bitbucket Tutorial <https://confluence.atlassian.com/bitbucket/create-a-git-repository-759857290.html>`__
to create project and copy the project URL. We'll use the URL in the later part.

Working with Remotes
====================

To be able to collaborate on any Git project, you need to know how to manage your
remote repositories. Remote repositories are versions of your project that are hosted
on the Internet or network somewhere. Collaborating with others involves
managing these remote repositories and pushing and pulling data to and from them when
you need to share work.

Pushing an existing Local Repository to Remote Repository
---------------------------------------------------------

Create a remote that tells your local repository you have a remote repository
somewhere on the Internet and you want to transfer all the commits over.

#. :cmd_host:`$ git remote add origin <URL>`

   :hl:`<URL>` is the one you copied in \ `Create a Remote Repository`_ section.

   :hl:`origin` is just a short name for the <URL>. You can theoretically call
   it anything you want but by convention, most people keep the name :hl:`origin`.

#. :cmd_host:`$ git push -u origin master`

   :hl:`master` branch is the default/main branch of your commits. This command
   helps to push your :hl:`master` branch to your :hl:`origin` server.

After the above steps, head back to remote repository and you'll see all your files are
hosted there with all the commit messages.

Fetch & Pull
------------

* Get data from the remote project that you don’t have yet.

  :cmd_host:`$ git fetch <remote> <branch>`

  This command fetches a specific :hl:`<branch>` from the :hl:`<remote>` repo
  which you can merge in or inspect at any time. (Leave off :hl:`<branch>` to
  fetch all remote references.)

  Then if you want your :hl:`master` branch with up-to-date progress, merge :hl:`<branch>`
  into :hl:`master` branch.

  :cmd_host:`$ git merge <branch>`

* If you understand the concept of :hl:`fetch` command, then there won't be any
  problem dealing with :hl:`pull` command since :hl:`git pull = git fetch + git merge`

  :cmd_host:`$ git pull <remote> <branch>`

  Leave off :hl:`<branch>` to pull all remote references.

Cloning a Remote Repository to your Local Machine
-------------------------------------------------

Download your own project or other projects you're interested in to your local
machine. (You can find the :hl:`<URL>` as mentioned in the previous section.)

:cmd_host:`$ git clone <URL>`

This command copies the whole project and store in a directory
of the same name. Not only the files but also the history commits, branches, tags,
etc. will be downloaded.

Reference
=========

* `ProGit <https://git-scm.com/book/en/v2>`_
* `Learn Git Branching <https://learngitbranching.js.org/>`_
