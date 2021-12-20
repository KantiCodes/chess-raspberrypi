# chess-raspberrypi

My end goal is to combine TensorFlow/Lite and RaspberryPI to process images from a chess board. I want my software to recognize movement of the pieces based on the real time image processing but I will not distinguish beteen the types of the pieces(more on that approach later).

Later I want to use python-library [chess](https://python-chess.readthedocs.io/en/latest/#features) to display the game on a screen as players make their movements. 
I want to be able track the game live and alert the players if they do illegal movements etc.

Such projects have already been carried out by other people - but my approach differs slightly. From what I saw, most of the solutions are board/pieces dependant where people train their models to recognize their pieces from pictures of their board. I want to do something a bit easier yet more flexible in terms of the boards. I want to be able to track only white/black pieces movements and then keep the state of the chess board to recognize which pieces were moved. 


# Blog part
I've done few projects before and I found documenting the project day after day easier. I will keep this format so that my progress can be tracked in a chronological - true to my process, manner. As for the technical parts I will add them as separate sections and add references to them.

## Day 0 - Setting up the raspberry PI 2
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

## Day 1 - The camera is here!
Today my camera arrvied and my goal was simple - take a picture of myself :D

For the hardware part of plugging the camera I used the help of my dad as for the Pi, similairly to the _ssh connection_ I had to enable it. More on that [here](#enabling-the-camera-on-pi).

Then I found a Python library [Picamera](https://picamera.readthedocs.io/en/release-1.13/) that allows to operate on the camera through code.


## Day 2 - How the hell is this going to work?
Today I didn't code much, instead I spent whole day thinking about practical issues of image detection and how the hell am I going to create my data set, how is the model going to learn what is a chess board and finally whether I should create my model from the scratch. As always after few hours of thinking in my head not being able to figure it out I got demotivated but
If you haven't heard about transfer learning learning or fine tunning I will try to briefly explain them.
Companies like Google have huge potential in terms of data and computational power. The use it to build powerful models that solve general tasks. 

One example that is very famous - MobileNets, is a family convolutional neural networks for image processing that Google trained and shared with public. This models usually serve general purpose, for instance:
- the network is not capable of distinguishing German Shepards from Pudels but it can recognize dogs vs cats
- the network is not capable of distinguishing slim fit shirts from regular shirts but is able to find a difference between a shirt and a sweater.

_I hope you get what I mean general usecase by now!_

We as public can use this general use case models to build something more specialized. If we have enough data on slim shirts and regular ones we can use to with the help of MobileNets solve the problem of distinguishing them.

**Now the promised explanation**:
Let's assume that MobileNets is build from hundred of blocks connected together as a horizontal line, like so:
- B1, B2, B3, B4, B6 .... BN 
If we take our picture of a dog and put it through each of this blocks in chronological order, then the last block will be able to tell us that indeed the picture consists a dog.

If we then wanted  
enormous resources to train machine learning model for general use cases and th these are techniques that use general use case, pre-trainned neural network for is a way for people to use neural networks that were trained for

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
