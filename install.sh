
sudo apt install python3 -y
sudo apt install python3-dev gcc -y

cd ~

git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py
sudo python3 setup.py install

sudo apt install alsa-utils -y

sudo apt install mopidy mopidy-mpd mpc -y