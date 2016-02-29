## -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import kazoo.client
import kazoo.exceptions
import requests
import requests.exceptions

from .. import log

from . import zookeeper

class MarathonResolver(object):
    def __init__(self, zk):
        self.zk = zk

    def resolve(self):
        hosts, path = self.zk[5:].split("/", 1)
        path = "/" + path + "/leader"

        with zookeeper.client(hosts=hosts, read_only=True) as zk:
            try:
                marathon_addresses = map(lambda path: client.get(path)[0], map(lambda n: '/marathon-cluster/leader/' + n, zk.get_children(path)))
            except kazoo.exceptions.NoNodeError:
                log.fatal(INVALID_PATH.format(cfg))

            return marathon_addresses

class MarathonMaster(object):
    def __init__(self, addresses):
        self.addresses = addresses
