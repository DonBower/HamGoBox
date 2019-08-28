# Setup the environment
One step that I like to perform before building software on Linux is to set some compiler optimization flags, so that the compiled code will be the most efficient for the RaspberryPi.
If you elect this step, you'll need to determine the proper flags for your machine.
If you have a recent version of GCC, such as that available in the most recent couple of versions of Raspbian, you can set the flags to select the best values at runtime.
To do this, run these commands in the terminal before proceeding:
```
export CXXFLAGS='-O2 -march=native -mtune=native'
export CFLAGS='-O2 -march=native -mtune=native'
```


# Prerequisite Packages

The Fldigi build process requires a number of prerequisites.
These include GUI, image, and sound libraries, among others.
The process described below also requires that you build an XMLRPC library written by the Fldigi team, as well as a recent version of the hamlib radio control interface library.
Installing and building the prerequisite packages should be done at a command prompt, most likely a terminal.

First, we will install the prerequisite system packages.
These are packages that are maintained by the Raspbian team, and can be installed using apt-get.
The only requirement is that the RaspberryPi needs to have some kind of Internet access, so it can download the packages from the Raspbian repositories.

At a terminal prompt, run the following commands, one after another.
```
sudo apt-get --assume-yes update
sudo apt-get --assume-yes install libfltk1.3-dev \
                                  libjpeg9-dev \
                                  libxft-dev \
                                  libxinerama-dev \
                                  libxcursor-dev \
                                  libsndfile1-dev \
                                  libsamplerate0-dev \
                                  portaudio19-dev \
                                  libusb-1.0-0-dev \
                                  libpulse-dev
```


```
mkdir -p ~/Developer/fldigi
```

Compile fldigi
```
cd ~/Developer/fldigi
wget http://www.w1hkj.com/files/flxmlrpc/flxmlrpc-0.1.4.tar.gz
tar -xzvf flxmlrpc-0.1.4.tar.gz
cd ~/Developer/fldigi/flxmlrpc-0.1.4
./configure --prefix=/usr/local --enable-static
make && sudo make install
```

Compile hamlib
```
cd ~/Developer/fldigi
wget https://sourceforge.net/projects/hamlib/files/hamlib/3.3/hamlib-3.3.tar.gz
tar -xzvf hamlib-3.3.tar.gz
cd ~/Developer/fldigi/hamlib-3.3
./configure --prefix=/usr/local --enable-static
make && sudo make install
```

Compile flrig
```
cd ~/Developer/fldigi
wget http://www.w1hkj.com/files/flrig/flrig-1.3.48.tar.gz
tar -xzvf flrig-1.3.48.tar.gz
cd ~/Developer/fldigi/flrig-1.3.48
./configure --prefix=/usr/local --enable-static
make && sudo make install
```

Compile fldigi
```
mkdir -p ~/Developer/fldigi
cd ~/Developer/fldigi
wget http://www.w1hkj.com/files/fldigi/fldigi-4.1.08.tar.gz
tar -xzvf fldigi-4.1.08.tar.gz
cd ~/Developer/fldigi/fldigi-4.1.08
./configure --prefix=/usr/local --enable-static
make && sudo make install
```
