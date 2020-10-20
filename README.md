# MonitoringbyPing

MonitoringbyPing is a tool that can be used to determine if the network devices are currently up and running by simply sending a ping request. After each execution the program sends an email with a list of devices that did not respond to the ping request.

### Installation

MonitoringbyPing requires [Python](https://www.python.org/downloads/) v3.5+ to run.

```py
$ cd MonitoringbyPing
$ pip install -r requirements.txt
$ python setup.py test #run all test cases
$ python setup.py install
```
### Configuration
```py
$ cd monitoringbyping
# edit host_info and config.json file to add email server and host ip infos
```

#### Execute/Run
```py
$ python run.py
```
