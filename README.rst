=======
withenv
=======

.. image:: https://travis-ci.org/ionrock/withenv.png?branch=master
        :target: https://travis-ci.org/ionrock/withenv

.. image:: https://pypip.in/d/withenv/badge.png
        :target: https://pypi.python.org/pypi/withenv


We use environment variables all the time, but they can be painful to
maintain because a shell is sticky. It is too easy to set an
environment variable in your shell, only to have that variable stick
around when you change projects.

`withenv` aims to help this problem by providing a simple way to
prefix commands targeting YAML files that will be added to the
environment prior to the command running.

Usage
=====

The `withenv` package installs the `we` executable. Here is the basic
usage.


.. code-block:: bash

   $ we --environment foo.yml printenv

The YAML in `foo.yml` gets loaded and applied to the environment. If
the value already exists in the environment, that value will be
overwritten.

You can also use a directory of YAML files.

.. code-block:: bash

   $ we --directory myenv printenv

The files will be applied to the environment in alphabetical order.

You can shorten the flags as well as mixing files and directories.

.. code-block:: bash

   $ we -e foo.yml -d bar/ -e baz.yml printenv

Each flag will be applied in order from left to right.






* Free software: BSD license
* Documentation: https://withenv.readthedocs.org.
