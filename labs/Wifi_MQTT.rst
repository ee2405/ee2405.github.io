mbed Lab 10 WiFi and MQTT
##################################################
:Date:    2022-04-27 15:00
:Tags:    Labs
:Summary: WiFi Communication and MQTT

.. sectnum::
      :depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

   The goal of this lab is to learn:

   #. Learn WiFi interface on an IoT Node 
   #. Learn MQTT protocols

****************
Lab Due
****************

**Apr. 27, 2022**

****************
Lab Introduction
****************

B-L4S5I-IOT01A includes an ism43362 WiFi chip on the board (connected with a
SPI interface).  In this lab, we will use an mbed Ethernet driver to connect to
a WiFi access point and access a web server on installed PC.

In the later parts of the lab, we use MQTT to transfer structured information
between mbed and PC.  MQTT protocol is an easy and commonly used standard in
many IoT devices for collecting sensor data. In this lab, We will use WiFi
interface to create an MQTT connection between mbed and PC.

***************
Equipment List
***************

#. B-L4S5I-IOT01A * 1

***************
Lab Description
***************

Lecture Notes
=============

- Chapter 11: TCP/IP, WiFi, MQTT `ch11_wifi_mqtt.pdf <notes/ch11_wifi_mqtt.pdf>`__

Connect B-L4S5I-IOT01A to WiFi
===============================

.. container:: instruct

   Note 1: :hl:`It's recommended to setup your own hotspot to avoid network congestion on public routers.`

   Note 2: :hl:`Your PC and B_L4S5I_IOT01A should both be connected to the same hotspot (belong to the same sub-network).`

   Note 3: :hl:`You may share the same hotspot with other students. Just to make sure to connect to your own host IP.`

   Note 4: :hl:`This lab does not need data communication to public ethernet. However, if you share Cell hotspot from your cell phone with your PC,
   other programs on your PC may consume the bandwidth of your data plan.`

   #. Windows 10

      #. Select the Start button, then select Settings -> Network & Internet -> Mobile hotspot.

      #. For **Share my Internet connection from**, choose the Internet connection you want to share.

      #. Select Edit -> enter a new network name and password -> Save.

      #. Turn on **Share my Internet connection with other devices**.

   #. Mac OS

      #. Click :hl:`Apple icon > System Preferences > Sharing`, to go to the setting window.

      #. Click on Internet Sharing and set WIFI as the following. 
         `screenshot <labs/img/Wifi_MQTT/MACOS1.png>`__ `screenshot <labs/img/Wifi_MQTT/MACOS2.png>`__

      #. Now turn on Internet Sharing by clicking the tick mark next to Internet Sharing in the sidebar.

      #. Click Start on the menu that pops up in order to turn Internet Sharing on.

   #. Android

      #. Open the Settings app.

      #. Press the Network & Internet option.  `screenshot <labs/img/Wifi_MQTT/Windows_1.png>`__

      #. Press the Hotspot & tethering option.

      #. Toggle the switch next to Wi-Fi hotspot to on.

      #. Tap Set up Wi-Fi hotspot to manage name and password settings for your hotspot.  `screenshot <labs/img/Wifi_MQTT/Windows_2.png>`__

   #. iOS

      #. Open the Settings app.

      #. Tap Personal Hotspot.

      #. Switch the slider next to Personal Hotspot to the on position.

      #. From that same screen you can edit your Wi-Fi password.


.. container:: instruct

   We may setup a few WiFi hotspots. You may choose any of them depends on the signal intensity.
   :hl:`Note that your PC and mbed should be connected to the same hotspot`.

   +----------+------------+
   |   SSID   |  Password  |
   +==========+============+
   | emlab    | eenthu2405 |
   +----------+------------+

Setup Apache Web Server
-----------------------

#. Get the IP of your PC with:

   This IP will be used in the following lab. Every time you switch to a new hotspot, you should recheck the IP address of your PC.

   #. For Windows:

      #. Click the wifi icon on the task bar and click "Properties".

      #. Scroll down to check the IPv4 address.

      Or.

      #. Start GitHub bash

      #. Use :cmd_host:`$ ipconfig` to check IPv4 Address.

   #. For Mac OS:

      #. Click the wifi icon on the top status bar and click "Preference" (the last one).

      #. Check the IP address.

      Or.

      #. Start Terminal app

      #. Use :cmd_host:`$ ifconfig` to check inet Address.

#. Install apache2 web server 

   #. For Windows: (Reference: https://codebriefly.com/how-to-setup-apache-php-mysql-on-windows-10/)

      #. Download `httpd-2.4.52-win64-VS16.zip <https://www.apachelounge.com/download/VS16/binaries/httpd-2.4.52-win64-VS16.zip>`__

      #. Extract the zip. Here we assume it's "C:\\Apache24"

      #. Edit :file:`C:\\Apache24\\conf\\httpd.conf` and change the following line to your installation directory:

         .. code-block:: none
        
            Define SRVROOT "C:/Apache24"

      #. Start Git bash 

      #. Go to the installation directory:

         :cmd_host:`$ cd C:\Apache24\bin` 

      #. Start Apache service

         :cmd_host:`$ ./httpd.exe` 

	 This is a temparory setup for Apache server. You may kill it with :hotkey:`Ctrl+C`. 

	 If you want to start it as a service, you need to install it with :cmd_host:`$ ./httpd.exe -k install`. 
	 And then start Windows **Run** box with :hotkey:`Windows+R` and type "services.msc"
         Search for Apache and click "Start the service".

      #. Open network port 80 for Apache web services for Windows firewall (defender)

         If you use other Firewall software (or any Antivirus), you should consult the software's manual or search web on how to setup a port.

         Please follow `設定Window防火牆 <https://jimirobot.tw/esp32-mosquitto-windows-mqtt-tutorial/#3_設定_window_防火牆>`__ 
	 or `Setup port for Windows <https://bytesofgigabytes.com/networking/how-to-open-port-in-windows/>`__

	 #. Press Windows+R

         #. Type firewall.cpl in Open field and Click OK.

	 #. Click on **Advanced settings**

	 #. First click on **Inbound Rules** and then Click on **New Rule**

	 #. To open port, Please select Rule Type as **Port** and click **Next**.

	 #. Select TCP. Set "**Specify local ports**" as 80. Click on Next.

	 #. Select Allow the connection and click Next

	 #. Check "Private" and click on Next

	 #. Enter the name for opening port rule, e.g., "Web Service Input Port".

	 #. Repeat above again for **Outbound Rules** 

	 #. First click on **Outbound Rules** and then Click on **New Rule**

	 #. To open port, Please select Rule Type as **Port** and click **Next**.

	 #. Select TCP. Set "**Specify local ports**" as 80. Click on Next.

	 #. Select Allow the connection and click Next

	 #. Check "Private" and click on Next

	 #. Enter the name for opening port rule, e.g., "Web Service Output Port".


      #. Copy the following :file:`index.html` to the directory of "DocumentRoot" set in "C:\\Apache24\\conf\\httpd.conf".
         For example, it's in "<SRVRoot>\\htdocs", e.g., "C:\\Apache24\\htdocs".

         .. code-block:: html
           :linenos: inline
 
           <!DOCTYPE doctype PUBLIC "-//w3c//dtd html 4.0 transitional//en">
           <html>
           <head>
                   <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
                   <title>A Test Web Page</title>
                   <meta name="author" content="jj">
           </head>
           
           <body bgcolor="#ffffcc" dir="ltr" link="#000000" text="#000000" vlink="#3333ff">
           
           <h2><font color="#000099">EE2405 Lab</font>&nbsp;</font></h2>
           <h2>Test web page for Apache</h2>
           
           <hr><br>
           
           <p>
           You may modify this page and add additional contents.
           </p>
 
           </body>
           </html>
 
      #. Use web browser to open the URL on the host. For example, if PC's IP is 192.168.1.3, and then type URL as "192.168.1.3/index.html".
         You should see the light yellow background with "Test web page for Apache".

   #. For Mac OS: 
      
      Apache is pre-installed on Mac OS. We just need to start it as a service.

      #. Start a Terminal app 

      #. Start the Apache service

         :cmd_host:`$ sudo apachectl start` 

	 If you want to stop Apache, type :cmd_host:`$ sudo apachectl stop`.

      #. By default, Mac OS does not start a network firewall.
         If you setup a firewall, please allow port 80 in the configuration.
	 Please refer to `the tutorial <https://www.lifewire.com/open-a-port-on-a-routers-or-computers-firewall-5072435>`__
	 for opening a port in Mac OS (scroll down to skip Windows part):

      #. Copy the following "index.html" to the directory of "DocumentRoot" set in :file:`/etc/apache2/httpd.conf`.
         For example, the default directory in Mac OS is :file:`/Library/WebServer/Documents`.

         .. code-block:: html
           :linenos: inline
 
           <!DOCTYPE doctype PUBLIC "-//w3c//dtd html 4.0 transitional//en">
           <html>
           <head>
                   <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
                   <title>A Test Web Page</title>
                   <meta name="author" content="jj">
           </head>
           
           <body bgcolor="#ffffcc" dir="ltr" link="#000000" text="#000000" vlink="#3333ff">
           
           <h2><font color="#000099">EE2405 Lab</font>&nbsp;</font></h2>
           <h2>Test web page for Apache</h2>
           
           <hr><br>
           
           <p>
           You may modify this page and add additional contents.
           </p>
 
           </body>
           </html>
 
      #. Use web browser to open the URL on the host. For example, if PC's IP is 192.168.1.3, and then type URL as "192.168.1.3/index.html".
         You should see the light yellow background with "Test web page for Apache".

Setup mbed Ethernet Example
----------------------------

#. Create a new program.

#. Open the **File** menu and select **Import Program....**

#. Copy "https://github.com/ARMmbed/mbed-os-example-sockets.git" in URL.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".
   
#. The original code should run without problem, but to connect to your PC server, understand and modify the codes in :file:`main.cpp`.

   You will need to change the following HOST_IP to match your PC IP.

   #. Revise the "HOST_IP" in :file:`main.cpp` to the IP of your PC. For example, my IP is 192.168.1.3:
   
      line 8:

      .. code-block:: c++
   
         static constexpr char*  HOST_IP="192.168.1.3";

      line 82:

      .. code-block:: c++
   
         const char buffer[] = "GET / HTTP/1.1\r\n" "Host: 192.168.1.3\r\n" "Connection: close\r\n" "\r\n";


      .. code-block:: c++
         :linenos: inline
       
         #include "mbed.h"
         #include "wifi_helper.h"
         #include "mbed-trace/mbed_trace.h"
       
         class SocketDemo {
             static constexpr size_t MAX_NUMBER_OF_ACCESS_POINTS = 10;
             static constexpr size_t MAX_MESSAGE_RECEIVED_LENGTH = 100;
             static constexpr char*  HOST_IP="192.168.1.3";
             static constexpr size_t REMOTE_PORT = 80; // standard HTTP port
       
         public:
             SocketDemo() : _net(NetworkInterface::get_default_instance()) {}
       
             ~SocketDemo()
             {
                 if (_net)
                     _net->disconnect();
             }
       
             void run()
             {
                 if (!_net) {
                     printf("Error! No network interface found.\r\n");
                     return;
                 }
       
                 printf("Connecting to the network...\r\n");
       
                 nsapi_size_or_error_t result = _net->connect();
                 if (result != 0) {
                     printf("Error! _net->connect() returned: %d\r\n", result);
                     return;
                 }
       
                 print_network_info();
       
                 result = _socket.open(_net);
                 if (result != 0) {
                     printf("Error! _socket.open() returned: %d\r\n", result);
                     return;
                 }
       
                 SocketAddress address(HOST_IP, REMOTE_PORT); //Set IP and port directly 
       
                 //if (!resolve_hostname(address)) return;
                 //address.set_port(REMOTE_PORT);
       
                 printf("Opening connection to remote port %d\r\n", REMOTE_PORT);
       
                 result = _socket.connect(address);
                 if (result != 0) {
                     printf("Error! _socket.connect() returned: %d\r\n", result);
                     return;
                 }
       
                 if (!send_http_request() || !receive_http_response()) 
                     return;
       
                 printf("Demo concluded successfully \r\n");
             }
       
         private:
             bool resolve_hostname(SocketAddress &address)
             {
                 const char hostname[] = MBED_CONF_APP_HOSTNAME;
       
                 printf("\nResolve hostname %s\r\n", hostname);
                 nsapi_size_or_error_t result = _net->gethostbyname(hostname, &address);
                 if (result != 0) {
                     printf("Error! gethostbyname(%s) returned: %d\r\n", hostname, result);
                     return false;
                 }
       
                 printf("%s address is %s\r\n", hostname, (address.get_ip_address() ? address.get_ip_address() : "None") );
       
                 return true;
             }
       
             bool send_http_request()
             {
                 /* loop until whole request sent */
                 const char buffer[] = "GET / HTTP/1.1\r\n" "Host: HOST_IP\r\n" "Connection: close\r\n" "\r\n";
       
                 nsapi_size_t bytes_to_send = strlen(buffer);
                 nsapi_size_or_error_t bytes_sent = 0;
       
                 printf("\r\nSending message: \r\n%s", buffer);
       
                 while (bytes_to_send) {
                     bytes_sent = _socket.send(buffer + bytes_sent, bytes_to_send);
                     if (bytes_sent < 0) {
                         printf("Error! _socket.send() returned: %d\r\n", bytes_sent);
                         return false;
                     } else
                         printf("sent %d bytes\r\n", bytes_sent);
       
                     bytes_to_send -= bytes_sent;
                 }
       
                 printf("Complete message sent\r\n");
       
                 return true;
             }
       
             bool receive_http_response()
             {
                 char buffer[MAX_MESSAGE_RECEIVED_LENGTH];
                 int remaining_bytes = MAX_MESSAGE_RECEIVED_LENGTH;
                 int received_bytes = 0;
       
                 /* loop until there is nothing received or we've ran out of buffer space */
                 nsapi_size_or_error_t result = remaining_bytes;
                 while (result > 0 && remaining_bytes > 0) {
                     nsapi_size_or_error_t result = _socket.recv(buffer + received_bytes, remaining_bytes);
                     if (result < 0) {
                         printf("Error! _socket.recv() returned: %d\r\n", result);
                         return false;
                     }
       
                     received_bytes += result;
                     remaining_bytes -= result;
                 }
       
                 printf("received %d bytes:\r\n%.*s\r\n\r\n", received_bytes, strstr(buffer, "\n") - buffer, buffer);
       
                 return true;
             }
       
             void print_network_info()
             {
                 SocketAddress a;
                 _net->get_ip_address(&a);
                 printf("IP address: %s\r\n", a.get_ip_address() ? a.get_ip_address() : "None");
                 _net->get_netmask(&a);
                 printf("Netmask: %s\r\n", a.get_ip_address() ? a.get_ip_address() : "None");
                 _net->get_gateway(&a);
                 printf("Gateway: %s\r\n", a.get_ip_address() ? a.get_ip_address() : "None");
             }
       
         private:
             NetworkInterface *_net;
             TCPSocket _socket;
         };
       
         int main() {
             printf("\r\nStarting socket demo\r\n\r\n");
       
         #ifdef MBED_CONF_MBED_TRACE_ENABLE
             mbed_trace_init();
         #endif
       
             SocketDemo *example = new SocketDemo();
             MBED_ASSERT(example);
             example->run();
       
             return 0;
         }


#. Revise the "HOST_IP" in :file:`mbed_app.json` to the IP of your PC.  For example, PC's IP is 192.168.1.3:

   line 5:

   .. code-block:: c++
   
      "value": "\"192.168.1.3\""

   .. code-block:: c++

      {
          "config": {
              "hostname": {
                  "help": "The demo will try to connect to this web address on port 80 (or port 443 when using tls).",
                  "value": "\"HOST_IP\""
              },
              "use-tls-socket": {
                  "value": false
              }
          },

      }

#. Change the SSID and PASSWORD below to match the ones of your WiFi access point in :file:`mbed_app.json`. 

   .. code-block:: c++

      {
          "target_overrides": {
              "*": {
                  "nsapi.default-wifi-security": "WPA_WPA2",
                  "nsapi.default-wifi-ssid": "\"SSID\"",
                  "nsapi.default-wifi-password": "\"PASSWORD\"",
                  "platform.stdio-baud-rate": 9600,
                  "mbed-trace.enable": false,
                  "mbed-trace.max-level": "TRACE_LEVEL_DEBUG",
                  "rtos.main-thread-stack-size": 8192
              },
          }
      }


#. In :file:`mbed_app.json`, 
   add the following **"B_L4S5I_IOT01A":** section after the **"*":** in **"target_overrides"**:

   .. code-block:: c++

        {
            "target_overrides": {
                "*": {
                    "nsapi.default-wifi-security": "WPA_WPA2",
                    "nsapi.default-wifi-ssid": "\"SSID\"",
                    "nsapi.default-wifi-password": "\"PASSWORD\"",
                    "platform.stdio-baud-rate": 9600,
                    "mbed-trace.enable": false,
                    "mbed-trace.max-level": "TRACE_LEVEL_DEBUG",
                    "rtos.main-thread-stack-size": 8192
                },
                "B_L4S5I_IOT01A": {
                    "target.components_add": ["ism43362"],
                    "ism43362.provide-default": true,
                    "target.network-default-interface-type": "WIFI",
                    "target.macros_add" : ["MBEDTLS_SHA1_C"]
                }
            }
        }

   .. container:: warning

         Be ware of the config format in JSON. The string value is enclosed by :hl:`"\\"` and :hl:`\\""`.

         Change the SSID and PASSWORD below to match the ones of your WiFi access point.

#. Compile and run the program.

#. Screenshot the information of this WiFi demo on the screen. (It may take a while).

#. Push the main.cc code to your GitHub repo.

MQTT Broker and Client
=========================
.. container:: instruct

      In this part, we implement a MQTT server to deliver informations between B_L4S5I_IOT01A and a Ubuntu PC.

.. container:: instruct

      What is MQTT?

      MQTT (Message Queue Telemetry Transport) is a simple and ‘lightweight’ way for internet-connected devices to send each other messages. Devices using MQTT communicate by publishing data to topics. MQTT devices subscribe to a topic, and when data is published to that topic it is pushed to all the subscribers.

      For more details, please visit `What is MQTT and How It Works <https://www.youtube.com/watch?v=EIxdz-2rhLs>`__.

      The example we used is to publish message by pressing the button on B_L4S5I_IOT01A, and receive it from python client on pc.

MQTT Broker 
-------------------------------

#. Install the MQTT broker service.

   .. container:: instruct

      What is MQTT broker?

      Mosquitto is an open source (EPL/EDL licensed) message broker that implements the MQTT protocol versions 3.1 and 3.1.1. Mosquitto is lightweight and is suitable for use on all devices from low power single board computers to full servers.

   #. For Windows:

      #. Download and install `mosquitto-2.0.14-install-windows-x64.exe <https://mosquitto.org/files/binary/win64/mosquitto-2.0.14-install-windows-x64.exe>`__

	 If you don't need to install "Visual Studio Runtime", please uncheck the selection.
	 Also we probably don't need to install Windows Service, please uncheck the "Service" selection.

      #. Open network port 1883 for Mosquitto services for Windows firewall (defender)

         Please follow `設定Window防火牆 MQTT 1883 <https://jimirobot.tw/esp32-mosquitto-windows-mqtt-tutorial/#3_設定_window_防火牆>`__ 
	 or `Setup MQTT 1883 port for Windows <https://bytesofgigabytes.com/networking/how-to-open-port-in-windows/>`__

	 #. Press Windows+R

         #. Type firewall.cpl in Open field and Click OK.

	 #. Click on **Advanced settings**

	 #. First click on **Inbound Rules** and then Click on **New Rule**

	 #. To open port, Please select Rule Type as **Port** and click **Next**.

	 #. Select TCP. Set "**Specify local ports**" as 1883. Click on Next.

	 #. Select Allow the connection and click Next

	 #. Check "Private" and click on Next

	 #. Enter the name for opening port rule, e.g., "MQTT Service Input Port".

	 #. Repeat above again for **Outbound Rules** 

	 #. First click on **Outbound Rules** and then Click on **New Rule**

	 #. To open port, Please select Rule Type as **Port** and click **Next**.

	 #. Select TCP. Set "**Specify local ports**" as 1883. Click on Next.

	 #. Select Allow the connection and click Next

	 #. Check "Private" and click on Next

	 #. Enter the name for opening port rule, e.g., "MQTT Service Output Port".

      #. Edit :file:`mosquitto.conf` in :file:`C:\\Program  Files\\mosquitto`.

         #. Search for "# listener port-number" add the following line:

            .. code-block:: none
           
               listener 1883

         #. Search for "# allow_anonymous false" add the following line:

            .. code-block:: none
           
               allow_anonymous true


      #. Start a Git Bash and start Mosquitto service

         We can start Mosquitto manually as follows. To stop the service, simply type :hotkey:`Ctrl+C`.

	 Go to the Mosquitto directory:

         :cmd_host:`$ cd /c/Program\ Files/mosquitto`
	 
	 Start Mosquitto:

         :cmd_host:`$ ./mosquitto.exe -c mosquitto.conf -v`

      #. Test Mosquitto service

	 #. Start a Git Bash and use a client to subscribe to a topic "test"
       
            Replace the following "HOST IP" with your actual PC server IP.

   	    Go to the Mosquitto directory:

            :cmd_host:`$ cd /c/Program\ Files/mosquitto`
	 
	    Subscribe:
            
	    :cmd_host:`$ ./mosquitto_sub.exe -h "HOST IP" -t test`

	 #. Start another Git Bash and publish a message "Hello" to the topic "test"
       
            Replace the following "HOST IP" with your actual PC server IP.

   	    Go to the Mosquitto directory:

            :cmd_host:`$ cd /c/Program\ Files/mosquitto`
	 
	    Publish:
            
	    :cmd_host:`$ ./mosquitto_pub.exe -h "HOST IP" -t test -m "Hello”`

	    The "Hello" message should show at the first terminal.
	    If the message did not show up, you may try to publish again with another message.
	    You should also see connection messages at the Mosquitto service terminal.

   #. For Mac OS:

      #. Install Brew:
         `Homebrew <https://brew.sh/index_zh-tw>`__
      
         :cmd_host:`$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

      #. Install Mosquitto

         :cmd_host:`$ brew install mosquitto`

      #. Edit :file:`/usr/local/etc/mosquitto/mosquitto.conf`

         #. Search for "# listener port-number" add the following line:

            .. code-block:: none
           
               listener 1883

         #. Search for "#allow_anonymous false" add the following line:

            .. code-block:: none
           
               allow_anonymous true

      #. By default, Mac OS does not start a network firewall.
         If you setup a firewall, please allow port 1883 in the configuration.
	 Please refer to `the tutorial <https://www.lifewire.com/open-a-port-on-a-routers-or-computers-firewall-5072435>`__
	 for opening a port in Mac OS (scroll down to skip Windows part):

      #. Start a Terminal and start Mosquitto service

         We can start Mosquitto manually as follows. To stop the service, simply type :hotkey:`Ctrl+C`.

         :cmd_host:`$ /usr/local/opt/mosquitto/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf`

      #. Test Mosquitto service
       
         Replace the following "HOST IP" with your actual PC server IP.

	 #. Start a Terminal app and use a client to subscribe to a topic "test"
            
	    :cmd_host:`$ mosquitto_sub -h "HOST IP" -t test`

	 #. Start another Terminal app and publish a message "Hello" to the topic "test"
            
	    :cmd_host:`$ mosquitto_pub -h "HOST IP" -t test -m "Hello”`

	    The "Hello" message should show at the first terminal.
	    If the message did not show up, you may try to publish again with another message.
	    You should also see connection messages at the Mosquitto service terminal.

mbed MQTT Client
-------------------------------

#. Start a Terminal app in Mac OS or Git Bash in Windows.

#. Install MQTT libraries for Python.

   :cmd_host:`$ python3 -m pip install paho-mqtt`

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *10_2_MQTT* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".
   
#. Import ISM43362 library for WiFi.

   #. Click **+** in the Library tab under program source.

   #. Fill in "https://github.com/ARMmbed/wifi-ism43362"
      And click "Next"

   #. Select "Master" branch and click "Finish"
   
#. Import MQTT library 

   #. Click **+** in the Library tab under program source.

   #. Fill in "https://gitlab.larc-nthu.net/ee2405_2022/paho_mqtt.git"
      And click "Next"

   #. Select "Master" branch and click "Finish"


#. Create a file :file:`mbed_app.json`.

   .. container:: warning

      Be ware of the config format in JSON. The string value is enclosed by :hl:`"\\"` and :hl:`\\""`.

      Please change the SSID and PASSWORD below to match the ones of your WiFi access point.

   .. _mbed_app.json:

      .. code-block:: c++
         :linenos: inline
 
         {
             "config": {
             "wifi-ssid": {
                     "help": "WiFi SSID",
                     "value": "\"SSID\""
             },
             "wifi-password": {
                     "help": "WiFi Password",
                     "value": "\"PASSWORD\""
             }
             },
             "target_overrides": {
                 "B_L4S5I_IOT01A": {
                     "target.components_add": ["ism43362"],
                     "ism43362.provide-default": true,
                     "target.network-default-interface-type": "WIFI",
                     "target.macros_add" : ["MBEDTLS_SHA1_C"]
                 }
             }
         }

#. Please revise the codes in :file:`main.cpp` as follows.

   This is a mbed program acts as a MQTT client to publish messages from B_L4S5I_IOT01A.

   Change the following :hl:`host` string in :file:`main.cpp` to your PC IP address, which run the Mosquitto server.

   .. code-block:: c++

      //TODO: revise host to your IP
      const char* host = "Your IP";

   The :file:`main.cpp` mbed program:

   .. code-block:: c++
        :linenos: inline

        #include "mbed.h"
        #include "MQTTNetwork.h"
        #include "MQTTmbed.h"
        #include "MQTTClient.h"

        // GLOBAL VARIABLES
        WiFiInterface *wifi;
        InterruptIn btn2(BUTTON1);
        //InterruptIn btn3(SW3);
        volatile int message_num = 0;
        volatile int arrivedcount = 0;
        volatile bool closed = false;

        const char* topic = "Mbed";

        Thread mqtt_thread(osPriorityHigh);
        EventQueue mqtt_queue;

        void messageArrived(MQTT::MessageData& md) {
            MQTT::Message &message = md.message;
            char msg[300];
            sprintf(msg, "Message arrived: QoS%d, retained %d, dup %d, packetID %d\r\n", message.qos, message.retained, message.dup, message.id);
            printf(msg);
            ThisThread::sleep_for(1000ms);
            char payload[300];
            sprintf(payload, "Payload %.*s\r\n", message.payloadlen, (char*)message.payload);
            printf(payload);
            ++arrivedcount;
        }

        void publish_message(MQTT::Client<MQTTNetwork, Countdown>* client) {
            message_num++;
            MQTT::Message message;
            char buff[100];
            sprintf(buff, "QoS0 Hello, Python! #%d", message_num);
            message.qos = MQTT::QOS0;
            message.retained = false;
            message.dup = false;
            message.payload = (void*) buff;
            message.payloadlen = strlen(buff) + 1;
            int rc = client->publish(topic, message);

            printf("rc:  %d\r\n", rc);
            printf("Puslish message: %s\r\n", buff);
        }

        void close_mqtt() {
            closed = true;
        }

        int main() {

            wifi = WiFiInterface::get_default_instance();
            if (!wifi) {
                    printf("ERROR: No WiFiInterface found.\r\n");
                    return -1;
            }


            printf("\nConnecting to %s...\r\n", MBED_CONF_APP_WIFI_SSID);
            int ret = wifi->connect(MBED_CONF_APP_WIFI_SSID, MBED_CONF_APP_WIFI_PASSWORD, NSAPI_SECURITY_WPA_WPA2);
            if (ret != 0) {
                    printf("\nConnection error: %d\r\n", ret);
                    return -1;
            }


            NetworkInterface* net = wifi;
            MQTTNetwork mqttNetwork(net);
            MQTT::Client<MQTTNetwork, Countdown> client(mqttNetwork);

            //TODO: revise host to your IP
            const char* host = "192.168.1.150";
	    const int port=1883;
            printf("Connecting to TCP network...\r\n");
            printf("address is %s/%d\r\n", host, port); 

            int rc = mqttNetwork.connect(host, port);//(host, 1883);
            if (rc != 0) {
                    printf("Connection error.");
                    return -1;
            }
            printf("Successfully connected!\r\n");

            MQTTPacket_connectData data = MQTTPacket_connectData_initializer;
            data.MQTTVersion = 3;
            data.clientID.cstring = "Mbed";

            if ((rc = client.connect(data)) != 0){
                    printf("Fail to connect MQTT\r\n");
            }
            if (client.subscribe(topic, MQTT::QOS0, messageArrived) != 0){
                    printf("Fail to subscribe\r\n");
            }

            mqtt_thread.start(callback(&mqtt_queue, &EventQueue::dispatch_forever));
            btn2.rise(mqtt_queue.event(&publish_message, &client));
            //btn3.rise(&close_mqtt);

            int num = 0;
            while (num != 5) {
                    client.yield(100);
                    ++num;
            }

            while (1) {
                    if (closed) break;
                    client.yield(500);
                    ThisThread::sleep_for(500ms);
            }

            printf("Ready to close MQTT Network......\n");

            if ((rc = client.unsubscribe(topic)) != 0) {
                    printf("Failed: rc from unsubscribe was %d\n", rc);
            }
            if ((rc = client.disconnect()) != 0) {
            printf("Failed: rc from disconnect was %d\n", rc);
            }

            mqttNetwork.disconnect();
            printf("Successfully closed!\n");

            return 0;
        }


Python MQTT Client
-------------------------------

This is a python program acts as another MQTT client to receive messages from B_L4S5I_IOT01A.

#. Please edit and revise the codes in :file:`mqtt_client.py` as follows. 

   Change the following :hl:`host` string in :file:`mqtt_client.py` to your PC IP address.

   .. code-block:: python

      # TODO: revise host to your IP
      host = "Your IP"

   The :file:`mqtt_client.py` Python program:

   .. code-block:: python
        :linenos: inline

        import paho.mqtt.client as paho
        import time

        # https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

        # MQTT broker hosted on local machine
        mqttc = paho.Client()

        # Settings for connection
        # TODO: revise host to your IP
        host = "192.168.1.150"
        topic = "Mbed"

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

        # Publish messages from Python
        num = 0
        while num != 5:
            ret = mqttc.publish(topic, "Message from Python!\n", qos=0)
            if (ret[0] != 0):
                    print("Publish failed")
            mqttc.loop()
            time.sleep(1.5)
            num += 1

        # Loop forever, receiving messages
        mqttc.loop_forever()

Test MQTT Client and Server
-------------------------------
#. Start your Mosquitto service.

   .. class:: terminal
   
   ::

     1643685626: mosquitto version 2.0.14 starting
     1643685626: Config loaded from /usr/local/etc/mosquitto/mosquitto.conf.
     1643685626: Opening ipv6 listen socket on port 1883.
     1643685626: Opening ipv4 listen socket on port 1883.
     1643685626: mosquitto version 2.0.14 running
     1643685629: New connection from 192.168.50.192:65147 on port 1883.
     1643685629: New client connected from 192.168.50.192:65147 as auto-6E6EAC05-2C6E-16DC-CBB0-36F045DC68E5 (p2, c1, k60).
     1643685994: New connection from 192.168.50.56:14645 on port 1883.
     1643685994: New client connected from 192.168.50.56:14645 as Mbed (p1, c1, k60).
     
#. Compile and run the mbed program.

#. Run the Python script.

#. Mbed should receive several messages from Python client. 

   .. class:: terminal
   
   ::

     Connecting to SSID...
     Connecting to TCP network...
     address is 192.168.50.192/1883
     Successfully connected!
     Message arrived: QoS0, retained 0, dup 0, packetID 816
     Payload Message from Python!

     Message arrived: QoS0, retained 0, dup 0, packetID 816
     Payload Message from Python!
     
     Message arrived: QoS0, retained 0, dup 0, packetID 816
     Payload Message from Python!
          
     Message arrived: QoS0, retained 0, dup 0, packetID 816
     Payload Message from Python!
     
     Message arrived: QoS0, retained 0, dup 0, packetID 816
     Payload Message from Python!
     
     rc:  0
     Puslish message: QoS0 Hello, Python! #1
     Message arrived: QoS0, retained 0, dup 0, packetID 816
     Payload QoS0 Hello, Python! #1

#. Press the user button on B_L4S5I_IOT01A, you should see the messages received at the Python client.

   .. class:: terminal
   
   ::

     $ python3 mqtt_client.py
     Connecting to 192.168.50.192/Mbed
     Connected rc: 0
     Subscribed OK
     [Received] Topic: Mbed, Message: b'Message from Python!\n'

     [Received] Topic: Mbed, Message: b'Message from Python!\n'
     
     [Received] Topic: Mbed, Message: b'Message from Python!\n'
     
     [Received] Topic: Mbed, Message: b'Message from Python!\n'
     
     [Received] Topic: Mbed, Message: b'Message from Python!\n'
     
     [Received] Topic: Mbed, Message: b'QoS0 Hello, Python! #1\x00'

#. Push the codes to your GitHub repo.

********************
Demo and Checkpoints
********************

#. You need to know how to use ISM43362 on B-L4S5I-IOT01A to connect WiFi.

#. You need to know what is MQTT and how it works.

#. Use the resource from Lab 8, revise the project to send the data of accelerometer from B-L4S5I-IOT01A to pc host every 0.5 second using WiFi and MQTT.

#. Show your git remote repository.

***
FAQ
***

#. **No network interface found** `screenshot <labs/img/Wifi_MQTT/No_WiFi_interface.png>`__

   This indicates that there is something wrong in the setting of mbed_app.json.

   #. Double check mbed_app.json as described above. It must include a session for **"target_overrides": {"B_L4S5I_IOT01A": {...}}**.

   #. Check mbed_app.json is in the source directory 

#. **_net->connect() returned: -3011** `screenshot <labs/img/Wifi_MQTT/-3011.png>`__

   This means that your B-L4S5I-IOT01A cannot connect to a WiFi hotspot or router.

   #. SSID and PASSWORD in mbed_app.json are not correct.

   #. Your hotspot signal is too weak or not stable. Please try another one.

   #. Your hotspot frequency band may be set to 5 GHz by default. Please change it to 2.4 GHz or try others.

   #. Too many devices are using the 2.4 GHz frequency band around you. There are too much noise for WiFi signal band.
      You can see the list in your WiFi hotspot list in Windows or Mac.

#. **_socket->connect() returned: -3012** `screenshot <labs/img/Wifi_MQTT/-3012.png>`__

   This means that your B-L4S5I-IOT01A has connected to WiFi, but it cannot access to PC services (e.g., web server).
   Make sure your B-L4S5I-IOT01A and Ubuntu are under the same subnet. And check if the web or mqtt server is running.

**************
Reference List
**************

#. `WIFI module ISM43362 Firmware Update <https://github.com/ARMmbed/wifi-ism43362>`__

#. `Mbed MQTT Example <https://os.mbed.com/teams/Cloud-Hackathon/wiki/MQTT-Python-Broker-with-Mbed-Client>`__

#. `Python MQTT Client <https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client>`__

Update the firmware (optional)
==============================
.. container:: warning

   Do **NOT** perform this part unless consulting with a TA.
   
   Because the firmware update procedures are complicated, you should come back to update the firmware only if you confront the related error.
   
   It's recommended to skip this part, try `Connect B-L4S5I-IOT01A to WiFi`_ section directly.
   

.. container:: instruct

   We need to update the firmware on a Windows machine.
   If your notebook uses macOS or Linux, please use the desktop at your seat for this update.

   Do **NOT** connect your mbed board and start VMware.

#. Download firmware update tool.

   Firmware download link: `Lab10_firmware_update <labs/doc/mbed10/Lab10_firmware_update.zip>`__

#. Unzip the firmware update tool.

#. Move the whole sub-directory "STMicroelectronics", i.e. "C:\\Users\\USER\\Downloads\\Lab10_firmware_update\\STMicroelectronics" into "C:\\Program Files (x86)\\".

**Install STM USB driver on your computer**

#. Open the folder "C:\\Program Files (x86)\\STMicroelectronics\\STM32 ST-LINK Utility\\ST-LINK_USB_V2_1_Driver".

#. Run :file:`stlink_winusb_install.bat`. Confirm the permission when asked by the Windows. 

#. Installation wizard will pops up. `Step 1 <labs/img/Wifi_MQTT/Device_Driver_Installation.png>`__

#. Continuously press 'Next' to complete the routines. `Step 2 <labs/img/Wifi_MQTT/Completing_Device_Driver_Installation.png>`__

**Install a new ST_LINK firmware**

#. Open the folder "C:\\Program Files (x86)\\STMicroelectronics\\STM32 ST-LINK Utility\\ST-LINK Utility".

#. Run :file:`STM32 ST-LINK Utility.exe`. The GUI of the utility will pops up: `Step 0 <labs/img/Wifi_MQTT/STM32_ST-Link_Utility_Step_0.png>`__

#. Plug in your B_L4S5I_IOT01A. Press the plug icon in the GUI to make your computer connected with B_L4S5I_IOT01A. `Step 1 <labs/img/Wifi_MQTT/STM32_ST-Link_Utility_Step_1.png>`__

#. Click ST_LINK/Firmware update. `Step 2 <labs/img/Wifi_MQTT/STM32_ST-Link_Utility_Step_2.png>`__

#. Click "Device Connect" `Step 3 <labs/img/Wifi_MQTT/STM32_ST-Link_Utility_Step_3.png>`__

#. Click "YES" to confirm the update. `Step 4 <labs/img/Wifi_MQTT/STM32_ST-Link_Utility_Step_4.png>`__

#. After the update is successful, press the reset button on B_L4S5I_IOT01A. `Step 5 <labs/img/Wifi_MQTT/STM32_ST-Link_Utility_Step_5.png>`__

**Update WiFi firmware**

#. Open the folder "C:\\Users\\USER\\Downloads\\Lab10_firmware_update\\en.inventek_fw_updater\\bin".

#. Run :file:`STM32 ST-LINK Utility.exe`. Windows command line (cmd) will pops up and execute the file. `Step 0 <labs/img/Wifi_MQTT/cmd_exe_Step_0_.png>`__

#. The utility should run automatically after your click it. 

   If "No ST_LINK" / "No target" message shows up, please make sure that you
   didn't start VMware and connect the mbed board.
   In this case, please terminate VMWare and try to press and hold the reset button when you execute :file:`STM32 ST-LINK
   Utility.exe` again. After you release the reset button, the screen should show messages like Step_1: `Step 1 <labs/img/Wifi_MQTT/cmd_exe_Step_1_.png>`__

#. It will automatically ended after downloading and verifying all 10 firmware sectors. `Step 2 <labs/img/Wifi_MQTT/cmd_exe_Step_2_.png>`__

