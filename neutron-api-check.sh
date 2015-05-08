#! /bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
export PYTHONPATH=$PYTHONPATH:${DIR}
python -m uptimemonitor.agentplugin.neutron_check_plugin \
        -a $1 -u $2 -k $3 -t $4 -r $5
