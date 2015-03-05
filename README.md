uptime-monitor
==============

Monitoring agent plugin to track Nova API uptime. It basically just uses
novaclient to make a flavor-list call and outputs the result in the format
needed Cloud Monitoring.

If the script is able to make the call, the result will have a status of 'OK'.
If the script fails (NOT that the nova call fails) the status is 'FAIL'.

Each call results in one of the following metrics being recorded:

'2xx'     'double'    1
'5xx'     'double'    1
'other'   'double'    1
'error'   'double'    1   # In the case of script failure

Deployment
==========

Servers
-------
(See PasswordSafe for passwords)

Server/Entity   IP                Monitored Regions
---------------------------------------------------
IAD API Check		162.242.230.146		DFW, ORD, LON
DFW API Check		104.130.157.143		IAD
HKG API Check		119.9.93.166		  SYD
SYD API Check		119.9.27.131		  HKG

Cloud Accounts
--------------
(See PasswordSafe for passwords, get api keys from cloud cp)

inframon
inframonuk

Install Agent
-------------
Per instructions found at:
http://www.rackspace.com/knowledge_center/article/install-and-configure-the-cloud-monitoring-agent

Install Dependencies
--------------------
# The agent install actually performs an update, so you can skip this one
apt-get update
apt-get install python-pip python-dev python-netifaces unzip
pip install rackspace-novaclient

Install the nova check agent plugin
-----------------------------------
Because the code is on the internal Rackspace Github, the most straightforward
way is to download the zip of the repo and scp that to the server running
the check.

(This will move to the 'common' group soon)
https://github.rackspace.com/eddie-sheffield/uptime-monitor

(from local box)
scp uptime-monitor-master.zip root@<server>:/root/uptime-monitor-master.zip

(on server as root)
unzip uptime-monitor-master.zip
mkdir -p /usr/lib/rackspace-monitoring-agent/plugins
cp -R ~/uptime-monitor-master/* /usr/lib/rackspace-monitoring-agent/plugins/

Create YAMLs for plugins
------------------------
Note that for the IAD server, since it monitors LON as well as DFW and ORD,
the create_yaml.sh script will need to be run twice, once with the US
regions and credentials and a second time with the LON region and credentials.

cd /usr/lib/rackspace-monitoring-agent/plugins
./create_yaml.sh

Fill in prompts as required. Regions refers to the regions that this server
will be monitoring, not the region the server is in. This can be a
space-separated list and must be all uppercase.

Copy YAMLs to agent config dir
------------------------------
cp /usr/lib/rackspace-monitoring-agent/plugins/etc/rackspace-monitoring-agent.conf.d/* /etc/rackspace-monitoring-agent.conf.d/

Restart the agent
-----------------
service rackspace-monitoring-agent restart

Within each of the Cloud Monitoring entities, there will be checks for each
of the regions monitored by that entity with a label in the form of
'<Region>: Nova API availability test'