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

=======
History
=======

0.1.5 (2019-05-28)
------------------

* Updated Trove classifiers
* Refactored the generation of package metadata when build from source
* Marked release as stable

0.1.2 (2019-04-13)
------------------

* First version that can really detect selinux on system and load it, allowing
  users of isolated virtualenvs to be able to load selinux.
* Library is supoosed to load nothing on non-Linux systems
* Only one warning is raised if the library failes to find system selinux

0.1.0 (2019-03-12)
------------------

* First release on PyPI.
