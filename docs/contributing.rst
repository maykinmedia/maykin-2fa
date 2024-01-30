============
Contributing
============

We have a strong vision about the scope of this package and the "less is more" principle
resonates here. That being said, we will of course greatly appreciate contributions in
any form, such as suggestions, remarks, documentation improvements, bugfixes... If a
contribution does not solve any of our (Maykin) particular needs, it is unlikely to be
accepted.

That said - if you're a Maykin employee, Open Source enthusiast or just a generally
interested person, we have some guidance on how to get started.

Installing the package and "test" application locally
=====================================================

We recommend setting up a virtualenv or similar. You can then install the library for
local development and/or experimenting:

.. code-block:: bash

    pip install -e .[tests,coverage,docs,release]

Due to some Python path details, we also recommend setting some environment variables:

.. code-block:: bash

    # run in the top-level directory - you can also make this part of your virtualenv
    # activation script
    export PYTHONPATH=$(pwd) DJANGO_SETTINGS_MODULE=testapp.settings

The ``PYTHONPATH`` in particular is needed to avoid import errors due to how Python
discovers modules.

Running tests
=============

Running tests for the current environment:

.. code-block:: bash

    pytest

Running tests against all envs:

.. code-block:: bash

    tox

Running a local development server
==================================

You can use the ``django-admin`` script instead of ``manage.py`` as you might be used to
in projects:

.. code-block:: bash

    django-admin check
    django-admin runserver

Alternatively, you can use ``python -m django <command>``.

Code contributions
==================

Code formatting is checked in the CI pipeline. We make use of the following tools:

* black
* isort
* flake8

You are encouraged to set up a pre-commit hook to apply these, but ultimately this is
your choice!

Commit messages
===============

Commit messages contain the "why" of changes - please practice good commit hygiene:

* reference an issue ID when relevant
* use a short summary line and a more elaborate body explaining why things are done a
  certain way, which references are relevant...
* gitmoji is encouraged, which helps with...
* use atomic commits that describe a single change
* feel free to rebase PR feedback back into their "original" commits
