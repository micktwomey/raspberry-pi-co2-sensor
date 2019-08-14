# raspberry-pi-c02-sensor

Reading CO2 with a Pi and an SCD30. Publishes to Adafruit IO and exposes Prometheus metrics.

# Using

Rough steps:

1. Checkout and build co2trh from https://github.com/metebalci/rpi-scd30
2. Set up an Adafruit IO account and nab the credentials
3. `pipenv install`
4. `pipenv run python co2_sensor.py`

Optional: `prometheus --config.file=prometheus.yml` to run a prometheus instance which scrapes the readings.

# Testing

You can use dummy_co2trh.py to mock out the co2trh binary, it publishes some random samples from real readings.
