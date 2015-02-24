from novaclient.openstack.common.apiclient import exceptions
import novaclient.auth_plugin
from novaclient import client
from status import Status
import argparse

AUTH_SYSTEM = 'rackspace'

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--auth_url", help="Auth endpoint url")
    parser.add_argument("-u", "--username", help="Account to use for the test")
    parser.add_argument("-k", "--api_key", help="API key for the account")
    parser.add_argument("-t", "--tenant", help="Tenant name")
    parser.add_argument("-r", "--region", help="The region to test")
    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    try:
        auth_plugin = novaclient.auth_plugin.load_plugin(AUTH_SYSTEM)
        c = client.Client('2', args.username, args.api_key, args.tenant,
                          args.auth_url, region_name=args.region,
                          auth_system=AUTH_SYSTEM, auth_plugin=auth_plugin)
        c.flavors.list()
        result = Status()
        result.add_metric('api_ok', 'int32', 1)
    except exceptions.HttpError as e:
        result = Status()

        http_status = e.http_status
        if 500 <= http_status < 600:
            result.add_metric('api_ok', 'int32', 0)
        else:
            result.add_metric('api_ok', 'int32', 1)

        result.add_metric('http_status', 'uint32', http_status)
    except:
        result = Status(status='FAIL')
        result.add_metric('api_ok', 'int32', -1)

    print(result)
