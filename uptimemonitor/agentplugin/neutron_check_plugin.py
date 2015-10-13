from status import Status
import argparse
import json
import requests

AUTH_SYSTEM = 'rackspace'

CLIENT_VERSION = '2.0'


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

    status = Status(status='OK')

    try:
        headers = {"Content-type": "application/json"}
        payload = {
            "auth": {
                "RAX-KSKEY:apiKeyCredentials":
                    {"username": args.username, "apiKey": args.api_key}}}
        token_url = '%s/tokens' % args.auth_url
        response = requests.post(token_url, data=json.dumps(payload),
                                 headers=headers)
        token = response.json()['access']['token']['id']
        url = ("https://%s.networks.api.rackspacecloud.com/v2.0/networks" %
               args.region.lower())
        headers['X-Auth-Token'] = token
        response = requests.get(url, headers=headers)
        if 200 == response.status_code:
            status.add_metric('2xx', 'double', 1)
        elif 500 <= response.status_code < 600:
            status.add_metric('5xx', 'double', 1)
        else:
            status.add_metric('other', 'double', 1)
    except:
        status.status = 'FAIL'
        status.add_metric('error', 'double', 1)

    print(status)
