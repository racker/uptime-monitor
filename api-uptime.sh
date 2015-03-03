#! /bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export PYTHONPATH=$PYTHONPATH:${DIR}
python -m uptimemonitor.agentplugin.nova_uptime_plugin \
        -u $1 -k $2 -r $3 -w $4
