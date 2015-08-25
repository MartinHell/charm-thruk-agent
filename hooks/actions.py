from charmhelpers.core import hookenv
import os
import sys
import stat
import pwd
import grp
import subprocess
import hashlib
# import thruk_helpers


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
    if os.path.exists(livestatus_path):
        livestatus_dir = os.path.dirname(livestatus_path)
        uid = pwd.getpwnam("nagios").pw_uid
        gid = grp.getgrnam("www-data").gr_gid
        os.chown(livestatus_path, uid, gid)
        os.chown(livestatus_dir, uid, gid)
        # st = os.stat(livestatus_path)
        # st_dir = os.stat(livestatus_dir)
        os.chmod(livestatus_path, 0770)
        os.chmod(livestatus_dir, 2771)
        fixpath(livestatus_path)
    else:
        hookenv.log("ERROR: livestatus socket doesn't exist")
        sys.exit(1)


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


def notify_thrukmaster_relation(service_name):
    # rel_data = thruk_helpers.ThrukAgentRelation()
    thruk_data = {}

    # Need to check that we actually have a thruk-agent relation
    # before trying to pull out the data
    host = hookenv.unit_get('private-address')
    url = 'http://{}/'.format(host)
    thruk_data['url'] = url

    keypath = '/var/lib/thruk/secret.key'
    with open(keypath) as keyfile:
        key = keyfile.read()
        thruk_key = key.rstrip('\n')
    thruk_data['thruk_key'] = thruk_key

    m = hashlib.md5()
    m.update(hookenv.config('nagios_context'))
    thruk_data['thruk_id'] = m.hexdigest()
    thruk_data['nagios_context'] = hookenv.config('nagios_context')

    for rel_id in hookenv.relation_ids('thruk-agent'):
        hookenv.relation_set(relation_id=rel_id, relation_settings=thruk_data)
