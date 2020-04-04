# PySafe

_Default password: hello_

PySafe is a highly customizeable and beginner-friendly Arduino enabled smart-safe that communicates with Python for authentification via the serial interface.

#### [Click here to see it in action!](https://youtu.be/4i5Rg6EGQqU)

## Arduino code:
* Communicates with serial interface and carries out the following instructions:
	* 'unlock' -> 0 degrees (parallel to lid)
	* 'lock' -> 90 degrees (perpendicular to lid)

## Python code:
The UI consists of 3 main pages.

### Menu
* Input the password -> compares the inputted password against the master password -> gives/declines authorization
* __What can be worked on:__ clear password input upon entering so the user could try again without having to run the program again

![](/readme-pysafe/intro.png)

* __Lock/Unlock__
	* Uses pyserial to communicate with the port where the Arduino is plugged into.
	* Self explanatory - click 'Lock PySafe' to lock, and 'Unlock PySafe' to unlock

![](/readme-pysafe/settings.png)
* __Reset Password__
	* Takes input for the new password and writes it to the password.key file.
	* __What can be worked on:__ Implement hashing (attempted to but came across problems with byte/string/hash conversions) for security



### Things to note when using pyserial and/or working with Arduino and Python:
When a serial port is initialized, the Arduino automatically reboots itself. This means that it can't receive and execute instructions right away. If you want to write something to it immediately after initializing the serial, make sure to sleep/delay for 2 seconds first.

### Looking to customize it?
Make sure to change the port value within the code accordingly! You can check which port your Arduino is using by going into Device Manager > Ports.
				
