from novaclient import exceptions
from novaclient import client

auth_url = 'https://identity.api.rackspacecloud.com/v2.0'
username = 'inframon'
password = ''
#api_key = ''
tenant_name = '945348'
region = 'IAD'

if __name__ == '__main__':
    c = client.Client('2', username, password, tenant_name, auth_url,
                      region_name=region)
    print(c.flavors.list())
