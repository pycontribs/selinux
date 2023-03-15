# -*- coding: utf-8 -*-

"""That is shim pure-python module that detects and loads the original selinux
package from outside the current virtualenv, avoiding a very common error
inside virtualenvs: ModuleNotFoundError: No module named 'selinux'
"""

__author__ = """Sorin Sbarnea"""
__email__ = "sorin.sbarnea@gmail.com"
__version__ = "0.1.4"

import json
import os
import platform
import subprocess
import sys

try:
    from importlib import reload  # type: ignore  # noqa
except ImportError:  # py < 34
    from imp import reload  # type: ignore  # noqa

import distro


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


def should_have_selinux():
    if platform.system() == "Linux" and os.path.isfile("/etc/selinux/config"):
        if distro.id() not in ["ubuntu", "debian"]:
            return True
    return False


# selinux python library should be loaded only on selinux systems
if should_have_selinux():

    def add_location(location):
        """Try to add a possible location for the selinux module"""
        if os.path.isdir(os.path.join(location, "selinux")):
            with add_path(location):
                # And now we replace outselves with the original selinux module
                reload(sys.modules["selinux"])
                # Validate that we can perform libselinux calls
                if sys.modules["selinux"].is_selinux_enabled() not in [0, 1]:
                    raise RuntimeError("is_selinux_enabled returned error.")
                return True
        return False

    def check_system_sitepackages():
        """Try add selinux module from any of the python site-packages of probably installed python variants"""

        # Here we can add other possible python installation paths
        # The %s will be replaced with the curren python version
        python_paths = [
            "/usr/bin/python%s",
            "/usr/local/bin/python%s"
            ]

        path_check_count = 0
        success = False

        getsitepackages_subprocess = lambda python_path: json.loads(
            subprocess.check_output(
                [
                    python_path,
                    "-c",
                    "import json, site; print(json.dumps(site.getsitepackages()))",
                ]
            ).decode("utf-8")
        )

        # First we'll check for the currently executed python
        tmp = [sys.executable]
        # Then we'll try other commonly used python installation places for the current python version
        for python_path in python_paths:
            tmp.append(
                python_path % ".".join(
                    [str(item) for item in platform.python_version_tuple()[0:2]]
                )
            )
        python_paths = tmp
        del tmp

        # We try to find selinux in all provided paths
        while path_check_count < len(python_paths) and not success:
            try:
                system_sitepackages = getsitepackages_subprocess(python_paths[path_check_count])
                for candidate in system_sitepackages:
                    success = add_location(candidate)
                    if success:
                        break

            except FileNotFoundError:
                # We could not find python under the provided path so we just try the next one
                pass

            finally:
                path_check_count += 1

        if not success:
            raise Exception(
                "Failed to detect selinux python bindings at %s" % " or ".join(python_paths)
            )

    check_system_sitepackages()
