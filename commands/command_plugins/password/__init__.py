# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
#  Copyright (c) 2011 Openstack, LLC.
#  All Rights Reserved.
#
#     Licensed under the Apache License, Version 2.0 (the "License"); you may
#     not use this file except in compliance with the License. You may obtain
#     a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#     WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#     License for the specific language governing permissions and limitations
#     under the License.
#

"""
password commands plugin
"""

import base64
import binascii
import os
import subprocess
from Crypto.Cipher import AES
import crypt

import commands

# This is to support older python versions that don't have hashlib
try:
    import hashlib
except ImportError:
    import md5

    class hashlib(object):
        """Fake hashlib module as a class"""

        @staticmethod
        def md5():
            return md5.new()


class PasswordError(Exception):
    """
    Class for password command exceptions
    """

    def __init__(self, response):
        # Should be a (ResponseCode, ResponseMessage) tuple
        self.response = response

    def __str__(self):
        return "%s: %s" % self.response

    def get_response(self):
        return self.response


def _make_salt(length):
    """Create a salt of appropriate length"""

    salt_chars = 'abcdefghijklmnopqrstuvwxyz'
    salt_chars += 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    salt_chars += '0123456789./'

    rand_data = os.urandom(length)
    salt = ''
    for c in rand_data:
        salt += salt_chars[ord(c) % len(salt_chars)]
    return salt


def _create_temp_password_file(user, password, filename):
    """Read original passwd file, generating a new temporary file.

    Returns: The temporary filename
    """

    with open(filename) as f:
        file_data = f.readlines()
    stat_info = os.stat(filename)
    tmpfile = '%s.tmp.%d' % (filename, os.getpid())

    # We have to use os.open() so that we can create the file with
    # the appropriate modes.  If we create it and set modes later,
    # there's a small point of time where a non-root user could
    # potentially open the file and wait for data to be written.
    fd = os.open(tmpfile,
            os.O_CREAT | os.O_TRUNC | os.O_WRONLY,
            stat_info.st_mode)
    f = None
    success = False
    try:
        os.chown(tmpfile, stat_info.st_uid, stat_info.st_gid)
        f = os.fdopen(fd, 'w')
        for line in file_data:
            if line.startswith('#'):
                f.write(line)
                continue
            try:
                (s_user, s_password, s_rest) = line.split(':', 2)
            except ValueError:
                f.write(line)
                continue
            if s_user != user:
                f.write(line)
                continue
            if s_password.startswith('$'):
                # Format is '$ID$SALT$HASH' where ID defines the
                # ecnryption type.  We'll re-use that, and make a salt
                # that's the same size as the old
                salt_data = s_password[1:].split('$')
                salt = '$%s$%s$' % (salt_data[0],
                        _make_salt(len(salt_data[1])))
            else:
                # Default to MD5 as a minimum level of compatibility
                salt = '$1$%s$' % _make_salt(8)
            enc_pass = crypt.crypt(password, salt)
            f.write("%s:%s:%s" % (s_user, enc_pass, s_rest))
        f.close()
        f = None
        success = True
    except Exception, e:
        logging.error("Couldn't create temporary password file: %s" % str(e))
        raise
    finally:
        if not success:
            # Close the file if it's open
            if f:
                try:
                    os.unlink(tmpfile)
                except Exception:
                    pass
            # Make sure to unlink the tmpfile
            try:
                os.unlink(tmpfile)
            except Exception:
                pass

    return tmpfile


def set_password(user, password):
    """Set the password for a particular user"""

    INVALID = 0
    PWD_MKDB = 1
    RENAME = 2

    files_to_try = {'/etc/shadow': RENAME,
            '/etc/master.passwd': PWD_MKDB}

    for filename, ftype in files_to_try.iteritems():
        if not os.path.exists(filename):
            continue
        tmpfile = _create_temp_password_file(user, password, filename)
        if ftype == RENAME:
            bakfile = '/etc/shadow.bak.%d' % os.getpid()
            os.rename(filename, bakfile)
            os.rename(tmpfile, filename)
            os.remove(bakfile)
            return
        if ftype == PWD_MKDB:
            pipe = subprocess.PIPE
            p = subprocess.Popen(['/usr/sbin/pwd_mkdb', tmpfile],
                    stdin=pipe, stdout=pipe, stderr=pipe)
            (stdoutdata, stderrdata) = p.communicate()
            if p.returncode != 0:
                if stderrdata:
                    stderrdata.strip('\n')
                else:
                    stderrdata = '<None>'
                logging.error("pwd_mkdb failed: %s" % stderrdata)
                try:
                    os.unlink(tmpfile)
                except Exception:
                    pass
                raise PasswordError(
                        (500, "Rebuilding the passwd database failed"))
            return
    raise PasswordError((500, "Unknown password file format"))


@commands.command_add('password', 'password')
def password_cmd(data_values):
    """ change password """
    try:
        set_password('root', data)
    except PasswordError, e:
        return e.get_response()

    return True
