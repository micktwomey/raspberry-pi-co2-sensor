import logging
import os
import subprocess
import time

import Adafruit_IO
import click
import coloredlogs
import prometheus_client

CO2_GAUGE = prometheus_client.Gauge("co2_ppm", "CO2 in ppm")
TEMPERATURE_GAUGE = prometheus_client.Gauge("temperature_celcius", "Temperature in Celcius")
HUMIDITY_GAUGE = prometheus_client.Gauge("humidity_percent", "Humidity percentage")

@click.command()
@click.option("--co2trh-binary", default="../rpi-scd30/co2trh", type=click.Path(exists=True, dir_okay=False))
@click.option("--sudo/--no-sudo", default=True)
@click.option("--prometheus-port", default=8080, type=int)
@click.option("--aio-user", default=lambda: os.environ.get('ADAFRUIT_IO_USERNAME', ''))
@click.option("--aio-key", default=lambda: os.environ.get('ADAFRUIT_IO_KEY', ''))
@click.option("--sleep-seconds", default=10.0, type=float)
def main(co2trh_binary, sudo, prometheus_port, aio_user, aio_key, sleep_seconds):
    coloredlogs.install(
        level="INFO", fmt="%(asctime)s %(levelname)s %(name)s %(message)s"
    )

    prometheus_client.start_http_server(port=prometheus_port, addr="0.0.0.0")
    logging.info("Prometheus metrics listening on 0.0.0.0:{}".format(prometheus_port))

    aio = Adafruit_IO.Client(aio_user, aio_key)

    while True:
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
        aio.send("pi-co2-sensor.co2", co2)
        aio.send("pi-co2-sensor.temperature", temperature)
        aio.send("pi-co2-sensor.humidity", humidity)
        time.sleep(sleep_seconds)

if __name__ == "__main__":
    main()
