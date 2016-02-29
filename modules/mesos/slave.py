# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

import urlparse

import requests
import requests.exceptions

from .. import log, util
from . import exceptions


class MesosSlave(object):

    def __init__(self, items):
        self.__items = items

    def __getitem__(self, name):
        return self.__items[name]

    def __str__(self):
        return self.key()

    def key(self):
        return self["pid"].split('@')[-1]

    @property
    def host(self):
        return "{0}://{1}:{2}".format(
            CFG["scheme"],
            self["hostname"],
            self["pid"].split(":")[-1])

    @log.duration
    def fetch(self, url, **kwargs):
        try:
            return requests.get(urlparse.urljoin(
                self.host, url), timeout=CFG["response_timeout"], **kwargs)
        except requests.exceptions.ConnectionError:
            raise exceptions.SlaveDoesNotExist(
                "Unable to connect to the slave at {0}".format(self.host))

    @util.CachedProperty(ttl=5)
    def state(self):
        return self.fetch("/slave(1)/state.json").json()

    @property
    def frameworks(self):
        return util.merge(self.state, "frameworks", "completed_frameworks")

    def task_executor(self, task_id):
        for fw in self.frameworks:
            for exc in util.merge(fw, "executors", "completed_executors"):
                if task_id in list(map(
                        lambda x: x["id"],
                        util.merge(
                            exc, "completed_tasks", "tasks", "queued_tasks"))):
                    return exc
        raise exceptions.MissingExecutor("No executor has a task by that id")

    def file_list(self, path):
        # The sandbox does not exist on the slave.
        if path == "":
            return []

        resp = self.fetch("/files/browse.json", params={"path": path})
        if resp.status_code == 404:
            return []
        return resp.json()

    def file(self, task, path):
        return mesos_file.File(self, task, path)

    @util.CachedProperty(ttl=1)
    def stats(self):
        return self.fetch("/monitor/statistics.json").json()

    def executor_stats(self, _id):
        return list(filter(lambda x: x["executor_id"]))

    def task_stats(self, _id):
        eid = self.task_executor(_id)["id"]
        stats = list(filter(
            lambda x: x["executor_id"] == eid,
            self.stats
        ))

        # Tasks that are not yet in a RUNNING state have no stats.
        if len(stats) == 0:
            return {}
        else:
            return stats[0]["statistics"]

    @property
    @util.memoize
    def log(self):
        return mesos_file.File(self, path="/slave/log")
