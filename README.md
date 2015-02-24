uptime-monitor
==============

Monitoring agent plugin to track Nova API uptime. It basically just uses
novaclient to make a flavor-list call and outputs the result in the format
needed Cloud Monitoring.

If the script is able to make the call, the result will have a status of 'OK'.
If the script fails (NOT that the nova call fails) the status is 'FAIL'.

There is always a metric (int32) recorded named 'api_ok' with one of
three values:

 1 = nova call succeeded (non-5xx response)
 0 = nova call failed (5xx response)
-1 = script encountered another error, nova status unknown

In the case of nova call failed (0) there is another metric, the actual
response code. This is a uint32 value with name 'http_status'.

The http status is not recorded on non-5xx responses since it isn't always
available.

Requirements
============

Install:
  - apt-get install python-pip python-dev, python-netifaces
  - pip install rackspace-novaclient

