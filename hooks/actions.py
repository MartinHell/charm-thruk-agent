from charmhelpers.core import hookenv
import os
import stat
import pwd
import grp
import subprocess


def log_start(service_name):
    hookenv.log('thruk-agent starting')


def fixpath(path):
    if os.path.isdir(path):
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IXOTH)
    if path != "/":
        fixpath(os.path.split(path)[0])


def pwgen():
    return str(subprocess.check_output(['pwgen', '-s', '16'])).strip()


def fix_livestatus_perms(service_name):
    livestatus_path = hookenv.config('livestatus_path')
    uid = pwd.getpwnam("nagios").pw_uid
    gid = grp.getgrnam("www-data").gr_gid
    os.chown(livestatus_path, uid, gid)
    st = os.stat(livestatus_path)
    os.chmod(livestatus_path, st.st_mode | stat.S_IRGRP)
    fixpath(livestatus_path)


def thruk_set_password(service_name):
    passwd_file = "/var/lib/thruk/thrukadmin.passwd"
    if not os.path.exists(passwd_file):
        password = pwgen()
        with open(passwd_file, 'w') as pfile:
            pfile.write(password)
            os.chmod(pfile.name, 0600)

        ret = subprocess.call(["/usr/bin/htpasswd", "-b", "/etc/thruk/htpasswd",
                              "thrukadmin", password])
        if not ret:
            hookenv.log('WARNING: thruk htpassword reset failed!')
    else:
        with open(passwd_file) as pfile:
            password = pfile.read().strip()
