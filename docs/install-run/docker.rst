.. _install-docker:

=============
Run on Docker
=============

.. CAUTION::

   This command will get you up and running for the first time.

   By default, the CrateDB Docker image stores data inside the container. If
   you delete the container, the data will be deleted along with it. When
   you're ready to start using CrateDB for data that you care about, you should
   consult the `full guide to CrateDB and Docker`_.

CrateDB and Docker_ are a great match thanks to CrateDB's shared-nothing,
horizontally scalable architecture that lends itself well to containerization.


.. _install-docker-one-step:

One-step setup
==============

Spin up the official `CrateDB Docker image`_, like so:

.. code-block:: console

   sh$ docker run -p "4200:4200" crate

.. TIP::

   If this command aborts with an error, consult the `troubleshooting guide`_.


.. _install-docker-next:

Next steps
==========

Now you have CrateDB up and running, :ref:`take the guided tour <use>`.


.. _bootstrap check: https://crate.io/docs/crate/howtos/en/latest/admin/bootstrap-checks.html
.. _CrateDB Docker image: https://hub.docker.com/_/crate/
.. _Docker: https://www.docker.com/
.. _full guide to CrateDB and Docker: https://crate.io/docs/crate/howtos/en/latest/deployment/containers/docker.html
.. _resource constraints: https://crate.io/docs/crate/howtos/en/latest/deployment/containers/docker.html#resource-constraints
.. _troubleshooting guide: https://crate.io/docs/crate/howtos/en/latest/deployment/containers/docker.html#troubleshooting
