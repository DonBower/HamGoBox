How to change Raspberry Pi's Swapfile Size on Raspbian
11 Feb 2015
Written by Shane Pfaffly
Reason Why
Ever get the dreaded error:

Virtual memory exhausted: Cannot allocate memory
With the first iterations of Raspberry Pi the Model A comes with 256mb of memory. While the Raspberry Pi B comes with a modest 512mb of memory. For most applications this amount of memory is actually quiet a bit. As soon as you start compiling your own binaries this amount starts to seem dismal.

*Insert reason why swap on flash-based memory is bad here.

Limitations
The Raspbian distribution comes with a 100mb swapfile. This is actually a bit on the small side. A general rule of thumb is swapfile size should be about twice as much as the available RAM on the machine. In the examples below I have a Raspberry Pi B+. So the amount of swap I use is 1024mb.

Commands
We will change the configuration in the file */etc/dphys-swapfile *:

sudo nano /etc/dphys-swapfile
The default value in Raspbian is:

CONF_SWAPSIZE=100
We will need to change this to:

CONF_SWAPSIZE=1024
Then you will need to stop and start the service that manages the swapfile own Rasbian:

sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start
You can then verify the amount of memory + swap by issuing the following command:

free -m
The output should look like:

total     used     free   shared  buffers   cached
Mem:           435       56      379        0        3       16
-/+ buffers/cache:       35      399
Swap:         1023        0     1023
Finished!
That should be enough swap to complete any future compiles I may do in the future.
