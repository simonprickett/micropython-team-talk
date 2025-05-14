# TODO Pimoroni Enviro+ Demo

![A Grafana dashboard showing output from this project](pimoroni_enviro_plus_dashboard_example.png)

## Hardware

TODO what hardware do we need here?

* 1 Raspberry Pi [Pico W](https://shop.pimoroni.com/products/raspberry-pi-pico-w?variant=40059369652307) - get one with headers already attached, so that you don't have to buy these separately and solder them on yourself. These are also known as the "WH" versions.  At the time of writing, the required MicroPython build for this project wasn't readily available for the Pico 2 W so avoid those and stick with the original model.
* 1 Pimoroni [Pico Enviro+ Pack](https://shop.pimoroni.com/products/pico-enviro-pack?variant=40045073662035) (just get the pack, you don't need any of the extra accessories such as the external particulate sensor).
* TODO Micro USB cable

## Assembling the Hardware

TODO

## MicroPython Version

You'll need to install a MicroPython runtime on the Pico W. The Enviro+ Pack uses a specific build of Pimoroni MicroPython which has all of the sensor drivers you need built in.  Download the latest from Pimoroni's GitHub [here](https://github.com/pimoroni/pimoroni-pico/releases). Be sure to get the file named `enviro-<version>-pimoroni-micropython.uf2`.

TODO how to install that.

## Install Dependencies

TODO `mpremote` install instructions.

```bash
mpremote mip install github:ttk1/prometheus_remote_write_payload
```

TODO how to verify the installation.
