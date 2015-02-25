from novaclient.openstack.common.apiclient import exceptions
import novaclient.auth_plugin
from novaclient import client
from status import Status
import argparse
import os
import json
import time

AUTH_SYSTEM = 'rackspace'
HOME = os.path.expanduser('~')
DATA_FILE = HOME + '/uptime_data.json'
WINDOW = 5

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth_url", help="Auth endpoint url")
    parser.add_argument("-u", "--username", help="Account to use for the test")
    parser.add_argument("-k", "--api_key", help="API key for the account")
    parser.add_argument("-t", "--tenant", help="Tenant name")
    parser.add_argument("-r", "--region", help="The region to test")
    parser.add_argument("-w", "--window",
                        help="Sliding window for calculating uptime, "
                             "in minutes", default=WINDOW)
    return parser


def load_existing_data():
    data = []
    if os.path.isfile(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            s = ''.join(f.readlines())
            data = json.loads(s)

    return data


def save_data(data=[]):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)


def trim_data(data=[], window=WINDOW):
    if len(data) >= 0:
        now = int(time.time())
        oldest = now - window * 60
        data = [d for d in data if d['time'] >= oldest ]

    return data


def get_uptime_summary(data=[]):
    if len(data) == 0:
        return 0.0;

    ok_count = 0
    for d in data:
        if d['api_ok'] == 1:
            ok_count += 1

    count = len(data)
    pct = float(ok_count) / count

    return ok_count, count, pct


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    data = load_existing_data()

    datum = {
        'time' : int(time.time()),
        'api_ok': 1,
        'http_status': None
    }

    try:
        auth_plugin = novaclient.auth_plugin.load_plugin(AUTH_SYSTEM)
        c = client.Client('2', args.username, args.api_key, args.tenant,
                          args.auth_url, region_name=args.region,
                          auth_system=AUTH_SYSTEM, auth_plugin=auth_plugin)
        c.flavors.list()

        datum['api_ok'] = 1
        datum['http_status'] = '2xx'
    except exceptions.HttpError as e:
        result = Status()

        http_status = e.http_status
        if 500 <= http_status < 600:
            datum['api_ok'] = 0
        else:
            datum['api_ok'] = 1

        datum['http_status'] = http_status
    except:
        datum['api_ok'] = -1
        datum['http_status'] = None

    data.append(datum)
    data = trim_data(data, args.window)
    save_data(data)

    ok_count, count, pct = get_uptime_summary(data)

    status = Status()
    status.add_metric('uptime_pct', 'double', pct)
    status.add_metric('ok_count', 'uint32', ok_count)
    status.add_metric('data_points', 'uint32', count)

    print(status)
