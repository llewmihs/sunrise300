# From a basic install of Raspbian

## Install python pip:

`sudo apt-get install python3-pip`

## Remote acces through remote.it

`sudo apt update && sudo apt install -y connectd && sudo connectd_installer`

## The following modules are needed:

* dropbox `pip3 install dropbox`
* pushbullet `pip3 install pushbullet.py`
* astral `pip3 install astral`
* python-crontab `pip3 install python-crontab`

## Github

`sudo apt install git`

## Enable camera: 

`sudo raspi-config`

## Now for ffmpeg...

From here: https://github.com/JolleJolles/pirecorder/wiki/Installing-ffmpeg-on-Raspberry-Pi-with-h264-support

### First we'll get the h264 encoder

```
git clone --depth 1 https://code.videolan.org/videolan/x264.git
cd x264
./configure --host=arm-unknown-linux-gnueabi --enable-static --disable-opencl 
make -j4
sudo make install
```
Note: -j4 is for four cores.

### Then we'll sort ffmpeg:

```
git clone git://source.ffmpeg.org/ffmpeg --depth=1
cd ffmpg
./configure --arch=armel --target-os=linux --enable-gpl --enable-libx264 --enable-nonfree
make -j4
sudo make install
```

