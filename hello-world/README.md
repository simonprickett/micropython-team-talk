# Hello World Example

This is the basic flashing LED "Hello World" example in MicroPython.

## Hardware

You'll want either a [Raspberry Pi Pico W](https://shop.pimoroni.com/products/raspberry-pi-pico-w?variant=40059369652307) or the newer [Pico 2 W](https://shop.pimoroni.com/products/raspberry-pi-pico-2-w?variant=54852253024635).  As we're not connecting any other hardware to the microcontroller, you don't need to buy one with the headers attached. However, if you also want to try the [button counter example project](../button-counter/), you should get the "WH" version with the headers pre-soldered.

To get the code onto the device and power it, you'll need a [USB to Micro USB data cable](https://shop.pimoroni.com/products/usb-a-to-microb-cable-black?variant=31241639562) too.

## MicroPython Version 

You'll need to install a MicroPython runtime on the Pico W.  Get the latest `.uf2` image and follow the installation instructions:

* [Image for Raspberry Pi Pico W](https://micropython.org/download/RPI_PICO_W/)
* [Image for Raspberry Pi Pico 2 W](https://micropython.org/download/RPI_PICO2_W/)

We've tested the code using MicroPython 1.25.

## Run the Code

With your Pico W connected to your machine by the USB to MicroUSB cable, run the code like so:

```bash
mpremote run blink.py
```

You should see output similar to the following on the MicroPython console:

```
LED starts flashing...
```

and the built in LED on your Pico W should flash on and off continuously.