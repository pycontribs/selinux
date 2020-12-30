.. image:: https://zuul-ci.org/gated.svg
    :target: https://dashboard.zuul.ansible.com/t/ansible/builds?project=pycontribs/selinux

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/python/black
   :alt: Python Black Code Style

selinux
=======

Pure-python selinux **shim** module for use in virtualenvs in order to avoid
failure to load selinux in Ansible modules.

You still need to have libselinux python bindings package installed on your
system for it to work but you no longer have the problem of not being able
to import it from inside isolated (default) virtualenvs.

This package was also tested as installed outside virtualenvs and seems not
to interfere with the original library.

So far testing is done on:

* CentOS 7
* CentOS 8
* Debian (latest)
* Fedora 28
* RHEL 8
* Ubuntu (latest)

The change-list can be accessed at `releases`__.

__ https://github.com/pycontribs/selinux/releases
