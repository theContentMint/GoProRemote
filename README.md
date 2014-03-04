GoPro Remote
============

This is an attempt to reverse engineer the GoPro wifi remote protocol. 

The GoPro has two wifi modes. "App mode" and "Wifi RC". In "app mode" the GoPro becomes a wifi host, and commands are sent using http requests. The list of commands can be found at ... A python interface for them can be found at GoProController... 

As yet I have not been able to find similar resources for the "Wifi RC" mode. This is an attempt to create a place ...

In "Wifi RC" mode the Wifi remote becomes the wifi host and the GoPro becomes the client. The communication happens directly via the UDP protocol. 

At the moment it only simulates a GoPro listening to commands from the remote, and responds like a GoPro would.

This was used in the Bridgestone Bikebooth project ... 

A next step would be to simulate the wifi remote to control the GoPros from a computer. This would alow a computer to send simultanious commands to many GoPros.

The limitations of this method is that it is not possible to create live stream from the GoPros.
