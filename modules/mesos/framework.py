# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

class Framework(object):
    def __init__(self, items):
        self.__items = items

    def __getitem__(self, name):
        return self.__items[name]

    def __str__(self):
        return "{0}:{1}".format(self.name, self.id)

    @property
    def id(self):
        return self['id']

    @property
    def name(self):
        return self['name']

    @property
    def hostname(self):
        return self['hostname']

    @property
    def active(self):
        return self['active']

    @property
    def task_count(self):
        return len(self['tasks'])

    @property
    def user(self):
        return self['user']

    @property
    def cpu_allocated(self):
        return self._resource_allocated("cpus")

    @property
    def mem_allocated(self):
        return self._resource_allocated("mem")

    @property
    def disk_allocated(self):
        return self._resource_allocated("disk")

    def _resource_allocated(self, resource):
        return self["resources"][resource]

