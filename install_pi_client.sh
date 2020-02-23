#!/bin/sh

set -e

cp blinds_pi_client.service /etc/systemd/system/
systemctl start blinds_pi_client
systemctl enable blinds_pi_client
