# chess-raspberrypi

My end goal is to combine TensorFlow/Lite and RaspberryPI to process images from a chess board. I want my software to recognize movement of the pieces based on the real time image processing but I will not distinguish beteen the types of the pieces(more on that approach later).

Later I want to use Python library [chess](https://python-chess.readthedocs.io/en/latest/#features) to display the game on a screen as players make their movements. 
I want to be able track the game live and alert the players if they do illegal movements etc.

Such projects have already been carried out by other people - but my approach differs slightly. From what I saw, most of the solutions are board/pieces dependant where people train the models to recognize their and their only pieces. It isn't a suprise that such models do not work for other boards. I want to do something a bit easier yet more flexible in terms of different boards application. I want to be able to tell whether certain piece is white or black and what is it's position. 
For all chess games the initial position of the pieces is the same, therefore if I can "look" at the game from its begining I should be able to track the movements only by knowing the position of the piece being moved.

Let's do it!


# Blog part
I'll try to blog document it as a blog to track progress and later add more organised documentation on difference steps etc.

If you are new to Python or Software development and some things does not make sense, please open an Issue and I will do my best to add necessary clarification to the text.

## Setting up the raspberry PI 2
I borrowed a raspberry Pi 2 to do some experiments before my own arrives(btw I bought Pi 4, 4GB and it's on the way!)

What is necessary to know about the type of the Raspberry Pis I am using, is that you need few things in order to make them work, namely power supply, SD card and optionally: Mouse, Keyboard, HDMI Cable and Screen to plug the HDMI to. It might be very logical for you but I, a newbie, didn't really know how to setup all of these things and had to do some research!

**From my own experience in order for Pi to transfer video to your screen the HDMI cable has to be plugged in both the screen and the Pi before plugging the power supply**

### Installing Operating System
Raspberry Pi does not have an operating system by default. What you need to do is to get a **Micro SD CARD**, plug it into your machine with card reader, or buy one online (look for **Micro SD card reader** they are very cheap).

Then follow the installation process(recommended)[from official website tutorial](https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system) or you can try to make use of my experience and follow this steps:

- Download and install official software [Raspberry Pi Imager](https://www.raspberrypi.com/software/) for installing the Operating System(OS) on your card:
- Make sure that the Micro SD card is in the reader
- Run Raspberry Pi Imager
- Select the SD card you wish to install the OS on
- Choose the OS (I chose Raspbian as it seems like the general use case version of the Operating Systems available)

### Starting the Pi
I took out the card from the SD card reader inserted it inside my Pi. (For me the SD slot was on the bottom part of the Pi, if you are unsure where it is just google for it!)
Now I plugged my mouse, keyboard, screen, ethernet cable and finnaly power supply.

Pi started successfully and I could see GUI of the system. Then the system asked me if I wish to install the necessary updates and it took around 2 hours :)

After it installed I checked what kind of version of **Python** I had on my system(3.9.2), setup Github account and then tried to run some basic Python scripts.

Then I spent some time with my dad where he explained me what is the job of the pins on my raspberry Pi and how can the electronics work. How to plug sensors etc.

As working with Pi for me will mostly involve using terminal I decided that I want to have a remote connection to my Pi from my regular laptop.

I managed to open and SSH port to my Pi and started using the terminal from my mac. See [How to enable ssh to your raspberrypi](#how-to-enable-ssh-to-your-raspberrypi)

That was it for the day! Day 0 was succesful.

## The camera is here!
Today my camera arrvied and my goal was simple - take a picture of myself :D

For the hardware part of plugging the camera I used the help of my dad. As for the Pi however, similairly to the _ssh connection_ I had to enable it camera access. 

You can find the Python code to take a picture below and more information about that topic here: [Enabling the camera](#enabling-the-camera-on-pi)

```Python 
from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
sleep(1)
camera.capture('foo.jpg')
```
_Important: The sleep(1) function gives the necessary time for the camera to prepare. If you remove it you might encounter difficulties_

## How the hell is this going to work?
Today I again didn't code much, instead I spent whole day thinking about practical issues of image detection and how the hell am I going to create my data set, how is the model going to learn what is a chess board and finally whether I should create my model from the scratch. 

As always after few hours of extensive thinking and not being able figure it out I got demotivated and started doubting whether is it even possible. Then I started talking to my friends and with their help I managed to organise my thoughts and pinpoint important things:

- I am going to transfer learning to train my model
- I am going to first train it on an easy [dataset](https://www.kaggle.com/koryakinp/chess-positions) and then use camera to check how is that model working with real images
- The format of my data is going to be a flattened 8x8 matrix see [representing my target feature](#representation-of-the-target-feature)


### Transfer learning
If you haven't heard about transfer learning or fine tunning I will try to briefly explain them, however the intuition behind it is to use some knowledge from one domain and transfer it to solve problems from other domain.
Companies like Google have huge potential in terms of data and computational power. They use it to build powerful models that solve general tasks. 

One example that is very famous - MobileNets, is a family convolutional neural networks for image processing that Google trained and shared with the public. Such models usually serve general purpose, for instance:
- the network is not capable of distinguishing _German Shepards_ from _Pudels_ but it can recognize _dogs_ vs _cats_
- the network is not capable of distinguishing _slim fit shirts_ from _regular shirts_ but is able to find a difference between a _shirt_ and a _sweater_

_I hope you get what I mean by general usecase by now!_

We as public can use this general use case models to build something more specialized. If we have enough data on slim shirts and regular ones we can use to with the help of MobileNets solve the problem of distinguishing between these two.

**I will use so called fine tunning**:

Let's assume that MobileNets is built from hundred of blocks connected together as a horizontal line, like so:
- B1, B2, B3, B4, B6 .... BN 

The blocks on the left handside are able to recognize simple features such as shapes, lines, curves. The blocks closer to the right hand side are capable of finding out whether certain picture contains a tail, eyes, buttons, wheels - in general more conrete things. They together are capable of understanding the picture and knowing the differences between dogs and cats, shirts and sweaters and so on. If we take our picture of a dog and put it through each of this blocks in chronological order, then the last block will be able to tell us that indeed the picture represents a dog.

If we then wanted to specialise our blocks to solve the _German Shepards vs Pudels_ problem, we could take the last/right handside 10% of the blocks (as they hold more concrete features) and start manipulating them so that instead of remembering differences between cats/dogs, it would start to memorize differences between _German Shepards_ and _Pudels_ - that approach is called **Fine tunning**. We tune only that last layers of neural network so that instead of solving general problem it solves our specific problem. Idea behind it is that we trained our model long enough, the first 90% of the blocks for generalised would be the same as the 90% of the first blocks for the specialized problem and it is only the last "blocks" that learn to recognize the breed of the dog.

So hopefully by know you somewhat figured out what I am planning to do. I will get one of the Networks from MobileNets and optimize it to learn how to serve my purpose of analysing the chess board.

# Technical part

## How to enable ssh to your raspberrypi
One of the first things I did was to have an option to ssh to my Raspberry Pi from my Mac (it's really convenient).  
I followed these steps:

- We need to allow other computers to connect to our Raspberry Pi. In order to do that I followed this [link](https://phoenixnap.com/kb/enable-ssh-raspberry-pi#:~:text=into%20your%20device.-,Enable,-SSH%20on%20Raspberry). It's roughly like this: **Preferences -> Raspberry Pi Configuration -> Interfaces -> Enable SSH**
- Generate a ssh key (I'm using Mac os)
```console
pi:~$ ssh-keygen -t rsa -C "myfakeemail@fake.com"
```

```console
pi:~$ ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.0.16  netmask 255.255.255.224  broadcast 192.168.0.31
        inet6 fe80::845a:ba70:e515:f44c  prefixlen 64  scopeid 0x20<link>
        inet6 ::883c:a41b:8d12:4650  prefixlen 64  scopeid 0x0<global>
        ether b8:27:eb:10:ff:6e  txqueuelen 1000  (Ethernet)
        RX packets 1339  bytes 122361 (119.4 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 3440  bytes 384632 (375.6 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
- Finally I have SSHED to my pi from my Mac (be ready to give the password to your PI)
```console
mac:~$ ssh pi@192.168.0.16
```

## Enabling the camera on Pi

To enable the camera I used [this link](https://www.arrow.com/en/research-and-events/articles/raspberry-pi-camera-options-and-usage) I think it's great tutorial and however I try I won't make it simpler/better

## Taking a picture

In order to take a picture you need to make sure that you have the [Picamera](https://picamera.readthedocs.io/) installed/

Shut down your raspberry Pi and unplug the power(just for safety) then follow this 2 minute video to properly connect you camera tape with the Pi - [Video](https://www.youtube.com/watch?v=lAbpDRy-gc0&t=83s)

Remember:

-blue part of the tape should face the USB ports
- make sure you have properly closed the plastic to secure the camera tape

Create a file with a following code and save it - for instance as: _photo_maker.py_

```Python
from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
sleep(1)
camera.capture('foo.jpg')
```
_Important: The sleep(1) function gives the necessary time for the camera to prepare. If you remove it you might encounter difficulties_

Then open the terminal, make sure that your current directory is the directory that the Python file was saved, then execute:
```console
pi:~$ python3 photo_maker.py
```

You should be able to find your picture in the same directory as your python file.

## Representation of the target feature
Target feature is what I want my model to predict.My output should be the representation of 8x8 matrix with 3 possible values:
- E for empty field
- W field with a white piece
- B field with a black piece

When predicting, my neural network will return me the data in the form of a vector but for the sake of simplicity let's represent the output as 8x8 matrix correlating to a chess board.

                1 2 3 4 5 6 7 8
                
           A    B B B B B B B B
           B    B B B B B B B B
           C    E E E E E E E E
           D    E E E E E E E E
           E    E E E E E E E E
           F    E E E W E E E E
           G    W W W E W W W W
           H    W W W W W W W W

The board above represents the first move of the game, where White moved pawn from G4 to F4
There! Now I can work from my machine and have the pi terminal available.

# Inference

![Inference Model](photos/inferencechess.drawio.png)
