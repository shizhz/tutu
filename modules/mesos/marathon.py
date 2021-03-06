## -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import logging
from tornado import gen

import re
import requests
import kazoo.client
import kazoo.exceptions
import requests
import requests.exceptions

from . import exceptions
from . import zookeeper
from .. import log, util
from modules.util import flat_list
from modules.cache import CURRENT as cache
from config.config import marathon_zks, CACHE as cache_cfg, envs, TEST, env_config_for_zk

logger = logging.getLogger('tutu.modules.mesos.' + __name__)

class MarathonResolver(object):
    bucket = {}

    def __init__(self, zk):
        self.zk = zk

    @classmethod
    def is_cached(cls, zk):
        return zk in cls.bucket

    @classmethod
    def cache(cls, zk, addresses):
        cls.bucket[zk] = addresses

    @classmethod
    def clear_cache_for_zk(cls, zk):
        del cls.bucket[zk]

    @classmethod
    def get_addresses_from_cache(cls, zk):
        return cls.bucket[zk]

    def resolve(self):
        if not TEST:
            if not self.is_cached(self.zk):
                hosts, path = self.zk[5:].split("/", 1)
                path = "/" + path + "/leader"

                with zookeeper.client(hosts=hosts, read_only=True) as zk:
                    try:
                        marathon_addresses = map(lambda path: zk.get(path)[0], map(lambda n: '/marathon-cluster/leader/' + n, zk.get_children(path)))
                    except kazoo.exceptions.NoNodeError:
                        log.fatal(INVALID_PATH.format(cfg))

                    self.cache(self.zk, marathon_addresses)
                    return marathon_addresses
            else:
                return self.get_addresses_from_cache(zk)

    def refresh(self):
        self.clear_cache_for_zk(self.zk)
        return self.resolve()


class Marathon(object):
    def __init__(self, zk):
        self.zk = zk
        self.resolver = MarathonResolver(zk)
        self.addresses = self.resolver.resolve()
        self.refreshed = False

    def is_addressa_alive(self, address):
        return requests.get('http://' + address + '/ping').ok

    def get_marathon_address(self):
        for address in self.addresses:
            if self.is_addressa_alive(address):
                return 'http://' + address

        if not self.refreshed:
            self.refreshed = True
            self.addresses = self.resolver.refresh()
            return self.get_marathon_address()

        raise MarathonConnectionException("None of these address works `{0}`, please check whether marathon is alive".format(','.join(self.addresses)))

    def resolve_apps(self):
        return map(lambda mi: MarathonApp(self, mi), requests.get(self.get_marathon_address() + '/v2/apps').json()['apps']) if not TEST else []


    def apps_by_id_pattern(self, pattern):
        logger.debug('Filtering apps by app id pattern: {0}'.format(str(pattern)))
        pattern = '.*' + pattern if pattern.endswith('$') else pattern + '.*' if pattern.startswith('^') else pattern
        return filter(lambda app: re.match(pattern, app.id) or pattern in app.id, self.apps())

    def apps_by_id_patterns(self, patterns):
        return flat_list(map(lambda p: self.apps_by_id_pattern(p), patterns))

    @gen.coroutine
    def register_callback(self, callback):
        registry_url = self.get_marathon_address().rstrip('/') + '/v2/eventSubscriptions?callbackUrl=' + callback
        logger.debug('Registerring callback: {0}'.format(registry_url))
        requests.post(registry_url, headers={'Content-Type': 'application/json; charset=utf-8'})

    @property
    def id(self):
        return self.zk

    @property
    def cache_key(self):
        return cache_cfg.get('APPS_PREFIX') + self.id

    def contains_ip(self, ip):
        return ip in map(lambda address: address.split(':')[0], self.addresses)

    def apps(self):
        if not cache.is_cached(self.cache_key):
            cache.set_cache(self.cache_key, self.resolve_apps())

        return cache.get_cache(self.cache_key)

class BaseInfo(object):
    def _val_of_key(self, key):
        return util.val_from_json(self.info, key)

    def _has_val(self, key):
        return self._val_of_key(key) is not None

class MarathonTask(BaseInfo):
    def __init__(self, app, task_info):
        self.app = app
        self.task_info = task_info

    @property
    def info(self):
        return self.task_info

    @property
    def app_id(self):
        return self._val_of_key('appId')

    @property
    def id(self):
        return self._val_of_key('id')

    @property
    def host(self):
        return self._val_of_key('host')

    @property
    def ports(self):
        return self._val_of_key('ports')

    @property
    def started_at(self):
        return self._val_of_key('startedAt')

    @property
    def staged_at(self):
        return self._val_of_key('stagedAt')

    def __str__(self):
        return """
        Actual Service Address:
                {0}
        Started at: {1} """.format('\n\t\t'.join(map(lambda port: 'http://' + self.host + ":" + str(port), self.ports)), self.started_at)

class MarathonApp(BaseInfo):
    def __init__(self, marathon, app_info):
        self.marathon = marathon
        self.app_info = app_info

    @property
    def info(self):
        return self.app_info

    @property
    def id(self):
        return self.app_info['id'][1:]

    def env_config(self):
        evs = filter(lambda e: e.get('app-prefix') and self.id.startswith(e.get('app-prefix')), envs)

        return evs[0] if len(evs) > 0 else env_config_for_zk(self.marathon.zk)

    def api_gateway_address(self):
        api_gateway = self.env_config()['api_gateway']
        apis_url = api_gateway + ':8001/apis'
        apis_data = None
        try:
            logger.debug('Fetching all api data from: {0}'.format(apis_url))
            apis_data = requests.get(apis_url).json()
            all_apis = apis_data['data']
            if apis_data.has_key('data'):
                bamboo_addresses = self.bamboo_addresses()

                apis = filter(lambda api: api.get('upstream_url') in bamboo_addresses, all_apis)

                api_info = [api_gateway + ':8000' + api['request_path'] for api in apis]

                logger.debug('Found api address: {0}'.format(str(api_info)))

                return api_info
            elif apis_data.has_key('message'):
                logger.warn("Seems something wrong's happening on API-Gateway: {0}".format(apis_url))
                return ['Message got from API-Gateway: {0}'.format(apis_url)]
            else:
                logger.warn("Response from API-Gateway: {0}".format(str(apis_data)))
                return ['Unexcepted response from API-Gateway: {0}'.format(str(apis_data))]
        except requests.ConnectionError, e:
            logger.exception(e)
            logger.warn('Cannt connect to api-gateway: {0}'.format(apis_url))
            return ["Cann't connect to API-Gateway :{0}".format(apis_url)]

    def bamboo_addresses(self):
        bamboo_address = self.env_config()['bamboo_url']
        if self._has_val('env.BAMBOO_HTTP_PORTS'):
            bamboo_ports = self._val_of_key('env.BAMBOO_HTTP_PORTS').split(',')

            return [bamboo_address + ':' + port for port in bamboo_ports]

        return []

    def str_api_gateway_address(self):
        api_gateway = self.api_gateway_address()
        return '\n\t'.join(api_gateway) if api_gateway else 'Not configured behinded API-Gateway yet.'

    def str_bamboo_address(self):
        if self._has_val('env.BAMBOO_HTTP_PORTS'):
            bamboo_addresses = self.bamboo_addresses()
            docker_port_mappings = map(lambda dp: dp['containerPort'], self._val_of_key("container.docker.portMappings"))

            mappings = []

            for i in range(len(docker_port_mappings)):
                mappings.append("Service on Port: " + str(docker_port_mappings[i]) + " is on Bamboo:  " + bamboo_addresses[i])

            return '\n\t'.join(mappings)
        else:
            return "No bamboo config found"

    @property
    def tasks(self):
        # TODO: consider cache task info to speed up.
        tasks_url = self.marathon.get_marathon_address().rstrip('/') + '/v2/apps/' + self.id + '/tasks'
        logger.debug('Fetching task info for {0} : {1}'.format(self.id, tasks_url))
        return map(lambda t: MarathonTask(self, t), requests.get(tasks_url).json()['tasks'])

    def task_info(self):
        return '\n\t'.join(map(str, self.tasks))

    @property
    def cpus(self):
        return self._val_of_key('cpus')

    @property
    def mem(self):
        return self._val_of_key('mem')

    @property
    def instances(self):
        return self._val_of_key('instances')

    def is_dockerized(self):
        return self._has_val('container') and self._val_of_key('container.type') == 'DOCKER'

    def docker_container_info(self):
        if self.is_dockerized():
            return DockerContainerInfo(self._val_of_key('container'))
        else:
            return None

    def container_info(self, verbose=False):
        ci = self.docker_container_info()
        return ci.to_str(verbose=verbose) if ci else "<No Container Info>"

    @property
    def version(self):
        return self._val_of_key('version')

class DockerVolumeInfo(BaseInfo):
    def __init__(self, volume_info):
        self.volume_info = volume_info

    @property
    def info(self):
        return self.volume_info

    @property
    def container_path(self):
        return self._val_of_key('containerPath')

    @property
    def host_path(self):
        return self._val_of_key('hostPath')

    @property
    def mode(self):
        return self._val_of_key('mode')

    def __str__(self):
        return "{0} -> {1}, Mode: {2}".format(self.container_path, self.host_path, self.mode)

class DockerContainerInfo(BaseInfo):
    def __init__(self, docker_info):
        self.docker_info = docker_info

    @property
    def info(self):
        return self.docker_info

    @property
    def volumes(self):
        return map(lambda v: DockerVolumeInfo(v), self._val_of_key('volumes'))

    @property
    def image(self):
        return self._val_of_key('docker.image')

    @property
    def network(self):
        return self._val_of_key('docker.network')

    @property
    def port_mappings(self):
        return self._val_of_key('docker.portMappings')

    def str_port_mappings(self):
        if self.port_mappings:
            pm = map(lambda pm: "{0} -> {1}".format(pm['containerPort'], "Random Port Mapping" if pm['hostPort'] == 0 else pm['hostPort']), self.port_mappings)
            return '\n\t\t'.join(pm)
        else:
            return "No port mappings found"

    def str_volumes(self):
        return '\n\t\t'.join(map(str, self.volumes))

    @property
    def privileged(self):
        return self._val_of_key('docker.privileged') == 'true'

    @property
    def parameters(self):
        return self._val_of_key('docker.parameters')

    def str_parameters(self):
        return '\n\t\t'.join(["{0} : {1}".format(x['key'], x['value']) for x in self.parameters])

    @property
    def force_pull_image(self):
        return self._val_of_key('docker.forcePullImage') == 'true'

    def __str__(self):
        return """
        Image: {0}
        Network: {1}
        Privileged: {2}
        Force pull image: {3}
        Port Mappings:
                {4}
        Volumes:
                {5}
        Parameters:
                {6}
        """.format(self.image, self.network, self.privileged, self.force_pull_image, self.str_port_mappings(), self.str_volumes(), self.str_parameters())

    def to_str(self, verbose=False):
        return """
        Image: {0}
        Port Mappings:
                {1}
        Volumes:
                {2}
        """.format(self.image, self.str_port_mappings(), self.str_volumes()) if not verbose else str(self)


marathons = map(lambda zk: Marathon(zk), marathon_zks)

def marathon_of_env(env):
    for e in envs:
        if e.get('name') == env.lower():
            return filter(lambda m: m.zk == e.get('marathon_url'), marathons)[0]
