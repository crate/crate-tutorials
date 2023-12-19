.. _debian:

================
Debian GNU/Linux
================

CrateDB actively maintains packages for the following Debian versions:

- `Bookworm`_ (12.x)
- `Bullseye`_ (11.x)
- `Buster`_ (10.x)

This guide will show you how to install, control, and configure a single-node
CrateDB on a local Debian system.

.. rubric:: Table of contents

.. contents::
   :local:


Configure Apt
=============

You need to configure `Apt`_ (the package manager) to trust and to add the
CrateDB repositories:

.. code-block:: sh

   # Add the CrateDB GPG key
   sh$ wget -qO- https://cdn.crate.io/downloads/apt/DEB-GPG-KEY-crate | sudo tee /etc/apt/trusted.gpg.d/crate.asc

   # Add CrateDB repository to Apt
   sh$ echo "deb https://cdn.crate.io/downloads/debian/stable/ default main" | sudo tee /etc/apt/sources.list.d/crate-stable.list

.. NOTE::

   CrateDB provides two repositories. A *stable* and a *testing* repository. To use
   the testing repository, replace ``stable`` with ``testing`` in the command
   above. You can read more about our `release workflow`_.

Now update Apt:

.. code-block:: sh

   sh$ sudo apt update

You should see a success message. This indicates that the CrateDB release
channel is correctly configured and the ``crate`` package has been registered
locally.


Install CrateDB
===============

You can now install CrateDB:

.. code-block:: sh

   sh$ sudo apt install crate

After the installation is finished, you can start the ``crate`` service::

   sh$ sudo systemctl start crate

Once the service is up and running, you can access CrateDB by visiting::


  http://localhost:4200/

.. CAUTION::
   When you install via Apt, CrateDB automatically starts as a single-node
   cluster and you won't be able to add additional nodes. In order to form a
   multi-node cluster, you will need to remove the cluster state after
   changing the configuration.


Control CrateDB
===============

You can control the ``crate`` service with the `systemctl` utility:

.. code-block:: sh

    sh$ sudo systemctl COMMAND crate

Replace ``COMMAND`` with ``start``, ``stop``, ``restart``, ``status`` and so on.
so on.

.. CAUTION::

    Be sure to read the guide to :ref:`rolling upgrades <rolling_upgrade>` and
    :ref:`full restart upgrades <full_restart_upgrade>` before attempting to
    upgrade a running cluster.


Configure CrateDB
=================

In order to configure CrateDB, take note of the configuration file
location and the available environment variables.


Configuration files
-------------------

The main CrateDB `configuration files`_ are located in the ``/etc/crate``
directory.


Environment
-----------

The CrateDB startup script `sources`_ `environment variables`_ from the
``/etc/default/crate`` file. Here is an example:

.. code-block:: sh

   # Heap Size (defaults to 256m min, 1g max)
   CRATE_HEAP_SIZE=2g

   # Maximum number of open files, defaults to 65535.
   # MAX_OPEN_FILES=65535

   # Maximum locked memory size. Set to "unlimited" if you use the
   # bootstrap.mlockall option in crate.yml. You must also set
   # CRATE_HEAP_SIZE.
   MAX_LOCKED_MEMORY=unlimited

   # Additional Java OPTS
   # CRATE_JAVA_OPTS=

   # Force the JVM to use IPv4 stack
   CRATE_USE_IPV4=true


Customized setups
=================

A full list of package files can be obtained with this command::

     sh$ dpkg-query -L crate

If you want to deviate from the way that the ``crate`` package integrates with
your system, we recommend that you go with a `basic tarball installation`_.


.. _Apt: https://wiki.debian.org/Apt
.. _basic tarball installation: https://crate.io/docs/crate/tutorials/en/latest/install.html#install-adhoc
.. _Bookworm: https://www.debian.org/releases/bookworm/
.. _Bullseye: https://www.debian.org/releases/bullseye/
.. _Buster: https://www.debian.org/releases/buster/
.. _configuration files: https://crate.io/docs/crate/reference/en/latest/config/index.html
.. _environment variables: https://crate.io/docs/crate/reference/en/latest/config/environment.html
.. _release workflow: https://github.com/crate/crate/blob/master/devs/docs/release.rst
.. _sources: https://en.wikipedia.org/wiki/Source_(command)
.. _Stretch: https://www.debian.org/releases/stretch/
