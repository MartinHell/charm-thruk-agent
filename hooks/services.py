#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers
from charmhelpers.core import hookenv

import actions
import thruk_helpers


def manage():
    config = hookenv.config()
    nagios_context = config['nagios_context']
    livestatus_path = config['livestatus_path']
    #print "Context is %s, livestatus_path is %s" % (context, livestatus_path)
    hookenv.log('Context is {}, livestatus_path is {}'.format(nagios_context, livestatus_path))
    manager = ServiceManager([
        {
            'service': 'thruk',
            #'ports': [],  # ports to after start
            'provided_data': [
                # context managers for provided relations
                # e.g.: helpers.HttpRelation()
                thruk_helpers.ThrukAgentRelation()
            ],
            #'required_data': [
                # data (contexts) required to start the service
                # e.g.: helpers.RequiredConfig('domain', 'auth_key'),
                #       helpers.MysqlRelation(),
            #    helpers.RequiredConfig('livestatus_path', 'context')
            #],
            #'required_data': [nagios_context, livestatus_path],
            'required_data': [thruk_helpers.ThrukInfo()],
            'data_ready': [
                helpers.render_template(
                    source='thruk_local.conf',
                    target='/etc/thruk/thruk_local.conf'),
                actions.log_start,
            ],
        },
    ])
    manager.manage()
