mbed Lab 14 Machine Vision with OpenMV H7 Plus (Optional)
##################################################################
:Date:    2022-05-25 15:00
:Tags:    Labs
:Summary: Learn image processing (person detection, image classification etc.) with OpenMV H7 Plus

.. sectnum::
   :depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

   The goal of this lab is to learn:

   #. Learn practical image processing
   #. Use OpenMV H7 board

****************
Lab Introduction
****************

For more information about OpenMV Cam, please visit https://openmv.io/products/openmv-cam-h7-plus.
For documentation of micropython libraries, please check https://docs.openmv.io/library/index.html#libraries-specific-to-the-openmv-cam.

***************
Equipment List
***************

#. PC or notebook with internet connection

#. OpenMV H7 Plus

#. L-shape metal connector * 2

#. M2.7*6mm screws * 4

#. M2.7 nuts * 4

***************
Lab Description
***************

Lecture Notes
=============

- Chapter 14: OpenMV `ch14_openmv.pdf <notes/ch14_openmv.pdf>`__

Preparation
===========
#. Install OpenMV IDE from the following `link.
   <https://openmv.io/pages/download>`__

#. Download the latest OpenMV firmware for OpenMV H7 plus from `here <https://github.com/openmv/openmv/releases/>`__.

#. Connect your OpenMV H7 plus to your host machine (Windows or Mac OS). 

#. Open IDE, select `tools <labs/img/ML_on_OpenMV/run_bootloader.png>`__ and click Run Bootloader (Load Firmware).

#. Select the `firmware path <labs/img/ML_on_OpenMV/select_firmware.png>`__ you
   just downloaded, and choose folder `OPENMV4P`. Then click "run". If you followed
   the instruction, the OpenMV H7 plus firmware will become the latest version you just downloaded.

Take and store a picture by OpenMV H7 Plus
==========================================
#. This part does not require mbed Studio.

#. Copy the following code into IDE

   The programming language for OpenMV H7 Plus (H7+) is Micro-Python, which is a sub-set of Python plus
   a I/O library for the board. Even though it should be relatively easy to learn Micro-Python,
   you are not required to program with the language in this lab. Students only need to apply
   H7+ codes provided in this lab for final projects.

   .. code-block:: python
      :linenos: inline

      import sensor, image, pyb

      RED_LED_PIN = 1
      BLUE_LED_PIN = 3

      sensor.reset() # Initialize the camera sensor.
      sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
      sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
      sensor.skip_frames(time = 2000) # Let new settings take affect.

      pyb.LED(RED_LED_PIN).on()
      sensor.skip_frames(time = 2000) # Give the user time to get ready.

      pyb.LED(RED_LED_PIN).off()
      pyb.LED(BLUE_LED_PIN).on()

      print("You're on camera!")
      sensor.snapshot().save("example.jpg") # or "example.bmp" (or others)

      pyb.LED(BLUE_LED_PIN).off()
      print("Done! Reset the camera to see the saved image.")

#. Click Connect and Start `(Run Script) <labs/img/ML_on_OpenMV/ide_start.png>`__. **(It will take 2 seconds to get ready.)**

#. Press **Tools > Reset OpenMV Cam** to save the image.

#. We can see the image in your OpenMV device.

#. **Note that OpenMV H7 Plus will run main.py if** `start <labs/img/ML_on_OpenMV/ide_start.png>`__ **is not clicked.**

QR Code Decoding (Optional)
===========================
#. In this example, we use OpenMV H7 plus to get the information from a QR Code.

#. Please generate a QR code with known information and display it on screen.
   You may use on-line QR code services or install a QR code generator as your browser extension.

#. Copy the following code into IDE and run to decode above QR code

   .. code-block:: python
      :linenos: inline

      import sensor, image, time

      sensor.reset()
      sensor.set_pixformat(sensor.RGB565)
      sensor.set_framesize(sensor.QVGA)
      sensor.skip_frames(time = 2000)
      sensor.set_auto_gain(False) # must turn this off to prevent image washout...
      clock = time.clock()

      while(True):
         clock.tick()
         img = sensor.snapshot()
         img.lens_corr(1.8) # strength of 1.8 is good for the 2.8mm lens.
         for code in img.find_qrcodes():
            img.draw_rectangle(code.rect(), color = (255, 0, 0))
            print(code)
         print(clock.fps())

#. Click Connect and Start (Run Script).

Data Matrices Decoding (Optional)
=================================
#. In this example, we use OpenMV H7 plus to get information stored in a `Data Matrices <https://en.wikipedia.org/wiki/Data_Matrix>`_.
   Also we get the viewing angle to the data matrix image, which is useful for BB car position calibration.

#. Please show `this Data Matrix <labs/img/ML_on_OpenMV/Data_matrix.png>`__ on screen.

#. Copy the following code into IDE and run to decode above Data Matrices.

   .. code-block:: python
      :linenos: inline

      import sensor, image, time, math

      sensor.reset()
      sensor.set_pixformat(sensor.RGB565)
      sensor.set_framesize(sensor.QVGA)
      sensor.skip_frames(time = 2000)
      sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
      sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
      clock = time.clock()

      while(True):
         clock.tick()
         img = sensor.snapshot()
         img.lens_corr(1.8) # strength of 1.8 is good for the 2.8mm lens.

         matrices = img.find_datamatrices()
         for matrix in matrices:
            img.draw_rectangle(matrix.rect(), color = (255, 0, 0))
            print_args = (matrix.rows(), matrix.columns(), matrix.payload(), (180 * matrix.rotation()) / math.pi, clock.fps())
            print("Matrix [%d:%d], Payload \"%s\", rotation %f (degrees), FPS %f" % print_args)
         if not matrices:
            print("FPS %f" % clock.fps())

#. Click Connect and Start (Run Script).

#. **Note that we could also get the angle between the camera of OpenMV H7 plus and the wall with the data matrix image.**

AprilTags
==============
#. In this example, we will use OpenMV H7 plus to get information stored in a
   `Apriltag <https://april.eecs.umich.edu/software/apriltag>`_. Via Apriltags, we
   are able to get the rotational angle and the relative translational distance
   from an object, which is useful in 3D positioning and camera calibration.

#. Please show `this AprilTag <labs/img/ML_on_OpenMV/tag_36h11.png>`__ on screen.

#. Copy the following code into IDE and run to decode above AprilTag.

   .. code-block:: python
      :linenos: inline

      import sensor, image, time, math

      sensor.reset()
      sensor.set_pixformat(sensor.RGB565)
      sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
      sensor.skip_frames(time = 2000)
      sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
      sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
      clock = time.clock()

      # Note! Unlike find_qrcodes the find_apriltags method does not need lens correction on the image to work.

      # What's the difference between tag families? Well, for example, the TAG16H5 family is effectively
      # a 4x4 square tag. So, this means it can be seen at a longer distance than a TAG36H11 tag which
      # is a 6x6 square tag. However, the lower H value (H5 versus H11) means that the false positve
      # rate for the 4x4 tag is much, much, much, higher than the 6x6 tag. So, unless you have a
      # reason to use the other tags families just use TAG36H11 which is the default family.

      # The AprilTags library outputs the pose information for tags. This is the x/y/z translation and
      # x/y/z rotation. The x/y/z rotation is in radians and can be converted to degrees. As for
      # translation the units are dimensionless and you must apply a conversion function.

      # f_x is the x focal length of the camera. It should be equal to the lens focal length in mm
      # divided by the x sensor size in mm times the number of pixels in the image.
      # The below values are for the OV7725 camera with a 2.8 mm lens.

      # f_y is the y focal length of the camera. It should be equal to the lens focal length in mm
      # divided by the y sensor size in mm times the number of pixels in the image.
      # The below values are for the OV7725 camera with a 2.8 mm lens.

      # c_x is the image x center position in pixels.
      # c_y is the image y center position in pixels.

      f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
      f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
      c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
      c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

      def degrees(radians):
         return (180 * radians) / math.pi

      while(True):
         clock.tick()
         img = sensor.snapshot()
         for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
            img.draw_rectangle(tag.rect(), color = (255, 0, 0))
            img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
            print_args = (tag.x_translation(), tag.y_translation(), tag.z_translation(), \
                  degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))
            # Translation units are unknown. Rotation units are in degrees.
            print("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args)
         print(clock.fps())

#. Click connect and Start(Run Script).

#. Note that the translational distance of each dimension is relative, you
   might need to construct a conversion table on your own. In our measurement
   (with the shown AprilTag and OpenMV H7 plus), the constant is approximately
   6.2cm to 1 unit from the Apriltag.

Line Detection
==============

#. In this example, we use OpenMV H7 plus to detect lines in an image.
   This is useful if we want to develop a line-following BB Car.

#. Copy the folowing code into IDE and run to dectect line.

   .. code-block:: python
      :linenos: inline

      import sensor, image, time
      enable_lens_corr = False # turn on for straighter lines...
      sensor.reset()
      sensor.set_pixformat(sensor.RGB565) # grayscale is faster
      sensor.set_framesize(sensor.QQVGA)
      sensor.skip_frames(time = 2000)
      clock = time.clock()

      # All lines also have `x1()`, `y1()`, `x2()`, and `y2()` methods to get their end-points
      # and a `line()` method to get all the above as one 4 value tuple for `draw_line()`.

      while(True):
         clock.tick()
         img = sensor.snapshot()
         if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...

         # `merge_distance` controls the merging of nearby lines. At 0 (the default), no
         # merging is done. At 1, any line 1 pixel away from another is merged... and so
         # on as you increase this value. You may wish to merge lines as line segment
         # detection produces a lot of line segment results.

         # `max_theta_diff` controls the maximum amount of rotation difference between
         # any two lines about to be merged. The default setting allows for 15 degrees.

         for l in img.find_line_segments(merge_distance = 0, max_theta_diff = 5):
            img.draw_line(l.line(), color = (255, 0, 0))
            # print(l)

         print("FPS %f" % clock.fps())

#. Click Connect and Start (Run Script)

Tensorflow lite (Optional)
=============================

You may skip the following two parts, since we may not need them in the homework or final projects.

Person Detection (Optional)
-----------------------------

#. OpenMV H7 Plus has a build-in person detection model in its firmware.
   In the following codes, we try to load and use the network to detect a person in an image.

#. Copy the following code into IDE

   .. code-block:: python
      :linenos: inline

      import sensor, image, time, os, tf

      sensor.reset()                         # Reset and initialize the sensor.
      sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
      sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
      sensor.set_windowing((240, 240))       # Set 240x240 window.
      sensor.skip_frames(time=2000)          # Let the camera adjust.

      # Load the built-in person detection network (the network is in your OpenMV Cam's firmware).
      net = tf.load('person_detection')
      labels = ['unsure', 'person', 'no_person']

      clock = time.clock()
      while(True):
         clock.tick()

         img = sensor.snapshot()
         # default settings just do one detection... change them to search the image...
         for obj in net.classify(img, min_scale=1.0, scale_mul=0.5, x_overlap=0.0, y_overlap=0.0):
            print("**********\nDetections at [x=%d,y=%d,w=%d,h=%d]" % obj.rect())
            for i in range(len(obj.output())):
                  print("%s = %f" % (labels[i], obj.output()[i]))
            img.draw_rectangle(obj.rect())
            img.draw_string(obj.x()+3, obj.y()-1, labels[obj.output().index(max(obj.output()))], mono_space = False)
         print(clock.fps(), "fps")

#. Click Connect and Start (Run Script).

Image Classification - MNIST (Optional)
-----------------------------------------

We will classify hand-written numbers by training a model based on MNIST data.
We recommend edgeimpulse.com service to train the MNIST data, which is simpler than writing Tensorflow script.

#. Training a classifier with MNIST

   #. Open `link <https://www.edgeimpulse.com/>`__ in the browser, sign up to use the platform.

   #. Follow the tutorial `here <https://docs.edgeimpulse.com/docs/image-classification>`__, play around the settings.

   #. You are encouraged to collect you own datasets with OpenMV H7 plus according to 4.3. Besides, we also provide part of our data set for training. Yet, this part is optional as you may directly apply our trained and converted tflite model.

   #. If you don't want to collect your own dataset, you can use ours: :cmd_host:`$ git clone https://gitlab.larc-nthu.net/ee2405_2021/mnist_jpg.git`

   #. The dataset is large, it may take a long time to upload and train, you can either reduce the train and test set, or you can use only the test set and let edge impulse split them into test and train automatically.

   #. After training, choose **deployment**, then choose **OpenMV cam** to download the tflite file.

   .. container:: warning

      - **Hint for training your own model and using the model that we provide.**

      - Please download the openmv_mnist dataset and check images inside each categories.
        The lighting and viewing angles of images may have a great impact on actual image classification.

      - At least 200 images for each category is recommended.

      - The order of label might be different to the order of class name.

#. Apply trained model from Edge Impulse

   #. After you trained your own dataset, please copy the python code generated from edge
      impulse. **do not copy the following codes**. Also, make sure your tflite file
      has the correct naming to match the codes.

   #. **Remember to put the tflite file inside the OpenMV!!**

   #. Click Connect and Start (Run Script).

#. Run a pre-trained model (optional)

   You can skip this part if you train and run the model yourself as above process.

   #. For those who want to skip the training part, 
      we also provide a pre-trained tflite model: 
      :cmd_host:`$ git clone https://gitlab.larc-nthu.net/ee2405_2021/pretrained_mnist.git` with label.txt

   #. If you download the tflite file from gitlab, copy the following codes into IDE.

      .. code-block:: python
         :linenos: inline

         # Edge Impulse - OpenMV Image Classification Example

         import sensor, image, time, os, tf

         sensor.reset()                         # Reset and initialize the sensor.
         sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
         sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
         sensor.set_windowing((240, 240))       # Set 240x240 window.
         sensor.skip_frames(time=2000)          # Let the camera adjust.

         net = "trained.tflite"
         labels = [line.rstrip('\n') for line in open("labels.txt")]

         clock = time.clock()
         while(True):
            clock.tick()

            img = sensor.snapshot()

            # default settings just do one detection... change them to search the image...
            for obj in tf.classify(net, img, min_scale=1.0, scale_mul=0.5, x_overlap=0.0, y_overlap=0.0):
               for i in range(len(obj.output())):
                  print("%s = %f" % (labels[i], obj.output()[i]))
            img.draw_rectangle(obj.rect())
            img.draw_string(obj.x()+3, obj.y()-1, labels[obj.output().index(max(obj.output()))], mono_space = False)
            print("This is : ",labels[obj.output().index(max(obj.output()))])


   #. **Remember to put the tflite file and the label.txt inside the OpenMV!!**

   #. Click Connect and Start (Run Script).

Serial connection of OpenMV H7 plus with mbed (Optional)
==============================================================

If you skip the previous part on TF Lite, please also skip this part, too.

#. In this example, OpenMV H7 plus will communicate with mbed through UART.

#. The default UART pins for OpenMV H7 plus are TX (P4), RX (P5). 
   For reference, please check the `Open MV H7+ page <https://openmv.io/products/openmv-cam-h7-plus>`_ for the pin names.
   Please connect  OpenMV TX (P4) to mbed RX (D0), and OpenMV RX (P5) to STM32 TX (D1) like `this <labs/img/ML_on_OpenMV/stm_uart_openmv.png>`__.
   Remember to set the same baud rate for OpenMV and mbed. 

#. Start mbed Studio and create a new Mbed program with "14_1_OpenMV_UART".

#. Edit :file:`main.cpp`.

#. Copy the following codes into :file:`main.cpp`.

   Note that this program simply send a "image_classification" string to H7+.
   And when H7+ sees this string the corresponding function will be called
   and return with classification results.
   Therefore, we can extend such a simple interface to include QR code decoding and
   other functions if necessary.

   .. code-block:: c++
      :linenos: inline

      #include"mbed.h"

      Thread thread1;
      Thread thread2;

      BufferedSerial pc(USBTX,USBRX); //tx,rx
      BufferedSerial uart(D1,D0); //tx,rx
      DigitalIn button(BUTTON1);

      void recieve_thread(){   
         while(1) {
            if(uart.readable()){
               char recv[1];
               uart.read(recv, sizeof(recv));
               // print out the recieved data
               pc.write(recv, sizeof(recv));
               printf("\r\n");
            }
         }
      }

      void send_thread(){
         while(1){
            // if button is pressed
            if(button == 0){ 
               char s[] = "image_classification\0";
               uart.write(s, sizeof(s));
               printf("send\r\n");
               ThisThread::sleep_for(1s);
            }
         }
      }

      int main(){
         uart.set_baud(9600);
         thread1.start(send_thread);
         thread2.start(recieve_thread);
      }

#. Compile and run the program.

#. **Put your trained `.tflite` file inside OpenMV, as in 4.7**

#. For OpenMV, copy the following codes into IDE.

   .. code-block:: python
      :linenos: inline

      import pyb
      import sensor, image, time, os, tf

      uart = pyb.UART(3,9600,timeout_char=1000)
      uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)
      tmp = ""

      def image_classification():
         sensor.reset()                         # Reset and initialize the sensor.
         sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565 (or GRAYSCALE)
         sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (?x?)
         sensor.set_windowing((240, 240))       # Set 240x240 window.
         sensor.skip_frames(time=2000)          # Let the camera adjust.
    
         img = sensor.snapshot(())
         net = "trained.tflite"
         labels = [line.rstrip('\n') for line in open("labels.txt")]
         # default settings just do one detection... change them to search the image...
         for obj in tf.classify(net, img, min_scale=1.0, scale_mul=0.5, x_overlap=0.0, y_overlap=0.0):
            img.draw_rectangle(obj.rect())
            img.draw_string(obj.x()+3, obj.y()-1, labels[obj.output().index(max(obj.output()))], mono_space = False)
         return labels[obj.output().index(max(obj.output()))]
    
      while(1):
         a = uart.readline()
         if a is not None:
            tmp += a.decode()
            print(a.decode())
    
         if tmp == "image_classification\0":
            print("classify images")
            tmp =""
            label = image_classification()
            print(label)
            uart.write(label.encode())
            uart.readchar()

#. Click Connect and Start (Run Script).

Put OpenMV H7 plus on the BOE BOT Car
=====================================

Here we install the OpenMV H7 plus on BB Car for mbed to use the vision and detection.

#. Install the L-shape metal connector on the OpenMV H7 plus with M2.7*6mm screws * 2 and M2.7 nuts * 2, and then it should become like `this <labs/img/bbcar_installation/06_openmv/install-openmv-1.jpg>`__.

#. Put OpenMV H7 plus on the BOE BOT Car with M2.7*6mm screws * 2 and M2.7 nuts * 2, and then it should become like `this <labs/img/bbcar_installation/06_openmv/install-openmv-2.jpg>`__.

#. Please connect OpenMV TX (P4) to mbed RX (D0), and OpenMV RX (P5) to mbed TX (D1) like `this <labs/img/ML_on_OpenMV/stm_uart_openmv.png>`__.


   For reference, please check the `Open MV H7+ page <https://openmv.io/products/openmv-cam-h7-plus>`_ for the pin names. Remember to set the same baud rate for OpenMV and mbed. 

#. Start mbed Studio and create a new Mbed program with "14_2_OpenMV_BOE_BOT_Car".

#. Copy the following codes into :file:`main.cpp`.

   .. code-block:: c++
      :linenos: inline

      #include"mbed.h"

      BufferedSerial pc(USBTX,USBRX); //tx,rx
      BufferedSerial uart(D1,D0); //tx,rx

      int main(){
         uart.set_baud(9600);
         while(1){
            if(uart.readable()){
                  char recv[1];
                  uart.read(recv, sizeof(recv));
                  pc.write(recv, sizeof(recv));
            }
         }
      }

#. Compile and run the program.

#. Plug the OpenMV H7 plus to PC.

#. Paste following code into the :file:`main.py` in the OpenMV H7 plus.
   This program will be executed automatically when OpenMV is booted.

   .. code-block:: python
      :linenos: inline

      import pyb, sensor, image, time, math

      sensor.reset()
      sensor.set_pixformat(sensor.RGB565)
      sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
      sensor.skip_frames(time = 2000)
      sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
      sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
      clock = time.clock()

      f_x = (2.8 / 3.984) * 160 # find_apriltags defaults to this if not set
      f_y = (2.8 / 2.952) * 120 # find_apriltags defaults to this if not set
      c_x = 160 * 0.5 # find_apriltags defaults to this if not set (the image.w * 0.5)
      c_y = 120 * 0.5 # find_apriltags defaults to this if not set (the image.h * 0.5)

      def degrees(radians):
         return (180 * radians) / math.pi

      uart = pyb.UART(3,9600,timeout_char=1000)
      uart.init(9600,bits=8,parity = None, stop=1, timeout_char=1000)

      while(True):
         clock.tick()
         img = sensor.snapshot()
         for tag in img.find_apriltags(fx=f_x, fy=f_y, cx=c_x, cy=c_y): # defaults to TAG36H11
            img.draw_rectangle(tag.rect(), color = (255, 0, 0))
            img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
            # The conversion is nearly 6.2cm to 1 -> translation
            print_args = (tag.x_translation(), tag.y_translation(), tag.z_translation(), \
                  degrees(tag.x_rotation()), degrees(tag.y_rotation()), degrees(tag.z_rotation()))
            # Translation units are unknown. Rotation units are in degrees.
            uart.write(("Tx: %f, Ty %f, Tz %f, Rx %f, Ry %f, Rz %f" % print_args).encode())
         uart.write(("FPS %f\r\n" % clock.fps()).encode())


#. Unplug OpenMV H7 plus and plug the OpenMV H7 plus to the portable charger. The charger should connect to OpenMV(Vin).

#. Use OpenMV H7 plus to view the `AprilTag <labs/img/ML_on_OpenMV/tag_36h11.png>`__.

#. **Note that now mbed on BB Car could get the rotational angle and the translational relative distance for each dimension.**
   If we also use PING to estimate the distance between BB Car and the wall, we can estimate the location of BB Car.
   This part will be applied in the final project.

********************
Demo and Checkpoints
********************
#. Please download an AprilTag from https://github.com/AprilRobotics/apriltag-imgs/ 

#. Show your AprilTag on screen and find out the ID information in the AprilTag (They should match with the number on
   the png file name.

#. The png file in the github is small. Please download the file and open it with paint(小畫家). Use the resize tool twice to get a reasonable size for scanning. 

#. Please send the AprilTag information back to mbed and show the information of on screen.

**************
Reference List
**************

#. `TensorFlow-Slim image classification model library <https://github.com/tensorflow/models/tree/master/research/slim?fbclid=IwAR3CeDa2WRadJT7cvaZa723IJGDV72QhXXCNj4NXJc41U0Of6PkQaa5EG5c#preparing-the-datasets>`__

#. `Tensorflow transfer learning <https://www.tensorflow.org/tutorials/images/transfer_learning>`__
