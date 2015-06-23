=======
 Usage
=======

The `withenv` package installs the `we` executable. Here is the basic
usage.


.. code-block:: bash

   $ we --env foo.yml printenv

The YAML in `foo.yml` gets loaded and applied to the environment. If
the value already exists in the environment, that value will be
overwritten.

You can also use a directory of YAML files.

.. code-block:: bash

   $ we --dir myenv printenv

The files will be applied to the environment in alphabetical order.

You can shorten the flags as well as mixing files and directories.

.. code-block:: bash

   $ we -e foo.yml -d bar -e baz.yml printenv

Each flag will be applied in order from left to right.


YAML Format
===========

You can use a hash or list of hashes in your YAML file. For example:

.. code-block:: yaml

   ---
   FOO: bar
   BAR: hello $FOO

It is not recommended to use a hash in this format because the order
cannot be gauranteed, although, it will probably work just fine. If
you need explicit ordering within your file, use a list of hashes.

.. code-block:: yaml

   ---
   - FOO: bar
   - BAR: hello $FOO


Creating an Alias
=================

Sometimes you'll find that your environment is composed of a suite of
details. Say for example, you were deploying an application via some
script that uses environment variables to choose what region, cloud
account and process to run.

.. code-block:: bash

   $ we -d envs/apps/foo \
        -e envs/acct/dev.yml \
	-e envs/regions/us-east \
	./create-app-server

We can create an alias for this by creating an alias YAML file.

.. code-block:: yaml

   # myalias.yml
   ---
   - directory: envs/apps/foo
   - file: envs/acct/dev.yml
   - file: envs/regions/us-east

We can then run our command with a shortened `we` command.

.. code-block:: bash

   $ we -a myalias create-app-server
