# Uninformed Search

Required libraries.
===================
The user must have the libraries installed below to run the program:

* util
* time
* pygame
* search
* numpy as np
* matplotlib
* graphviz
* IPython
* os
* sys
* numpy 
* pyautogui


Backends
--------

The server abstracts over the underlying robot via a Backend. A backend accepts messages from the robot's internals. A message is forwarded to the web page via websockets.

Currently, only a ROS backend is implemented:

### Subscriptions:

* ```operator_text std_msgs/String``` What the robot has heard the operator say
* ```robot_text std_msgs/String``` What the robot itself is saying
* ```challenge_step std_msgs/UInt32``` Active item index in the plan or action sequence the robot is executing.
* ```image sensor_msgs/Image``` Image of what the robo sees or anything else interesting to the audience

### Publications
* ```command std_msgs/String``` Command HTTP POSTed to the robot.

TODO
----

* Allow robot to push action sequence and challenge name to server. Allows for GPSR action sequences etc.

Installation and try out
-------
```bash
git clone https://github.com/LoyVanBeek/vizbox.git
cd vizbox
sudo pip install -r requirements.txt

roscore # in separate terminal
./server.py image:=/usb_cam/image_raw # Remaps the image-topic to output of the USB cam, see below
```

Open [The web page on localhost](http://localhost:8888)

To reproduce the the screenshot:
```bash
roslaunch usb_cam usb_cam-test.launch # separate terminal
rostopic pub /challenge_step std_msgs/UInt32 "data: 0" --once
rostopic pub /robot_text std_msgs/String "data: 'Hello operator'" --once
rostopic pub /operator_text std_msgs/String "data: 'Robot, follow me'" --once
rostopic pub /robot_text std_msgs/String "data: 'OK, I will follow you'" --once;
rostopic pub /challenge_step std_msgs/UInt32 "data: 1" --once
```

POST commands
=============
Use
```bash
http -f POST localhost:8888/command command="Robot, follow me"
```
(Using the very handy [HTTPie](https://httpie.org/) utility) to get a publication on the ```/command``` topic

Buttons
=============

Buttons are pushing messages in `next_step` topic.

To see pushed messages use :
```bash
rostopic echo next_step # separate terminal
```



