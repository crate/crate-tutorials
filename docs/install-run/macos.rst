.. _mac-install:

========================
Install CrateDB on macOS
========================

Because CrateDB is a Java application, it runs effortlessly on macOS.

.. SEEALSO::

   These instructions are designed to get you up and running on your personal
   computer.

   For putting CrateDB into production, you can learn more about
   `deploying`_ or `scaling`_ CrateDB in the `CrateDB Guide`_.

.. rubric:: Table of contents

.. contents::
   :local:


One-step setup
==============

You can install and run CrateDB on macOS with one simple command in your
terminal application:

.. code-block:: console

   sh$ bash -c "$(curl -L https://try.crate.io/)"

If you don't already have `Java 11`_ installed, the above command will try to
take care of that for you along with a few other housekeeping tasks.


Next steps
==========

Now you have CrateDB up and running, :ref:`take the guided tour <first-use>`.


.. _bootstrap checks: https://crate.io/docs/crate/guide/en/latest/admin/bootstrap-checks.html
.. _CrateDB Guide: https://crate.io/docs/crate/guide/en/latest/
.. _deploying: https://crate.io/docs/crate/guide/en/latest/deployment/index.html
.. _Java 11: https://www.oracle.com/technetwork/java/javase/downloads/index.html
.. _Oracle's Java: http://www.java.com/en/download/help/mac_install.xml
.. _scaling: https://crate.io/docs/crate/guide/en/latest/scaling/index.html
