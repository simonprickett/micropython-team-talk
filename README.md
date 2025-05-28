# MicroPython Examples with Grafana and Prometheus

This repository contains some example MicroPython scripts that explore different ways to get metrics from devices to Prometheus / Grafana Cloud. The code runs on Raspberry Pi Pico W microcontrollers. One example requires a couple of arcade or similar type buttons, another is specific to the Pimoroni Enviro+ Pack.

## Get the Code and Setup Your Machine

Before trying the examples, you'll need to complete a few common setup steps...

### Get the Code

At the terminal, clone this repository to your local machine:

```bash
git clone https://github.com/simonprickett/micropython-team-talk.git
```

### Install mpremote

We'll use MicroPython's `mpremote` command to copy files to the Pico W and run them.  Install `mpremote` on your local machine by following [these instructions](https://docs.micropython.org/en/latest/reference/mpremote.html).

Verify that `mpremote` has been installed by checking its version:

```bash
mpremote --version
```

You should see output similar to this:

```
mpremote 1.25.0
```

## Demos

This repository contains a number of MicroPython demos. Each is standalone and contains its own detailed README file. If you're new to MicroPython and want to follow more of a learning path through the code, we'd suggest looking at the demos in this order:

1. [Hello World](./hello-world/) - a simple blinking LED.
1. [Counting with Arcade Buttons](./button-counter/) - sending button count metrics to a Prometheus remote write endpoint.
1. [Scraping Metrics with Prometheus](./prometheus-scrape/) - exposing metrics via HTTP so that Prometheus can scrape them.
1. [Environment Monitoring with the Pimoroni Enviro+ and Grafana Cloud](./pimoroni-enviro-plus/) - monitoring the environment in a room with a variety of sensors connected to the Pimoroni Enviro+ add-on pack.