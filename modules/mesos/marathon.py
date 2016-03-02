## -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import logging
from tornado import gen

import requests
import kazoo.client
import kazoo.exceptions
import requests
import requests.exceptions

from . import zookeeper
from .. import log, util
from modules.cache import CURRENT as cache
from config.config import marathon_zks, CACHE as cache_cfg, envs, TEST

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
        return map(MarathonApp, requests.get(self.get_marathon_address() + '/v2/apps').json()['apps']) if not TEST else []

    def ids_of_apps(self):
        return map(lambda app: app['id'][1:], self.apps())

    def app_by_id(self, app_id):
        app = filter(lambda app: app_id in app['id'], self.apps())

        if not app:
            raise AppNotFoundException(app_id)

        return MarathonApp(app[0])

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

class MarathonApp(BaseInfo):
    def __init__(self, app_info):
        self.app_info = app_info

    @property
    def info(self):
        return self.app_info

    @property
    def id(self):
        return self.app_info['id'][1:]

    def access_address(self, bamboo_address):
        if self._has_val('env.BAMBOO_HTTP_PORTS'):
            bamboo_ports = self._val_of_key('env.BAMBOO_HTTP_PORTS').split(',')
            docker_port_mappings = self._val_of_key("container.docker.portMappings")
            return [dp["containerPort"] + ' -> ' + bamboo_address + ':' + bp.strip() for dp in docker_port_mappings for bp in bamboo_ports]

    @property
    def cpus(self):
        return self._val_of_key('cpus')

    @property
    def instances(self):
        return self._val_of_key('instances')

    def docker_container_info(self):
        if self._has_val('container') and self._val_of_key('container.type') == 'DOCKER':
            return DockerContainerInfo(self._val_of_key('container'))
        else:
            return None

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

class DockerContainerInfo(BaseInfo):
    def __init__(self, docker_info):
        self.docker_info

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

    @property
    def privileged(self):
        return self._val_of_key('docker.privileged') == 'true'

    def parameters(self):
        return self._val_of_key('docker.parameters')

    @property
    def force_pull_image(self):
        return self._val_of_key('docker.forcePullImage') == 'true'


marathons = map(lambda zk: Marathon(zk), marathon_zks)

def marathon_of_env(env):
    for e in envs:
        if e.get('name') == env.lower():
            return filter(lambda m: m.zk == e.get('marathon_url'), marathons)[0]
