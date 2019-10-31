#!/usr/bin/env python3

"""Fancy pants install-o-matic

Point it at your pis and install stuff.

Ansible is too heavy weight to configure, shell scripts are a bunch of work and manual sucks.

Things to do:

* Goal: make it relatively painless to configure a pi for a particular project, and be able to wipe and reset without fretting
* Add pis to the list of known machines, inventory on disk (dropbox or git)
* Add notes on pis
* run apt-get update + upgrade
* install and enable a service from different sources (apt, prometheus.zip, my source, etc). Generate configs or have a pool of ready ones.
* Configure hardware (raspi-config)
* Bootstrap a new instance (via SD card mounted for basics and then via ssh)
* configure and add to wireguard mesh
* Specify sets of dependencies (e.g. to use scd30 I need i2c disabled and pigpio)
* pi discovery via MAC? Generate hostnames based on MAC address.
* Be a little more prescriptive (like pibakery which is cool), have more precanned parts to choose from.
* Curses UI 'cos why not :)

"""
