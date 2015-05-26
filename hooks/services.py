#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers
from charmhelpers.core import hookenv

import actions
import thruk_helpers


def manage():
    config = hookenv.config()
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
                actions.notify_thrukmaster_relation,
            ],
        },
        {
            'service': 'thruk-monitoring',
            'required_data': [
                thruk_helpers.NEMRelation(),
                helpers.RequiredConfig(),
            ],
            'data_ready': [
                helpers.render_template(
                    source='thruk-nrpe.j2',
                    target='/etc/nagios/nrpe.d/check_{}.cfg'.format(
                       hookenv.local_unit().replace('/', '-'),
                    )
                ),
                helpers.render_template(
                    source='thruk-nagios.j2',
                    target='/var/lib/nagios/export/service__{}-{}.cfg'.format(
                        config['nagios_context'],
                        hookenv.local_unit().replace('/', '-'),
                    )
                ),
            ],
         },
    ])
    manager.manage()
