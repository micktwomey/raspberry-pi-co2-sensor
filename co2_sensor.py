import logging
import os
import subprocess
import time

import Adafruit_IO
import click
import coloredlogs
import prometheus_client
from prometheus_client import parser

CO2_GAUGE = prometheus_client.Gauge("co2_ppm", "CO2 in ppm")
TEMPERATURE_GAUGE = prometheus_client.Gauge("temperature_celcius", "Temperature in Celcius")
HUMIDITY_GAUGE = prometheus_client.Gauge("humidity_percent", "Humidity percentage")

def go(co2trh_binary, sudo, prometheus_port, aio_user, aio_key, aio_publish_interval_seconds, sleep_seconds, sensors_file, use_sensors_file):
    logging.info("Using Adafruit username {} and key len {}".format(aio_user, len(aio_key)))
    aio = Adafruit_IO.Client(aio_user, aio_key)

    then = time.time()

    while True:
        if use_sensors_file:
            logging.info(sensors_file)
            content = open(sensors_file).read()
            logging.info(content)
            values_by_name = {}
            for metric in parser.text_string_to_metric_families(content):
                values_by_name[metric.name] = metric.samples[0].value
            co2 = values_by_name["gas_ppm"]
            temperature = values_by_name["temperature_degC"]
            humidity = values_by_name["humidity_rel_percent"]
        else:
            cmd = [co2trh_binary]
            if sudo:
                cmd = ["sudo"] + cmd
            output = subprocess.check_output(cmd)
            logging.info(output)
            (co2, temperature, humidity) = [float(x) for x in output.decode("utf-8").strip().split(" ")]
        logging.info((co2, temperature, humidity))
        CO2_GAUGE.set(co2)
        TEMPERATURE_GAUGE.set(temperature)
        HUMIDITY_GAUGE.set(humidity)
        now = time.time()
        if (now - then) >= aio_publish_interval_seconds:
            logging.info("Publishing to Adafruit ({} - {} = {} vs {})".format(now, then, now - then, aio_publish_interval_seconds))
            aio.send("pi-co2-sensor.co2", co2)
            aio.send("pi-co2-sensor.temperature", temperature)
            aio.send("pi-co2-sensor.humidity", humidity)
            then = now
        time.sleep(sleep_seconds)


@click.command()
@click.option("--co2trh-binary", default="../rpi-scd30/co2trh", type=click.Path(exists=True, dir_okay=False))
@click.option("--sudo/--no-sudo", default=True)
@click.option("--prometheus-port", default=8080, type=int)
@click.option("--aio-user", default=lambda: os.environ.get('ADAFRUIT_IO_USERNAME', ''))
@click.option("--aio-key", default=lambda: os.environ.get('ADAFRUIT_IO_KEY', ''))
@click.option("--aio-publish-interval-seconds", default=15.0, type=float)
@click.option("--sleep-seconds", default=2.0, type=float)
@click.option("--sensors-file", default="/run/sensors/scd30/last", type=click.Path(dir_okay=False))
@click.option("--use-sensors-file/--no-use-sensors-file", default=False)
def main(co2trh_binary, sudo, prometheus_port, aio_user, aio_key, aio_publish_interval_seconds, sleep_seconds, sensors_file, use_sensors_file):
    coloredlogs.install(
        level="INFO", fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    prometheus_client.start_http_server(port=prometheus_port, addr="0.0.0.0")
    logging.info("Prometheus metrics listening on 0.0.0.0:{}".format(prometheus_port))

    while True:
        try:
            go(co2trh_binary, sudo, prometheus_port, aio_user, aio_key, aio_publish_interval_seconds, sleep_seconds, sensors_file, use_sensors_file)
        except Exception:
            logging.exception("Uh oh! Let's go again!")

if __name__ == "__main__":
    main() # pylint: disable=no-value-for-parameter
