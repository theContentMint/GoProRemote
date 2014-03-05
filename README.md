GoPro Remote
============

This is an attempt to reverse engineer the GoPro wifi remote protocol. 

The GoPro (Hero 3 and Hero 2 with wifi backpack) has two wifi modes. "App mode" and "Wifi RC". In "app mode" the GoPro becomes a wifi host, and commands are sent using http requests. The list of commands can be found at https://github.com/KonradIT/goprowifihack . A python interface for them can be found at https://github.com/joshvillbrandt/GoProController . 

As yet I have not been able to find similar resources for the "Wifi RC" mode. This is an attempt to create such a place.

Current Functionality and Example
---------------------------------

In "Wifi RC" mode the Wifi remote becomes the wifi host and the GoPro becomes the client. The communication happens directly via the UDP protocol. 

To connect to the remote, let the Wifi Remote look for cameras by holding the top button and pressing the bottom one. You should see a camera with arrows underneath. While the remote is in this state it broadcasts its wifi network. Connect to this network from your computer. Then start the gopro class. (If the remote is not looking for a camera it does not broadcast the network. You will have to be able to connect to a hidden wifi network.) 

At the moment it only simulates a GoPro listening to commands from the remote, and responds like a GoPro would. When a "start recording" command (SH) is recieved the time is saved in `self.start_time`. When a "stop recording" command is recieved the time is saved in `self.stop_time` and the double is written to a line in the csv file defined in `self.filename`.

If the computer is the only thing connected to the remote it will display an image sent by the computer. Thanks Michael for providing a suitable image.

This example starts a thread which listens to start and stop recoding commands and records them to a csv file.

    import gopro
    import time
    gp = gopro.gopro()
    gp.start()
    time.sleep(10)
    gp.stop()
    

This was used in the Bridgestone Bikebooth project. (Link to follow soon)

Next Steps
----------

A next step would be to simulate the wifi remote to control the GoPros from a computer. This would alow a computer to send simultanious commands to many GoPros. The limitations of this method is that it is not possible to create live stream from the GoPros or change the settings of the gopros as far as I am aware.

The class should be expanded to make it more modular.

A full catalogue of the commands should be compiled with what the right responses should be, as well as how the state variable changes with these commands (see below).

How the remote works
--------------------

The remote sends a series of UPD commands to all the cameras connected to it. It waits for a response from each one. It also broadcasts a state (st) command via the broadcast channel. The wifi remote waits until all the state responses are the same. 

The UDP packet has the following form in hex: 00 00 XX 00 00 00 00 
Where XX are ASCII characters. The ASCII characters explain what the command is for. Many of the meanings can be gathered from the links above, but there are some new ones.

How to Help
-----------

Connect to a remote's network. Connect a GoPro to the networks as well. Open wireshark (or tcp dump) to listen to the trafic. Descyfer the commands and responces. As well as the changes in the state response. 

