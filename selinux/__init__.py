# -*- coding: utf-8 -*-

"""That is shim pure-python module that detects and loads the original selinux
package from outside the current virtualenv, avoiding a very common error
inside virtualenvs: ModuleNotFoundError: No module named 'selinux'
"""

__author__ = """Sorin Sbarnea"""
__email__ = 'sorin.sbarnea@gmail.com'
__version__ = '0.1.0'

import imp
import os
import platform
import sys
import warnings


if platform.system() == 'Linux':

    if platform.architecture()[0] == '64bit':
        arch = 'lib64'
    else:
        arch = 'lib'

    location = '/usr/%s/python%s/site-packages/selinux' % \
        (arch, ".".join(platform.python_version_tuple()[:2]))

    if not os.path.isdir(location):
        warnings.warn(
            "Failed to detect selinux python bindings at %s" % location)
    else:
        sys.modules['selinux'] = \
            imp.load_source('selinux', location)
