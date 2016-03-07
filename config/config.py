# -*- coding: utf-8 -*-
import os

TEST = False
PUBKEY_LOCATION = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'id_rsa.pub')
Jenkins_url = 'jenkins_url_here'
DEV = {
    'app-prefix': 'dev-',
    'name': 'dev',
    'marathon_url': 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/marathon-cluster',
    'mesos_url': 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/mesos-cluster',
    'bamboo_url': 'http://192.168.0.170',
    'api_gateway': 'http://192.168.0.165'
}

SIT = {
    'app-prefix': 'sit-',
    'name': 'sit',
    'marathon_url': 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/marathon-cluster',
    'mesos_url': 'zk://192.168.0.119:2181,192.168.0.120:2181,192.168.0.121:2181,192.168.0.122:2181,192.168.0.123:2181/mesos-cluster',
    'bamboo_url': 'http://192.168.0.175',
    'api_gateway': 'http://192.168.0.164'
}

UAT = {
    'app-prefix': 'uat-',
    'name': 'uat',
    'marathon_url': 'zk://172.16.10.35:2181,172.16.10.36:2181,172.16.10.37:2181,172.16.10.38:2181,172.16.10.43:2181/marathon-cluster',
    'mesos_url': 'zk://172.16.10.35:2181,172.16.10.36:2181,172.16.10.37:2181,172.16.10.38:2181,172.16.10.43:2181/mesos-cluster',
    'bamboo_url': 'http://172.16.10.40',
    'api_gateway': 'http://192.168.0.164'
}

PROD = {
    'app-prefix': 'prod-',
    'name': 'prod',
    'marathon_url': 'zk://10.10.12.41:2181,10.10.12.42:2181,10.10.12.43:2181,10.10.12.44:2181,10.10.12.45:2181/marathon-cluster',
    'mesos_url': 'zk://10.10.12.41:2181,10.10.12.42:2181,10.10.12.43:2181,10.10.12.44:2181,10.10.12.45:2181/mesos-cluster',
    'bamboo_url': 'http://192.168.0.170',
    'api_gateway': 'http://192.168.0.164'
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

def env_config_for_zk(zk):
    return filter(lambda env: env['marathon_url'] == zk, envs)[0]

def help_info():
    def format_env_config_info(env):
        return """
    {env_name}:
       Marathon: {marathon}
       Mesos: {mesos}
       Bamboo: {bamboo}
       API-Gateway: {api_gateway}
    """.format(marathon=env['marathon_url'],
               mesos=env['mesos_url'],
               env_name=env['name'],
               api_gateway=env['api_gateway'],
               bamboo=env['bamboo_url'])
    return '    Jenkins Address: ' + Jenkins_url + ''.join(map(format_env_config_info, envs))
