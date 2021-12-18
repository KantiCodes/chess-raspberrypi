# chess-raspberrypi
End goal: Use TensorFlow Lite + RaspberryPI to process a chessboard using a camera and correctly read out loud and visualise moves

## Blog part
Feels a bit easier to document the project working day after working day thereore I will keep this format and then at the end of the this section the technical description of the project will follow.

### Day 0 - Setting up the raspberry PI 2
I borrowed raspberry Pi 2 to do some experiments before my own arrives(btw I bought Pi 4, 4GB and it's on the way!)

What is necessary to know about raspberry PIs is that you need few things in order to make them work, namely Power Supply, SD card and optionally: Mouse, Keyboard, HDMI Cable and Screen to plug the HDMI to.

**From my own experience in order for Pi to transfer video to your screen the HDMI cable has to be plugged in both the screen and the Pi before plugging the power supply**

### Installing Operating System
Raspberry PI does not have an operating system by default. What you need to do is to get a **Micro SD CARD**, plug it into your machine with card reader, or buy one online (look for **Micro SD card reader** they are very cheap).

Then follow the installation process(recommended)[from official website tutorial](https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system) or you can try to make use of my experience and follow this steps:

- Downloand and install official software [Raspberry Pi Imager](https://www.raspberrypi.com/software/) for installing the Operating System(OS) on your card:
- Make sure that the Micro SD card is in the reader
- Run Raspberry Pi Imager
- Select the Sd card I wish to install the OS
- Choose the OS, I chose Raspbian as it seems like the general use case version of the Operating Systems available

### Starting the Pi
I took out the card from the SD card reader inserted it inside my Pi. (For me the SD slot was on the bottom part of the Pi, if you are unsure where it is just google for it!)
Now I plugged my mouse, keyboard, screen, ethernet cable and finnaly power supply.

Pi started successfully and I could see GUI of the system. Then the system asked me if I wish to install the necessary updates and it took around 2 hours :)

After, it installed I checked what kind of version of python I had on my system(3.9.2), setup Github account and then tried to run some basic python scripts.

Then I spent some time with my dad where he explained me what is the job of the pins on my raspberry Pi and how can the electronics work. How to plug sensors etc.

As working with Pi for me will mostly involve using terminal I decided that I want to have a remote connection to my Pi from my regular laptop.

I managed to open and SSH port to my Pi and started using the terminal from my mac. See [How to enable ssh to your raspberrypi](#how-to-enable-ssh-to-your-raspberrypi)

That was it for the day! Day 0 was succesful.

## How to enable ssh to your raspberrypi
One of the first things I did was to have an option to ssh to my Raspberry Pi from my Mac (it's convenient).  
For starters I plugged a screen keyboard and an ethernet cable to my PI and did following things:

- We need to allow other computers to connect to our Raspberry Pi. Preferences -> Raspberry Pi Configuration -> Interfaces -> Enable SSH
- Generate a ssh key (I'm using Mac os)
```console
pi:~$ sh-keygen -t rsa -C "myfakeemail@fake.com"
```
- Then I followed this [link](https://phoenixnap.com/kb/enable-ssh-raspberry-pi#:~:text=into%20your%20device.-,Enable,-SSH%20on%20Raspberry) to enable my PI take ssh connections.  
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
There! Now I can work from my machine and have the pi terminal available.
