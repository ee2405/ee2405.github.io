Virtual Machine Performance Improvement Tutorial
################################################
:Date:    2020-03-02 20:00
:Tags:    Tutorial
:Summary: Virtual Machine settings
:Status: Draft

.. sectnum::
	 :depth: 2

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

	The goal of this lab is to learn:

	#. How to improve the performance of Virtual Machine

****************
Lab Introduction
****************
Virtual machines provide virtual hardware and run multiple operating
systems on your computer at once. As time passes, they may result in slow operating
system performance, slow application performance, and the inability of an application
to load or continue to run. Among many tips, here are two simple ones that help squeeze every
last drop of performance out of your virtual machines.

For more solutons to speed up virtual machines, please refer to the \ `Reference List`_.

**Notes: In all cases, ensure the virtual machine is power-off before changing settings.**

***************
Lab Description
***************

Allocate More CPU
====================

#. **Introduction**

   You can assign vCPU to a virtual machine if your host system has at least two logical processors.
   The following hosts are considered to have such configuration.

   - multiprocessor hosts with two or more physical CPUs
   - single-processor hosts with a multicore CPU
   - single-processor hosts with hyperthreading enabled

#. **Settings**

VMware
```````

#. Select your virtual machine and click **Player > Manage > Virtual Machine Settings**:

   .. image:: tutorial/images/Virtual%20Machine%20Performance%20Improvement/vCPU-1.png
      :alt: VM Settings

#. On the **Hardware** tab, choose **Processors** and change **Number of processor cores** on the right side.

   .. image:: tutorial/images/Virtual%20Machine%20Performance%20Improvement/vCPU-2.png
      :alt: vCPU

#. Increase the cores as you want. *( Notice: It's not allowed to configure cores more than the host supports. )*

#. Power on the virtual machine for the changes to take effect.

VirtualBox
```````````

#. Select your virtual machine and click **Settings**:

   .. image:: tutorial/images/Virtual%20Machine%20Performance%20Improvement/vbCPU-1.png
      :alt: VB Settings

#. On the **System** tab, choose **Processor** and change the number of processors.

   .. image:: tutorial/images/Virtual%20Machine%20Performance%20Improvement/vbCPU-2.png
      :alt: vbCPU

#. Increase the cores as you want. *( Notice: It's not allowed to configure cores more than the host supports. )*

#. Power on the virtual machine for the changes to take effect.


Assign More Memory
===========================

#. **Introduction**

   If too much memory is shared out, your physical PC may not have enough RAM to complete regular tasks. Similarly, if
   little memory is assigned to your virtual machines, it may result in poor performance. As a result, we recommend you to give out
   1/2 of your computer's available RAM.

#. **Settings**

VMware
```````

#. Select your virtual machine and click **Player > Manage > Virtual Machine Settings**:

   .. image:: tutorial/images/Virtual%20Machine%20Performance%20Improvement/vCPU-1.png
      :alt: VM Settings

#. On the **Hardware** tab, choose **Memory** and change **Memory for this virtual machine** on the right side.

   .. image:: tutorial/images/Virtual%20Machine%20Performance%20Improvement/vRAM.png
      :alt: vRAM

#. Vary the memory to half of your computer's memory as recommended.

#. Power on the virtual machine for the changes to take effect.

VirtualBox
```````````

#. Select your virtual machine and click **Settings**:

   .. image:: tutorial/images/Virtual%20Machine%20Performance%20Improvement/vbCPU-1.png
      :alt: VB Settings

#. On the **System** tab, choose **Motherboard** and change **Base Memory**.

   .. image:: tutorial/images/Virtual%20Machine%20Performance%20Improvement/vbRAM.png
      :alt: vbRAM

#. Vary the memory to half of your computer's memory as recommended.

#. Power on the virtual machine for the changes to take effect.

**************
Reference List
**************

- `Guides to Speed Up Your Virtual Machines <https://www.howtogeek.com/124796/the-htg-guide-to-speeding-up-your-virtual-machines/>`__
