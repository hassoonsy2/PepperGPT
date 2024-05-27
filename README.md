# Pepper GPT

![Peper](https://github.com/hassoonsy2/Robotics_Project/blob/main/R%20(1).jpg)


## Description:
Welcome to the Hublab project repository! This innovative project is centered around integrating Pepper, a friendly humanoid robot, into the HUB-lab environment to serve as an interactive assistant for visitors. The HUB-lab, located within the HU library, is a dynamic space that offers access to cutting-edge technologies such as Virtual Reality, Robotics, Gamification, and Artificial Intelligence.

## Our mission is to enhance the visitor experience in two significant ways:

Human-Robot Interaction: We aim to explore and improve how visitors interact with technology, specifically through their engagement with Pepper. This component focuses on assessing participants' attitudes towards technology and refining Pepper's conversational abilities. By incorporating gestures and movements, we strive to make interactions not only more engaging but also more informative.
Technical Development: For those with a technical inclination, this aspect of the project involves enhancing Pepper's ability to understand and respond to visitor inquiries. We're exploring the integration of advanced AI solutions, including ChatGPT, to enable Pepper to provide accurate and helpful information about the lab's resources and how to utilize various technologies. This will be particularly beneficial in workshop settings, where Pepper can assist participants more effectively.
Project Goals:

- To make Pepper a knowledgeable and engaging assistant for visitors and workshop participants.
- To study and improve human-robot interactions within an educational and technological setting.
- To provide both less technical and technical students with hands-on experience in working with AI and robotics.


#Code

The code interfaces [OpenAI GPT-3](https://openai.com/) with the [Aldebaran](https://www.aldebaran.com/en) Pepper and Nao robots, allowing open verbal conversation with these robots on a wide range of subjects.

## Video of the Result
ToDO

## Installation

[PepperGPT](https://github.com/hassoonsy2/PepperGPT) depends on the NaoQi software to interface with the Pepper and Nao robots, and the OpenAI API to interface with GPT-3. Please refer to the detailed setup instructions below for your preferred operating system.

### Setup for Windows

NaoQi is old and runs on Python 2.7 while OpenAI requires Python 3. We therefore need both Python versions installed. Here's a step by step guide for setup on Windows 11.

1. Make sure Python 3.x is installed on the system. 
1. Install [Python 2.7](https://www.python.org/downloads/release/python-2718/). Select the 32 bit msi installer.
1. Add ```C:\Python27``` to the environment PATH.
1. Open a terminal and verify that ```python``` refers to Python2.7 and ```python3``` refers to your Python 3.x distribution.
2. Install [Ollama](https://ollama.com/download)
3. after installing ollama start a power shell and install the Phi3 model  ```ollama pull phi3:mini ```
4. Then you can test the model using ``` ollama run phi3:mini```

Now we need a few of dependencies:

* Install all dependencies for Python 2: ```python -m pip install -r .\requirements.py2.txt```
* Install all dependencies for Python 3: ```python3 -m pip install -r .\requirements.py3.txt```

We will use VS Code to run things, you may also use another environment if you prefer. 

Now we need the Python NaoQi API for communicating with the Pepper robot. 

* Download and extract [NaoQi Python SDK](https://www.softbankrobotics.com/emea/en/support/pepper-naoqi-2-9/downloads-softwares/former-versions?os=45&category=108) to a folder (pynaoqi-python2.7-2.5.7.1-win32-vs2013/lib) of your choice and add its path the PYTHONPATH environment variable in Windows. 
* You may also want to install [Choreographe 2.5.10.7](https://www.softbankrobotics.com/emea/en/support/pepper-naoqi-2-9/downloads-softwares/former-versions?os=45&category=108). It is however not strictly needed. 

Finally, we are ready to check out the repository. 

* Check out this repository and open the folder in VS Code
* Open a terminal and run ```python init.py``` to set up a default environment. Have your OpenAI account key available so that this can be stored with your configuration. 

### Setup for OSX and Linux

NaoQi is old and runs on Python 2.7 while OpenAI requires Python 3. 

1. Open a terminal and verify that ```python2``` refers to Python2.7 and ```python3``` refers to your Python 3.x distribution. If any of them are missing, please install through your preferred package manager.  

Now we need a few of dependencies:

* Install all dependencies for Python 2: ```python2 -m pip install -r .\requirements.py2.txt```
* Install all dependencies for Python 3: ```python3 -m pip install -r .\requirements.py3.txt```

We are now ready to check out the repository:

* Check out this repository and open the folder in VS Code
* Open a terminal and run ```python init.py``` to set up a default environment. Have your OpenAI account key available so that this can be stored with your configuration. 

We will use [VS Code](https://code.visualstudio.com/) to run things, you may also use another environment if you prefer. 

Now we need the Python NaoQi API for communicating with the Pepper robot. 

* Download and extract NaoQi Python SDK for [Nao](https://www.softbankrobotics.com/emea/en/support/nao-6/downloads-softwares) or [Pepper](https://www.softbankrobotics.com/emea/en/support/pepper-naoqi-2-9/downloads-softwares/former-versions?os=45&category=108) matching the version of your robot's software. Tested with Pynaoqi 2.8.6.
* Update your terminal profile (e.g. *.zshrc*) with the following:
    * export PYTHONPATH=${PYTHONPATH}:/path/to/python-sdk/lib/python2.7/site-packages
    * export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:/path/to/python-sdk/lib
    * export QI_SDK_PREFIX=/path/to/python-sdk
* Start ```python2``` and make sure you can import ```naoqi```. OSX may throw a lot of warnings the first time NaoQi is imported. Google for the exact way to approve these. 

I haven't been able to make Choreographe to run on recent versions of OSX, but it's not needed for running this app. 

## Run
Make sure you've gone through all steps in the Setup guide above before you start. 

Note that the Speech recognition module uses a NaoQi (*Autonomous Life Proxy*) to switch focus to *nao_focus*. You may not have this script on your own robot and the the code will throw an exception as a result. This call is made solely to prevent the default dialogue system of the robot to interfere with PepperChat. You may safely comment this away or upload your own preferred focus script to the robot, e.g. using Choreograph. 

* Start the OpenAI GPT-3 chatbot service by opening a terminal and execute ```python3 startDialogueServer.py --server ```. If everything goes well, the server should respond with _Starting OpenAI chat server... or  _Starting Tinyllama server... besed on your server prefrence within the parameter
Type an input message to test your chatbot..._
* Next, start Google's text to speech recognition service for Pepper by opening a new terminal and execute ```python module_speechrecognition.py --pip pepper.local``` (where _pepper.local_ refers to your robot's ip ).
* We are now ready to start the dialogue service by opening another terminal and executing ```python module_dialogue.py --pip pepper.local  --server the model that you want``` (where _pepper.local_ refers to your robot's ip ). This script will ask for a participant id and then connect to the OpenAI chatbot server we started earlier. If everything goes well it will continue and register another NaoQi module that runs the dialogue. _Pepper should now be ready to chat!_

## License

This project is released under the MIT license. Please refer to [LICENSE.md](LICENSE.md) for license details.

Parts of the source code have specific license formulations. Please see the file headers for details.

--------------------------------------------
## Importent Links :

- Resarch plan  : https://www.overleaf.com/6338562289yxpdhtvhmmjq#f09f90
- Current \& Future Customer Journey Map "MAP" : https://www.canva.com/design/DAF82leUJ1A/O19ehrI2XOTL2FS1DScvvQ/edit
- Design Methods for Social Robotics Document : https://www.overleaf.com/4988576184hwtjqsymjzpg#a22a78
- VPC : https://www.canva.com/design/DAF8y5bZGHY/lTmAirM6dRAS8QF9V8TFSw/edit


