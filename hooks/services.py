#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers

import actions
import thruk_helpers


def manage():
    manager = ServiceManager([
        {
            'service': 'thruk',
            'provided_data': [
                thruk_helpers.ThrukAgentRelation()
            ],
            'required_data': [thruk_helpers.ThrukInfo()],
            'data_ready': [
                helpers.render_template(
                    source='thruk_local.conf',
                    target='/etc/thruk/thruk_local.conf'),
                actions.log_start,
                actions.fix_livestatus_perms,
                actions.thruk_set_password,
            ],
        },
    ])
    manager.manage()
