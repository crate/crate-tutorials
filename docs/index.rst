.. highlight:: bash

.. _index:

============
Installation
============

Introduction
============

This part of the documentation covers the installation of CrateDB on Linux,
macOS and Windows systems.
The first step to using any software package is getting it properly installed.
Please read this section carefully.

Try CrateDB Cloud
=================

The easiest way to get started with CrateDB is to use a 30 day free CrateDB
Cloud cluster, no credit card requrired. Visit the `sign up page`_ to start your
CrateDB cluster today.

Try CrateDB locally
===================

If you want to try out CrateDB locally on Linux or macOS but would prefer to
avoid the hassle of manual installation or extracting release archives, you can
get a fresh CrateDB node up and running in your current working directory with a
single command:

.. code-block:: console

   sh$ bash -c "$(curl -L https://try.crate.io/)"


.. NOTE::

    This is a quick way to *try out* CrateDB. It is not the recommended method
    to *install* CrateDB in a durable way. The following sections will outline
    that method.


Installing CrateDB
==================

This section of the documentation shows you how to deploy CrateDB in different
environments.

.. rubric:: Table of contents

.. toctree::
   :maxdepth: 3
   :titlesonly:

   basic/index
   self-hosted/index
   containers/index
   cloud/index



.. _sign up page: https://crate.io/lp-free-trial
