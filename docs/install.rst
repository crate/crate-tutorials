.. highlight:: bash

.. _install:

==================
Quick installation
==================

.. contents::
   :local:
   :depth: 1


Preface
=======

This part of the documentation covers the installation of CrateDB on Linux,
macOS and Windows systems.
The first step to using any software package is getting it properly installed.
Please read this section carefully.


Introduction
============

By installing CrateDB the way as outlined in this document, you will be able to
quickly setup and run a single-node cluster.

After the installation is finished, the CrateDB service should be up and
running. Now, you can access the :ref:`Admin UI <admin-ui:index>` from your
local machine by navigating to::

    http://localhost:4200/

After successfully installing the software, you might want to follow up with
:ref:`taking the guided tour <use>`.

Also, you might enjoy to be guided into further information about how to
quickly adjust the :ref:`configuration settings <configure>`, read more
details about the :ref:`reference:config` of CrateDB, the background about
:ref:`howtos:bootstrap-checks`, multi-node configuration within the section
about :ref:`howtos:clustering` and :ref:`howtos:going-into-production`. When
operating a CrateDB cluster in production, `performance tuning`_ will also be
of interest.

.. _performance tuning: https://crate.io/docs/crate/howtos/en/latest/performance/

.. NOTE::

    To add additional CrateDB nodes to this kind of cluster in order to make it
    form a multi-node cluster, you will need to remove the cluster state after
    changing the configuration.

.. NOTE::

    If you are interested to follow the development more closely, please check
    out the :ref:`reference:release_notes` for more specific information about
    each CrateDB release. `Other releases of CrateDB`_ are also available.


Prerequisites
=============

CrateDB requires a `Java virtual machine`_ to run.

- Starting with CrateDB 4.2, a `Java virtual machine`_ is bundled with CrateDB
  and no extra installation is necessary.

- CrateDB version 3.0 to 4.1 required a separate Java installation, version
  11 was the minimum requirement. Earlier versions required Java 8.
  We recommend using OpenJDK_ on Linux Systems and `Oracle Java`_ on
  Microsoft Windows and macOS.


Basic setup
===========

This section of the documentation outlines how to use the release archives to
install CrateDB.


Automatic installation
----------------------

CrateDB has an effortless installer suitable for all `Unix-like`_ systems
running ``bash``::

    bash -c "$(curl -L https://try.crate.io/)"


Manual installation
-------------------

This walkthrough is suitable to install and run CrateDB on both `Unix-like`_
systems as well as on Microsoft Windows.

#. Download the latest `CrateDB release archive`_. Please make sure to select
   the right release archive matching your system.

#. Once downloaded, extract the archive either using your favorite terminal or
   command line shell or by using a GUI tool like `7-Zip`_::

       tar -xzf crate-*.tar.gz

#. On the terminal, change into the extracted ``crate`` directory::

       cd crate-*

#. Run a CrateDB single-node instance on the local network interface::

       ./bin/crate

#. In order to stop CrateDB again, use :kbd:`ctrl-c`.

.. SEEALSO::

      Consult the :ref:`reference:cli` documentation for further information
      about the ``./bin/crate`` command.


Notes about Microsoft Windows
-----------------------------

If you are installing CrateDB on a recent `Windows Server`_ edition, setting
up the latest *Microsoft Visual C++ 2019 Redistributable* package is required.
You can download it at `msvcrt x86-64`_, `msvcrt x86-32`_ or `msvcrt ARM64`_.

Within the terminal, as a Windows user, the prompt after `starting PowerShell`_
will look like this.

.. code-block:: doscon

    PS> ./bin/crate


Debian and Ubuntu
=================

This section of the documentation outlines how to install CrateDB deb_ packages
using the apt_ package manager.


Configure package repository
----------------------------

You will need to configure your system to register with and trust packages from
the CrateDB package repository::

    # Install prerequisites.
    apt-get install sudo
    sudo apt-get install curl gnupg software-properties-common apt-transport-https apt-utils

    # Import the public GPG key for verifying the package signatures.
    curl -sS https://cdn.crate.io/downloads/deb/DEB-GPG-KEY-crate | sudo apt-key add -

    # Register with the CrateDB package repository.
    [[ $(lsb_release --id --short) = "Debian" ]] && repository="apt"
    [[ $(lsb_release --id --short) = "Ubuntu" ]] && repository="deb"
    distribution=$(lsb_release --codename --short)
    sudo add-apt-repository "deb https://cdn.crate.io/downloads/${repository}/stable/ ${distribution} main"


.. NOTE::

    CrateDB provides both *stable release* and *testing release* channels. To
    use the testing channel, replace ``stable`` with ``testing`` in the command
    line above. You can read more about the `release workflow`_.


Now update the package sources::

    sudo apt update

You should see a success message. This indicates that the CrateDB package
repository is correctly registered.

Install CrateDB
---------------

With everything set up, you can install CrateDB::

    sudo apt install crate


Control CrateDB
---------------

You can control the ``crate`` service with the ``systemctl`` utility program::

    sudo systemctl COMMAND crate

Replace ``COMMAND`` with ``start``, ``stop``, ``restart``, ``status`` and
so on.



Red Hat Linux and CentOS
========================

This section of the documentation outlines how to install CrateDB RPM_ packages
using the YUM_ package manager.


Configure package repository
----------------------------

You will need to configure your system to register with and trust packages
from the CrateDB package repository::

    # Install prerequisites.
    yum install sudo

    # Import the public GPG key for verifying the package signatures.
    sudo rpm --import https://cdn.crate.io/downloads/yum/RPM-GPG-KEY-crate

    # Register with the CrateDB package repository.
    sudo rpm -Uvh https://cdn.crate.io/downloads/yum/7/x86_64/crate-release-7.0-1.x86_64.rpm

The command above will install the ``/etc/yum.repos.d/crate.repo`` package
repository configuration file.

.. NOTE::

    CrateDB provides both *stable release* and *testing release* channels. You
    can read more about the `release workflow`_.

    By default, yum_ (Red Hat's package manager) will use the stable
    repository. This is because the testing repository is disabled.
    If you would like to enable the testing repository, edit the ``crate.repo``
    file and set ``enabled=1`` within the ``[crate-testing]`` section.


Install CrateDB
---------------

With everything set up, you can install CrateDB::

    sudo yum install crate

After the installation is finished, the ``crate`` service should be installed,
but not running. Use the following command to start CrateDB::

    sudo systemctl start crate

In order to make the service reboot-safe, invoke::

    sudo systemctl enable crate


Control CrateDB
---------------

You can control the ``crate`` service with the ``systemctl`` utility program::

    sudo systemctl COMMAND crate

Replace ``COMMAND`` with ``start``, ``stop``, ``restart``, ``status`` and
so on.


Docker
======

CrateDB and Docker_ are great matches thanks to CrateDB's shared-nothing,
horizontally scalable architecture that lends itself well to containerization.

In order to spin up a container using the most recent stable version of the
official `CrateDB Docker image`_, use::

    docker run --publish=4200:4200 --publish=5432:5432 crate

.. TIP::

    If this command aborts with an error, please consult the `Docker
    troubleshooting guide`_. You are also welcome learn more about
    :ref:`howtos:resource_constraints` with respect to running CrateDB within
    containers.

.. CAUTION::

    This type of invoking CrateDB will get you up and running quickly.

    Please note, by default, the CreateDB Docker container is ephemeral, so
    data will not be stored in a persistent manner. When stopping the
    container, all data will be lost.

    When you are ready to start using CrateDB for data you care about, please
    consult the :ref:`full guide to CrateDB and Docker <howtos:cratedb-docker>`
    in order to configure the Docker setup appropriately by using persistent
    disk volumes.


.. _configure:

Basic configuration
===================

In order to configure CrateDB, take note of the configuration file location and
the available environment variables.


Configuration files
-------------------

The main CrateDB configuration files are located within the ``/etc/crate``
directory.


Environment variables
---------------------

The CrateDB startup script uses :ref:`reference:conf-env` from the
``/etc/default/crate`` file. Here is an example::

    # Configure heap size (defaults to 256m min, 1g max).
    CRATE_HEAP_SIZE=2g

    # Maximum number of open files, defaults to 65535.
    # MAX_OPEN_FILES=65535

    # Maximum locked memory size. Set to "unlimited" if you use the
    # bootstrap.mlockall option in crate.yml. You must also set
    # CRATE_HEAP_SIZE.
    MAX_LOCKED_MEMORY=unlimited

    # Provide additional Java OPTS.
    # CRATE_JAVA_OPTS=

    # Force the JVM to use IPv4 only.
    CRATE_USE_IPV4=true


.. _7-Zip: https://www.7-zip.org/
.. _apt: https://en.wikipedia.org/wiki/APT_(software)
.. _CrateDB Docker image: https://hub.docker.com/_/crate/
.. _CrateDB release archive: https://crate.io/download/
.. _deb: https://en.wikipedia.org/wiki/Deb_(file_format)
.. _Docker: https://www.docker.com/
.. _Docker troubleshooting guide: https://crate.io/docs/crate/howtos/en/latest/deployment/containers/docker.html#troubleshooting
.. _Java virtual machine: https://en.wikipedia.org/wiki/Java_virtual_machine
.. _msvcrt ARM64: https://aka.ms/vs/16/release/VC_redist.arm64.exe
.. _msvcrt x86-32: https://aka.ms/vs/16/release/vc_redist.x86.exe
.. _msvcrt x86-64: https://aka.ms/vs/16/release/vc_redist.x64.exe
.. _OpenJDK: https://openjdk.java.net/projects/jdk/
.. _Oracle Java: https://www.oracle.com/java/technologies/javase-downloads.html
.. _Other releases of CrateDB: https://cdn.crate.io/downloads/releases/
.. _release workflow: https://github.com/crate/crate/blob/master/devs/docs/release.rst
.. _RPM: https://en.wikipedia.org/wiki/RPM_Package_Manager
.. _starting PowerShell: https://docs.microsoft.com/en-us/powershell/scripting/learn/ps101/01-getting-started?view=powershell-7.1#how-do-i-launch-powershell
.. _Unix-like: https://en.wikipedia.org/wiki/Unix-like
.. _Windows Server: https://www.microsoft.com/en-us/windows-server
.. _YUM: https://en.wikipedia.org/wiki/Yum_(software)
