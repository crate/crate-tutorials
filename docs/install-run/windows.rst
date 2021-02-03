.. _install-windows:

========================
Quick Install on Windows
========================

.. CAUTION::

   These instructions are designed to get you quickly up and running on your
   local computer. For putting CrateDB into production, check out the `How-To
   Guides`_.


.. _install-windows-prereq:

Prerequisites
=============

Because CrateDB is a Java application, it runs effortlessly on Microsoft
Windows.


CrateDB versions 4.2 and above include a JVM and do not require a separate
installation. For earlier versions,  CrateDB requires a `Java virtual machine`_
to run. Versions from 3.0 to 4.1 require a `Java 11`_ installation. We
recommend using `Oracle's Java`_ on Microsoft Windows. Earlier versions
required Java 8.

If you are installing on `Windows Server`_, you must install the `Microsoft
Visual C++ 2019 Redistributable`_ package.


.. _install-windows-download-run:

Download and run
================

For this specialized guide, we have adapted the :ref:`Basic tarball
Installation <install>` instructions for use with Windows `PowerShell`_.

1. Download `the latest CrateDB release`_.
2. Once downloaded, expand the tarball using a tool like `7-Zip`_.
3. `Start PowerShell`_
4. `Change into the expanded tarball folder`_, and start CrateDB, like so:

   .. code-block:: doscon

       PS> ./bin/crate


.. _install-windows-next:

Next steps
==========

Now you have CrateDB up and running, :ref:`take the guided tour <use>`.


.. _7-Zip: https://www.7-zip.org/
.. _bootstrap checks: https://crate.io/docs/crate/guide/en/latest/admin/bootstrap-checks.html
.. _change into the expanded tarball folder: https://docs.microsoft.com/en-us/powershell/scripting/getting-started/cookbooks/managing-current-location?view=powershell-6
.. _How-To Guides: https://crate.io/docs/crate/howtos/en/latest/
.. _Java 11: https://www.oracle.com/technetwork/java/javase/downloads/index.html
.. _Java virtual machine: https://en.wikipedia.org/wiki/Java_virtual_machine
.. _Microsoft Visual C++ 2019 Redistributable: https://www.itechtics.com/microsoft-visual-c-redistributable-versions-direct-download-links/#Microsoft_Visual_C_2019_Redistributable
.. _Oracle's Java: https://www.oracle.com/technetwork/java/javase/downloads/index.html
.. _PowerShell: https://docs.microsoft.com/en-us/powershell/
.. _Start PowerShell: https://docs.microsoft.com/en-us/powershell/scripting/setup/starting-windows-powershell?view=powershell-6
.. _the latest CrateDB release: https://crate.io/download/
.. _Windows Server: https://www.microsoft.com/en-us/windows-server
