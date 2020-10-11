.. _create-user:

===================
Create User
===================

CrateDB ships with a superuser (``crate``) which has the privileges to do anything. With the default configuration however you can only use the superuser from the local machine you installed CrateDB on.
If you are trying to connect from another host, you are prompted to enter a username and password.

.. NOTE::

   `User Management`_ and `privileges`_ are `enterprise features`_.

In order to create a user, that can be used to authenticate from another host first `install Crash`_ (or `another client`_) on the same machine you installed CrateDB on.
Then, you can start the shell like so, to connect to CrateDB running on ``localhost``.

.. code-block:: console

   sh$ crash

Add your first user with a secure password to the database:

.. code-block:: psql

   cr> CREATE USER username WITH (password = 'a_secret_password');

Grant all priviliges to the newly created user:

.. code-block:: psql

   cr> GRANT ALL PRIVILEGES TO username;

.. image:: _assets/img/create-user.png

Now try accessing the Admin UI from your client in your browser using a URL like the following (replacing ``remote-host`` with the ``hostname`` or ``ip-adress`` of the remote host) and login with your newly created user::

   http://remote-host:4200/

You should see something like this:

.. image:: _assets/img/first-use/admin-ui.png


After creating the user and granting all priviliges, you should be able to continue with :ref:`the guided tour <first-use>` connecting to CrateDB on a remote host.





.. _User Management: https://crate.io/docs/crate/reference/en/latest/admin/user-management.html
.. _privileges: https://crate.io/docs/crate/reference/en/latest/admin/privileges.html
.. _configuration: https://crate.io/docs/crate/reference/en/latest/config/index.html
.. _enterprise features: https://crate.io/enterprise/
.. _another client: https://crate.io/docs/crate/clients-tools/en/latest/
.. _install Crash: https://crate.io/docs/clients/crash/en/latest/getting-started.html#install