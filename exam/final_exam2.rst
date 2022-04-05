EE240502 Embedded System Laboratory Final Exam
################################################
:Date:    2019-06-18 15:30
:Tags:    Exams
:Summary: The Final Exam (EE240502)
:Status:  Draft


.. sectnum::
    :depth: 2

.. include:: ../LARC_def.txt

.. contents::

*******
Rule
*******

#. Search on the Internet is allowed.

#. Any communication with others is strictly prohibited.

#. To the coding progress, you **must** upload your local history or check in codes to a git repo.
   If you don't know how to record your coding history,
   please go through the instruction
   `here <https://www.ee.nthu.edu.tw/ee240500/exam-preparation.html#record-your-coding-histroy>`__.

#. Please take a photo of each major step of your work.
   If you don't know how to take a photo, please go through the instruction
   `here <https://www.ee.nthu.edu.tw/ee240500/exam-preparation.html#use-cheese-to-take-a-picture>`__.

**********
Submission
**********

* Due time: 17:00, June 18, 2019

* Submit your answer (source codes, local history and photos):

#. `XBee and MQTT <https://forms.gle/myjr1FhHCpQHMAet9>`__

*********
Questions
*********

XBEE and MQTT (100pt)
========================

#. Please write an mbed code to measure the accelerometers (X, Y and Z) by when the BB car goes forward and then backward repeatedly.
   The same mbed code will transmit the data to a PC with XBEE every 0.1 sec.
#. Please write a Python code to receive the accelerometers data from XBEE channel.
   With the same Python code, we publish the data to MQTT server.
#. Please write another Python code to subscribe to the data. It will plot the data over time with Matplot.
#. Hint: This is a sample code for publishing messages to localhost MQTT.

   .. code-block:: python
      :linenos: inline
      
      import paho.mqtt.client as paho
      import time
      mqttc = paho.Client()
    
      # Settings for connection
      host = "localhost"
      topic= "Mbed"
      port = 1883

      # Callbacks
      def on_connect(self, mosq, obj, rc):
          print("Connected rc: " + str(rc))

      def on_message(mosq, obj, msg):
          print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");

      def on_subscribe(mosq, obj, mid, granted_qos):
          print("Subscribed OK")

      def on_unsubscribe(mosq, obj, mid, granted_qos):
          print("Unsubscribed OK")

      # Set callbacks
      mqttc.on_message = on_message
      mqttc.on_connect = on_connect
      mqttc.on_subscribe = on_subscribe
      mqttc.on_unsubscribe = on_unsubscribe

      # Connect and subscribe
      print("Connecting to " + host + "/" + topic)
      mqttc.connect(host, port=1883, keepalive=60)
      mqttc.subscribe(topic, 0)

      while(1):
          mesg = "Hello, world!"
          mqttc.publish(topic, mesg)
          print(mesg)
          time.sleep(1)

#. You need to submit the mbed code, 2 python codes and the matplot figure.