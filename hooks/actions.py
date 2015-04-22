from charmhelpers.core import hookenv
import os
import stat
import pwd
import grp

def log_start(service_name):
    hookenv.log('thruk-agent starting')

def fixpath(path):
    if os.path.isdir(path):
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IXOTH)
    if path != "/":
          fixpath(os.path.split(path)[0])

def fix_livestatus_perms(service_name):
    livestatus_path = hookenv.config('livestatus_path')
    uid = pwd.getpwnam("nagios").pw_uid
    gid = grp.getgrnam("www-data").gr_gid
    os.chown(livestatus_path, uid, gid)
    st = os.stat(livestatus_path)
    os.chmod(livestatus_path, st.st_mode | stat.S_IRGRP)
    fixpath(livestatus_path)
