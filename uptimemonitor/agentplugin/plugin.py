from novaclient.openstack.common.apiclient import exceptions
import novaclient.auth_plugin
from novaclient import client
from status import Status

auth_url = 'https://identity.api.rackspacecloud.com/v2.0'
#auth_url = 'https://staging.identity-internal.api.rackspacecloud.com/v2.0/'
username = 'inframon'
password = '<api-key>'
tenant_name = 'inframon'
project_id = 'inframon'
region = 'IAD'
auth_system = 'rackspace'

if __name__ == '__main__':
    try:
        auth_plugin = novaclient.auth_plugin.load_plugin(auth_system)
        c = client.Client('1.1', username, password, tenant_name, auth_url,
                          region_name=region, auth_system=auth_system,
                          auth_plugin=auth_plugin)
        c.flavors.list()
        result = Status()
        result.add_metric('api_ok', 'string', 'true')
    except exceptions.HTTPError as e:
        result = Status()

        http_status = e.http_status
        if 500 <= http_status < 600:
            result.add_metric('api_ok', 'string', 'false')
        else:
            result.add_metric('api_ok', 'string', 'true')

        result.add_metric('http_status', 'uint32', http_status)
    except:
        result = Status(status='FAIL')
        result.add_metric('api_ok', 'string', 'unknown')

    print(result)
