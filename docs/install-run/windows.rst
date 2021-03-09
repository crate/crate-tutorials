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

CrateDB is a Java application and runs effortlessly on Microsoft Windows.

If you are installing on a recent `Windows Server`_ edition, setting up the
latest Microsoft Visual C++ 2019 Redistributable package is required.

You can download it at `msvcrt x86-64`_, `msvcrt x86-32`_ or `msvcrt ARM64`_.


.. _install-windows-download-run:

Download and run
================

1. Download `the latest CrateDB release`_.
2. Once downloaded, inflate the Zip archive.
3. `Start PowerShell`_.
4. `Change into the extracted folder`_, and start CrateDB, like so:

   .. code-block:: doscon

       PS> ./bin/crate


.. NOTE::

    CrateDB versions 4.2 and above include a JVM and do not require a separate
    installation. For earlier versions, CrateDB requires a `Java virtual
    machine`_ to run. Versions from 3.0 to 4.1 require a `Java 11`_
    installation. We recommend using `Oracle's Java`_ on Microsoft Windows.
    Earlier versions required Java 8.



.. _install-windows-next:

Next steps
==========

Now you have CrateDB up and running, :ref:`take the guided tour <use>`.


.. _bootstrap checks: https://crate.io/docs/crate/guide/en/latest/admin/bootstrap-checks.html
.. _Change into the extracted folder: https://docs.microsoft.com/en-us/powershell/scripting/getting-started/cookbooks/managing-current-location?view=powershell-6
.. _How-To Guides: https://crate.io/docs/crate/howtos/en/latest/
.. _Java 11: https://www.oracle.com/technetwork/java/javase/downloads/index.html
.. _Java virtual machine: https://en.wikipedia.org/wiki/Java_virtual_machine
.. _msvcrt ARM64: https://aka.ms/vs/16/release/VC_redist.arm64.exe
.. _msvcrt x86-32: https://aka.ms/vs/16/release/vc_redist.x86.exe
.. _msvcrt x86-64: https://aka.ms/vs/16/release/vc_redist.x64.exe
.. _Oracle's Java: https://www.oracle.com/technetwork/java/javase/downloads/index.html
.. _PowerShell: https://docs.microsoft.com/en-us/powershell/
.. _Start PowerShell: https://docs.microsoft.com/en-us/powershell/scripting/setup/starting-windows-powershell?view=powershell-6
.. _the latest CrateDB release: https://crate.io/download/
.. _Windows Server: https://www.microsoft.com/en-us/windows-server
