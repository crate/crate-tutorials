
==================================
Installation
==================================

.. contents::
   :local:
   :depth: 1

Prerequisites
=============

CrateDB requires a `Java virtual machine`_ to run.

- For CrateDB version 4.2 and newer
   
    - `Java virtual machine`_ is bundled with CrateDB and no extra installation is necessary.

- For CrateDB version 3.0 to 4.1 
   
   - `Java 11`_ installation is required. We recommend using `Oracle's Java`_ on macOS and Microsoft Windows and OpenJDK_ on Linux Systems. Earlier versions required Java 8.



Basic Installation
===================

For Linux, Micrsoft Windows and macOS

#. Download `the latest CrateDB release`_.
#. Once downloaded, expand the tarball

    * using the sh 
    
    .. code-block:: sh

       tar -xzf crate-*.tar.gz
    
    * using a tool like `7-Zip`_.
  
#. In the console change into the resulting crate directory

    .. code-block:: sh

       cd crate-*

#. Run CrateDB as single instance bound to the local IP address

   .. code-block:: sh

      ./bin/crate

#. You should be able to access it from your local machine by visiting ``http://localhost:4200/``

#. With :kbd:`ctrl-c` you can stop CrateDB

.. SEEALSO::

      Consult the `CrateDB reference documentation`_ for help using this command.

.. NOTE::

      Other releases of CrateDB are `also available`_. Check out the `release notes`_ for specific information about each CrateDB release.
   
Next steps
###########

Now you have CrateDB up and running, :ref:`take the guided tour <use>`.

Ubuntu and Debian (using APT) 
===============================

Configure APT
#############

You need to configure `APT`_ (the package manager) to trust and to add the
CrateDB repositories:

.. code-block:: sh

   # Download the CrateDB GPG key
   wget https://cdn.crate.io/downloads/deb/DEB-GPG-KEY-crate

   # Add the key to APT
   sudo apt-key add DEB-GPG-KEY-crate

   # Add CrateDB repositories to APT
   # `lsb_release -cs` returns the codename of your OS
   sudo add-apt-repository "deb https://cdn.crate.io/downloads/deb/stable/ $(lsb_release -cs) main"


.. NOTE::

   CrateDB provides a *stable release* and a *testing release* channel. To use
   the testing channel, replace ``stable`` with ``testing`` in the command
   above. You can read more about our `release workflow`_. 


Now update APT:

.. code-block:: sh

   sudo apt update

You should see a success message. This indicates that the CrateDB release
channel is correctly configured and the crate package has been registered
locally.

Install CrateDB
###############

With everything set up, you can install CrateDB, like so:

.. code-block:: sh

   sudo apt install crate

After the installation is finished, the ``crate`` service should be
up and running. You should be able to access it from your local machine by
visiting::

  http://localhost:4200/

.. CAUTION::
   When you install via APT, CrateDB automatically starts as a single-node
   cluster and you won't be able to add additional nodes. In order to form a
   multi-node cluster, you will need to remove the cluster state after
   changing the configuration.

Control CrateDB
###############

You can control the ``crate`` service
with the `systemctl` utility:

.. code-block:: sh

   sudo systemctl COMMAND crate

Next steps
###########

Now you have CrateDB up and running, :ref:`take the guided tour <use>`.

Red Hat Linux and CentOS (using YUM)
======================================

Configure YUM
#############

All CrateDB packages are signed with GPG. To get started, you must import the CrateDB public key, like so:

.. code-block:: sh

   sudo rpm --import https://cdn.crate.io/downloads/yum/RPM-GPG-KEY-crate

You must then install the CrateDB repository definition: 

.. code-block:: sh

   sudo rpm -Uvh https://cdn.crate.io/downloads/yum/7/x86_64/crate-release-7.0-1.x86_64.rpm

The above commands will create the ``/etc/yum.repos.d/crate.repo``
configuration file.

.. NOTE::

   CrateDB provides a *stable release* and a *testing release* channel. To use
   the testing channel, replace ``stable`` with ``testing`` in the command
   above. You can read more about our `release workflow`_.

   By default, `YUM`_ (Red Hat's package manager) will use the stable repository.
   This is because the testing repository's configuration marks it as disabled.

   If you would like to enable to testing repository, open the ``crate.repo`` file
   and set ``enabled=1`` under the ``[crate-testing]`` section.

.. _YUM: https://access.redhat.com/solutions/9934

Install CrateDB
###############

With everything set up, you can install CrateDB, like so:

.. code-block:: sh

   yum install crate

After the installation is finished, the ``crate`` service should be
installed, but not running. Use the following command to start CrateDB:

.. code-block:: sh

   sudo systemctl start crate

After the installation is finished, the ``crate`` service should be
up and running. You should be able to access it from your local machine by
visiting::

  http://localhost:4200/

Control CrateDB
###############

You can control the ``crate`` service with the `systemctl` utility:

.. code-block:: sh

   sudo systemctl COMMAND crate

Replace ``COMMAND`` with ``start``, ``stop``, ``restart``, ``status`` and
so on.

Next steps
###########

Now you have CrateDB up and running, :ref:`take the guided tour <use>`.

Run on Docker
=============

CrateDB and Docker_ are a great match thanks to CrateDB's shared-nothing,
horizontally scalable architecture that lends itself well to containerization.

Spin up the official `CrateDB Docker image`_, like so:

.. code-block:: sh

   docker run -p "4200:4200" crate

.. TIP::

   If this command aborts with an error, consult the `troubleshooting guide`_.

.. CAUTION::

   This command will get you up and running for the first time.

   By default, the CrateDB Docker image stores data inside the container. If
   you delete the container, the data will be deleted along with it. When
   you're ready to start using CrateDB for data that you care about, you should
   consult the `full guide to CrateDB and Docker`_.

Next steps
###########

Now you have CrateDB up and running, :ref:`take the guided tour <use>`.


Configure CrateDB
=================

In order to configure CrateDB, take note of the configuration file
location and the available environment variables.

Configuration files
###################

The main CrateDB `configuration files`_ are located in the ``/etc/crate``
directory.


Environment variables
#####################

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

.. _7-Zip: https://www.7-zip.org/
.. _Apt: https://wiki.debian.org/Apt
.. _also available: https://cdn.crate.io/downloads/releases/
.. _An introductory tutorial: https://crate.io/docs/crate/guide/tutorials/hello.html
.. _bootstrap checks: https://crate.io/docs/crate/guide/en/latest/admin/bootstrap-checks.html
.. _crash: https://crate.io/docs/crate/guide/getting_started/connect/crash.html
.. _CrateDB reference documentation: https://crate.io/docs/crate/reference/en/latest/run.html
.. _How to run CrateDB in a multi node setup: https://crate.io/docs/crate/guide/getting_started/scale/multi_node_setup.html
.. _How-To Guides: https://crate.io/docs/crate/howtos/en/latest/
.. _install section: https://crate.io/docs/crate/guide/getting_started/install/index.html
.. _Java 11: https://www.oracle.com/technetwork/java/javase/downloads/index.html
.. _Java virtual machine: https://en.wikipedia.org/wiki/Java_virtual_machine
.. _OpenJDK: https://openjdk.java.net/projects/jdk/11/
.. _release workflow: https://github.com/crate/crate/blob/master/devs/docs/release.rst
.. _Ubuntu 16.04.7 LTS: https://wiki.ubuntu.com/XenialXerus/ReleaseNotes
.. _CrateDB Docker image: https://hub.docker.com/_/crate/
.. _Docker: https://www.docker.com/
.. _full guide to CrateDB and Docker: https://crate.io/docs/crate/guide/en/latest/deployment/containers/docker.html
.. _resource constraints: https://crate.io/docs/crate/guide/en/latest/deployment/containers/docker.html#resource-constraints
.. _troubleshooting guide: https://crate.io/docs/crate/guide/en/latest/deployment/containers/docker.html#docker-troubleshooting
.. _environment variables: https://crate.io/docs/crate/reference/en/latest/config/environment.html
.. _sources: https://en.wikipedia.org/wiki/Source_(command)


.. _Oracle's Java: https://www.java.com/en/download/help/mac_install.xml
.. _release notes: https://crate.io/docs/crate/reference/en/latest/release_notes/index.html
.. _the latest CrateDB release: https://crate.io/download/
.. _Unix-like system: https://en.wikipedia.org/wiki/Unix-like
.. _web administration interface: https://crate.io/docs/crate/guide/getting_started/connect/admin_ui.html
