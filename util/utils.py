import os,getpass,stat,sys
import re
import time, datetime
import random
import inspect
import subprocess


def check_group():
    import grp
    user = getpass.getuser()
    groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
    if 'sysop' in groups:
        return True

    return False


def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, universal_newlines=True)
    output, error = process.communicate()
    retcode = process.poll()
    if retcode:
        raise subprocess.CalledProcessError(retcode, inspect.currentframe().f_back.f_code.co_name)
    return output


def get_support_version():
    command = 'echo -e "select XXX from XXX where ba_adap_id like \'XXX\';" |sqlplus -S omc/\'%s\'' % "db_pwd"
    versions = execute_command(command).strip().split('\n')
    support_version = versions[2]
    log.debug('support version : %s' % support_version)
    return support_version

def str_byte_convert():
    """str to byte"""
    a = b'hello'
    b = 'world'

    """str to byte"""
    b.encode(encoding='utf-8')
    bytes(b)

    """byte to str"""
    bytes.decode(b)
    str(b, encoding='utf-8')
