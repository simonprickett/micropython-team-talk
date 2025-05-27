# TODO

TODO Overview

## Hardware

TODO what hardware do we need here?

## MicroPython Version 

TODO

## Install Dependencies

TODO

## Run the Code

TODO

## Roll 'em!

Now the code's up and running, visit the URL that was output to the MicroPython console.  It'll be something like:

```
http://192.168.5.31:80/
```

You'll see a menu of actions.  Roll the dice a few times, then click "View the metrics" to see the page that Prometheus will scrape metrics from.  It'll look something like this:

```
dice_roll{number="1"} 3
dice_roll{number="2"} 5
dice_roll{number="3"} 3
dice_roll{number="4"} 3
dice_roll{number="5"} 4
dice_roll{number="6"} 3
```

You'll need to use your browser's back button to return to a page with the navigation options on it.

If you want to reset the roll counts to 0 at any point, click "Reset the counters."

## Example Prometheus Job Configuration

Configure Prometheus to monitor the Pico W by editing `prometheus.yml` and adding the following scrape configuration. You'll need to substitute the IP address that your Pico W connects to your network with.

```yaml
scrape_configs:
  - job_name: 'diceroller'
    scrape_interval: 10s

    static_configs:
      - targets: ['192.168.5.31:80']
```

## Checking that Promethus is Scraping the Pico W

Start Prometheus like so:

```bash
./prometheus --config.file=prometheus.yml
```

Then visit:

```
http://localhost:9090/query
```

and execute the following query expression:

```
dice_roll
```

You should see results similar to these, showing the number of times each number has been rolled:

```
dice_roll{instance="192.168.5.31:80", job="diceroller", number="1"}	  3
dice_roll{instance="192.168.5.31:80", job="diceroller", number="2"}	  5
dice_roll{instance="192.168.5.31:80", job="diceroller", number="3"}	  3
dice_roll{instance="192.168.5.31:80", job="diceroller", number="4"}	  3
dice_roll{instance="192.168.5.31:80", job="diceroller", number="5"}	  4
dice_roll{instance="192.168.5.31:80", job="diceroller", number="6"}	  3
```