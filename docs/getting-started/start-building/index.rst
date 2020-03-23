.. _start-building:

==============
Start building
==============

CrateDB is happy at the heart of any application stack, with a number of
libraries to support development.

Below is a selection of CrateDB client libraries.

Pick your library, and start building!

.. list-table::
    :header-rows: 1

    * - Language
      - Maintainers
      - Official support
      - Driver
    * - C# (.NET)
      - Crate.IO
      - ✔️
      - `Npgsql`_
    * - Erlang
      - Community
      - ❌
      - `craterl`_
    * - Go
      - Community
      - ✔️
      - `pgx`_
    * - Java
      - Crate.IO
      - ✔️
      - `crate-jdbc`_
    * - Node.JS
      - Community
      - ✔️
      - `node-postgres`_
    * - Node.JS
      - Community
      - ❌
      - `crate-connect`_
    * - Node.JS
      - Community
      - ❌
      - `cratejs`_
    * - Node.JS
      - Community
      - ❌
      - `node-crate`_
    * - PHP
      - Crate.IO
      - ✔️
      - `CrateDB PDO`_
    * - Perl
      - Community
      - ❌
      - `DBD::Crate`_
    * - Python
      - Crate.IO
      - ✔️
      - `crate-python`_
    * - Python
      - Community
      - ✔️
      - `asyncpg`_
    * - Ruby 
      - Community
      - ❌
      - `crate_ruby`_ 
    * - Scala
      - Community
      - ❌
      - `crate-scala`_


If you would like to see something added to this page, please `get in touch`_
or `edit this page`_ create a pull request.

.. TIP::

    CrateDB supports the `PostgreSQL wire protocol`_. Accordingly, many clients
    that work with PostgreSQL also work with CrateDB.

    You can try this out for yourself:

    - Configure a PostgreSQL connection, but point your client to a CrateDB
      server instead of a PostgreSQL server
    - `Authenticate`_ as the ``crate`` `superuser`_ with no password
    - Specify the ``doc`` `schema`_, if you're asked for a *database name*

    Check out the `client compatibility notes`_ and `implementation
    differences`_ for information about known limitations.

    If you run into issues, please `let us know`_. We regularly update CrateDB
    to accomodate new PostgreSQL clients.


.. _ActiveRecord: https://rubygems.org/gems/activerecord-crate-adapter
.. _asyncpg: https://github.com/MagicStack/asyncpg
.. _Authenticate: https://crate.io/docs/crate/reference/en/latest/admin/auth/index.html
.. _client compatibility notes: https://crate.io/docs/crate/reference/en/latest/interfaces/postgres.html#client-compatibility
.. _Crate.Client: https://github.com/mfussenegger/crate-mono
.. _crate-connect: https://www.npmjs.com/package/crate-connect
.. _CrateDB PDO: https://crate.io/docs/clients/pdo/en/latest/
.. _crate-jdbc: https://crate.io/docs/clients/jdbc/en/latest/
.. _cratejs: https://www.npmjs.com/package/cratejs
.. _crate-python: https://crate.io/docs/clients/python/en/latest/
.. _craterl: https://github.com/crate/craterl
.. _crate_ruby: https://rubygems.org/gems/crate_ruby
.. _crate-scala: https://github.com/alexanderjarvis/crate-scala
.. _DBAL: https://crate.io/docs/clients/dbal/en/latest/
.. _DBD::Crate: https://github.com/mamod/DBD-Crate
.. _edit this page: https://github.com/crate/crate-tutorials/blob/master/docs/getting-started/start-building/index.rst
.. _get in touch: https://crate.io/contact/
.. _implementation differences: https://crate.io/docs/crate/reference/en/latest/interfaces/postgres.html#implementation-differences
.. _let us know: https://crate.io/contact/
.. _Loopback: https://github.com/lovelysystems/loopback-connector-crateio
.. _node-crate: https://www.npmjs.com/package/node-crate
.. _node-postgres: https://node-postgres.com/
.. _Npgsql: https://crate.io/docs/clients/npgsql/en/latest/
.. _pgx: https://github.com/jackc/pgx
.. _PostgreSQL wire protocol: https://crate.io/docs/crate/reference/en/latest/interfaces/postgres.html
.. _schema: https://crate.io/docs/crate/reference/en/latest/general/ddl/create-table.html#schemas
.. _SQLAlchemy: https://crate.io/docs/clients/python/en/latest/sqlalchemy.html
.. _superuser: https://crate.io/docs/crate/reference/en/latest/admin/user-management.html#introduction
