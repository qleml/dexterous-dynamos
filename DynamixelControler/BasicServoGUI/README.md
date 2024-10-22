# Basic README for running Servo GUI for prototyping

### To install the dependencies (nothing special needed), run:

```pip3 install -r requirements.txt```


Maybe you will also need to install ```tkinter```. 

Ubuntu:
```sudo apt-get install python3-tk```


### The next steps must be followed

1. Connect servos of interest in a daisy-chain matter and connect one of them on the board provided for controlling the servos.
2. Connect the board to power and turn switch on.
3. Connect boar to laptop. They may be a probem of giving access to the USB port. Keep it in mind if an error occurs.
In ubuntu a possible solution is 
``` $ sudo usermod -aG dialout <your_account_id>``` followed by a reboot of the device. 


Even though this is not intuitive, because we wanted to use most of the provided code and functions, these steps need to be followed.

4. Get the absolute path of the ```DynamixelControler``` folder and put it in line 5 of ```servoGui.py``` code.

5. If you want to test less than 16 (all) of the servos, unfortunately you must start from 1 and go up. You **cannot** skip servos and have a gap in the motor ids. For example connect servos 1-6 and then 12-16.

6. Depending on the number of servos you are testing on step **4** you must have an equal number of lines in the ```cal.yaml``` file. Just put on a random value (something small like 1-2). After the first run we will calibrate the servo and the calibrated value will be stored. 

7. Finally you must modify also ```gripper_defs.yaml```. Examine the 2 provided finger layouts are written and write a new one accordingly. The comments on the file make it self-explanatory. A sum-up is:
Each fingers has specific number of (controllable) joints (with unique id) corresponding to it, the ```joint_ids``` . We have that each joint has an flexor and extendor tendon, thus the ```tendon_ids``` are double than the ```joints_ids```. The motor driving every 2 of the above tendons are the ```motor_ids``` (again unique). A mapping follows of the corresponding ```motor_id``` to each one of the ```tendon_ids``` (so the two of them have same size). Usually you just repeat each the ```motor_id``` with 2 times each ```motor_id```. FInally the ```spool_rad``` has the consists of the radius of the spool and it being either positive or negative. The servos will turn counterclockwise by default. So you put a negative value on the ```spool_rad``` if a positive angle should shorten the tendon length. Of course you must attach the tendon respectively in order to wind-up when the servo move counterclockwise (so attached tangent on the left).  


### Execute the python script. 

```python3 servoGui.py```


### How to use the "application" 

Select a servo you want to move. Then you can move the slider from 0 to 360 degress in order to move it (the direction is based on the sign of the first ```spool_rad``` value selected on step 5 matching the specific motor). 

The code can be changed in order to not start from "0 degrees" and only "add" angle. Change the ```DEFAULT_ANGLE = 0``` to whatever is prefered.

Reseting buttons, reset the servo values to 0 (or the newly defined ```DEFAULT_ANGLE = 0```). 

### Calibration 

You can calibrate a servo by selecting it and then pressing calibrate. You can either first use the slider to set the servo to the desired position and the press "Calibrate" and imediately "Finish Calibration" or by pressing "Calibrate" then moving with your hand to the desired position and then pressing "Finish Calibration". 


### Notes 

This code is far far from perfect but it is for basic prototyping and to help me understand better their given controller code. For any questions Whatsapp me and I'll help you out. I'd suggest playing around with it first before attaching any tendons that could potentially brake if something is not setup right.
