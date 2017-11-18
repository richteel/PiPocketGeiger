# THIS REPOSITORY IS OUT OF DATE!!! PLEASE PULL FROM SOURCE PROJECT, [MonsieurV/PiPocketGeiger](https://github.com/MonsieurV/PiPocketGeiger "MonsieurV/PiPocketGeiger")!!! #

# STOP #

# Raspberry Pi Pocket Geiger library

A Raspberry Pi library to interface with the [Radiation Watch Pocket Geiger counter](http://www.radiation-watch.co.uk/) (Type 5).

![](/misc/type5.jpg?raw=true "Radiation Watch Type 5 Pocket Geiger counter")

The library monitors the Pocket Geiger through interrupts - using the [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO) package - and processes the CPM and hourly [Sievert dose](https://en.wikipedia.org/wiki/Sievert).

Learn more about the Pocket Geiger counter on the Radiation Watch [FAQ](http://www.radiation-watch.co.uk/faqs) and on [our blog](https://blog.ytotech.com/2016/03/04/radiation-watch-raspberry/). Actually it is not a proper Geiger-Müller counter, but a Photodiode PIN sensor that can effectively counts gamma rays.

## Getting started

### Install the library

Using pip:

```
sudo pip install PiPocketGeiger
```

[PiPocketGeiger on Pypi](https://pypi.python.org/pypi/PiPocketGeiger/).

### Installing the library for Python3

Using pip:

```
sudo pip3 install git+https://github.com/richteel/PiPocketGeiger
```


### Wiring

The Pocket Geiger must be wired to the GPIO ports of the Raspberry Pi. Refer to the GPIO pin specification of your RPi revision.

For exemple you can wire the radiation and the noise pin on respectively the `GPIO24` and `GPIO23` of your Raspberry Pi.

| Pocket Geiger pin | Raspberry Pi pin | Standing for |
| ----------------- | ----------- | ------------ |
| `+V` | `3V3` | Alimentation pin (DC 3V~9V) |
| `GND` | `GND` | Ground pin |
| `SIG` | `GPIO24` | Radiation-detection pulse pin |
| `NS` | `GPIO23` | Noise-detection pulse pin |

![](/misc/wiring.png?raw=true "Wiring of the Pocket Geiger and Raspberry Pi B+")

The pin used are specified at the creation of the library object:

```
with RadiationWatch(24, 23) as radiationWatch:
  pass # Do something with the lib.
```

Even if the Pocket Geiger can handle voltage between 3V and 9V, the [RPi GPIO](https://www.raspberrypi.org/documentation/hardware/raspberrypi/gpio/README.md) only works on 3.3V levels, so **do NOT supply 5V** to your Pocket Geiger, but 3.3V instead.

[Pocket Geiger Type 5 interface specification](http://www.radiation-watch.co.uk/uploads/5t.pdf).

### Getting readings

To get readings, call the `status()` method:

```
print(radiationWatch.status())
# {'duration': 14.9, 'uSvh': 0.081, 'uSvhError': 0.081, 'cpm': 4.29}
```

Then do whatever you need with the results. For exemple, [log them to a terminal](https://github.com/MonsieurV/PiPocketGeiger/blob/master/examples/console_logger.py) or [write them on a file](https://github.com/MonsieurV/PiPocketGeiger/blob/master/examples/file_logger.py).

### React on radiation hits

The library allows to register callbacks that will be called in case of radiation or noise detection, using respectively the `registerRadiationCallback()` or `registerNoiseCallback()`:

```
def onRadiation():
    print("Ray appeared!")
def onNoise():
    print("Vibration! Stop moving!")
with RadiationWatch(24, 23) as radiationWatch:
   radiationWatch.registerRadiationCallback(onRadiation)
   radiationWatch.registerNoiseCallback(onNoise)
   while 1:
       time.sleep(1)
```

This can be used to simulate the typical [Geiger counter click sound](https://github.com/MonsieurV/PiPocketGeiger/blob/master/examples/geiger_click.py) or as a random generator.

### Stream in real-time on Plotly

As a more ellaborate idea, you can stream the data directly to Plotly, allowing to sharing it easily. See the [complete exemple](https://github.com/MonsieurV/PiPocketGeiger/blob/master/examples/plotly_streaming.py).

[![](/misc/plotly_streaming.gif?raw=true "Real-time streaming. Click to see on Plotly.")](https://plot.ly/137/~tournadey/)

In the same vein, you can [upload reading to a Google Docs](https://github.com/MonsieurV/PiPocketGeiger/blob/master/examples/google_docs.py) or also [broadcast on Twitter](https://github.com/MonsieurV/PiPocketGeiger/blob/master/examples/twitter.py).

Finally if you want to contribute to an open-data initiative you can [publish your measurements](https://github.com/MonsieurV/PiPocketGeiger/blob/master/examples/safecast.py) to [the Safecast API](http://blog.safecast.org/). More info on the [SafecastPy lib repo](https://github.com/MonsieurV/SafecastPy).

Yes, with a Raspberry Pi, Python and an internet access, there's not so much limits to what you can pretend!

## Note

Remember the Pocket Geiger can't record correctly in presence of vibration. For a more precise and mobile oriented unit, you may look at the [bGeigie Nano](http://blog.safecast.org/bgeigie-nano/) from the Safecast project.

-----------------------

Like it? Not so much? [Simply tell us](mailto:yoan@ytotech.com). Don't forget to check out [our blog](http://blog.ytotech.com)! :-)

Happy hacking!

### Notes regarding the Examples



1. The examples are for Python 2.7. For Python 3, change the using statement to: ```from PiPocketGeiger3 import RadiationWatch```

2. The code examples show the use of the "with" statement. If your code creates a RadiationWatch object without using a "with" statement then you must call the setup() method right after creating the object and call the close() method to destroy the object.

### Credits

Created upon the [Radiation Watch sample code](http://radiation-watch.sakuraweb.com/share/ARDUINO.zip).

### Contribute

Feel free to [open a new ticket](https://github.com/MonsieurV/PiPocketGeiger/issues/new) or submit a PR to improve the lib.
