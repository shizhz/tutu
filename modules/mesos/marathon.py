## -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import logging
from tornado import gen

import requests
import kazoo.client
import kazoo.exceptions
import requests
import requests.exceptions

from .. import log, util

from . import zookeeper

logger = logging.getLogger('tutu.modules.mesos.' + __name__)

class MarathonResolver(object):
    # TODO: Is there a thread safe problem?
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

    def apps(self):
        # TODO: consider cache the result for a short time like 10 seconds for speed (If there are more than 1 requests within that time)
        return requests.get(self.get_marathon_address() + '/v2/apps').json()['apps']

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

class MarathonApp(object):
    def __init__(self, marathon, app_info):
        self.app_info = app_info
        self.marathon = marathon

    def _val_of_key(self, key):
        return util.val_from_json(self.app_info, key)

    def _has_val(self, key):
        return self._val_of_key(key) is not None

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
