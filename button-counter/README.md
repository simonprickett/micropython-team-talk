# Button Counter Example

TODO

## Hardware

To try this out you'll need the following hardware:

* 1 Raspberry Pi [Pico W](https://shop.pimoroni.com/products/raspberry-pi-pico-w?variant=40059369652307) or [Pico 2 W](https://shop.pimoroni.com/products/raspberry-pi-pico-2-w?variant=54852253024635) - get one with headers already attached, so that you don't have to buy these separately and solder them on yourself. These are also known as the "WH" versions.
* 1 [USB to Micro USB data cable](https://shop.pimoroni.com/products/usb-a-to-microb-cable-black?variant=31241639562), used to power the Pico W and install software on it.
* TODO arcade buttons
* TODO jumper wires

## Assembling the Hardware

TODO

## MicroPython Version

You'll need to install a MicroPython runtime on the Pico W.  Get the latest `.uf2` image and follow the installation instructions:

* [Image for Raspberry Pi Pico W](https://micropython.org/download/RPI_PICO_W/)
* [Image for Raspberry Pi Pico 2 W](https://micropython.org/download/RPI_PICO2_W/)

We've tested the code using MicroPython 1.25.

## Install Dependencies

TODO `mpremote` install instructions.

```bash
mpremote mip install github:ttk1/prometheus_remote_write_payload
```

TODO how to verify the installation.