# -*- coding: utf-8 -*-

TEST = False
Jenkins_url = 'jenkins_url_here'
DEV = {
    'app-prefix': 'dev-',
    'name': 'dev',
    'marathon_url': 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/marathon-cluster',
    'mesos_url': 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/mesos-cluster',
    'bamboo_url': 'http://192.168.0.170'
}

SIT = {
    'app-prefix': 'sit-',
    'name': 'sit',
    'marathon_url': 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/marathon-cluster',
    'mesos_url': 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/mesos-cluster',
    'bamboo_url': 'http://192.168.0.175'
}

UAT = {
    'app-prefix': 'uat-',
    'name': 'uat',
    'marathon_url': 'zk://172.16.10.35:2181,172.16.10.36:2181,172.16.10.37:2181,172.16.10.38:2181,172.16.10.43:2181/marathon-cluster',
    'mesos_url': 'zk://172.16.10.35:2181,172.16.10.36:2181,172.16.10.37:2181,172.16.10.38:2181,172.16.10.43:2181/mesos-cluster',
    'bamboo_url': 'http://172.16.10.40'
}

PROD = {
    'app-prefix': 'prod-',
    'name': 'prod',
    'marathon_url': 'zk://10.10.12.41:2181,10.10.12.42:2181,10.10.12.43:2181,10.10.12.44:2181,10.10.12.45:2181/marathon-cluster',
    'mesos_url': 'zk://10.10.12.41:2181,10.10.12.42:2181,10.10.12.43:2181,10.10.12.44:2181,10.10.12.45:2181/mesos-cluster',
    'bamboo_url': 'http://192.168.0.170'
}

CACHE = {
    'APPS_PREFIX': 'marathon-apps-'
}

envs = [DEV, SIT, UAT, PROD]

envs = [DEV, SIT]

marathon_zks = list(set(map(lambda env: env['marathon_url'], envs)))

def env_config_of(env_name):
    evs = filter(lambda e: e['name'] == env_name, envs)

    return evs[0] if len(evs) > 0 else None

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
