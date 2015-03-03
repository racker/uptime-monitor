from rackspace_monitoring.providers import get_driver
from rackspace_monitoring.types import Provider
from status import Status
import argparse
import time

AUTH_SYSTEM = 'rackspace'
WINDOW = 5
#The monitoring lib only supports points rather than resolution right now
POINTS = 1000
METRICS = ['2xx', '5xx', 'other']

def get_parser():
    parser = argparse.ArgumentParser()
    # parser.add_argument("-a", "--auth_url", help="Auth endpoint url")
    parser.add_argument("-u", "--username", help="Account to use for the test")
    parser.add_argument("-k", "--api_key", help="API key for the account")
    # parser.add_argument("-t", "--tenant", help="Tenant name")
    parser.add_argument("-r", "--region", help="The region to test")
    parser.add_argument("-w", "--window",type=int,
                        help="Sliding window for calculating uptime, "
                             "in minutes", default=WINDOW)

    return parser


def get_entity(cm_driver, region):
    label = "%s - API Uptime Check" % region.upper()
    entities = cm_driver.list_entities()
    for entity in entities:
        if entity.label == label:
            return entity
    return None


def get_check_id(cm_driver, region, entity_id):
    label = "%s: Nova API availability test" % region
    checks = cm_driver.list_checks(entity_id)
    for check in checks:
        if check.label == label:
            return check
    return None


def get_unix_time_millis():
    return int(time.time() * 1000)


def get_metric_counts(driver, entity_id, check_id, from_ts, to_ts):
    counts = {'total': 0}

    for metric in METRICS:
        data_points = driver.fetch_data_point(entity_id, check_id, metric,
                                               from_ts, to_ts, POINTS)
        count = len(data_points)
        counts['total'] += count
        counts['count_%s' % metric] = len(data_points)

    return counts


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    status = Status(status='OK')
    try:
        Cls = get_driver(Provider.RACKSPACE)
        driver = Cls(args.username, args.api_key)

        entity = get_entity(driver, args.region)
        check = get_check_id(driver, args.region, entity)
        to_ts = get_unix_time_millis()
        from_ts = to_ts - (args.window * 60000)
        counts = get_metric_counts(driver, entity.id, check.id, from_ts, to_ts)

        uptime_pct = float(counts['count_2xx'] + counts['count_other']) / counts['total']

        status.add_metric('uptime_pct', 'double', uptime_pct)
    except:
        status.add_metric('uptime_pct', 'double', -1.0)

    print(status)
