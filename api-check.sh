#! /bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
python ${DIR}/uptimemonitor/agentplugin/plugin.py \
        -a $1 -u $2 -k $3 -t $4 -r $5
