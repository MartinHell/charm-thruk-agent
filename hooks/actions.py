from charmhelpers.core import hookenv
import os
import stat
import shutils

def log_start(service_name):
    hookenv.log('thruk-agent starting')

def fixpath(path):
    if os.path.isdir(path):
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IXOTH)
    if path != "/":
          fixpath(os.path.split(path)[0])

def fix_livestatus_perms():
    livestatus_path = hookenv.config('livestatus_path')
    shutils.chown(livestatus_path, group="www-data")
    st = os.stat(livestatus_path)
    os.chmod(livestatus_path, st.st_mode | stat.S_IRGRP)
    fixpath(livestatus_path)
