#!/bin/sh

YAML_DIR=etc/rackspace-monitoring-agent.conf.d

if [ ! -d "$YAML_DIR" ]; then
  mkdir -p ${YAML_DIR}
fi

AUTH_URL=https://identity.api.rackspacecloud.com/v2.0
USERNAME=inframon

read -e -p "Auth URL: " -i ${AUTH_URL} AUTH_URL
read -e -p "Username: " -i ${USERNAME} USERNAME
read -e -p "API Key : " API_KEY
read -e -p "Tenant  : " -i ${USERNAME} TENANT
read -e -p "Region(s): " REGIONS

for REGION in $REGIONS; do
(
cat <<EOF
type       : agent.plugin
label      : ${REGION}: Nova API availability test
disabled   : false
period     : 30
timeout    : 15
details    :
    file : api-check.sh
    args : [ '${AUTH_URL}', '${USERNAME}', '${API_KEY}', '${TENANT}', '${REGION}' ]
EOF
)> etc/rackspace-monitoring-agent.conf.d/${REGION}-api-check.yaml
done
