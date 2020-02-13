MFRC522-RadioControl
==============
A small program to work use mpd as a MP3 / netradio controlled with 5 push buttons and an RFID-Tag.

**Important notice:** This library has not being actively updated in almost four years.
It might not work as intended on more recent Raspberry Pi devices. You might want to 
take a look to the open pull-requests and forks to see other implementations and bug-fixes.

## Requirements
This code requires you to have SPI-Py installed from the following repository:
https://github.com/lthiery/SPI-Py

```
git clone https://github.com/lthiery/SPI-Py.git
sudo python setup.py install
```

## Examples
This repository includes a couple of examples showing how to read, write, and dump data from a chip. They are thoroughly commented, and should be easy to understand.

## Pins
You can use [this](http://i.imgur.com/y7Fnvhq.png) image for reference.

| Name               | Pin # | Pin name   | State       |
|:------------------:|:-----:|:----------:|:-----------:|
| SDA                | 24    | GPIO8      |             |
| SCK                | 23    | GPIO11     |             |
| MOSI               | 19    | GPIO10     |             |
| MISO               | 21    | GPIO9      |             |
| IRQ                | None  | None       |             |
| GND                | Any   | Any Ground |             |
| RST                | 22    | GPIO25     |             |
| 3.3V               | 1     | 3V3        |             |
| BUTTON_VOLUME_UP   | 18    | GPIO24     | with Pullup |
| BUTTON_VOLUME_DOWN | 16    | GPIO23     | with Pullup |
| BUTTON_PAUSE       | 15    | GPIO22     | with Pullup |
| BUTTON_TRACK_PREV  | 11    | GPIO17     | with Pullup |
| BUTTON_TRACK_NEXT  | 13    | GPIO27     | with Pullup |

## Usage
To start the radio control execute the Read.py.
To write a new card create a file writeCard in excution directory and put the playlist name

## License
This code and examples are licensed under the GNU Lesser General Public License 3.0.
