# Overview

This charm is intended to enable a Thruk(http://www.thruk.org/) web interface to a Nagios 
unit.  Essentially, it enables the Nagios unit to be consolidated into a Thruk view using 
a thruk-master charm.  You can use the local thruk directly, but it is not the intended 
use of the charm.

# Usage

Step by step instructions on using the charm:

    juju deploy nagios
    juju deploy thruk-agent
    juju deploy thruk-master
    juju add-relation nagios thruk-agent
    juju add-relation thruk-master thruk-agent

Then you should be able to go to http://<ip of thruk-master>/thruk/ and see the webui.

# Configuration

There are a handful of config options

* source - the PPA to install Thruk from

* nagios_context - the identifying string for this nagios instance

* livestatus_path - the path to the livestatus socket

# Contact Information

- Upstream website: http://www.thruk.org/
- Upstream bug tracker: https://github.com/sni/Thruk/issues
- Upstream mailing list: https://groups.google.com/forum/#!forum/thruk
