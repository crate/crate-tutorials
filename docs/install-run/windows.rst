.. _windows-install:

====================================
Install CrateDB on Microsoft Windows
====================================

Because CrateDB is a Java application, it runs effortlessly on Microsoft
Windows.

.. NOTE::

   CrateDB requires a `Java virtual machine`_ to run.

   Starting with CrateDB 4.2, a `Java virtual machine`_ is bundled with the
   tarball and no extra installation is necessary.

   Versions from 3.0 to 4.1 require a `Java 11`_ installation. We recommend
   using `Oracle's Java`_ on Microsoft Windows.

   Earlier versions required Java 8.

.. SEEALSO::

   These instructions are designed to get you up and running on your personal
   computer.

   For putting CrateDB into production, you can learn more about
   `deploying`_ or `scaling`_ CrateDB in the `CrateDB Guide`_.

.. rubric:: Table of contents

.. contents::
   :local:


Download and run
================

For this specialized guide, we have adapted the :ref:`basic tarball
installation <basic-install>` instructions for use with Windows
`PowerShell`_.

Download `the latest CrateDB release`_.

Once downloaded, expand the tarball using a tool like `7-Zip`_.

`Start PowerShell`_, `change into the expanded tarball folder`_, and start
CrateDB, like so:

.. code-block:: doscon

   PS> ./bin/crate


Next steps
==========

Now you have CrateDB up and running, :ref:`take the guided tour <first-use>`.


.. _7-Zip: http://www.7-zip.org/
.. _bootstrap checks: https://crate.io/docs/crate/guide/en/latest/admin/bootstrap-checks.html
.. _change into the expanded tarball folder: https://docs.microsoft.com/en-us/powershell/scripting/getting-started/cookbooks/managing-current-location?view=powershell-6
.. _CrateDB Guide: https://crate.io/docs/crate/guide/en/latest/
.. _deploying: https://crate.io/docs/crate/guide/en/latest/deployment/index.html
.. _Java 11: https://www.oracle.com/technetwork/java/javase/downloads/index.html
.. _Java virtual machine: https://en.wikipedia.org/wiki/Java_virtual_machine
.. _Oracle's Java: https://www.oracle.com/technetwork/java/javase/downloads/index.html
.. _PowerShell: https://docs.microsoft.com/en-us/powershell/
.. _scaling: https://crate.io/docs/crate/guide/en/latest/scaling/index.html
.. _Start PowerShell: https://docs.microsoft.com/en-us/powershell/scripting/setup/starting-windows-powershell?view=powershell-6
.. _the latest CrateDB release: https://crate.io/download/
