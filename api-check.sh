#! /bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
PYTHONPATH=$PYTHONPATH:${DIR}
python -m uptimemonitor.agentplugin.uptimeplugin \
        -a $1 -u $2 -k $3 -t $4 -r $5
