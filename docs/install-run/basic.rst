.. meta::
     :last-reviewed: 2020-07-09

.. highlight:: sh

.. _basic-install:

==================================
Basic tarball Installation
==================================

.. CAUTION::

   These instructions are designed to get you quickly up and running on your local
   computer. For putting CrateDB into production, you can learn more about
   `deploying`_ or `scaling`_ CrateDB in the `CrateDB Guide`_.

.. SEEALSO::

   This page shows you how get up and running directly from the tarball on any
   `Unix-like system`_.

   Specialised install guides are available for: :ref:`Linux <linux-install>`,
   :ref:`macOS <mac-install>`, :ref:`Microsoft Windows <windows-install>`, and
   :ref:`Docker <docker-install>`.

Prerequisites
=============
CrateDB requires a `Java virtual machine`_ to run.

.. NOTE::

   Starting with CrateDB 4.2, a `Java virtual machine`_ is bundled with the
   tarball and no extra installation is necessary.

Versions starting from 3.0 to 4.1 require a `Java 11`_ installation. We
recommend using `Oracle's Java`_ on macOS and OpenJDK_ on Linux Systems.
Earlier versions required Java 8.

.. _install_targz:

Download
========

1. Download `the latest CrateDB release`_.
2. Unpack the tarball and change into the resulting directory:

.. code-block:: console

   sh$ tar -xzf crate-*.tar.gz
   sh$ cd crate-*

.. SEEALSO::

   Other releases of CrateDB are `also available`_.

   Check out the `release notes`_ for specific information about each CrateDB
   release.


Run
===

You do not have to configure or build anything. Once unpacked, CrateDB can be started in the foreground like this:

.. code-block:: console

   sh$ ./bin/crate

This command runs a single instance of CrateDB that is bound to the local IP
address.
:kbd:`Control-C` will stop the process.

.. SEEALSO::

   Consult the `CrateDB reference documentation`_ for help using this command.


Next steps
==========

Now you have CrateDB up and running, :ref:`take the guided tour <first-use>`.


.. _also available: https://cdn.crate.io/downloads/releases/
.. _An introductory tutorial: https://crate.io/docs/crate/guide/tutorials/hello.html
.. _bootstrap checks: https://crate.io/docs/crate/guide/en/latest/admin/bootstrap-checks.html
.. _crash: https://crate.io/docs/crate/guide/getting_started/connect/crash.html
.. _CrateDB Guide: https://crate.io/docs/crate/guide/en/latest/
.. _CrateDB reference documentation: https://crate.io/docs/crate/reference/en/latest/run.html
.. _deploying: https://crate.io/docs/crate/guide/en/latest/deployment/index.html
.. _How to run CrateDB in a multi node setup: https://crate.io/docs/crate/guide/getting_started/scale/multi_node_setup.html
.. _install section: https://crate.io/docs/crate/guide/getting_started/install/index.html
.. _Java 11: https://www.oracle.com/technetwork/java/javase/downloads/index.html
.. _Java virtual machine: https://en.wikipedia.org/wiki/Java_virtual_machine
.. _OpenJDK: http://openjdk.java.net/projects/jdk/11/
.. _Oracle's Java: http://www.java.com/en/download/help/mac_install.xml
.. _release notes: https://crate.io/docs/crate/reference/en/latest/release_notes/index.html
.. _scaling: https://crate.io/docs/crate/guide/en/latest/scaling/index.html
.. _the latest CrateDB release: https://crate.io/download/
.. _Unix-like system: https://en.wikipedia.org/wiki/Unix-like
.. _web administration interface: https://crate.io/docs/crate/guide/getting_started/connect/admin_ui.html
