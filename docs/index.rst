Welcome to Refugee's documentation!
===================================

A simple way to migrate your data without being tied to an orm.


Design and Motivation
~~~~~~~~~~~~~~~~~~~~~

The use case for this design is to have a wrapper around sql and scripts that
help version and control the migration process. This should do the following

* require next to 0 setup
* control all migrations in a transaction and assure that each applies cleanly
* prevent migrations from being applied multiple times
* attempt to merge long branches of migrations

The simplest way to get started is to use the commandline interface.

Contents:

.. toctree::
   :glob:
   :maxdepth: 2

   refugee/index*

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

