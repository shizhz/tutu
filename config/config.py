# -*- coding: utf-8 -*-

Jenkins_url = 'jenkins_url_here'
DEV = {
    'marathon_url': 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/marathon-cluster',
    'mesos_url': 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/mesos-cluster',
    'bamboo_url': 'http://192.168.0.170'
}

SIT = {
    'marathon_url': 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/marathon-cluster',
    'mesos_url': 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/mesos-cluster',
    'bamboo_url': 'http://192.168.0.175'
}

UAT = {
    'marathon_url': 'zk://172.16.10.35:2181,172.16.10.36:2181,172.16.10.37:2181,172.16.10.38:2181,172.16.10.43:2181/marathon-cluster',
    'mesos_url': 'zk://172.16.10.35:2181,172.16.10.36:2181,172.16.10.37:2181,172.16.10.38:2181,172.16.10.43:2181/mesos-cluster',
    'bamboo_url': 'http://172.16.10.40'
}

PROD = {
    'marathon_url': 'zk://10.10.12.41:2181,10.10.12.42:2181,10.10.12.43:2181,10.10.12.44:2181,10.10.12.45:2181/marathon-cluster',
    'mesos_url': 'zk://10.10.12.41:2181,10.10.12.42:2181,10.10.12.43:2181,10.10.12.44:2181,10.10.12.45:2181/mesos-cluster',
    'bamboo_url': 'http://192.168.0.170'
}

CACHE = {

}

envs = [DEV, SIT, UAT, PROD]

envs = [DEV]

marathon_zks = list(set(map(lambda env: env['marathon_url'], envs)))

def help_info():
    return """
    Jenkins Address: {jenkins}

    DEV:
       Marathon: {dev_marathon}
       Mesos: {dev_mesos}
       Bamboo: {dev_bamboo}

    SIT:
       Marathon: {sit_marathon}
       Mesos: {sit_mesos}
       Bamboo: {sit_bamboo}
    """.format(jenkins=Jenkins_url,
               dev_marathon=DEV['marathon_url'],
               dev_mesos=DEV['mesos_url'],
               dev_bamboo=DEV['bamboo_url'],
               sit_marathon=SIT['marathon_url'],
               sit_mesos=SIT['mesos_url'],
               sit_bamboo=SIT['bamboo_url'])
