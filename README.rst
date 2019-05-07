.. image:: https://travis-ci.com/pycontribs/selinux.svg?branch=master
    :target: https://travis-ci.com/pycontribs/selinux

# selinux
Pure-python selinux shim module for use in virtualenvs in oder to avoid
failure to load selinux in Ansible modules.

You still need to have libselinux python bindings package installed on your
system for it to work but you no longer have the problem of not being able
to import it from inside isolated (default) virtualenvs.

This package was also tested as installed outside virtualenvs and seems not
to interfere with the original library.

So far testing was done on:
* CentOS 7 - python2
* Fedora 28 - python2 and python3
