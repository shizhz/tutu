# -*- coding: utf-8 -*-

Jenkins_url = 'jenkins_url_here'
DEV = {
    'marathon_url': 'marathon address in zk',
    'mesos_url': 'mesos cluster address in zk',
    'bamboo_url': 'http://192.168.0.170'
}

DEV = {
    'marathon_url': 'marathon address in zk',
    'mesos_url': 'mesos cluster address in zk',
    'bamboo_url': 'http://192.168.0.170'
}

SIT = {
    'marathon_url': 'marathon address in zk',
    'mesos_url': 'mesos cluster address in zk',
    'bamboo_url': 'http://192.168.0.170'
}

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
