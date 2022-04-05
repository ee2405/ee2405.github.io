mbed Lab 8 Machine Learning on mbed 
##################################################
:Date:    2022-03-30 15:00
:Tags:    Labs
:Summary: Use TensorFlow and deep learning models to classify the gesture on an mbed board.

.. sectnum::
   :depth: 3

.. include:: ../LARC_def.txt

.. contents::

.. container:: tasklist

   The goal of this lab is to learn:

   #. the flow of a deep learning framework
   #. inference of a trained model on an mbed board

****************
Lab Due
****************

**Mar. 30, 2022**

****************
Lab Introduction
****************
In this lab, we will introduce the workflow of deep learning for gesture
classification on B_L4S5I_IOT01A. The deep learning model is trained and tested
on Google's Colab service with TensorFlow. Then the model will be transferred
to B_L4S5I_IOT01A to perform inference with accelerometer data.

**************
Equipment List
**************

#. B_L4S5I_IOT01A * 1

**************************
Deep Learning Introduction
**************************

Deep learning neural network (DNN) algorithm train a model of multi-layer
convolutions to extract features on a large-scale data set (e.g., for images or
speeches).  Several DNN models have been shown to out-perform human. And there
could be several new applications in different domains with DNN such as
autonomous car, manufacturing, agriculture, etc.  Usually, there are 4 phases
in applying DNN algorithm: data collection, data labeling, model training, and
model deployment.

#. In :file:`data collection phase`,
   we have to collect relevant data for our application.
   Normally the quality of collected data has the huge impact on the
   performance for the task, and also the amount of data should be large
   enough. Otherwise, the model will not be effective.

#. In :file:`data labeling phase`, we have to label (tag) the collected data
   to denote the class of data. For example, to recognize different kinds of
   birds, we need to assign the correct name for each bird photo.

#. In :file:`model training phase`, we write a DNN model (usually in Python)
   and feed the collected data (with labels) to a DNN framework (TensorFlow)
   to train the model. Usually part of the data set is used as test data
   (to test the model independently). The remaining data will again be
   partitioned into two parts: training set and validation set. The training
   set is used to train the model and validation set is used to estimate the
   performance. Training and validation sets may be mixed,
   e.g., in cross-validation methods.

#. In :file:`model deployment phase`, we transfer the trained DNN model
   to the machine (B_L4S5I_IOT01A) in actual application environment
   for a final test and tuning.

Note: the description above is based on the supervised deep learning model,
which means you need to put labeled data to train the model. On the other hand,
using non-labeled data to train the model is unsupervised deep learning model
(e.g., clustering).

**In this lab, you will collect accelerometer data and prepare data for training
a classifier for gestures. And the model will be deployed on B_L4S5I_IOT01A.**

***************
Lab Description
***************

Lecture Notes
=============

- Chapter 9: Deep Neural Networks `ch9_dnn.pdf <notes/ch9_dnn.pdf>`__

Data Collection and Labeling
=============================================

.. container:: instruct

   You may skip this part the first time you do this lab.
   We have prepared two gestures' data and you can start the training process
   in the Colab (next section) to get familar with the overall process.

.. container:: instruct
    
   The purpose of this data collection is to get a sequence of accelerometer data 
   that are generated from similar gestures. We will put the data in a text format
   ("gesture_<label>.txt"), which will be eventually copied to "data/raw/gesture_<label>.txt" in the DNN
   training directory to be uploaded to your GitHub repo.

   To use the following code to collect data, it is recommended that you record each
   gesture at least 200 times. As for **negative** category of label, you
   should collect the gestures that don't belong to the other labels.

   We have collected a few labeled data for your reference:
   `gesture_ring.txt <labs/doc/ML_on_K66F/gesture_ring.txt>`__,
   `gesture_slope.txt <labs/doc/ML_on_K66F/gesture_slope.txt>`__,
   and `gesture_negative.txt <labs/doc/ML_on_K66F/gesture_negative.txt>`__.
   (You don't need to download them here, since we will copy from another remote repo
   in the next section.)

   The ring gesture is like `this <labs/img/ML_on_K66F/gesture_ring.png>`__,
   and the slope gesture is like `this <labs/img/ML_on_K66F/gesture_slope.png>`__.

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *8_1_data_collect* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".
   
#. Import BSP library for running accelerometer.

   .. container:: instruct

      The imported BSP (Board Support Package) library has drivers for STMicro B_L4S5I_IOT01A boards,
      which enable access to its sensors. In this part, we use the accelerometers. You are encouraged to 
      try other sensors. Please refer to `DISCO_L475VG_IOT01-Sensors-BSP <https://os.mbed.com/teams/ST/code/DISCO_L475VG_IOT01-Sensors-BSP//file/f49325f1e644/main.cpp/>`__ for more examples.


   #. Click **+** in the Library tab under program source.

   #. Fill in `https://gitlab.larc-nthu.net/ee2405_2022/bsp-b-l475e-iot01.git`
      And click "Next"

   #. Select "main" branch and click "Finish"

   #. Delete the following file:
      :file:`bsp-b-l475e-iot01/Drivers/BSP/B-L475E-IOT01/stm32l475e_iot01_qspi.*`
      "*" means any file extension.

#. mbed B_L4S5I_IOT01A part:

   #. Edit :file:`main.cpp`

      .. code-block:: c++
         :linenos: inline

         #include "mbed.h"
         #include "stm32l475e_iot01_accelero.h"

         InterruptIn btnRecord(BUTTON1);
         EventQueue queue(32 * EVENTS_EVENT_SIZE);
         Thread t;

         int16_t pDataXYZ[3] = {0};
         int idR[32] = {0};
         int indexR = 0;

         void record(void) {
            BSP_ACCELERO_AccGetXYZ(pDataXYZ);
            printf("%d, %d, %d\n", pDataXYZ[0], pDataXYZ[1], pDataXYZ[2]);
         }

         void startRecord(void) {
            printf("---start---\n");
            idR[indexR++] = queue.call_every(1ms, record);
            indexR = indexR % 32;
         }

         void stopRecord(void) {
            printf("---stop---\n");
            for (auto &i : idR)
               queue.cancel(i);
         }

         int main() {
            printf("Start accelerometer init\n");
            BSP_ACCELERO_Init();
            t.start(callback(&queue, &EventQueue::dispatch_forever));
            btnRecord.fall(queue.event(startRecord));
            btnRecord.rise(queue.event(stopRecord));
         }

   #. Compile and run the program.

   #. If the accelerometer values are appearing on the outputs when you press and hold USER button, release the User button 
      to stop the measurement. This would show that the program works.

   #. Quit Mbed Studio, since we will use Python to collect the data from the same UART port.

#. Python program to collect data from mbed:

   #. Edit :file:`data_collect.py`.
      Replace the following "serdev" with your UART device in your OS (i.e. COM7 or /dev/cu.usbmodem14603).

      .. code-block:: python
         :linenos: inline

         import serial
         import sys
         import time

         serdev = '/dev/ttyACM0'
         s = serial.Serial(serdev)

         data = []
         data_new = []
         while True:
           try:
             line = s.readline().decode()
             if '---start---' in line:
               print("---start---")
               data_new.clear()
             elif '---stop---' in line:
               print("---stop---")
               if len(data_new) > 0:
                 print("Data saved:")
                 print(data_new)
                 data.append(data_new.copy())
                 data_new.clear()
               print("Data Num =", len(data))
             else:
               print(line, end="")
               data_new.append(line)
           except KeyboardInterrupt:
             filename = "gesture_"+str(time.strftime("%Y%m%d%H%M%S"))+".txt"
             with open(filename, "w") as f:
               for lines in data:
                 f.write("-,-,-\n")
                 for line in lines:
                   f.write(line)
             print("Exiting...")
             print("Save file in", filename)
             s.close()
             sys.exit()

#. Start a Terminal app and go to the directory for the :file:`data_collect.py`.
   For example, 

   :cmd_host:`$ cd "Mbed Programs"/8_1_data_collect`

#. Execute the python script 

   :cmd_host:`$ python3 data_collect.py`

   Note that this program only works in a Terminal. Do not run this program in VS Code.

#. Press and hold the USER Button on mbed to record the gesture.

#. Release the USER button to stop recording.
   If you release USER Button but the it is still recording, just press the USER_BUTTON
   several times until it stops.

#. Press 'Ctrl + C' in terminal to terminate the program, and the program will give
   you a text file starting with :file:`gesture_`.

#. Rename the file to :file:`gesture_<label>.txt`. In next section, we will copy it to folder
   :file:`mbed08/data/raw`.

   Note: :file:`<time>` is like :file:`202004081520`;
   :file:`<label>` is like :file:`ring`.

#. Push your codes to a GitHub repo.

Model Training 
====================

In this part, we will feed the labeled data to train a model that classifies
gesture. We will use the data collected in the previous parts (for the first run, 
you may use our collected data sets) in `Google Colab <https://colab.research.google.com/#>`__.

Create a GitHub repo
--------------------

#. Please login github.com with your account.

#. Select "Import repository" (with the **+** at top-right besides your profile).

   #. Fill in URL: "https://gitlab.larc-nthu.net/ee2405_2022/gesture-dnn.git".

   #. Fill in "mbed08" as the repo name. 

   #. Set the repo as a "Public" repo.

   After the importing completed, you will have a repo at "git@github.com:<Your Git ID>/mbed08.git".
   Replace above <Your Git ID> with your GitHub ID or copy from GitHub "Code" tab.
   It will includes all source codes and example data for DNN training.
   For the first time to run the flow, you may skip the following step to proceed to Colab training.

Modify the repo
--------------------

Please skip this step for the first run to get familiar of the flow.

In the following, we show how to clone/modify/push the repo to add more gesture data.
Assume we want to add :file:`gesture_new.txt` and modify :file:`config.py` to include the new 
gesture data in the following.

#. Start a Terminal app or a Git Bash in Windows.

   :cmd_host:`$ cd ~/Mbed\ Programs`

   :cmd_host:`$ git clone git@github.com:<Your Git ID>/mbed08.git`

   Now we have cloned the mbed08 repo at :file:`~/Mbed\ Programs/mbed08` locally.

#. Copy :file:`gesture_new.txt` into :file:`~/Mbed\ Programs/mbed08/data/raw` 

   You may use Finder or File Explorer for this. In the following, we show a command line:

   :cmd_host:`$ cp ~/Mbed\ Programs/8_1_data_collect/gesture_new.txt ~/Mbed\ Programs/mbed08/data/raw`

#. Edit :file:`config.py` 

   You may use Finder or File Explorer for this. In the following, we show a command line:

   :cmd_host:`$ code ~/Mbed\ Programs/mbed08/src/model_train/config.py`

   Change the line with "labels =  ["ring", "slope", "negative"]".
   For example, "labels =  ["ring", "slope", "new", "negative"]".

   .. container:: instruct

      You can tune some parameters in the :file:`config.py`

      .. code-block:: python
         :linenos: inline

         DATA_NAME = "accel_ms2_xyz"
         LABEL_NAME = "gesture"

         # label name (you should keep "negative" in the end of the list)
         labels = ["ring", "slope", "negative"]

         # data split configuration
         # note that train_ratio + valid_ratio + test_ratio = 1
         train_ratio = 0.6
         valid_ratio = 0.3
         data_split_random_seed = 30

         # model configuration
         model = "CNN"
         seq_length = 64 # the input size of the model
         epochs = 50
         steps_per_epoch =1000
         batch_size = 64

#. In a Terminal, push new :file:`gesture_new.txt` and modified :file:`config.py` to your GitHub mbed08.

   :cmd_host:`$ cd ~/Mbed\ Programs/mbed08`

   :cmd_host:`$ git add data/raw/gesture_new.txt`

   :cmd_host:`$ git add src/model_train/config.py`

   :cmd_host:`$ git commit -m "add new training gesture"`

   :cmd_host:`$ git push`

   Please go to GitHub.com to double check if the files are updated.
   If so, you may proceed to the Colab training part.


Start a Colab script for training
----------------------------------

#. Open :hl:`https://colab.research.google.com/github/<Your Git ID>/mbed08/blob/master/src/model_train/train_magic_wand_model.ipynb` in the browser.

   Replace :file:`<Your Git ID>` is your GitHub user name.

#. Fill in :file:`"REPO_URL"` and :file:`"REPO_NAME"` in the first box at Google Colab to your github name and repo.

   .. code-block:: python
      :linenos: inline

      os.environ['REPO_URL'] = "https://github.com/ee2405/mbed08.git"
      os.environ['REPO_NAME'] = "mbed08"

#. Press the play button beside each of the cell to run the code in each cell of colab.

#. Copy and save from the last box for the following part. 
   It should looks like the following texts:

   .. class:: terminal

   ::

     unsigned char _content_mbed08_model_model_tflite[] = {
       0x1c, 0x00, 0x00, 0x00, 0x54, 0x46, 0x4c, 0x33, 0x14, 0x00, 0x20, 0x00,
       0x04, 0x00, 0x08, 0x00, 0x0c, 0x00, 0x10, 0x00, 0x14, 0x00, 0x00, 0x00,
       0x18, 0x00, 0x1c, 0x00, 0x14, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00,
       ...
     };
     unsigned int _content_mbed08_model_model_tflite_len = 12988;

Model Deployment 
======================

Following steps are meant to obtain a quantized version of NN that will be
deployable on an Arm Cortex-M microcontroller.  In the training above, the data
type is 32-bit floating point, but FP operation is inefficient on an embedded
system, so wee will quantize the weight to 8-bit integer and generate C++ files
that contains the inference of the network.

Now we create a new Mbed program and add a Tensorflow Lite library for inferencing. (BSP library is also needed)

#. Create a new program.

#. Open the **File** menu and select **New Program....**

#. Select "empty Mbed OS program" under **MBED OS 6**
   Enter *8_2_model_deploy* for Program name.
   Check "Make this the active program" (default).
   Under "**Mbed OS Location**", check "Link to an existing shared Mbed OS instance" 
   and select "~/Mbed Programs/mbed01/mbed-os/". This will reuse Mbed OS in mbed01/.
   Click "Add Program".

#. Copy all .cpp and .h files from https://gitlab.larc-nthu.net/ee2405_2022/code-example/-/tree/master/mbed%20Lab%2008%20Machine%20Learning%20on%20mbed/8_2%20Model%20Deploy into the 8_2_model_deploy folder.
   You may use drag and drop from Finder or File Explorer.

#. Import BSP library for getting accelerometer values.

   #. Click **+** in the Library tab under program source.

   #. Fill in `http://developer.mbed.org/teams/ST/code/BSP_B-L475E-IOT01/`
      And click "Next"

   #. Select "default" branch and click "Finish"

   #. Delete the following file:
      :file:`BSP_B-L475E-IOT01/Drivers/BSP/B-L475E-IOT01/stm32l475e_iot01_qspi.*`
      "*" means any file extension.

#. Import Tensorflow Lite library.

   #. Click **+** in the Library tab under program source.

   #. Fill in `https://gitlab.larc-nthu.net/ee2405_2021/tensorflowlite_mbed`
      And click "Next"

   #. Select "Master" branch and click "Finish"

#. Edit :file:`magic_wand_model_data.cpp` and fill in the blank according to the trained parameter data from the Google Colab.

   #. Change "g_magic_wand_model_data[]" array and "model_tflite_len".

   .. code-block:: c++
      const unsigned char g_magic_wand_model_data[] DATA_ALIGN_ATTRIBUTE = {
        // Paste the data of the char array in `src/model.cc` here
      };

      unsigned int model_tflite_len = ;// Fill the int in `src/model.cc` here

   .. code-block:: c++
      :linenos: inline

      #include "magic_wand_model_data.h"

      // We need to keep the data array aligned on some architectures.
      #ifdef __has_attribute
      #define HAVE_ATTRIBUTE(x) __has_attribute(x)
      #else
      #define HAVE_ATTRIBUTE(x) 0
      #endif
      #if HAVE_ATTRIBUTE(aligned) || (defined(__GNUC__) && !defined(__clang__))
      #define DATA_ALIGN_ATTRIBUTE __attribute__((aligned(4)))
      #else
      #define DATA_ALIGN_ATTRIBUTE
      #endif

      const unsigned char g_magic_wand_model_data[] DATA_ALIGN_ATTRIBUTE = {
        // Paste the data of the char array in `src/model.cc` here
      };

      unsigned int model_tflite_len = ;// Fill the int in `src/model.cc` here

#. Edit :file:`config_tflite.h`

   #. Change label_num to fit your gesture number, e.g., 3.

   .. code-block:: c++

      #define label_num 2

   #. Revise the output_message[] data array to fit your new gesture.

   .. code-block:: c++
      :linenos: inline

      #ifndef CONFIG_H_
      #define CONFIG_H_

      // The number of labels (without negative)
      #define label_num 2

      struct Config {

        // This must be the same as seq_length in the src/model_train/config.py
        const int seq_length = 64;

        // The number of expected consecutive inferences for each gesture type.
        const int consecutiveInferenceThresholds[label_num] = {20, 10};

        const char* output_message[label_num] = {
              "RING:\n\r"
              "          *       \n\r"
              "       *     *    \n\r"
              "     *         *  \n\r"
              "    *           * \n\r"
              "     *         *  \n\r"
              "       *     *    \n\r"
              "          *       \n\r",
              "SLOPE:\n\r"
              "        *        \n\r"
              "       *         \n\r"
              "      *          \n\r"
              "     *           \n\r"
              "    *            \n\r"
              "   *             \n\r"
              "  *              \n\r"
              " * * * * * * * * \n\r"};
      };

      Config config_tflite;
      #endif // CONFIG_H_


#. Compile and run the program to test with the DNN inference with your board by waving different gestures. 

#. Push the code to your GitHub repo. 

Model Deployment Code Reference
=================================

#. :file:`main.cpp`

   .. code-block:: c++
      :linenos: inline

      #include "accelerometer_handler.h"
      #include "config_tflite.h"
      #include "magic_wand_model_data.h"

      #include "tensorflow/lite/c/common.h"
      #include "tensorflow/lite/micro/kernels/micro_ops.h"
      #include "tensorflow/lite/micro/micro_error_reporter.h"
      #include "tensorflow/lite/micro/micro_interpreter.h"
      #include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
      #include "tensorflow/lite/schema/schema_generated.h"
      #include "tensorflow/lite/version.h"

      // Create an area of memory to use for input, output, and intermediate arrays.
      // The size of this will depend on the model you're using, and may need to be
      // determined by experimentation.
      constexpr int kTensorArenaSize = 60 * 1024;
      uint8_t tensor_arena[kTensorArenaSize];

      // Return the result of the last prediction
      int PredictGesture(float* output) {
        // How many times the most recent gesture has been matched in a row
        static int continuous_count = 0;
        // The result of the last prediction
        static int last_predict = -1;

        // Find whichever output has a probability > 0.8 (they sum to 1)
        int this_predict = -1;
        for (int i = 0; i < label_num; i++) {
          if (output[i] > 0.8) this_predict = i;
        }

        // No gesture was detected above the threshold
        if (this_predict == -1) {
          continuous_count = 0;
          last_predict = label_num;
          return label_num;
        }

        if (last_predict == this_predict) {
          continuous_count += 1;
        } else {
          continuous_count = 0;
        }
        last_predict = this_predict;

        // If we haven't yet had enough consecutive matches for this gesture,
        // report a negative result
        if (continuous_count < config_tflite.consecutiveInferenceThresholds[this_predict]) {
          return label_num;
        }
        // Otherwise, we've seen a positive result, so clear all our variables
        // and report it
        continuous_count = 0;
        last_predict = -1;

        return this_predict;
      }

      int main(int argc, char* argv[]) {

        // Whether we should clear the buffer next time we fetch data
        bool should_clear_buffer = false;
        bool got_data = false;

        // The gesture index of the prediction
        int gesture_index;

        // Set up logging.
        static tflite::MicroErrorReporter micro_error_reporter;
        tflite::ErrorReporter* error_reporter = &micro_error_reporter;

        // Map the model into a usable data structure. This doesn't involve any
        // copying or parsing, it's a very lightweight operation.
        const tflite::Model* model = tflite::GetModel(g_magic_wand_model_data);
        if (model->version() != TFLITE_SCHEMA_VERSION) {
          error_reporter->Report(
              "Model provided is schema version %d not equal "
              "to supported version %d.",
              model->version(), TFLITE_SCHEMA_VERSION);
          return -1;
        }

        // Pull in only the operation implementations we need.
        // This relies on a complete list of all the ops needed by this graph.
        // An easier approach is to just use the AllOpsResolver, but this will
        // incur some penalty in code space for op implementations that are not
        // needed by this graph.
        static tflite::MicroOpResolver<6> micro_op_resolver;
        micro_op_resolver.AddBuiltin(
            tflite::BuiltinOperator_DEPTHWISE_CONV_2D,
            tflite::ops::micro::Register_DEPTHWISE_CONV_2D());
        micro_op_resolver.AddBuiltin(tflite::BuiltinOperator_MAX_POOL_2D,
                                     tflite::ops::micro::Register_MAX_POOL_2D());
        micro_op_resolver.AddBuiltin(tflite::BuiltinOperator_CONV_2D,
                                     tflite::ops::micro::Register_CONV_2D());
        micro_op_resolver.AddBuiltin(tflite::BuiltinOperator_FULLY_CONNECTED,
                                     tflite::ops::micro::Register_FULLY_CONNECTED());
        micro_op_resolver.AddBuiltin(tflite::BuiltinOperator_SOFTMAX,
                                     tflite::ops::micro::Register_SOFTMAX());
        micro_op_resolver.AddBuiltin(tflite::BuiltinOperator_RESHAPE,
                                     tflite::ops::micro::Register_RESHAPE(), 1);

        // Build an interpreter to run the model with
        static tflite::MicroInterpreter static_interpreter(
            model, micro_op_resolver, tensor_arena, kTensorArenaSize, error_reporter);
        tflite::MicroInterpreter* interpreter = &static_interpreter;

        // Allocate memory from the tensor_arena for the model's tensors
        interpreter->AllocateTensors();

        // Obtain pointer to the model's input tensor
        TfLiteTensor* model_input = interpreter->input(0);
        if ((model_input->dims->size != 4) || (model_input->dims->data[0] != 1) ||
            (model_input->dims->data[1] != config_tflite.seq_length) ||
            (model_input->dims->data[2] != kChannelNumber) ||
            (model_input->type != kTfLiteFloat32)) {
          error_reporter->Report("Bad input tensor parameters in model");
          return -1;
        }

        int input_length = model_input->bytes / sizeof(float);

        TfLiteStatus setup_status = SetupAccelerometer(error_reporter);
        if (setup_status != kTfLiteOk) {
          error_reporter->Report("Set up failed\n");
          return -1;
        }

        error_reporter->Report("Set up successful...\n");

        while (true) {

          // Attempt to read new data from the accelerometer
          got_data = ReadAccelerometer(error_reporter, model_input->data.f,
                                       input_length, should_clear_buffer);

          // If there was no new data,
          // don't try to clear the buffer again and wait until next time
          if (!got_data) {
            should_clear_buffer = false;
            continue;
          }

          // Run inference, and report any error
          TfLiteStatus invoke_status = interpreter->Invoke();
          if (invoke_status != kTfLiteOk) {
            error_reporter->Report("Invoke failed on index: %d\n", begin_index);
            continue;
          }

          // Analyze the results to obtain a prediction
          gesture_index = PredictGesture(interpreter->output(0)->data.f);

          // Clear the buffer next time we read data
          should_clear_buffer = gesture_index < label_num;

          // Produce an output
          if (gesture_index < label_num) {
            error_reporter->Report(config_tflite.output_message[gesture_index]);
          }
        }
      }

#. :file:`accelerometer_handler.h`

   .. code-block:: c++
      :linenos: inline

      #ifndef ACCELEROMETER_HANDLER_H_
      #define ACCELEROMETER_HANDLER_H_

      #define kChannelNumber 3

      #include "tensorflow/lite/c/common.h"
      #include "tensorflow/lite/micro/micro_error_reporter.h"

      extern int begin_index;
      extern TfLiteStatus SetupAccelerometer(tflite::ErrorReporter* error_reporter);
      extern bool ReadAccelerometer(tflite::ErrorReporter* error_reporter,
                                    float* input, int length, bool reset_buffer);

      #endif  // ACCELEROMETER_HANDLER_H_

#. :file:`accelerometer_handler.cpp`

   .. code-block:: c++
      :linenos: inline

      #include "accelerometer_handler.h"
      #include "mbed.h"
      #include "stm32l475e_iot01_accelero.h"

      // Store x, y, z data
      int16_t pDataXYZ[3] = {0};
   
      // A buffer holding the last 200 sets of 3-channel values
      static float save_data[600] = {0.0};
      // Most recent position in the save_data buffer
      int begin_index = 0;
      // True if there is not yet enough data to run inference
      bool pending_initial_data = true;
      // How often we should save a measurement during downsampling
      int sample_every_n = 1;
      // The number of measurements since we last saved one
      int sample_skip_counter = 1;

      TfLiteStatus SetupAccelerometer(tflite::ErrorReporter* error_reporter) {
        // Init accelerometer
        BSP_ACCELERO_Init();
        return kTfLiteOk;
      }

      bool ReadAccelerometer(tflite::ErrorReporter* error_reporter, float* input,
                             int length, bool reset_buffer) {
        // Clear the buffer if required, e.g. after a successful prediction
        if (reset_buffer) {
          memset(save_data, 0, 600 * sizeof(float));
          begin_index = 0;
          pending_initial_data = true;
        }
        
        // Obtain a sample 
        while(sample_skip_counter <= sample_every_n) {
           BSP_ACCELERO_AccGetXYZ(pDataXYZ);
           sample_skip_counter += 1;
        }

        // Write samples to our buffer, converting to milli-Gs
        save_data[begin_index++] = (float)pDataXYZ[0];
        save_data[begin_index++] = (float)pDataXYZ[1];
        save_data[begin_index++] = (float)pDataXYZ[2];

        // Since we took a sample, reset the skip counter
        sample_skip_counter = 1;

        // If we reached the end of the circle buffer, reset
        if (begin_index >= 600) {
          begin_index = 0;
        }

        // Check if we are ready for prediction or still pending more initial data
        if (pending_initial_data && begin_index >= 200) {
          pending_initial_data = false;
        }

        // Return if we don't have enough data
        if (pending_initial_data) {
          return false;
        }

        // Copy the requested number of bytes to the provided input tensor
        for (int i = 0; i < length; ++i) {
          int ring_array_index = begin_index + i - length;
          if (ring_array_index < 0) {
            ring_array_index += 600;
          }
          input[i] = save_data[ring_array_index];
        }

        return true;
      }

#. :file:`magic_wand_model_data.h`

   .. code-block:: c++
      :linenos: inline

      #ifndef MAGIC_WAND_MODEL_DATA_H_
      #define MAGIC_WAND_MODEL_DATA_H_

      extern const unsigned char g_magic_wand_model_data[];
      extern const int g_magic_wand_model_data_len;

      #endif  // MAGIC_WAND_MODEL_DATA_H_

#. :file:`magic_wand_model_data.cpp` 

   .. code-block:: c++
      :linenos: inline

      #include "magic_wand_model_data.h"

      // We need to keep the data array aligned on some architectures.
      #ifdef __has_attribute
      #define HAVE_ATTRIBUTE(x) __has_attribute(x)
      #else
      #define HAVE_ATTRIBUTE(x) 0
      #endif
      #if HAVE_ATTRIBUTE(aligned) || (defined(__GNUC__) && !defined(__clang__))
      #define DATA_ALIGN_ATTRIBUTE __attribute__((aligned(4)))
      #else
      #define DATA_ALIGN_ATTRIBUTE
      #endif

      const unsigned char g_magic_wand_model_data[] DATA_ALIGN_ATTRIBUTE = {
        // Paste the data of the char array in `src/model.cc` here
      };

      unsigned int model_tflite_len = ;// Fill the int in `src/model.cc` here

#. Add and edit :file:`config_tflite.h`

   .. code-block:: c++
      :linenos: inline

      #ifndef CONFIG_H_
      #define CONFIG_H_

      // The number of labels (without negative)
      #define label_num 2

      struct Config {

        // This must be the same as seq_length in the src/model_train/config.py
        const int seq_length = 64;

        // The number of expected consecutive inferences for each gesture type.
        const int consecutiveInferenceThresholds[label_num] = {20, 10};

        const char* output_message[label_num] = {
              "RING:\n\r"
              "          *       \n\r"
              "       *     *    \n\r"
              "     *         *  \n\r"
              "    *           * \n\r"
              "     *         *  \n\r"
              "       *     *    \n\r"
              "          *       \n\r",
              "SLOPE:\n\r"
              "        *        \n\r"
              "       *         \n\r"
              "      *          \n\r"
              "     *           \n\r"
              "    *            \n\r"
              "   *             \n\r"
              "  *              \n\r"
              " * * * * * * * * \n\r"};
      };

      Config config_tflite;
      #endif // CONFIG_H_

#. TensorFlow Lite functions:

   #. Logging Method

      .. code-block:: c++

         static tflite::MicroErrorReporter micro_error_reporter;
         tflite::ErrorReporter* error_reporter = &micro_error_reporter;
         error_reporter->Report("Message\n");

      The implement method is similar to the code below but it will preprocess the variable you give it before printed.

      .. code-block:: c++

         void DebugLog(const char* s) {
           printf("%s", s);
         }

   #. Load a model

      Load a model from char array.

      .. code-block:: c++

         const tflite::Model* model = tflite::GetModel(g_magic_wand_model_data);

   #. Operations resolver

      This will be used by the interpreter to access the operations.

      To figure out the operations that provided by TensorFlow Lite,
      please check
      https://github.com/tensorflow/tensorflow/blob/master/tensorflow/lite/micro/kernels/all_ops_resolver.cc

      .. code-block:: c++

         tflite::ops::micro::AllOpsResolver micro_op_resolver;

      #. Just load the operation implementations we need

         The AllOpsResolver loads all of the operations available in TensorFlow
         Lite for Microcontrollers, which uses a lot of memory. Since a given
         model will only use a subset of these operations, it's recommended
         that real world applications load only the operations that are needed.

         To load the operation implementations we need, use the method below
         instead.

         .. code-block:: c++

            static tflite::MicroOpResolver<op_num> micro_op_resolver;
            micro_op_resolver.AddBuiltin(tflite::BuiltinOperator_OP_NAME, tflite::ops::micro::Register_OP_NAME());

   #. Interpreter

      #. Allocate memory

         We need to preallocate some of memory for input, output, and
         intermediate arrays.

         .. code-block:: c++

            const int tensor_arena_size = 60 * 1024;
            uint8_t tensor_arena[tensor_arena_size];

      #. Build the interpreter

         .. code-block:: c++

            static tflite::MicroInterpreter static_interpreter(model, micro_op_resolver, tensor_arena, kTensorArenaSize, error_reporter);
            tflite::MicroInterpreter* interpreter = &static_interpreter;

      #. Allocate tensors

         .. code-block:: c++

            interpreter->AllocateTensors();

      #. Get the pointer to model input

         .. code-block:: c++

            TfLiteTensor* model_input = interpreter->input(0);

      #. Validate input shape

         You can modify the condition to match your model.

         .. code-block:: c++

            if ((model_input->dims->size != 4) || (model_input->dims->data[0] != 1) ||
                (model_input->dims->data[1] != config_tflite.seq_length) ||
                (model_input->dims->data[2] != kChannelNumber) ||
                (model_input->type != kTfLiteFloat32)) {
                error_reporter->Report("Bad input tensor parameters in model");
                return -1;
            }

      #. Provide an input value

         .. code-block:: c++

            model_input->data.f[0] = 0.;

         In this lab, we use a function to provide an input value.

         .. code-block:: c++

            got_data = ReadAccelerometer(error_reporter, model_input->data.f, input_length, should_clear_buffer);

      #. Run the model

         .. code-block:: c++

            TfLiteStatus invoke_status = interpreter->Invoke();
            if (invoke_status != kTfLiteOk) {
              error_reporter->Report("Invoke failed\n");
            }

      #. Obtain the output

         .. code-block:: c++

            TfLiteTensor* output = interpreter->output(0);
            float value = output->data.f[0];

         In this lab, we use a function to obtain the output value.

         .. code-block:: c++

            gesture_index = PredictGesture(interpreter->output(0)->data.f);


********************
Demo and Checkpoints
********************

#. Show your git remote repository.
#. Show the result of inference of your gesture (not ring or slope).

**************
Reference List
**************

#. `How to use Google Colab <https://www.geeksforgeeks.org/how-to-use-google-colab/>`__
#. `TensorFlow Lite for Microcontrollers <https://www.tensorflow.org/lite/microcontrollers>`__
#. `Get started with microcontrollers <https://www.tensorflow.org/lite/microcontrollers/get_started>`__
#. `TensorFlow Lite API Reference <https://www.tensorflow.org/lite/api_docs/cc>`__
