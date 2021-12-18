# chess-raspberrypi
End goal: Use TensorFlow Lite + RaspberryPI to process a chessboard using a camera and correctly read out loud and visualise moves

## How to enable ssh to your raspberrypi
One of the first things I did was to have an option to ssh to my Raspberry Pi from my Mac (it's convenient).  
For starters I plugged a screen keyboard and an ethernet cable to my PI and did following things:  
- First I needed to generate a ssh key
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
