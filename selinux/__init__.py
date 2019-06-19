# -*- coding: utf-8 -*-

"""That is shim pure-python module that detects and loads the original selinux
package from outside the current virtualenv, avoiding a very common error
inside virtualenvs: ModuleNotFoundError: No module named 'selinux'
"""

__author__ = """Sorin Sbarnea"""
__email__ = 'sorin.sbarnea@gmail.com'
__version__ = '0.1.5'

import json
import os
import platform
import subprocess
import sys

try:
    from imp import reload
except ImportError:  # py34+
    from importlib import reload


class add_path(object):
    """Context manager for adding path to sys.path"""

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            sys.path.remove(self.path)
        except ValueError:
            pass


def is_selinux_enabled():
    return 0


def is_selinux_mls_enabled():
    return 0


# selinux python library should be loaded only on selinux systems
if platform.system() == 'Linux' and os.path.isfile('/etc/selinux/config'):

    def add_location(location):
        """Try to add a possble location for the selinux module"""
        if os.path.isdir(os.path.join(location, 'selinux')):
            with add_path(location):
                # And now we replace ourselves with the original selinux module
                reload(sys.modules['selinux'])
                # Validate that we can perform libselinux calls
                if sys.modules['selinux'].is_selinux_enabled() not in [0, 1]:
                    raise RuntimeError("is_selinux_enabled returned error.")
                return True
        return False


    def get_system_sitepackages():
        """Get sitepackage locations from sytem python"""
        system_python = "/usr/bin/python%s" % \
                        platform.python_version_tuple()[0]
        fnull = open(os.devnull, 'w')
        try:
            system_sitepackages = json.loads(
                subprocess.check_output([
                    system_python, "-c",
                    "import json, site; print(json.dumps(site.getsitepackages()))"
                ], stderr=fnull  # no need to print error as it will confuse users
                ).decode("utf-8")
            )
        except subprocess.CalledProcessError:
            # Centos/RHEL 6 python2 does not seem to have site.getsitepackages
            system_python_info = json.loads(
                subprocess.check_output([
                    system_python, "-c",
                    "import json, sys; print(json.dumps([sys.prefix, sys.exec_prefix, sys.version_info[:2],"
                    " sys.platform]))"
                ]
                ).decode("utf-8")
            )
            system_prefixes = [
                system_python_info[0],
                system_python_info[1]
            ]
            system_version_info = system_python_info[2]
            # system_platform = system_python_info[3]  # this was used in a couple of getsitepackages versions
            system_sitepackages = getsitepackages(system_prefixes, tuple(system_version_info))
        fnull.close()
        return system_sitepackages

    # Taken directly from python github https://github.com/python/cpython/blob/master/Lib/site.py
    def getsitepackages(prefixes, system_version_info):
        """Returns a list containing all global site-packages directories.
        For each directory present in ``prefixes`` (or the global ``PREFIXES``),
        this function will find its `site-packages` subdirectory depending on the
        system environment, and will return a list of full paths.
        """
        sitepackages = []

        for lib_type in ['lib', 'lib64']:  # centos/rhel also use lib64
            seen = set()
            for prefix in prefixes:
                if not prefix or prefix in seen:
                    continue
                seen.add(prefix)

                if os.sep == '/':
                    sitepackages.append(os.path.join(prefix, lib_type,
                                                     "python%d.%d" % system_version_info,
                                                     "site-packages"))
                else:
                    sitepackages.append(prefix)
                    sitepackages.append(os.path.join(prefix, "lib", "site-packages"))
        return sitepackages


    def check_system_sitepackages():
        """Try add selinux module from any of the python site-packages"""

        success = False
        system_sitepackages = get_system_sitepackages()
        for candidate in system_sitepackages:
            success = add_location(candidate)
            if success:
                break

        if not success:
            raise Exception("Failed to detect selinux python bindings at %s. Is libselinux-python installed?" %
                            system_sitepackages)


    check_system_sitepackages()
