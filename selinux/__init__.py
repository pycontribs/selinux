# -*- coding: utf-8 -*-

"""That is shim pure-python module that detects and loads the original selinux
package from outside the current virtualenv, avoiding a very common error
inside virtualenvs: ModuleNotFoundError: No module named 'selinux'
"""

__author__ = """Sorin Sbarnea"""
__email__ = 'sorin.sbarnea@gmail.com'
__version__ = '0.1.3'

import os
import platform
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


if platform.system() == 'Linux':

    if platform.architecture()[0] == '64bit':
        arch = 'lib64'
    else:
        arch = 'lib'

    location = '/usr/%s/python%s/site-packages' % \
        (arch, ".".join(platform.python_version_tuple()[:2]))

    if not os.path.isdir(location):
        raise Exception(
            "Failed to detect selinux python bindings at %s" % location)
    else:
        with add_path(location):
            # And now we replace outselves with the original selinux module
            reload(sys.modules['selinux'])
            # Validate that we can perform libselinux calls
            if sys.modules['selinux'].is_selinux_enabled() not in [0, 1]:
                raise RuntimeError("is_selinux_enabled returned error.")
