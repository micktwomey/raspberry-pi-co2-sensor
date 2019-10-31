#!/bin/bash

set -xeuo pipefail

GRAFANA_VERSION="6.3.3"
DEB_FILENAME="grafana_${GRAFANA_VERSION}_armhf.deb"
DEB_URL="https://dl.grafana.com/oss/release/${DEB_FILENAME}"


function do_install() {
    curl $DEB_URL > /tmp/${DEB_FILENAME}
    sudo dpkg -i /tmp/${DEB_FILENAME}
}

set +e
installed_version=$(dpkg -l grafanaa |grep grafana | awk '{print $3}')
set -e

if [ "${installed_version}" != "${GRAFANA_VERSION}" ]; then
    echo "Installing Grafana"
    do_install
    sudo /bin/systemctl daemon-reload
    sudo /bin/systemctl enable grafana-server
    sudo /bin/systemctl start grafana-server
else
    echo "Grafana ${GRAFANA_VERSION} already installed"
fi
