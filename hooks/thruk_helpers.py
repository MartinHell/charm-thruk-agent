#!/usr/bin/python

from charmhelpers.core import hookenv
from charmhelpers.core.services import helpers

import hashlib


class ThrukAgentRelation(helpers.RelationContext):
    """
    Relation context for the `thruk-agent` interface.

    :param str name: Override the relation :attr:`name`, since it can vary from charm to charm
    :param list additional_required_keys: Extend the list of :attr:`required_keys`
    """
    name = 'thruk-agent'
    interface = 'thruk-agent'

    def provide_data(self):
        keypath = '/var/lib/thruk/secret.key'
        with open(keypath) as keyfile:
            key = keyfile.read()
            thruk_key = key.rstrip('\n')

        m = hashlib.md5()
        m.update(hookenv.config('nagios_context'))
        thruk_id = m.hexdigest()

        return {
            'host': hookenv.unit_get('private-address'),
            'port': 80,
            'nagios_context': hookenv.config('nagios_context'),
            'thruk_key': thruk_key,
            'thruk_id': thruk_id,
        }


class ThrukInfo(dict):
    def __init__(self):
        self['nagios_context'] = hookenv.config('nagios_context')
        self['livestatus_path'] = hookenv.config('livestatus_path')
        m = hashlib.md5()
        m.update(hookenv.config('nagios_context'))
        self['thruk_id'] = m.hexdigest()
